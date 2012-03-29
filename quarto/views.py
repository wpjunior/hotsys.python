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

__all__ = ('AddQuarto', 'ListaQuarto', 'AtualizaQuarto', 'RemoveQuarto',
           'InicarEstadiaQuarto', 'AdicinarDanoQuarto')

from models import *
from forms import *
from hotsys.views import JSONResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    DeleteView, CreateView, UpdateView, ListView,
    FormView)

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

class InicarEstadiaQuarto(FormView):
    form_class = InicarEstadiaForm
    template_name = "quarto/iniciar_estadia.html"
    success_url = "/quarto/"
    _quarto = None

    def get_quarto(self):
        if not self._quarto:
            self._quarto = get_object_or_404(
                Quarto, pk=self.kwargs.get('pk'),
                estado='l')

        return self._quarto

    def get_context_data(self, *args, **kwargs):
        ctx = super(InicarEstadiaQuarto, self).get_context_data(*args, **kwargs)
        ctx['quarto'] = self.get_quarto()

        return ctx
                                             
    def _get_hospede(self):
        cpf = self.request.GET.get('cpf')

        try:
            hosp = Hospede.objects.get(cpf=cpf)
        except Hospede.DoesNotExist:
            return JSONResponse(None)
        else:
            return JSONResponse({'id': hosp.id,
                                 'nome': hosp.nome,
                                 'cpf': hosp.cpf})

    def get(self, *args, **kwargs):
        cmd = self.request.GET.get('cmd', None)

        if cmd == 'getHospede':
            return self._get_hospede()

        return super(InicarEstadiaQuarto, self).get(*args, **kwargs)

    def form_valid(self, form):
        quarto = self.get_quarto()
        
        estadia = Estadia(
            data_inicial=form.cleaned_data['data_inicial'],
            data_final=form.cleaned_data['data_final'],
            quarto=quarto)

        estadia.save()
        estadia.hospedes = form.cleaned_data['hospede']
        estadia.save()

        quarto.estadia_atual = estadia
        quarto.estado = 'o' #ocupado
        quarto.save()

        return redirect(self.get_success_url())


class AdicinarDanoQuarto(FormView):
    form_class = RegistrarDanoForm
    template_name = "quarto/reg_dano.html"
    _estadia = None
    success_url = "/quarto/"

    def get_estadia(self):
        if not self._estadia:
            quarto = get_object_or_404(
                Quarto, pk=self.kwargs.get('pk'),
                estado='o')

            self._estadia = quarto.estadia_atual

        return self._estadia

    def form_valid(self, form):
        dano = form.save(commit=False)
        dano.estadia = self.get_estadia()
        dano.save()

        if dano.grave:
            return redirect('/quarto/finalizar/%d/' % (dano.estadia.quarto.id))
        else:
            return redirect(self.get_success_url())
        
    def get_context_data(self, *args, **kwargs):
        ctx = super(AdicinarDanoQuarto, self).get_context_data(*args, **kwargs)
        
        ctx['estadia'] = self.get_estadia()
        
        return ctx
