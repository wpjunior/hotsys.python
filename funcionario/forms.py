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

__all__ = ("AddFuncionarioForm", "AtualizaFuncionarioForm", "SenhaFuncionarioForm")

from django import forms
from models import *

class AddFuncionarioForm(forms.ModelForm):
    senha1 = forms.CharField(label=u"Senha",
                             widget=forms.PasswordInput)
    senha2 = forms.CharField(label=u"Confirmação de senha",
                             widget=forms.PasswordInput)

    def clean_senha2(self):
        senha1 = self.cleaned_data.get("senha1", "")
        senha2 = self.cleaned_data["senha2"]

        if senha1 != senha2:
            raise forms.ValidationError(u"As duas senhas não são iguais")
        return senha2

    def save(self, commit=True):
        user = super(AddFuncionarioForm, self).save(commit=False)
        user.set_senha(self.cleaned_data["senha1"])

        if commit:
            user.save()

        return user

    class Meta:
        model = Funcionario
        exclude = ('senha',)


class AtualizaFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        exclude = ('senha',)

class SenhaFuncionarioForm(forms.Form):
    senha1 = forms.CharField(
        label=u"Nova senha",
        widget=forms.PasswordInput)

    senha2 = forms.CharField(
        label=u"Confirmação nova senha",
        widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SenhaFuncionarioForm, self).__init__(*args, **kwargs)

    def clean_senha2(self):
        senha1 = self.cleaned_data.get('senha1')
        senha2 = self.cleaned_data.get('senha2')

        if senha1 and senha2:
            if senha1 != senha2:
                raise forms.ValidationError(u"As senhas não conferem")
        return senha2

    def save(self, commit=True):
        self.user.set_senha(self.cleaned_data['senha1'])

        if commit:
            self.user.save()

        return self.user
