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

__all__ = ('ListaReserva', 'AddReserva', 'HospedarReserva',
           'AtualizaReserva', 'CancelarReserva', 'ConfirmarReserva')

from models import *
from forms import *

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    DeleteView, CreateView, UpdateView, ListView,
    FormView)

class ListaReserva(ListView):
    model = Reserva
    paginate_by = 20

class AddReserva(CreateView):
    model = Reserva
    success_url = "/reserva/"
    form_class = ReservaForm

class HospedarReserva(CreateView):
    model = Reserva
    success_url = "/reserva/"
    form_class = ReservaForm

class AtualizaReserva(UpdateView):
    model = Reserva
    success_url = "/reserva/"
    form_class = ReservaForm

class ConfirmarReserva(FormView):
    form_class = ConfirmarReservaForm
    template_name = "reserva/confirmar.html"
    success_url  = "/reserva/"

    def get_reserva(self):
        return get_object_or_404(
            Reserva,
            id=self.kwargs['pk'])

    def form_valid(self, form):
        reserva = self.get_reserva()
        valor = float(form.cleaned_data['valor'])

        reserva.confirmar(valor)

        return redirect(self.success_url)

class CancelarReserva(DeleteView):
    model = Reserva
    success_url = "/reserva/"
