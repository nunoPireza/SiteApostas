from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from .models import Utilizador, Concurso, Aposta, Conta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
    return render(request, 'core/admin.html')

def novoRegisto(request):
    try:
        if User.email.__eq__(request.POST['input_email']):
            raise
        fuser = User.objects.create_user(request.POST['input_username'], request.POST['input_email'],
                                         request.POST['input_password'])
        fuser.first_name = request.POST['input_name']
        fuser.last_name = request.POST['input_surname']
        fuser.save()
    except:
        context = {}
        context['same_user'] = True
        return render(request, 'core/registo.html', context)

    fuser = Utilizador(user=fuser)
    fuser.NIF = request.POST['input_nif']
    fuser.contacto = request.POST['input_contacto']
    if request.POST['input_morada']:
        fuser.morada = request.POST['input_morada']
    if request.POST['input_codpostal']:
        fuser.codigopostal = request.POST['input_codpostal']
    if request.POST['input_loc']:
        fuser.localidade = request.POST['input_loc']
    if request.POST['input_pais']:
        fuser.pais = request.POST['input_pais']

    fuser.save()
    emaildestino = request.POST['input_email']
    emailadmin = 'siteapostaspr@gmail.com'
    destinatario = request.POST['input_name'] + " " + request.POST['input_surname']
    titulo = 'Email de confirmação de registo'
    mensagem = 'Bem vindo ao site de apostas ' + destinatario + "."
    send_mail(titulo, mensagem, settings.EMAIL_HOST_USER, [emaildestino,emailadmin], fail_silently=True)
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

def apostar(request):
    return render(request, 'core/apostar.html')

@login_required
def areapessoal(request):
    return render(request, 'core/areapessoal.html')

def mostrardados(request):
    return render(request, 'core/mostrardados.html')

def carregarsaldo(request):
    return render(request, 'core/carregarsaldo.html')
		
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
    concurso = get_object_or_404(Concurso,pk=concurso_id)
    texto=request.POST['aposta']
    #concurso.op
    a=Aposta(concurso,dataAposta=timezone.now(),nome=texto)
    a.save()
    return HttpResponseRedirect(reverse('core:index'))

@login_required
def editardados(request):
    return render(request, 'core/editardados.html')

'''
def editRegisto(request):
    return render(request, 'core/inicio.html')


def editRegisto(request):
    fuser = User.objects.get(pk = 1)

    fuser.localidade = 'Viseu'
    fuser.save()

    return render(request, 'core/inicio.html')
'''

def editRegisto(request):
    fuser = User.objects.get(username='rfred')
    if request.user.is_authenticated:
        fuser = Utilizador(user=fuser)
        if request.POST['sloc']:
            fuser.localidade = request.POST['sloc']
        fuser.save()
        return HttpResponseRedirect(reverse('core:areapessoal'))

    else:
        return render(request, 'core/loginpage.html')

def enviarEmail(request):
    emaildestino = request.POST['input_email']
    titulo = 'Email de confirmação de registo'
    mensagem = 'Bem vindo ao site de apostas '
    send_mail(titulo, mensagem, settings.EMAIL_HOST_USER, [emaildestino], fail_silently=False)
    return render(request, 'core/homepage.html')