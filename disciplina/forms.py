# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from disciplina.models import Disciplina


class DisciplinaForm(forms.ModelForm):
    aluno = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(
        tipo=get_user_model().ALUNO),
        widget=widgets.FilteredSelectMultiple(verbose_name='Alunos', is_stacked=False), required=False)

    class Meta:
        model = Disciplina
        fields = (
            'nome',
            'turma',
            'limite_faltas',
            'limite_abonos',
            'data_inicio',
            'data_termino',
            'professor',
            'aluno',
        )
