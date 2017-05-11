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
    nSorteio=models.PositiveIntegerField(primary_key=True)
    dataSorteio=models.DateField(auto_now=False, auto_now_add=False)

    bola1 = models.PositiveSmallIntegerField(null=True, blank=True)
    bola2 = models.PositiveSmallIntegerField(null=True, blank=True)
    bola3 = models.PositiveSmallIntegerField(null=True, blank=True)
    bola4 = models.PositiveSmallIntegerField(null=True, blank=True)
    bola5 = models.PositiveSmallIntegerField(null=True, blank=True)
    estrela1 = models.PositiveSmallIntegerField(null=True, blank=True)
    estrela2 = models.PositiveSmallIntegerField(null=True, blank=True)

    activo=models.BooleanField(default=False)

    premio1 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio2 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio3 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio4 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio5 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio6 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio7 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio8 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio9 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio10 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio11 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio12 = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    premio13 = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return self.nSorteio

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
    bola1 = models.PositiveSmallIntegerField()
    bola2 = models.PositiveSmallIntegerField()
    bola3 = models.PositiveSmallIntegerField()
    bola4 = models.PositiveSmallIntegerField()
    bola5 = models.PositiveSmallIntegerField()
    estrela1 = models.PositiveSmallIntegerField()
    estrela2 = models.PositiveSmallIntegerField()


    def __str__(self):
        return self.id
