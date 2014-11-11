var ajusteHistorico = ajusteHistorico || {};

ajusteHistorico = (function () {
    'use strict';

    var linkHistorico = document.getElementsByClassName('historylink')[0];

    function init() {
        mensagemChangeLinkText();
    }

    function mensagemChangeLinkText() {
        if (linkHistorico) {
            linkHistorico.textContent = 'Log';
        }
    }

    return {
        init: init
    };

})();

ajusteHistorico.init();
