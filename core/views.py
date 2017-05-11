import os,csv
from access_tokens import tokens
from decimal import *
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.contrib import messages
from .models import Utilizador, Aposta, Conta, Sorteio, Bolas, Estrelas


def inicio(request):
    return render(request, 'core/inicio.html')

def exitMenor(request):
    return render(request, 'core/exitMenor.html')

def idade(request):
    now = datetime.now()
    a = int(request.POST['yy'])
    m = int(request.POST['mm'])
    d = int(request.POST['dd'])
    anoa = now.year
    mesa = now.month
    diaa = now.day
    age = (anoa - a) - ((mesa, diaa) < (m, d))
    if age >= 18 and request.user.is_authenticated:
        return render(request, 'core/areacomum.html')
    elif age >= 18 and request.user.is_anonymous:
        return render(request, 'core/homepage.html')
    else:
        return render(request, 'core/exitMenor.html')

def homepage(request):
    return render(request, 'core/homepage.html')

@login_required
def areacomum(request):
    ultimoSorteio = Sorteio.objects.values('nSorteio').filter(activo=False)
    apostasporsorteio = Aposta.objects.values('nConta_id').filter(nSorteio_id=ultimoSorteio)
    context = {'ultimoSorteio': ultimoSorteio, 'apostasporsorteio': apostasporsorteio}  # dicionário de contexto
    return render(request, 'core/areacomum.html', context)

@login_required
def areapessoal(request):
    apostasuser = Aposta.objects.all().filter(nConta_id=request.user.id)
    context = {'apostasuser': apostasuser}
    return render(request, 'core/areapessoal.html',context)

@login_required
def admin(request):
    context = {}
    if User.is_superuser:
        context['isadmin'] = True
    return render(request, 'core/admin.html', context)

def novoRegisto(request):
    context = {}
    nif_str = len(str(request.POST['input_nif']))
    contact_str = len(str(request.POST['input_contacto']))

    if int(nif_str) != 9:
        context['nifgreater'] = True
        return render(request, 'core/registo.html', context)

    if int(contact_str) != 9:
        context['contactogreater'] = True
        return render(request, 'core/registo.html', context)

    try:
        for u in User.objects.all():
            if u.email == (request.POST['input_email']):
                context['same_email'] = True
                raise

        fuser = User.objects.create_user(request.POST['input_username'], request.POST['input_email'],
                                         request.POST['input_password'])
        fuser.first_name = request.POST['input_name']
        fuser.last_name = request.POST['input_surname']
        fuser.save()
    except:
        if context['same_email'] == False:
            context['same_user'] = True
        return render(request, 'core/registo.html', context)

    fuser = Utilizador(user=fuser)
    fuser.NIF = request.POST['input_nif']
    fuser.contacto = request.POST['input_contacto']

    if request.POST['input_morada']:
        fuser.morada = request.POST['input_morada']
    if request.POST['input_pais']:
        fuser.pais = request.POST['input_pais']

    fuser.save()
    emaildestino = request.POST['input_email']
    destinatario = request.POST['input_name'] + " " + request.POST['input_surname']
    titulo = 'Email de confirmação de registo'
    mensagem = 'Bem vindo ao site de apostas ' + destinatario + "."
    send_mail(titulo, mensagem, settings.EMAIL_HOST_USER, [emaildestino,settings.EMAIL_HOST_USER], fail_silently=True)
    return render(request, 'core/homepage.html')


def registo(request):
    return render(request, 'core/registo.html')


def loginpage(request):
    return render(request, 'core/loginpage.html')

def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('core:areacomum'))
    else:
        messages.warning(request, 'Os dados introduzidos estão incorretos')
        return render(request, "core/loginpage.html")

@login_required
def logoutview(request):
    logout(request)
    return render(request, 'core/homepage.html')


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('/siteapostas/personalpage')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'core/changepassword.html')

