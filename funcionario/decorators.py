# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Funcionario

def acesso_ao_cargo(function, cargo):
    """
    Usado para pedir permissoes apenas para o creas
    """
    def call(request, *args, **kwargs):
        if not isinstance(request.user, Funcionario):
            reason = u"Você não possui as permissões necessárias"
            return render(request, 'acesso_negado.html', locals())

        if cargo and request.user.tipo != cargo:
            reason = u"Você não possui as permissões necessárias"
            return render(request, 'acesso_negado.html', locals())

        return function(request, *args, **kwargs)
            

    return call
