# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from disciplina.models import Avaliacao


@user_passes_test(lambda u: (u.tipo == u.ALUNO and not u.bloqueado))
def disciplinas(request):
    context = {}
    avaliacoes = Avaliacao.objects.filter(aluno=request.user)
    context['avaliacoes'] = avaliacoes

    return render(request, 'disciplinas.html', context)
