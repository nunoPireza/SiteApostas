import os
from access_tokens import tokens
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
from datetime import datetime
from .models import Utilizador, Aposta, Conta, Sorteio, Bolas, Estrelas


def inicio(request):
    return render(request, 'core/inicio.html')

def exitMenor(request):
    return render(request, 'core/exitMenor.html')

def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'core/areacomum.html')
    else:
        return render(request, 'core/homepage.html')

@login_required
def areacomum(request):
    return render(request, 'core/areacomum.html')

def admin(request):
    context = {}
    if request.user.is_authenticated:
        usr = get_object_or_404(User, user=request.user.id)
        if usr.username == "admin":
            context['isadmin']=True
    return render(request, 'core/admin.html')

def novoRegisto(request):
    context = {}
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
    context = {}
    context = {}
    if user is not None:
        login(request, user)
        args = {}
        for each in User._meta.fields:
            args[each.name] = getattr(User, each.name)
        return render(request, 'core/areacomum.html', args)

    else:
        context['noUser'] = True
        return render(request, "core/loginpage.html", context)

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
def areapessoal(request):
    return render(request, 'core/areapessoal.html')

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
    r = get_object_or_404(Conta, pk=request.user.id)
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








def apostar(request):
    return render(request, 'core/apostar.html')

@csrf_exempt
def sugestoes(request):
    listaSugestoes={}
    bolasEscolhidas = {}
    datas=[]
    if request.POST:
    #se não for na abertura da página (ou refresh)
        nvazio=set()
        if request.POST['eb1'] is not '':
            bolasEscolhidas['eb1']=int(request.POST['eb1'])
            nvazio.add('eb1')
        if request.POST['eb2'] is not '':
            bolasEscolhidas['eb2']=int(request.POST['eb2'])
            nvazio.add('eb2')
        if request.POST['eb3'] is not '':
            bolasEscolhidas['eb3']=int(request.POST['eb3'])
            nvazio.add('eb3')
        if request.POST['eb4'] is not '':
            bolasEscolhidas['eb4']=int(request.POST['eb4'])
            nvazio.add('eb4')
        if request.POST['eb5'] is not '':
            bolasEscolhidas['eb5']=int(request.POST['eb5'])
            nvazio.add('eb5')

        #obter sugestões
        size=len(bolasEscolhidas)
        if size==1:#obter duetos
            b1=bolasEscolhidas.get(nvazio.pop())
            s1=Bolas.objects.filter(bola=b1)
            for s in s1:
                d1=s.ocorrencias
                tmp=(Bolas.objects.filter(ocorrencias=d1).exclude(bola=s.bola).values('bola').annotate(vezes=Count('ocorrencias')))

                for t in tmp:
                    if t.get('bola') in listaSugestoes:
                        listaSugestoes[t.get('bola')]+= 1
                    else:
                        listaSugestoes[t.get('bola')]=1 #t.get('vezes')

 #  Fim de sugestões para Duetos
        if size == 2:  # obter trios

            b1 = bolasEscolhidas.get(nvazio.pop())
            b2 = bolasEscolhidas.get(nvazio.pop())
            s1 = Bolas.objects.filter(bola=b1)


            for s in s1:
                d1 = s.ocorrencias
                s2= (Bolas.objects.filter(ocorrencias=d1).filter(bola=b2))
                for j in s2:
                    d2=j.ocorrencias
                    tmp=Bolas.objects.filter(ocorrencias=d2).values('bola').exclude(bola=b2).exclude(bola=b1)
                    for t in tmp:
                        if t.get('bola') in listaSugestoes:
                            listaSugestoes[t.get('bola')]+= 1
                        else:
                            listaSugestoes[t.get('bola')]=1

#Fim de sugestões para Trios
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
                    for r3 in q3: #q3 contem as datas onde ocorreram as 3 bolas escolhidas
                        d3 = r3.ocorrencias
                        tmp = Bolas.objects.filter(ocorrencias=d3).values('bola').exclude(bola=b2).exclude(
                        bola=b1).exclude(bola=b3) #obtidas todas as bolas que apareceram nas mesmas datas que forma comums às 3
                        for t in tmp: # faz a contagem e adiciona á listaSugestões no formato pretendido
                            if t.get('bola') in listaSugestoes:
                                listaSugestoes[t.get('bola')] += 1
                            else:
                                listaSugestoes[t.get('bola')] = 1

#Fim de sugestões para Quartetos

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
                        q4=(Bolas.objects.filter(ocorrencias=d3).filter(bola=b4))
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

#inicio verificar se já saiu chave
        if size == 5:  # obter Quintetos

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
                                datas.append(d5.ocorrencias)



    else:
        #a listaSugestões poderia ser obtida diretamente de Query? (a tentar)

        listaTmp= Bolas.objects.values('bola').annotate(vezes=Count('ocorrencias'))
        for t in listaTmp:
            b=t['bola']
            v=t['vezes']
            listaSugestoes[b]=v

    return render(request, 'core/sugestoes.html', {'lista': listaSugestoes, 'escolhas':bolasEscolhidas, 'data5':datas})

def carregarficheiro(request):
    return render(request, 'core/carregarficheiro.html')

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
        bolas = [int(i) for i in s[2:7]]
        estrelas = [int(i) for i in s[7:9]]
        # Atualiza tabela Tabela de Sorteio
        si = Sorteio(nSorteio=n, dataSorteio=data, bola1=bolas[0], bola2=bolas[1], bola3=bolas[2], bola4=bolas[3],
                     bola5=bolas[4], estrela1=estrelas[0], estrela2=estrelas[1])
        si.save()
        # Ordena chave
        bolas.sort()
        estrelas.sort()
        # Vai preencher as restantes tabelas
        preencheTabelasBolas(bolas,data)
        preencheTabelasEstrelas(estrelas, data)

    return HttpResponse(estrelas)
    # return HttpResponse("-----"+n+","+str(data)+","+str(bolas)+","+str(estrelas))
    # return HttpResponse(linhas)
    # return HttpResponse ("Página de administração")


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
    return render(request, 'core/homepage.html')
