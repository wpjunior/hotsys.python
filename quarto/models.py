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


import datetime
from django.db import models
from hospede.models import Hospede
from django.db.models import Sum
from decimal import Decimal

QUARTO_ESTADOS = (
    ('l', "Livre"),
    ('o', "Ocupado"),
    ('r', "Reservado"),
    ('m', u"Manutenção"))

class Quarto(models.Model):
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome")

    preco = models.DecimalField(
        decimal_places=2, max_digits=10,
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

    estadia_atual = models.ForeignKey(
        "Estadia",
        blank=True, null=True,
        related_name="estadia atual")

    class Meta:
        db_table = "quarto"
        ordering = ['nome']


    def tem_reserva(self, data_inicial, data_final):
        """
        Retorna se o quarto atual possui reserva.
        """
        from reserva.models import Reserva

        return Reserva.objects.filter(
            models.Q(data_inicial__range=(data_inicial, data_final))|
            models.Q(data_final__range=(data_inicial, data_final))).count() > 0

class Estadia(models.Model):
    data_inicial = models.DateTimeField()
    data_final = models.DateTimeField(blank=True, null=True)
    finalizada = models.BooleanField(default=False)
    hospedes = models.ManyToManyField(Hospede)
    quarto = models.ForeignKey(Quarto,
                               related_name="quarto utilizada")

    class Meta:
        db_table = "estadia"

    @property
    def qtde_dias(self):
        """
        Retorna quantidade de dias hospedados
        """
        
        if self.finalizada:
            f = self.data_final
        else:
            f = datetime.datetime.now()

        #TODO: implementar regra de negocio do horario
        return (f - self.data_inicial).days

    @property
    def danos(self):
        """
        Retorna a lista de danos da estadia
        """
        return Dano.objects.filter(estadia=self)

    @property
    def produtos(self):
        """
        Retorna a lista de produtos utilizados
        """
        from hotsys.produto.models import ProdutoItem
        return ProdutoItem.objects.filter(estadia=self)

    @property
    def total_danos(self):
        """
        Retorna o valor total de danos
        """
        data = self.danos.aggregate(Sum('valor'))
        return data['valor__sum']

    @property
    def total_produtos(self):
        """
        Retorna o valor total de danos
        """
        data = self.produtos.aggregate(Sum('valor_total'))
        return data['valor_total__sum']

    @property
    def total_estadia(self):
        """
        Retorna o valor das estadias
        """
        return self.qtde_dias * self.quarto.preco

    @property
    def total_pagar(self):
        """
        Total a pagar da estadia
        """
        total = Decimal('0.00')
        t_danos = self.total_danos
        t_produtos = self.total_produtos
        t_estadia = self.total_estadia

        if t_danos:
            total += t_danos

        if t_produtos:
            total += t_produtos

        if t_estadia:
            total += t_estadia

        return total

    def finalizar(self):
        self.data_final = datetime.datetime.now()
        self.finalizada = True
        self.save()

        self.quarto.estadia_atual = None
        self.quarto.estado = 'l' #Livre
        self.quarto.save()

class Dano(models.Model):
    estadia = models.ForeignKey("Estadia")
    desc = models.CharField(
        max_length=200,
        verbose_name=u"Descrição")

    valor = models.DecimalField(
        decimal_places=2, max_digits=10,
        verbose_name="Valor")

    grave = models.BooleanField(
        verbose_name="Grave")

    class Meta:
        db_table = "dano"


class RelatorioEstadiasMes(object):
    def __init__(self, mes):
        self.mes = mes
        self.queryset = Estadia.objects.filter(
            finalizada=True,
            data_inicial__year=mes.year,
            data_inicial__month=mes.month)

    def __iter__(self):
        return self.queryset.__iter__()
        
class RelatorioEstadias(object):
    def __init__(self):
        self.parts = [
            RelatorioEstadiasMes(d)
            for d in
            Estadia.objects.filter(finalizada=True).dates(
                'data_inicial', 'month', order='DESC')]


    def __iter__(self):
        return self.parts.__iter__()
