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

__all__ = ('AddFuncionario', 'ListaFuncionario',
           'AtualizaFuncionario', 'RemoveFuncionario',
           'SenhaFuncionario')

from models import *
from forms import *
from django.views.generic import (
    DeleteView, CreateView,
    UpdateView, ListView, FormView)

from django.shortcuts import get_object_or_404

class AddFuncionario(CreateView):
    model = Funcionario
    success_url = "/funcionario/"
    form_class = AddFuncionarioForm

class AtualizaFuncionario(UpdateView):
    model = Funcionario
    success_url = "/funcionario/"
    form_class = AtualizaFuncionarioForm

class RemoveFuncionario(DeleteView):
    model = Funcionario
    success_url = "/funcionario/"

class ListaFuncionario(ListView):
    model = Funcionario
    paginate_by = 20
    template_name = "funcionario/funcionario_list.html"

class SenhaFuncionario(FormView):
    success_url = "/funcionario/"
    template_name = "funcionario/senha.html"

    def get_object(self):
        return get_object_or_404(Funcionario, id=self.kwargs.get('pk'))

    def get_form(self, *args, **kwargs):
        return SenhaFuncionarioForm(self.get_object())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = SenhaFuncionarioForm(self.object, request.POST)
        
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
