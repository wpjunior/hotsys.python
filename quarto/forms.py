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

__all__ = ("QuartoForm", "InicarEstadiaForm", "RegistrarDanoForm")

import datetime

from django import forms
from models import *
from fields import HospedesField

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
        label="Data inicial",
        input_formats=('%d/%m/%Y',),
        widget=forms.DateInput(format='%d/%m/%Y'))
    
    hospede = HospedesField()

    def clean_hospede(self):
        data = self.cleaned_data['hospede']
        return Hospede.objects.in_bulk(data).values()

class RegistrarDanoForm(forms.ModelForm):
    class Meta:
        model = Dano
        exclude = ('estadia',)
