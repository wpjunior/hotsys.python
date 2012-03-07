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

__all__ = ('AddQuarto', 'ListaQuarto', 'AtualizaQuarto', 'RemoveQuarto')

from models import *
from forms import *
from django.views.generic import DeleteView, CreateView, UpdateView, ListView

class AddQuarto(CreateView):
    model = Quarto
    success_url = "/hospede/"
    form_class = QuartoForm

class AtualizaQuarto(UpdateView):
    model = Quarto
    success_url = "/quarto/"
    form_class = QuartoForm

class RemoveQuarto(DeleteView):
    model = Quarto
    success_url = "/quarto/"

class ListaQuarto(ListView):
    model = Quarto
    paginate_by = 20
