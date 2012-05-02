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

__all__ = ("QuartoForm", "InicarEstadiaForm", "RegistrarDanoForm",
           "RegistrarConsumoForm", "AddConsumoForm")

import datetime

from django import forms
from models import *
from fields import HospedesField, ProdutosField
from hotsys.produto.models import Produto

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        exclude = ('estadia_atual', 'estado')


class InicarEstadiaForm(forms.Form):
    data_inicial = forms.DateField(
        label="Data inicial",
        input_formats=('%d/%m/%Y',),
        initial=datetime.date.today,
        widget=forms.DateInput(format='%d/%m/%Y'))

    data_final = forms.DateField(
        label="Data final",
        input_formats=('%d/%m/%Y',),
        widget=forms.DateInput(format='%d/%m/%Y'))
    
    reserva = forms.CharField(
        widget=forms.HiddenInput,
        required=False)

    hospede = HospedesField()

    def clean_hospede(self):
        data = self.cleaned_data['hospede']
        return Hospede.objects.in_bulk(data).values()

    def set_reserva(self, reserva):
        self.initial['data_inicial'] = reserva.data_inicial
        self.initial['data_final'] = reserva.data_final
        self.initial['reserva'] = reserva.id

class RegistrarDanoForm(forms.ModelForm):
    class Meta:
        model = Dano
        exclude = ('estadia',)

class RegistrarConsumoForm(forms.Form):
    produto = ProdutosField()

    def clean_produto(self):
        data = self.cleaned_data['produto']
        qtdes = {}
        
        for d in data:
            id, qtde = d.split('-')
            qtdes[int(id)] = int(qtde)
        
        prods = Produto.objects.in_bulk(qtdes.keys())

        return [(v, qtdes[k]) for k, v in prods.iteritems()]


    def save(self, *args, **kwargs):
        return self.cleaned_data['produto']

class AddConsumoForm(forms.Form):
    produto = forms.ChoiceField(
        label="Produto")

    qtde = forms.IntegerField(
        initial=1,
        label="Quantidade")


    def __init__(self, *args, **kwargs):
        super(AddConsumoForm, self).__init__(*args, **kwargs)
        choices = [(p.id, p.nome) for p in Produto.objects.all()]

        self.fields['produto'].choices = [('', '-----')] +choices
