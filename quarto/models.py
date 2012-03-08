#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Trabalho de conclusão de curso
# Alunos
#
# Wilson Pinto Júnior <wilsonpjunior@gmail.com>
# Mateus Fedrigo de Moura <mateusfedrigo@gmail.com>
# Jonathas Peixoto <jonathas.peixoto@gmail.com>
#
# Este programa é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 2 da 
# Licença, ou (na sua opnião) qualquer versão.

# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
# MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from django.db import models
from hospede.models import Hospede

QUARTO_ESTADOS = (
    ('l', "Livre"),
    ('o', "Ocupado"),
    ('r', "Reservado"),
    ('m', u"Manutenção"))

class Quarto(models.Model):
    nome = models.CharField(max_length=150,
                            verbose_name="Nome")
    preco = models.DecimalField(decimal_places=2, max_digits=10,
                                verbose_name="Preço")
    
    num_leitos = models.IntegerField(
        verbose_name=u"Número de leitos")
    suite = models.BooleanField(
        verbose_name="é suite")
    cama_casal = models.BooleanField(
        verbose_name="Possui cama de casal")
    estado = models.CharField(max_length=1,
                              choices=QUARTO_ESTADOS,
                              default='l')
    estadia_atual = models.ForeignKey("Estadia",
                                      blank=True, null=True)

    class Meta:
        db_table = "quarto"

class Estadia(models.Model):
    data_inicial = models.DateTimeField()
    data_final = models.DateTimeField(blank=True, null=True)
    hospedes = models.ManyToManyField(Hospede)

    class Meta:
        db_table = "estadia"

class Dano(models.Model):
    estadia = models.ForeignKey("Estadia")
    desc = models.CharField(max_length=200)
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    grave = models.BooleanField()

    class Meta:
        db_table = "dano"
