# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import router
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy, ugettext as _
from downloads.models import Monografia, ArquivoHistorico


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


@admin.register(Monografia)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'autor',)
    readonly_fields = ('downloads',)
    actions = [delete_selected]


@admin.register(ArquivoHistorico)
class ArquivoHistoricoAdmin(admin.ModelAdmin):
    list_display = ('data', 'arquivo', 'usuario', 'ip',)
    list_display_links = None
    search_fields = ('arquivo__nome', 'ip', 'usuario',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ArquivoHistoricoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
