# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


def home(request):
    return render(request, 'base.html')


def contato(request):
    return render(request, 'base.html')


def access(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if not username:
        messages.add_message(request, messages.ERROR, 'O CPF do usuário é obrigatório')
    elif not password:
        messages.add_message(request, messages.ERROR, 'A senha do usuário é obrigatória')
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Usuário autenticado com sucesso!')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválida!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.WARNING, 'Você desconectou-se')
    return HttpResponseRedirect('/')


@login_required
def alterar_senha(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Sua senha foi alterada com sucesso. Por favor, autentique-se novamente')
            return HttpResponseRedirect('/')

    return render(request, 'change_password.html', {'form': form})
