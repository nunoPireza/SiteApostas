from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
   login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
)

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    url(r'^logout/$', logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^changepassword/$', views.changePassword, name='changepassword'),
    url(r'^exitMenor$', views.exitMenor, name='exitMenor'),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^areacomum/$', views.areacomum, name='areacomum'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^registo$', views.registo, name='registo'),
    url(r'^novoRegisto$', views.novoRegisto, name='novoRegisto'),
    url(r'^loginpage$', views.loginpage, name='loginpage'),
    url(r'^loginview$', views.loginview, name='loginview'),
    url(r'^logoutview/$',views.logoutview, name='logoutview'),
    url(r'^submeterpass/$', views.submeterpass, name='submeterpass'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
	url(r'^apostar/$', views.apostar, name='apostar'),
    url(r'^areapessoal/$', views.areapessoal, name='areapessoal'),
    url(r'^carregarsaldo$', views.carregarsaldo, name='carregarsaldo'),
    url(r'^editardados/$', views.editardados, name='editardados'),
    url(r'^editRegisto/$', views.editRegisto, name='editRegisto'),
    url(r'^mostardados$', views.mostrardados, name='mostrardados'),
	url(r'^$', views.aposta, name='aposta'),
    url(r'^(?P<aposta_id>[0-9]+)/$', views.detalhe, name='detalhe'),
    url(r'^novaaposta/$', views.novaaposta, name='novaaposta'),
    url(r'^gravaAposta/$', views.gravaAposta, name='gravaAposta'),
    ]
