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

from django.conf.urls.defaults import patterns, url
from views import *
from hotsys.funcionario.decorators import acesso_ao_cargo

urlpatterns = patterns(
    '',
    url(r'^$', acesso_ao_cargo(ListaProduto.as_view(), 'g')),
    url(r'^add/$', acesso_ao_cargo(AddProduto.as_view(), 'g')),
    url(r'^atualiza/(?P<pk>\d+)/$', acesso_ao_cargo(AtualizaProduto.as_view(), 'g')),
    url(r'^remove/(?P<pk>\d+)/$', acesso_ao_cargo(RemoveProduto.as_view(), 'g')),
)