def submeterpass(request):
    acco = get_object_or_404(Utilizador, user=request.user)
    context = {}
    context['acc'] = acco
    if request.user.is_authenticated:
        try:
            if request.user.check_password(request.POST['oldpassword']):
                if request.POST['newpassword'] == request.POST['confnewpassword']:
                    request.user.set_password(request.POST['newpassword'])
                    request.user.save()

                    return render(request, "core/areapessoal.html")
                else:
                    context['no_match'] = True
                    return render(request, "core/changepassword.html", context)
            else:
                context['old'] = True
                return render(request, "core/changepassword.html", context)

        except MultiValueDictKeyError:
            return HttpResponseRedirect(reverse('core:changepassword'))
    else:
        return HttpResponse("É necessário estar autenticado.")
'''
def apostar(request):
    return render(request, 'core/apostar.html')
'''

@login_required
def mostrardados(request):
    return render(request, 'core/mostrardados.html')

def aposta(request):
    apostas = Aposta.objects.all()
    template = loader.get_template('core/index.html')
    context = {'apostas': apostas}
    return render(request, 'core/index.html', context)

def detalhe(request, aposta_id):
    aposta = get_object_or_404(Aposta, pk=aposta_id)
    return render(request, 'core/detalhe.html', {'aposta': aposta})

def novaaposta(request):
    return render(request, 'core/novaaposta.html')

def gravaAposta(request,concurso_id):
    concurso = get_object_or_404(Sorteio,pk=concurso_id)
    texto=request.POST['aposta']
    #concurso.op
    a=Aposta(concurso,dataAposta=timezone.now(),nome=texto)
    a.save()
    return HttpResponseRedirect(reverse('core:index'))

@login_required
def editardados(request):
    return render(request, 'core/editardados.html')

def editRegisto(request):
    if request.user.is_authenticated:
        usr = get_object_or_404(Utilizador, user=request.user.id)
        #cnt = get_object_or_404(Conta, user=request.user.id)
        try:
            if request.POST['snome']:
                request.user.first_name = request.POST['snome']
            if request.POST['sapelido']:
                request.user.last_name = request.POST['sapelido']
            if request.POST['semail']:
                request.user.email = request.POST['semail']
                request.user.save()
            if request.POST['snif']:
                usr.NIF = request.POST['snif']
            if request.POST['scontacto']:
                usr.contacto = request.POST['scontacto']
            if request.POST['smorada']:
                usr.morada = request.POST['smorada']
            if request.POST['spais']:
                usr.pais = request.POST['spais']
            usr.save()
            messages.success(request, 'User atualizado')
            if request.POST['siban']:
                if Conta.objects.filter(user_id=request.user.id):
                    cnt = get_object_or_404(Conta, user=request.user.id)
                    cnt.IBAN = request.POST['siban']
                    cnt.save()
                else:
                    return HttpResponse('Não existem dados bancários')

            #context = {}
            #context['acc'] = acc
            return HttpResponseRedirect(reverse('core:editardados'))
        except MultiValueDictKeyError:
            #context = {}
            #context['acc'] = acc
            return HttpResponseRedirect(reverse('core:areapessoal'))
    else:
        return HttpResponse("Desculpe. Alguma coisa não funcionou!")

@login_required
def criarInfoBanc(request):
    return render(request, 'core/infoBanc.html')

def criarInfoB(request):
    usr = request.user.id
    cnt = Conta(IBAN=request.POST['input_iban'], saldo=0.0, premios=0.0, user_id=usr)
    cnt.save()
    return HttpResponseRedirect(reverse('core:areapessoal'))


@login_required
def carregarsaldo(request):
    return render(request, 'core/carregarsaldo.html')

def carregaS(request):
    if Conta.objects.filter(user_id=request.user.id).exists():
        r = get_object_or_404(Conta, user_id=request.user.id)
        if request.POST.get('5e'):
            r.saldo += 5
            r.save()
        elif request.POST.get('10e'):
            r.saldo += 10
            r.save()
        elif request.POST.get('25e'):
            r.saldo += 25
            r.save()
        return HttpResponseRedirect(reverse('core:carregarsaldo'))
    else:
        return HttpResponseRedirect(reverse('core:criarInfoBanc'))


