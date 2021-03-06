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
           'InicarEstadiaQuarto', 'AdicinarDanoQuarto', 'ConsumoQuarto',
           'FinalizarQuarto', 'RelatorioEstadiasView', 'DetalheEstadia')

from models import *
from forms import *
from hotsys.views import JSONResponse
from django.shortcuts import get_object_or_404, redirect
from hotsys.produto.models import Produto, ProdutoItem
from hotsys.reserva.models import Reserva
from django.views.generic import (
    DeleteView, CreateView, UpdateView, ListView,
    TemplateView, DetailView,
    FormView)

class AddQuarto(CreateView):
    model = Quarto
    success_url = "/quarto/"
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
    _reserva = None

    def get_reserva(self):
        if not self._reserva:
            if self.request.META['REQUEST_METHOD'] == 'GET':
                reserva_id = self.request.GET.get('reserva', None)
            else:
                reserva_id = self.request.POST.get('reserva', None)

            if reserva_id:
                try:
                    reserva = Reserva.objects.get(id=int(reserva_id))
                except Reserva.DoesNotExist:
                    reserva = None
                    
                self._reserva = reserva
            
        return self._reserva

    def get_form(self, *args, **kwargs):
        form = super(InicarEstadiaQuarto, self).get_form(*args, **kwargs)
        reserva = self.get_reserva()

        if reserva:
            form.set_reserva(reserva)

        return form

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
        reserva = self.get_reserva()

        estadia = Estadia(
            data_inicial=form.cleaned_data['data_inicial'],
            data_final=form.cleaned_data['data_final'],
            quarto=quarto)

        if reserva:
            if reserva.pago:
                estadia.pre_pago = reserva.pago
            reserva.delete()

        estadia.save()
        estadia.hospedes = form.cleaned_data['hospede']
        estadia.save()

        quarto.estadia_atual = estadia
        quarto.estado = 'o' #ocupado
        quarto.save()

        return redirect(self.success_url)


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
            return redirect(self.success_url)
        
    def get_context_data(self, *args, **kwargs):
        ctx = super(AdicinarDanoQuarto, self).get_context_data(*args, **kwargs)
        
        ctx['estadia'] = self.get_estadia()
        
        return ctx

class ConsumoQuarto(FormView):
    form_class = RegistrarConsumoForm
    template_name = "quarto/consumo.html"
    _estadia = None
    success_url = "/quarto/"

    def get_estadia(self):
        if not self._estadia:
            quarto = get_object_or_404(
                Quarto, pk=self.kwargs.get('pk'),
                estado='o')

            self._estadia = quarto.estadia_atual

        return self._estadia

    def get_context_data(self, *args, **kwargs):
        ctx = super(ConsumoQuarto, self).get_context_data(*args, **kwargs)
        
        ctx['estadia'] = self.get_estadia()
        ctx['add_form'] = AddConsumoForm()
        
        return ctx

    def _get_produto(self):
        produto_id = self.request.GET.get('produtoId', None)

        try:
            prod = Produto.objects.get(id=produto_id)
        except Produto.DoesNotExist:
            return JSONResponse({'erro': "Produto não encontrado"})

        return JSONResponse({'nome': prod.nome, 'valor': float(prod.valor),
                             'id': prod.id})

    def get(self, *args, **kwargs):
        cmd = self.request.GET.get('cmd', None)

        if cmd == 'getProduto':
            return self._get_produto()

        return super(ConsumoQuarto, self).get(*args, **kwargs)

    def form_valid(self, form):
        produtos = form.save()
        estadia = self.get_estadia()
        
        for produto, qtde in produtos:
            item = ProdutoItem(
                produto=produto,
                estadia=estadia,
                qtde=qtde,
                valor_total=produto.valor*qtde)
            
            item.save()

            if produto.qtde != None:
                produto.qtde -= qtde
                produto.save()

        return redirect(self.get_success_url())


class FinalizarQuarto(TemplateView):
    template_name = "quarto/finalizar.html"
    _estadia = None
    success_url = "/quarto/"

    def get_estadia(self):
        if not self._estadia:
            quarto = get_object_or_404(
                Quarto, pk=self.kwargs.get('pk'),
                estado='o')

            self._estadia = quarto.estadia_atual

        return self._estadia

    def get_context_data(self, *args, **kwargs):
        ctx = super(FinalizarQuarto, self).get_context_data(*args, **kwargs)
        
        ctx['estadia'] = self.get_estadia()
        
        return ctx


    def post(self, *args, **kwargs):
        est = self.get_estadia()
        est.finalizar()

        return redirect(self.success_url)



class RelatorioEstadiasView(TemplateView):
    template_name = "quarto/relatorio.html"

    def get_relatorio(self):
        return RelatorioEstadias()

    def get_context_data(self, *args, **kwargs):
        ctx = super(RelatorioEstadiasView, self).get_context_data(*args, **kwargs)

        ctx['relatorio'] = self.get_relatorio()
        
        return ctx        


class DetalheEstadia(DetailView):
    model = Estadia
