# -*- coding: utf-8 -*-

import unicodedata
from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse


class NewFileField(models.FileField):

    def __init__(self, *args, **kwargs):
        super(NewFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(NewFileField, self).clean(*args, **kwargs)
        if isinstance(data.name, unicode):
            data.name = unicodedata.normalize('NFKD', data.name).encode('ascii', 'ignore').lower()
        else:
            data.name = unicodedata.normalize('NFKD', unicode(data.name, 'UTF-8')).encode('ascii', 'ignore').lower()
        return data


class ArquivoQuerySet(models.QuerySet):
    def pesquisa(self, query):
        if not query:
            return self
        return self.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))


class Monografia(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    autor = models.CharField(max_length=255, verbose_name='Autor', default='Autor Desconhecido')
    slug = AutoSlugField(populate_from='nome', unique=True)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    arquivo = NewFileField()
    downloads = models.IntegerField(verbose_name='Quantidade de downloads realizados', default=0)

    objects = ArquivoQuerySet.as_manager()

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Monografia'

    def get_absolute_url(self):
        return reverse('download', kwargs={'slug': self.slug})

    def registre(self, pessoa, ip):
        if pessoa.is_anonymous():
            usuario = 'Anônimo'
        else:
            usuario = str(pessoa)
        ArquivoHistorico.objects.create(usuario=usuario, arquivo=self, ip=ip)


class ArquivoHistorico(models.Model):
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data da Ação")
    arquivo = models.ForeignKey(Monografia, verbose_name='Arquivo')
    ip = models.IPAddressField(verbose_name='Endereço IP')
    usuario = models.CharField(max_length=255, verbose_name="Usuário")

    def __unicode__(self):
        return u'[{2}][{0}] {1}: {3}'.format(self.data, self.arquivo, self.ip, self.usuario)

    class Meta:
        verbose_name = 'Estatísticas de Download'
        verbose_name_plural = verbose_name
