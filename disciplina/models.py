# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from pessoa.models import Pessoa


class AvaliacaoQuerySet(models.QuerySet):
    def aprovados(self):
        return self.filter(
            (
                models.Q(nota__gte=settings.BUSINESS['media_aprovacao']) &
                models.Q(faltas__lte=models.F('disciplina__limite_faltas'))
            ) |
            (
                models.Q(faltas__gt=models.F('disciplina__limite_faltas')) &
                models.Q(abonos__gte=models.F('disciplina__limite_abonos')) &
                models.Q(disciplina__limite_faltas__gte=models.F('faltas') - models.F('disciplina__limite_abonos'))
            ) |
            (
                models.Q(faltas__gt=models.F('disciplina__limite_faltas')) &
                models.Q(abonos__lt=models.F('disciplina__limite_abonos')) &
                models.Q(disciplina__limite_faltas__gte=(models.F('faltas') - models.F('abonos')))
            )
        )

    def reprovados_media(self):
        return self.filter(models.Q(nota__lt=settings.BUSINESS['media_aprovacao']))

    def reprovados_falta(self):
        return self.filter(
            (
                models.Q(faltas__gt=models.F('disciplina__limite_faltas')) &
                models.Q(abonos__gte=models.F('disciplina__limite_abonos')) &
                models.Q(disciplina__limite_faltas__lt=models.F('faltas') - models.F('disciplina__limite_abonos'))
            ) |
            (
                models.Q(faltas__gt=models.F('disciplina__limite_faltas')) &
                models.Q(abonos__lt=models.F('disciplina__limite_abonos')) &
                models.Q(disciplina__limite_faltas__lt=(models.F('faltas') - models.F('abonos')))
            )
        )


class AvaliacaoManager(models.Manager):
    def get_queryset(self):
        return AvaliacaoQuerySet(self.model, using=self._db)

    def aprovados(self):
        return self.get_queryset().aprovados()

    def reprovados_media(self):
        return self.get_queryset().reprovados_media()

    def reprovados_falta(self):
        return self.get_queryset().reprovados_falta()


class Disciplina(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Disciplina')
    turma = models.CharField(max_length=255, verbose_name='Turma', blank=True)
    limite_faltas = models.IntegerField(verbose_name='Limite de faltas')
    limite_abonos = models.IntegerField(verbose_name='Limite de abonos')
    data_inicio = models.DateField(verbose_name='Data de início')
    data_termino = models.DateField(verbose_name='Data de término')
    professor = models.ForeignKey(Pessoa, limit_choices_to={'tipo': Pessoa.PROFESSOR}, related_name='professor')
    aluno = models.ManyToManyField(Pessoa, limit_choices_to={'tipo': Pessoa.ALUNO}, related_name='alunos', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação', default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização', default=timezone.now)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Disciplina'

    def quant_alunos(self):
        return len(self.aluno.all())
    quant_alunos.short_description = "Quantidade de alunos"


class Avaliacao(models.Model):
    CURSANDO = 'cursando'
    APROVADO = 'aprovado'
    REPROVADO_MEDIA = 'reprovado por grau'
    REPROVADO_FALTA = 'reprovado por frequência'
    REPROVADO_MEDIA_FALTA = 'reprovado por grau e frequencia'

    CHOICES_SITUACAO = (
        (CURSANDO, 'Cursando',),
        (APROVADO, 'Aprovado',),
        (REPROVADO_MEDIA, 'Reprovado por grau'),
        (REPROVADO_FALTA, 'Reprovado por frequência'),
        (REPROVADO_MEDIA_FALTA, 'Reprovado por grau e frequência'),

    )
    disciplina = models.ForeignKey(Disciplina)
    aluno = models.ForeignKey(Pessoa, limit_choices_to={'tipo': Pessoa.ALUNO})
    nota = models.DecimalField(verbose_name='Nota', decimal_places=2, max_digits=5, default=None, null=True, blank=True)
    faltas = models.IntegerField(verbose_name='Faltas', default=0)
    abonos = models.IntegerField(verbose_name='Abonos', default=0)
    situacao = models.CharField(max_length=255, verbose_name='Situação', choices=CHOICES_SITUACAO, default=CURSANDO)

    objects = AvaliacaoManager()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.aluno, self.disciplina)

    def get_situacao(self):
        if self.situacao == self.REPROVADO_MEDIA_FALTA:
            return u'Reprovado por Grau e Frequência'
        elif self.situacao == self.REPROVADO_FALTA:
            return u'Reprovado por Frequência'
        elif self.situacao == self.REPROVADO_MEDIA:
            return u'Reprovado por Grau'
        elif self.situacao == self.APROVADO:
            return u'Aprovado'
        else:
            return u'Cursando'

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = 'Avaliações'


def disciplina_post_save(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        Avaliacao.objects.filter(disciplina=instance).exclude(aluno=instance.aluno.all).delete()

        for aluno in instance.aluno.all():
            Avaliacao.objects.get_or_create(aluno=aluno, disciplina=instance)

models.signals.m2m_changed.connect(disciplina_post_save, sender=Disciplina.aluno.through)
