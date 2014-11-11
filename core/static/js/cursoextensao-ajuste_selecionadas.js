var ajusteSelecionadas = ajusteSelecionadas || {};

ajusteSelecionadas = (function () {
    'use strict';

    var deleteSelected = document.getElementsByName('action')[0],
        text,
        selectContainer;

    function init() {
        mensagemDeleteSelected();
    }

    function mensagemDeleteSelected() {
        if (deleteSelected) {
            selectContainer = deleteSelected.options[1]
            text = selectContainer.textContent;
            selectContainer.textContent = text.replace(/selecionados$/gi, 'selecionadas');
        }
    }

    return {
        init: init
    };

})();

ajusteSelecionadas.init();
