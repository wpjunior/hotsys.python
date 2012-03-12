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

__all__ = ('Hospede',)

from django.db import models

class Hospede(models.Model):
    nome = models.CharField(
        max_length=220,
        verbose_name="Nome completo")

    data_nasc = models.DateField(
        verbose_name="Data de nascimento")

    cpf = models.CharField(
        max_length=16,
        verbose_name="CPF",
        unique=True)

    telefone = models.CharField(
        max_length=16,
        verbose_name="Telefone")

    logradouro = models.CharField(
        max_length=250,
        verbose_name="Logradouro")
    
    cidade = models.CharField(
        max_length=50,
        verbose_name="Cidade")

    necessidades = models.TextField(
        null=True, blank=True,
        verbose_name="Necessidades")

    observacoes = models.TextField(
        null=True, blank=True,
        verbose_name=u"Observações")
    
    class Meta:
        db_table = "hospede"
        ordering = ['nome']
