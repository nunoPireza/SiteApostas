# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170511_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aposta',
            name='premio1',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio10',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio11',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio12',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio13',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio2',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio3',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio4',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio5',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio6',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio7',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio8',
        ),
        migrations.RemoveField(
            model_name='aposta',
            name='premio9',
        ),
        migrations.RemoveField(
            model_name='sorteio',
            name='premio',
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio1',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio10',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio11',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio12',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio13',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio2',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio3',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio4',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio5',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio6',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio7',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio8',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sorteio',
            name='premio9',
            field=models.PositiveIntegerField(default=0),
        ),
    ]