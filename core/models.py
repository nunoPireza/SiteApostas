from django.db import models
from django.contrib.auth.models import User

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    NIF = models.IntegerField(null=True)
    contacto = models.IntegerField(null=True)
    codigopostal = models.IntegerField(null=True)
    morada = models.CharField(max_length=200, null=True)
    localidade = models.CharField(max_length=50, null=True)
    pais = models.CharField(max_length=50, null=True)
	

    def __str__(self):
        return self.user.username

class Saldo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=8, decimal_places=2, null= True)
    premios = models.DecimalField(max_digits=8, decimal_places=2, null= True)

class Conta(models.Model):
    saldo = models.IntegerField(default=0)
    nomeUtilizador = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    def __str__(self):
        return self.id

class Concurso(models.Model):
    dataConcurso = models.DateTimeField('dataconcurso')
    b1 = models.CharField(max_length=2)
    b2 = models.CharField(max_length=2)
    b3 = models.CharField(max_length=2)
    b4 = models.CharField(max_length=2)
    b5 = models.CharField(max_length=2)
    e1 = models.CharField(max_length=2)
    e2 = models.CharField(max_length=2)
    def __str__(self):
        return self.id

    def concurso_valido(self):
        return self.dataConcurso >= timezone.now() - datetime.timedelta(days=1)


class Aposta(models.Model):
    nConcurso = models.ForeignKey(Concurso, on_delete=models.CASCADE)
    nConta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    dataAposta = models.DateTimeField('dataaposta')
    nome = models.CharField(max_length=200)
    b1 = models.CharField(max_length=2)
    b2 = models.CharField(max_length=2)
    b3 = models.CharField(max_length=2)
    b4 = models.CharField(max_length=2)
    b5 = models.CharField(max_length=2)
    e1 = models.CharField(max_length=2)
    e2 = models.CharField(max_length=2)

    def __str__(self):
        return self.id	
