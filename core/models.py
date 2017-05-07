from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    NIF = models.IntegerField(null=True)
    contacto = models.IntegerField(null=True)
    morada = models.CharField(max_length=200, null=True)
    pais = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

class Conta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IBAN = models.IntegerField(null=True)
    saldo = models.DecimalField(max_digits=8, decimal_places=2, null= True)
    premios = models.DecimalField(max_digits=8, decimal_places=2, null= True)

    def __str__(self):
        return self.id

class Sorteio(models.Model):
    nSorteio=models.PositiveSmallIntegerField(primary_key=True)
    dataSorteio=models.DateField(auto_now=False, auto_now_add=False)
    bolas =models.PositiveSmallIntegerField()
    estrelas =models.PositiveSmallIntegerField()
    activo=models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def sorteio_valido(self):
        return self.dataSorteio >= timezone.now() - datetime.timedelta(days=1)

#V2
class Estrelas(models.Model):
    estrela = models.PositiveSmallIntegerField(primary_key=False)
    ocorrencias = models.DateField(auto_now=False, auto_now_add=False)

class Bolas(models.Model):
    bola = models.PositiveSmallIntegerField(primary_key=False)
    ocorrencias = models.DateField(auto_now=False, auto_now_add=False)    

class Aposta(models.Model):
    nSorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE)
    nConta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    dataAposta = models.DateTimeField('dataaposta')
    bolas = models.PositiveSmallIntegerField()
    estrelas = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.id
