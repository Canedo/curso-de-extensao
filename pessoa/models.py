# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, data_nascimento, password=None, tipo=None):
        if not cpf:
            raise ValueError(_('Usuários devem ter CPF'))

        user = self.model(
            cpf=cpf,
            data_nascimento=data_nascimento
        )

        if not password:
            password = str(data_nascimento).replace("/", "")

        if not tipo:
            tipo = user.ALUNO
        user.tipo = tipo
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, data_nascimento, password):
        if not cpf:
            raise ValueError(_('Usuários devem ter CPF'))

        user = self.create_user(
            cpf,
            data_nascimento,
            password
        )
        user.tipo = user.FUNCIONARIO
        user.save(using=self._db)
        return user


class Pessoa(AbstractBaseUser):
    FUNCIONARIO = 1
    PROFESSOR = 2
    ALUNO = 3
    CHOICES_TIPO_PESSOA = (
        (FUNCIONARIO, 'Funcionário'),
        (PROFESSOR, 'Professor'),
        (ALUNO, 'Aluno'),
    )
    nome = models.CharField(max_length=255, verbose_name='Nome')
    sobrenome = models.CharField(max_length=255, verbose_name='Sobrenome', blank=True)
    data_nascimento = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação', default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização', default=timezone.now)
    tipo = models.IntegerField(max_length=255, choices=CHOICES_TIPO_PESSOA, verbose_name='Tipo de pessoa')

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['data_nascimento']

    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.tipo == self.FUNCIONARIO

    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return u'{0} {1}'.format(self.nome, self.sobrenome)

    get_full_name.short_description = 'Nome completo'

    def get_short_name(self):
        return self.nome

    def __unicode__(self):
        if self.tipo == self.FUNCIONARIO:
            return self.get_full_name()
        return u'{0}'.format(self.get_full_name())

    class Meta:
        verbose_name = 'Pessoa'


class Contato(models.Model):
    TELEFONE = 'telefone'
    EMAIL = 'email'
    CHOICES_TIPO_CONTATO = (
        (TELEFONE, 'Telefone',),
        (EMAIL, 'Email',),
    )
    tipo = models.CharField(max_length=255, choices=CHOICES_TIPO_CONTATO, verbose_name='Tipo de Contato')
    descricao = models.CharField(max_length=255, verbose_name='Descrição')
    pessoa = models.ForeignKey(Pessoa)

    def __unicode__(self):
        return u'{0} - {1}'.format(dict(self.CHOICES_TIPO_CONTATO)[self.tipo], self.descricao)


class DocumentosPendentes(models.Model):
    aluno = models.OneToOneField(Pessoa, limit_choices_to={'tipo': Pessoa.ALUNO})
    documentos = models.CharField(max_length=255, verbose_name='Documentos pendentes')
    outros = models.CharField(max_length=255, verbose_name='Outros', blank=True, default="",
                              help_text="Por favor, use vírgula (,) como separador para definir multiplos documentos")

    class Meta:
        verbose_name = 'Documentos pendentes de aluno'
        verbose_name_plural = 'Documentos pendentes de aluno'

    def __unicode__(self):
        return self.aluno.get_full_name()
