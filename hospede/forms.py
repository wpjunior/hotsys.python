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

__all__ = ('HospedeForm',)

from models import *
from django import forms
from django.contrib.localflavor.br.forms import BRCPFField

class HospedeForm(forms.ModelForm):
    cpf = BRCPFField(
        label="CPF",
        required=True,
        error_messages={'invalid': u"CPF Inválido",
                        'max_digits': "Este campo requer 11 digitos",
                        'digits_only': "Este campo aceita apenas digitos"})

    data_nasc = forms.DateField(
        label="Data de nascimento",
        required=True,
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={'size':'15','class': 'date'}))

    class Meta:
        model = Hospede