@login_required
def apostar(request):
    context = {'submetido': False}
    context['Saldo'] = 0.0
    PRECOAPOSTA = 2.5

    if Conta.objects.filter(user_id=request.user.id).exists():
        conta = get_object_or_404(Conta,user_id=request.user.id)
        #if conta.saldo >= PRECOAPOSTA:
        context['Saldo'] = conta.saldo
        context['saldoOK'] = True

    return render(request, 'core/apostar.html', context)

@csrf_exempt
def sugestoes(request):
    listaSugestoes = {}
    sugestoesEstrelas={}
    bolasEscolhidas = {}
    estrelasEscolhidas={}
    estrelasPorNumeros={}
    numerosPorEstrelas={}
    datas5 = []
    datas2 = []
    if request.POST:
    # se não for na abertura da página (ou refresh)
        nvazio = set() #para evitar fazer queries com valores repetidos
        envazio = set() #e poder fazer pop,
        if request.POST['eb1'] is not '':
            b = int(request.POST['eb1'])
            bolasEscolhidas['eb1'] = b
            nvazio.add('eb1')
            dtmp = Bolas.objects.filter(bola=b)
            for d in dtmp:
                data= d.ocorrencias
                estrelasPorNumeros = epn(data, estrelasPorNumeros)
        if request.POST['eb2'] is not '':
            b = int(request.POST['eb2'])
            bolasEscolhidas['eb2'] = b
            nvazio.add('eb2')
            dtmp = Bolas.objects.filter(bola=b)
            for d in dtmp:
                data = d.ocorrencias
                estrelasPorNumeros = epn(data, estrelasPorNumeros)
        if request.POST['eb3'] is not '':
            b = int(request.POST['eb3'])
            bolasEscolhidas['eb3'] = b
            nvazio.add('eb3')
            dtmp = Bolas.objects.filter(bola=b)
            for d in dtmp:
                data = d.ocorrencias
                estrelasPorNumeros = epn(data, estrelasPorNumeros)
        if request.POST['eb4'] is not '':
            b = int(request.POST['eb4'])
            bolasEscolhidas['eb4'] = b
            nvazio.add('eb4')
            dtmp = Bolas.objects.filter(bola=b)
            for d in dtmp:
                data = d.ocorrencias
                estrelasPorNumeros = epn(data, estrelasPorNumeros)
        if request.POST['eb5'] is not '':
            b = int(request.POST['eb5'])
            bolasEscolhidas['eb5'] = b
            nvazio.add('eb5')
            dtmp = Bolas.objects.filter(bola=b)
            for d in dtmp:
                data = d.ocorrencias
                estrelasPorNumeros = epn(data, estrelasPorNumeros)
        if request.POST['ee1'] is not '':
                e = int(request.POST['ee1'])
                estrelasEscolhidas['ee1'] = e
                envazio.add('ee1')
                dtmp = Estrelas.objects.filter(estrela=e)
                for d in dtmp:
                    data = d.ocorrencias
                    numerosPorEstrelas = npe(data, numerosPorEstrelas)
        if request.POST['ee2'] is not '':
            e = int(request.POST['ee2'])
            estrelasEscolhidas['ee2'] = e
            envazio.add('ee2')
            dtmp = Estrelas.objects.filter(estrela=e)
            for d in dtmp:
                data = d.ocorrencias
                numerosPorEstrelas = npe(data, numerosPorEstrelas)

        # obter sugestões
        size = len(bolasEscolhidas)
        esize = len(envazio)
        #if size ==0:
         #listaSugestoes = getSugestoesBolas()

        if size == 1:  # obter duetos
            b1 = bolasEscolhidas.get(nvazio.pop())
            s1 = Bolas.objects.filter(bola=b1)
            for s in s1:
                d1 = s.ocorrencias
                tmp = (Bolas.objects.filter(ocorrencias=d1).exclude(bola=s.bola).values('bola').annotate(
                    vezes=Count('ocorrencias')))

                for t in tmp:
                    if t.get('bola') in listaSugestoes:
                        listaSugestoes[t.get('bola')] += 1
                    else:
                        listaSugestoes[t.get('bola')] = 1  # t.get('vezes')


                        #  Fim de sugestões para Duetos
        if size == 2:  # obter trios

            b1 = bolasEscolhidas.get(nvazio.pop())
            b2 = bolasEscolhidas.get(nvazio.pop())
            s1 = Bolas.objects.filter(bola=b1)

            for s in s1:
                d1 = s.ocorrencias
                s2 = (Bolas.objects.filter(ocorrencias=d1).filter(bola=b2))
                for j in s2:
                    d2 = j.ocorrencias
                    tmp = Bolas.objects.filter(ocorrencias=d2).values('bola').exclude(bola=b2).exclude(bola=b1)
                    for t in tmp:
                        if t.get('bola') in listaSugestoes:
                            listaSugestoes[t.get('bola')] += 1
                        else:
                            listaSugestoes[t.get('bola')] = 1

                            # Fim de sugestões para Trios
        if size == 3:  # obter Quartetos

            b1 = bolasEscolhidas.get(nvazio.pop())
            b2 = bolasEscolhidas.get(nvazio.pop())
            b3 = bolasEscolhidas.get(nvazio.pop())
            q1 = (Bolas.objects.filter(bola=b1))

            for r1 in q1:
                d1 = r1.ocorrencias
                q2 = (Bolas.objects.filter(ocorrencias=d1).filter(bola=b2))
                for r2 in q2:
                    d2 = r2.ocorrencias
                    q3 = (Bolas.objects.filter(ocorrencias=d2).filter(bola=b3))
                    for r3 in q3:  # q3 contem as datas onde ocorreram as 3 bolas escolhidas
                        d3 = r3.ocorrencias
                        tmp = Bolas.objects.filter(ocorrencias=d3).values('bola').exclude(bola=b2).exclude(
                            bola=b1).exclude(
                            bola=b3)  # obtidas todas as bolas que apareceram nas mesmas datas que forma comums às 3
                        for t in tmp:  # faz a contagem e adiciona á listaSugestões no formato pretendido
                            if t.get('bola') in listaSugestoes:
                                listaSugestoes[t.get('bola')] += 1
                            else:
                                listaSugestoes[t.get('bola')] = 1

                                # Fim de sugestões para Quartetos
        if size == 4:  # obter Quintetos

            b1 = bolasEscolhidas.get(nvazio.pop())
            b2 = bolasEscolhidas.get(nvazio.pop())
            b3 = bolasEscolhidas.get(nvazio.pop())
            b4 = bolasEscolhidas.get(nvazio.pop())

            q1 = (Bolas.objects.filter(bola=b1))
            for r1 in q1:
                d1 = r1.ocorrencias
                q2 = (Bolas.objects.filter(ocorrencias=d1).filter(bola=b2))
                for r2 in q2:
                    d2 = r2.ocorrencias
                    q3 = (Bolas.objects.filter(ocorrencias=d2).filter(bola=b3))
                    for r3 in q3:  # q3 contem as datas onde ocorreram as 3 bolas escolhidas
                        d3 = r3.ocorrencias
                        q4 = (Bolas.objects.filter(ocorrencias=d3).filter(bola=b4))
                        for r4 in q4:
                            d4 = r4.ocorrencias

                            tmp = Bolas.objects.filter(ocorrencias=d4).values('bola').exclude(bola=b1).exclude(
                                bola=b2).exclude(bola=b3).exclude(bola=b4)
                            for t in tmp:  # faz a contagem e adiciona á listaSugestões no formato pretendido
                                if t.get('bola') in listaSugestoes:
                                    listaSugestoes[t.get('bola')] += 1
                                else:
                                    listaSugestoes[t.get('bola')] = 1

                                # Fim de sugestões para Quintetos

                                # inicio verificar se já saiu chave
        if size == 5:  # obter datas

            b1 = bolasEscolhidas.get(nvazio.pop())
            b2 = bolasEscolhidas.get(nvazio.pop())
            b3 = bolasEscolhidas.get(nvazio.pop())
            b4 = bolasEscolhidas.get(nvazio.pop())
            b5 = bolasEscolhidas.get(nvazio.pop())

            q1 = (Bolas.objects.filter(bola=b1))
            for r1 in q1:
                d1 = r1.ocorrencias
                q2 = (Bolas.objects.filter(ocorrencias=d1).filter(bola=b2))
                for r2 in q2:
                    d2 = r2.ocorrencias
                    q3 = (Bolas.objects.filter(ocorrencias=d2).filter(bola=b3))
                    for r3 in q3:  # q3 contem as datas onde ocorreram as 3 bolas escolhidas
                        d3 = r3.ocorrencias
                        q4 = (Bolas.objects.filter(ocorrencias=d3).filter(bola=b4))

                        for r4 in q4:
                            d4 = r4.ocorrencias
                            q5 = (
                                Bolas.objects.filter(ocorrencias=d4).filter(bola=b5))  # datas onde saiu a chave
                            for d5 in q5:
                                datas5.append(d5.ocorrencias)
       # if esize==0:
        # sugestoesEstrelas = getSugestoesEstrelas()
        if esize==1: # se for selecionada só uma estrela
            e1=estrelasEscolhidas.get(envazio.pop())
            s1 = Estrelas.objects.filter(estrela=e1)
            for s in s1:
                d1 = s.ocorrencias
                tmp = (Estrelas.objects.filter(ocorrencias=d1).exclude(estrela=s.estrela).values('estrela').annotate(
                    vezes=Count('ocorrencias')))

                for t in tmp:
                    if t.get('estrela') in sugestoesEstrelas:
                        sugestoesEstrelas[t.get('estrela')] += 1
                    else:
                        sugestoesEstrelas[t.get('estrela')] = 1

                        #  Fim de uma estrela escolhida
        if esize==2: # se 2 estrelas escolher datas
            e1 = estrelasEscolhidas.get(envazio.pop())
            e2 = estrelasEscolhidas.get(envazio.pop())
            q1 = Estrelas.objects.filter(estrela=e1)
            for r1 in q1:
                d1 = r1.ocorrencias
                q2 = Estrelas.objects.filter(estrela=e2).filter(ocorrencias=d1)
                for r2 in q2:
                    d2=r2.ocorrencias
                    datas2.append(d2)

                        #  Fim de 2 estrelas escolhidas



    #else:
        # a listaSugestões poderia ser obtida diretamente de Query? (a tentar)
        #sugestoesEstrelas = getSugestoesEstrelas()
        #listaSugestoes= getSugestoesBolas()

    return render(request, 'core/sugestoes.html',
                  {'frequenciasBolas':getFrequenciasBolas(),'frequenciasEstrelas':getFrequenciasEstrelas(),'sugestoes': listaSugestoes, 'escolhas': bolasEscolhidas, 'data5': datas5, 'estrelasSugeridas':sugestoesEstrelas, 'estrelasEscolhidas':estrelasEscolhidas, 'data2':datas2, 'estrelasPorNumeros':estrelasPorNumeros, 'numerosPorEstrelas':numerosPorEstrelas})

