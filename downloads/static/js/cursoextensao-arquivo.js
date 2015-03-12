var updateHistory = function(slug, page) {
    if (page === undefined) page = 1;
    var arqHistory = $('.file-history'),
        pager = $('.history-pager'),
        pageNext = $('.history-next'),
        pagePrevious = $('.history-previous'),
        numPage = $('.history-page'),
        maxPage = $('.history-maxpages');
    arqHistory.html('');
    $.get('history/' + slug + '?page=' + page, function(history) {
        if (page == history.num_pages) {
            pageNext.parent().attr('class', 'disabled');
            pageNext.attr('href', '#');
        } else {
            pageNext.parent().attr('class', '');
        }
        if (page == 1) {
            pagePrevious.parent().attr('class', 'disabled');
            pagePrevious.attr('href', '#');
        } else {
            pagePrevious.parent().attr('class', '');
        }
        numPage.text(history.number);
        maxPage.text(history.num_pages);
        pager.data('slug', slug);
        pager.data('page', page);
        pager.data('num_pages', history.num_pages);

        $.each(history.actions, function(index, action) {
            var text = action.fields.data + ' - ' + action.fields.ip + ' - ' + action.fields.usuario;
            $('<li>')
                .attr('class', 'list-group-item')
                .text(text)
                .appendTo(arqHistory);
        });
    });
}

var arquivoModal = function() {
    var $that = $(this),
        arqNome = $('.file-nome'),
        arqDescricao = $('.file-descricao'),
        arqDownloads = $('.file-downloads'),
        arqHistory = $('.file-history'),
        downloads = $('#download');
    arqDescricao.html('');
    arqDownloads.html('');
    arqHistory.html('');

    $('#modal-arquivo').modal('show');

    $.get('info/' + $that.data('slug'), function(info) {
        arqNome.html(info.fields.nome);
        arqDescricao.html(info.fields.descricao);
        arqDownloads.html(info.fields.downloads);
        downloads.attr('href', info.url);
        downloads.toggleClass('unavailable', !info.tem_arquivo)
        updateHistory($that.data('slug'));
    });
    return false;
}


$(document).ready(function() {
    var pageNext = $('.history-next'),
        pagePrevious = $('.history-previous'),
        historyPager = $('.history-pager');

    $('.file-link').click(arquivoModal);
    pageNext.click(function() {
        if ($(this).parent().attr('class') !== 'disabled') {
            updateHistory(historyPager.data('slug'), historyPager.data('page') + 1);
        }
        return false;
    });
    pagePrevious.click(function() {
        if ($(this).parent().attr('class') !== 'disabled') {
            updateHistory(historyPager.data('slug'), historyPager.data('page') - 1);
        }
        return false;
    });
});
