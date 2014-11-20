# -*- coding: utf-8 -*-

from core.models import CHOICES_DOCUMENTOS
from disciplina.models import Disciplina
from django import forms
from localflavor.br.forms import BRCPFField
from pessoa.models import Pessoa, DocumentosPendentes


class PessoaChangeForm(forms.ModelForm):
    cpf = BRCPFField()

    class Meta:
        model = Pessoa
        fields = ('nome', 'data_nascimento', 'cpf', 'email', 'bloqueado', 'tipo',)

    def clean_password(self):
        return self.initial.get('password')

    def clean_tipo(self):
        alterado = self.cleaned_data.get('tipo')
        inicial = self.initial.get('tipo')

        if alterado == inicial or inicial != Pessoa.PROFESSOR:
            return alterado

        instancia_id = self.instance.id
        instancia_nome = self.instance.nome
        professor_ativo = Disciplina.objects.filter(professor__id=instancia_id)

        if inicial == Pessoa.PROFESSOR and professor_ativo:
            mensagem_erro = 'O(A) professor(a) {nome_professor} possui disciplinas ligados a ele(a), \
                             portanto não é permitido alterar o seu tipo.'.format(nome_professor=instancia_nome)
            raise forms.ValidationError(mensagem_erro)

        return alterado


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
