var adminHistoricoDownload = adminHistoricoDownload || {};

adminHistoricoDownload = (function () {
    'use strict';

    var resultList = document.getElementById('result_list'),
        resultListBody = resultList.getElementsByTagName('tbody')[0],
        lengthOfResultList = resultListBody.getElementsByTagName('tr').length,
        paginator = document.getElementsByClassName('paginator')[0],
        contentContainer = document.getElementById('content'),
        headerContent = contentContainer.getElementsByTagName('h1')[0],
        stringToMatch = 'Estatísticas';

    function init() {
        headerDownloads();
        mensagemHistoricoDownload();
    }

    function mensagemHistoricoDownload() {
        if (headerContent.textContent.indexOf(stringToMatch) > -1) {
            if (lengthOfResultList == 1) {
                paginator.textContent = lengthOfResultList + ' download realizado';
            } else if (lengthOfResultList == 0) {
                paginator.textContent = 'Nenhum download realizado';
            } else {
                paginator.textContent = lengthOfResultList + ' downloads realizados';
            }
        }
    }

    function headerDownloads() {
        if (headerContent.textContent == 'Selecione Estatísticas de Download para modificar'){
            headerContent.textContent = 'Estatísticas de Download';
        }
    }

    return {
        init: init
    };

})();

adminHistoricoDownload.init();