def getFrequenciasEstrelas():
    frequenciasEstrelas={}
    listaTmp = Estrelas.objects.values('estrela').annotate(vezes=Count('ocorrencias'))
    for t in listaTmp:
        frequenciasEstrelas[t['estrela']] = t['vezes']
    return frequenciasEstrelas

def getFrequenciasBolas():
    listaFrequencias={}
    listaTmp = Bolas.objects.values('bola').annotate(vezes=Count('ocorrencias'))
    for t in listaTmp:
        b = t['bola']
        v = t['vezes']
        listaFrequencias[b] = v
    return listaFrequencias

def epn(data,estrelasPorNumeros):
    # vai procurar as estrelas
    # do dia do sorteio  das bolas escolhidas
    # para juntar ás anteriores
    epn = Estrelas.objects.filter(ocorrencias=data)
    for t in epn:
        #if t.get('estrela') in estrelasPorNumeros:
        if t.estrela in estrelasPorNumeros:
            estrelasPorNumeros[t.estrela] += 1
        else:
            estrelasPorNumeros[t.estrela] = 1
    return estrelasPorNumeros

def npe(data, numerosPorEstrelas):
    # vai procurar bolas q ocorreram com as estrelas escolhidas
    # para juntar ás anteriores
    npe = Bolas.objects.filter(ocorrencias=data)
    for t in npe:

        if t.bola in numerosPorEstrelas:
            numerosPorEstrelas[t.bola] += 1
        else:
            numerosPorEstrelas[t.bola] = 1
    return numerosPorEstrelas



