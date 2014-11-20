# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db import router
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy, ugettext as _
from pessoa.models import Pessoa, Contato, DocumentosPendentes
from pessoa.forms import PessoaChangeForm, PessoaCreationForm, DocumentosPendentesForm


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


class ContatoInline(admin.StackedInline):
    model = Contato
    extra = 0
    min_num = 1


class DocumentosPendentesInline(admin.StackedInline):
    model = DocumentosPendentes
    extra = 0
    min_num = 1
    form = DocumentosPendentesForm


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    add_form_template = 'admin/pessoa/add_form.html'
    list_display = ('nome', 'cpf', 'data_nascimento', 'email', 'tipo', )
    list_display_links = ('nome',)
    list_filter = ('tipo', 'is_active',)
    search_fields = ('nome', 'cpf',)
    readonly_fields = ('data_criacao', 'data_atualizacao',)
    inlines = [DocumentosPendentesInline, ContatoInline]
    form = PessoaChangeForm
    add_form = PessoaCreationForm
    actions = [delete_selected]

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'email', 'data_nascimento',),
        }),
        ('Permissões', {
            'fields': ('tipo', 'is_active',),
        })
    )
    add_fieldsets = fieldsets
    ordering = ('nome',)
    filter_horizontal = ()

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, DocumentosPendentesInline) and (not obj or obj.tipo != obj.ALUNO):
                continue
            yield inline.get_formset(request, obj), inline

    class Media:
        js = ('js/django.jquery.js', 'js/jquery.inputmask.min.js', 'js/django.inputmask.js',)


admin.site.unregister(Group)
