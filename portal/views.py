# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from disciplina.models import Avaliacao
from pessoa.models import Pessoa
from django.contrib.sites.shortcuts import get_current_site
from portal.forms import CustomPasswordResetForm

def home(request):
    return render(request, 'base.html')


def witty(request):
    context = {'link': settings.IFRAME_URL}
    return render(request, 'witty.html', context)


@user_passes_test(lambda u: u.tipo == u.FUNCIONARIO)
def historicos(request):
    context = {}
    aluno_id = int(request.GET.get('aluno', 0))
    alunos_pk_list = Avaliacao.objects.values_list('aluno__pk').distinct()
    alunos = Pessoa.objects.filter(id__in=alunos_pk_list)
    historicos = Avaliacao.objects.all()

    if aluno_id:
        historicos = historicos.filter(aluno__id=aluno_id)
    if historicos.count() == 0 and aluno_id:
        messages.add_message(request, messages.ERROR, 'O aluno informado não existe')

    context['aluno_id'] = aluno_id
    context['alunos'] = alunos
    context['historicos'] = historicos
    return render(request, 'historico.html', context)


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
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválida!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_logout(request):
    logout(request)
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

def esqueci_senha(request):
    return password_reset(request,
                          template_name='forgot_password.html',
                          password_reset_form=CustomPasswordResetForm,
                          subject_template_name='email/password_reset_confirm_subject.txt',
                          html_email_template_name='email/password_reset_confirm',)

def esqueci_senha_sucesso(request):
    messages.add_message(request, messages.SUCCESS, 'Um email será enviado em breve para o endereço de email informado com mais informações para redefinir a sua senha.')
    return HttpResponseRedirect(reverse('home'))

def redefinir_senha(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='password_reset.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('home'))