def submeteraposta(request): #grava na base de dados
    PRECOAPOSTA=2.5
    sorteioAtual = Sorteio.objects.values('nSorteio').filter(activo=True).order_by('nSorteio').last()
    if sorteioAtual: #os admins podem ter se esquecido de ativar o concurso!
        sorteioAtual = sorteioAtual['nSorteio']
    else:
        #falta implementar
        donothing=0
    bolas=set()
    estrelas=set()
    #transfere os dados do form para um set (remove repetidos)
    bolas.add(int(request.POST['Bola1']))
    bolas.add(int(request.POST['Bola2']))
    bolas.add(int(request.POST['Bola3']))
    bolas.add(int(request.POST['Bola4']))
    bolas.add(int(request.POST['Bola5']))
    estrelas.add(int(request.POST['Estrela1']))
    estrelas.add(int(request.POST['Estrela2']))

    verificada= verificaAposta(bolas,estrelas) #verifica se é uma aposta válida
    if not verificada:
        messages.error(request,"aposta inválida")
    if verificada:
        repetida=verificaRepeticao(bolas,estrelas) #verifica se já foi submetida
        if repetida:
            messages.error(request, "Aposta já foi submetida neste concurso")
        if not repetida:
            if Conta.objects.filter(user_id=request.user.id).exists():
                    conta=get_object_or_404(Conta,user_id=request.user.id)
                    if conta.saldo>=PRECOAPOSTA:
                        conta.saldo-= Decimal(PRECOAPOSTA) #remove saldo
                        conta.save()
                        user_id=conta.user_id
                        #grava aposta na BD
                        b1 = bolas.pop()
                        b2 = bolas.pop()
                        b3 = bolas.pop()
                        b4 = bolas.pop()
                        b5 = bolas.pop()
                        e1 = estrelas.pop()
                        e2 = estrelas.pop()
                        a = Aposta(dataAposta=datetime.now(), nConta_id=user_id, nSorteio_id=sorteioAtual, bola1=b1,bola2=b2,bola3=b3,bola4=b4,bola5=b5,estrela1=e1,estrela2=e2 )
                        a.save()
                        messages.success(request, 'Aposta submetida')
                    else:
                        messages.error(request, "Saldo insuficiente")

    return render(request, 'core/apostar.html' )

