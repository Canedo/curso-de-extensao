# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from downloads.models import Monografia, ArquivoHistorico


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def download(request, slug):
    arquivo = get_object_or_404(Monografia, slug=slug)
    arquivo.downloads += 1
    arquivo.save()
    arquivo.registre(request.user, _get_client_ip(request))
    response = HttpResponse(arquivo.arquivo)
    response['Content-Disposition'] = u'attachment; filename={0}'.format(arquivo.arquivo.name[2:])
    return response


def monografias(request):
    page = int(request.GET.get('page', 1))
    q = request.GET.get('q', '')

    qs = Monografia.objects.pesquisa(q)
    paginator = Paginator(qs, 25)
    try:
        lista_arquivos = paginator.page(page)
    except EmptyPage:
        lista_arquivos = paginator.page(paginator.num_pages)

    return render(request, 'arquivos.html', {'arquivos': lista_arquivos, 'q': q})


def info(request, slug):
    arquivo = get_object_or_404(Monografia, slug=slug)
    obj_to_json = lambda obj: json.loads(serialize('json', obj))
    formatted = obj_to_json([arquivo])[0]
    formatted['url'] = arquivo.get_absolute_url()
    formatted['tem_arquivo'] = True if arquivo.arquivo else False
    return JsonResponse(formatted, safe=False)


@user_passes_test(lambda u: u.tipo == u.FUNCIONARIO)
def history(request, slug):
    historico = get_list_or_404(ArquivoHistorico, arquivo__slug=slug)
    obj_to_json = lambda obj: json.loads(serialize('json', obj))
    page = int(request.GET.get('page', 1))
    paginator = Paginator(historico, 10)
    try:
        historico_pag = paginator.page(page)
    except EmptyPage:
        historico_pag = paginator.page(paginator.num_pages)

    formatted = {}
    formatted['actions'] = obj_to_json(historico_pag)
    formatted['number'] = historico_pag.number
    formatted['num_pages'] = historico_pag.paginator.num_pages
    formatted['next_page_number'] = historico_pag.next_page_number() if page < historico_pag.paginator.num_pages else None
    formatted['previous_page_number'] = historico_pag.previous_page_number() if page > 1 else None
    return JsonResponse(formatted, safe=False)
