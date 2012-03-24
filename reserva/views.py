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

import datetime
import json

from models import *
from forms import *

from hotsys.quarto.models import Quarto
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    DeleteView, CreateView, UpdateView, ListView,
    FormView)

class BuscarQuartosMixIn(object):
    def _buscar_quartos(self):
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')

        try:
            data_inicial = datetime.datetime.strptime(data_inicial, '%d/%m/%Y').date()
        except ValueError:
            return {'erro': u"data inicial inválida"}

        try:
            data_final = datetime.datetime.strptime(data_final, '%d/%m/%Y').date()
        except ValueError:
            return {'erro': u"data final inválida"}

        data = []
        for q in Quarto.objects.all():
            if not q.tem_reserva(data_inicial, data_final):
                data.append([q.id, q.nome, float(q.preco), q.num_leitos])

        return data

    def get(self, *args, **kwargs):
        acao = self.request.GET.get('acao')
        
        if acao == 'buscar_quartos':
            resp = self._buscar_quartos()
            return HttpResponse(json.dumps(resp))

        return super(BuscarQuartosMixIn, self).get(*args, **kwargs)

class ListaReserva(ListView):
    model = Reserva
    paginate_by = 20

class AddReserva(BuscarQuartosMixIn, CreateView):
    model = Reserva
    success_url = "/reserva/"
    form_class = ReservaForm

class HospedarReserva(CreateView):
    model = Reserva
    success_url = "/reserva/"
    form_class = ReservaForm

class AtualizaReserva(BuscarQuartosMixIn, UpdateView):
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