def verificaAposta(bolas,estrelas): #verifica se obdece ás regras
    #mudar de set para lista
    bolas=list(bolas)
    estrelas=list(estrelas)

    if(len(bolas)!=5 or len(estrelas)!=2): #dimensão
        return False #se houver bolas repetidas são detetadas aqui
    #i = 0
    for b in bolas:
        if (b<1 or b>50): # não é um número válido
            return False
    for e in estrelas:
        if(e<1 or e>12): #não é uma estrela válida
            return False

    '''j = 1+i
    for nextB in bolas[j,]: #Repeticões não é necessário pq passou por um set(.)
        if nextB==b:
            return False
        else:
            j+=1
        i+=1'''
    return True

def verificaRepeticao(bolas,estrelas): #devolve verdade se repetida
    #obter as apostas já submetidas
    apostas = Aposta.objects.all()
    # mudar de set para lista
    bolas = list(bolas)
    estrelas = list(estrelas)
    for a in apostas:
        for b in bolas:
            if b!=a.bola1:
                if b!=a.bola2:
                    if b!=a.bola3:
                        if b!=a.bola4:
                            if b!=a.bola5:
                                return False

        for e in estrelas:
            if e!=a.estrela1:
                if e != a.estrela2:
                    return False
    return True

def inserirconcurso(request):
    concursoAtivo=Sorteio.objects.filter(activo=True)
    concursoAtivo=concursoAtivo[0].nSorteio


    return render(request, 'core/inserirconcurso.html', {'concursoAtivo':concursoAtivo})



