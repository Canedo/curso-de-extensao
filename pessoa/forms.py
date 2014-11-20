# -*- coding: utf-8 -*-

from django import forms
from pessoa.models import Pessoa, DocumentosPendentes
from localflavor.br.forms import BRCPFField
from core.models import CHOICES_DOCUMENTOS


class PessoaChangeForm(forms.ModelForm):
    cpf = BRCPFField()

    class Meta:
        model = Pessoa
        fields = ('nome', 'data_nascimento', 'cpf', 'email', 'bloqueado', 'tipo',)

    def clean_password(self):
        return self.initial['password']


class PessoaCreationForm(PessoaChangeForm):

    def save(self, commit=True):
        user = super(PessoaCreationForm, self).save(commit)
        user.set_password(self.cleaned_data['data_nascimento'].strftime('%d%m%Y'))
        if commit:
            user.save()
        return user


class DocumentosPendentesForm(forms.ModelForm):
    documentos = forms.MultipleChoiceField(choices=CHOICES_DOCUMENTOS, widget=forms.CheckboxSelectMultiple,
                                           required=False, label='Documentos Pendentes')

    class Meta:
        model = DocumentosPendentes
        fields = ('documentos', 'outros')
