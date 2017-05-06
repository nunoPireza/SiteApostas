# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 23:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataAposta', models.DateTimeField(verbose_name='dataaposta')),
                ('b1', models.CharField(max_length=2)),
                ('b2', models.CharField(max_length=2)),
                ('b3', models.CharField(max_length=2)),
                ('b4', models.CharField(max_length=2)),
                ('b5', models.CharField(max_length=2)),
                ('e1', models.CharField(max_length=2)),
                ('e2', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Bolas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bola', models.PositiveSmallIntegerField()),
                ('ocorrencias', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('premios', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Estrelas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estrela', models.PositiveSmallIntegerField()),
                ('ocorrencias', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sorteio',
            fields=[
                ('nSorteio', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('dataSorteio', models.DateField()),
                ('bola1', models.PositiveSmallIntegerField()),
                ('bola2', models.PositiveSmallIntegerField()),
                ('bola3', models.PositiveSmallIntegerField()),
                ('bola4', models.PositiveSmallIntegerField()),
                ('bola5', models.PositiveSmallIntegerField()),
                ('estrela1', models.PositiveSmallIntegerField()),
                ('estrela2', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IBAN', models.IntegerField(null=True)),
                ('NIF', models.IntegerField(null=True)),
                ('contacto', models.IntegerField(null=True)),
                ('morada', models.CharField(max_length=200, null=True)),
                ('pais', models.CharField(max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='aposta',
            name='nConta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Conta'),
        ),
        migrations.AddField(
            model_name='aposta',
            name='nSorteio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Sorteio'),
        ),
    ]
