# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import router
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy, ugettext as _
from disciplina.models import Disciplina, Avaliacao
from disciplina.forms import DisciplinaForm


def delete_selected(modeladmin, request, queryset):
    opts = modeladmin.model._meta

    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)

    n = queryset.count()
    if n:
        for obj in queryset:
            obj_display = force_text(obj)
            modeladmin.log_deletion(request, obj, obj_display)
        queryset.delete()
        modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
            "count": n, "items": model_ngettext(modeladmin.opts, n)
        }, messages.SUCCESS)

    return redirect('.')

delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")


def atualizar_situacao(modeladmin, request, queryset):
    queryset.aprovados().update(situacao=Avaliacao.APROVADO)
    queryset.reprovados_media().update(situacao=Avaliacao.REPROVADO_MEDIA)
    queryset.reprovados_falta().update(situacao=Avaliacao.REPROVADO_FALTA)
    queryset.reprovados_media().reprovados_falta().update(situacao=Avaliacao.REPROVADO_MEDIA_FALTA)

atualizar_situacao.short_description = "Atualizar situação dos alunos selecionados"


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'professor', 'turma', 'limite_faltas', 'limite_abonos', 'quant_alunos', 'data_inicio', 'data_termino')
    list_display_links = ('nome',)
    search_fields = ('nome', 'professor__nome')
    readonly_fields = ('data_criacao', 'data_atualizacao',)
    form = DisciplinaForm
    actions = [delete_selected]


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'nota', 'faltas', 'abonos', 'situacao',)
    list_editable = ('nota', 'faltas', 'abonos',)
    list_display_links = None
    search_fields = ('aluno__nome', 'disciplina__nome', 'disciplina__professor__nome')
    list_filter = ('disciplina__nome',)
    actions = [atualizar_situacao]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(AvaliacaoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