def carregaF(request):
    Bolas.objects.all().delete()
    Estrelas.objects.all().delete()
    cabecalho = 1
    f = open(os.path.join(settings.PROJECT_ROOT, 'euromillions.csv'), "r")
    linhas = f.readlines()
    # maxSorteios=len(linhas)-cabecalho
    sorteios = linhas[1:]
    for s in sorteios:
        s = s.rstrip('\n')
        s = s.split(';')
        n = s[0]
        data = s[1]
        data = datetime.strptime(data, '%d/%m/%Y')
        #premioV = s[2]
        bolas = [int(i) for i in s[2:7]]
        estrelas = [int(i) for i in s[7:9]]
        premios=[Decimal(i)for i in s[9:23]]
        # Atualiza tabela Tabela de Sorteio
        si = Sorteio(nSorteio=n, dataSorteio=data, premio=premioV, bola1=bolas[0], bola2=bolas[1], bola3=bolas[2], bola4=bolas[3],
                     bola5=bolas[4], estrela1=estrelas[0], estrela2=estrelas[1], premio1=premios[0],premio2=premios[1],premio3=premios[2],premio4=premios[3],premio5=premios[4],premio6=premios[5],premio7=premios[6],premio8=premios[7],premio9=premios[8],premio10=premios[9],premio11=premios[10],premio12=premios[11],premio13=premios[12],)
        si.save()
        # Ordena chave
        bolas.sort()
        estrelas.sort()
        # Vai preencher as restantes tabelas
        preencheTabelasBolas(bolas,data)
        preencheTabelasEstrelas(estrelas, data)
        #as tabelas supra podem deixar de ser necessárias
        # se os filter feitos a estas passarem para a tabela sorteio
        #a PK de Sorteio não podia ser só o n.º de concurso
        #(para pensar melhor)

        #encher tabela apostas
        f = open(os.path.join(settings.PROJECT_ROOT, 'apostas.csv'), "r")
        linhasapostas = f.readlines()
        apostas = linhasapostas[1:]
        for s in apostas:
            s = s.rstrip('\n')
            s = s.split(';')
            n = s[0]
            data = s[1]
            data = datetime.strptime(data, '%d/%m/%Y')
            bolas1 = s[2]
            bolas2 = s[3]
            bolas3 = s[4]
            bolas4 = s[5]
            bolas5 = s[6]
            estrelas1 = s[7]
            estrelas2 = s[8]
            conta = s[9]
            sorteio = s[10]
            # Atualiza tabela Tabela APOSTA
            si = Aposta(id=n, dataAposta=data, bola1=bolas1, bola2=bolas2, bola3=bolas3, bola4=bolas4, bola5=bolas5,
                        estrela1=estrelas1, estrela2=estrelas2, nConta_id=conta, nSorteio_id=sorteio)
            si.save()


        context={}
        context['done']=True
        context['isadmin']=True

    return render(request, 'core/admin.html', context)


def preencheTabelasBolas(novasBolas, data):

    for b in novasBolas:
        s = Bolas(bola=b, ocorrencias=data)
        s.save()

def preencheTabelasEstrelas(novasEstrelas, data):
    for e in novasEstrelas:
        s = Estrelas(estrela=e, ocorrencias=data)
        s.save()

def enviarEmail(request):
    todosEmails = User.objects.values('email')
    mensagem = request.POST['email_input']
    msg = EmailMessage('Informação - Todos os Utilizadores - Site Apostas',
                       mensagem,
                       settings.EMAIL_HOST_USER,
                       [todosEmails],
                       cc=[settings.EMAIL_HOST_USER])
    msg.content_subtype = "html"
    msg.send()
    context = {}
    if User.is_superuser:
        context['isadmin'] = True
        context['messagesuccess']  = True
        return render(request, 'core/admin.html', context)
    else:
        return render(request, 'core/areacomum.html')

