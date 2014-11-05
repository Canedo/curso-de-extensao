# -*- encoding: utf-8 -*-
from django import forms
from pessoa.models import Pessoa
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not Pessoa.objects.filter(email=email).exists():
            raise forms.ValidationError('Por favor, insira um email válido cadastrado no sistema.')
        return email
