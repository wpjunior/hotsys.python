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
from hotsys.quarto.models import Quarto

class Reserva(models.Model):
    reservante = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    
    data_inicial = models.DateTimeField()
    data_final = models.DateTimeField(blank=True, null=True)

    confirmada = models.BooleanField()
    quartos = models.ManyToManyField(Quarto)

    pago = models.DecimalField(decimal_places=2, max_digits=10,
                               verbose_name="Valor pré-pago",
                               blank=True, null=True)

    class Meta:
        db_table = "reserva"

    def confirmar(self, valor):
        self.confirmada = True
        self.pago = valor

        self.save()
