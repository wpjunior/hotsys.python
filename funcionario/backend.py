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

from django.core.validators import email_re
from models import Funcionario

class LoginBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        # verifica se e um email
        if email_re.match(username):
            try:
                user = Funcionario.objects.get(email=username)
            except Funcionario.DoesNotExist:
                return None

        # caso nao autentica no modo padrao
        else:
            try:
                user = Funcionario.objects.get(usuario=username)
            except Funcionario.DoesNotExist:
                return None

        if user:
            if password and user.check_senha(password):
                return user

        return None

    def get_user(self, user_id):
        return Funcionario.objects.get(id=user_id)