def submeterApostas(request): #grava ficheiro CSV para registar na SantaCasa
    # Create the HttpResponse object with the appropriate CSV header.
    context = {}

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="submeterApostas.csv"'
    try:
        sorteioAtual = Sorteio.objects.values('nSorteio').filter(activo=True).order_by('nSorteio').last()
        sorteioAtual = sorteioAtual['nSorteio']
        Sorteio.objects.filter(pk=sorteioAtual).update(activo=False)
    except:

        context['isadmin'] = True
        context['faildSubmit'] = True
        return render(request, 'core/admin.html', context)

#    a = Aposta(dataAposta=datetime.now(),nConta_id=1,nSorteio_id=sorteioAtual,bola1=1,bola2=2,bola3=3,bola4=4,bola5=4,estrela1=1,estrela2=8)
 #   a.save()

    writer = csv.writer(response)
    apostaList = Aposta.objects.filter(nSorteio_id=sorteioAtual)
    writer.writerow(['Sorteio','Bola1','Bola2','Bola3','Bola4','Bola5','Estrela1','Estrela2'])
    for n in apostaList:
        writer.writerow([n.nSorteio_id,n.bola1,n.bola2,n.bola3,n.bola4,n.bola5,n.estrela1,n.estrela2])

    return response

'''def distribuipremio:
    #premioMax = Sorteio.objects.values('premio').get(activo=False).order_by('nSorteio').last()
    premioMax = 200000
    sorteioAtual = Sorteio.objects.values('nSorteio').get(activo=False).order_by('nSorteio').last()
    sorteioAtual = sorteioAtual['nSorteio']

    #chave de premio
    chavePremio = {}
    listabolaspremio = []
    listabolaspremio.append(Sorteio.objects.values('bola1').filter(nSorteio=sorteioAtual))
    listabolaspremio.append(Sorteio.objects.values('bola2').filter(nSorteio=sorteioAtual))
    listabolaspremio.append(Sorteio.objects.values('bola3').filter(nSorteio=sorteioAtual))
    listabolaspremio.append(Sorteio.objects.values('bola4').filter(nSorteio=sorteioAtual))
    listabolaspremio.append(Sorteio.objects.values('bola5').filter(nSorteio=sorteioAtual))
    listaestrelaspremio = []
    listaestrelaspremio.append(Sorteio.objects.values('estrela1').filter(nSorteio=sorteioAtual))
    listaestrelaspremio.append(Sorteio.objects.values('estrela2').filter(nSorteio=sorteioAtual))
    chavePremio['bolas']= listabolaspremio
    chavePremio['estrelas']= listaestrelaspremio

    #chaves jogadas - dicionario  {'contaId': nConta_id, 'listaBolasAposta':[lista de bolas], 'listaEstrelasAposta: [lista de estrelas]}
    chavesjogadas = {}
    listaApostaporSorteio = Aposta.objects.filter(nSorteio_id=sorteioAtual)
    listaContaId = []
    chavesjogadas['contaId'] = listaContaId
    listabolasAposta = []
    chavesjogadas['listaBolasAposta'] = listabolasAposta
    listaestrelasAposta = []
    chavesjogadas['listaEstrelasAposta'] = listaestrelasAposta

    for contaId in listaApostaporSorteio:
        #preencher contaID
        listaContaId.append((contaId.nConta_id))

        #preecher lista de bolas
        listabolasAposta.append(contaId.bola1)
        listabolasAposta.append(contaId.bola2)
        listabolasAposta.append(contaId.bola3)
        listabolasAposta.append(contaId.bola4)
        listabolasAposta.append(contaId.bola5)

        #preecher lista de estrelas
        listaestrelasAposta.append(contaId.estrela1)
        listaestrelasAposta.append(contaId.estrela2)


        #averiguar premios por contaId
        listaPremios = []
        for linha in chavesjogadas:
            for i in range(4):
                if linha['listaBolasAposta'][i] == listabolaspremio[i]:
                    
                    '''

