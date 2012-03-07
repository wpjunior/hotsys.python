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

FUNCIONARIO_TIPO = (
    ('g', "Gestor"),
    ('b', "Balconista"),
    ('r', "Recepcionista"))

class Funcionario(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome")

    email = models.EmailField(
        verbose_name="E-Mail")

    tipo = models.CharField(
        max_length=1,
        choices=FUNCIONARIO_TIPO,
        verbose_name="Tipo")

    usuario = models.CharField(
        max_length=50,
        verbose_name="Usuário")

    senha = models.CharField(max_length=40)

    ativo = models.BooleanField()
    cpf = models.CharField(
        max_length=16,
        verbose_name="CPF")

    class Meta:
        db_table = "funcionario"
