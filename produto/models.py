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
from quarto.models import Estadia

class Produto(models.Model):
    """
    Classe Produto
    
    representa todo produto cadastrado no estoque da pousada.
    attributos:
    nome: nome real do produto
    valor: valor de venda do produto
    qtde: quantidade em estoque
    """
    nome = models.CharField(
        max_length=20,
        verbose_name="Nome")

    valor = models.DecimalField(
        decimal_places=2, max_digits=10,
        verbose_name="Valor")

    qtde = models.IntegerField(
        null=True, blank=True,
        verbose_name="Quantidade")
    
    class Meta:
        db_table = "produto"

class ProdutoItem(models.Model):
    """
    Classe ProdutoItem
    representa a ligação de um produto consumido na estadia.
    """
    produto = models.ForeignKey(Produto)
    estadia = models.ForeignKey(Estadia)
    qtde = models.IntegerField()
    valor_total = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "produto_item"
