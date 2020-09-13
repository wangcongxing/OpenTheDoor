$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
        }
    });

    var currentUrl = window.location.href;
    if (currentUrl.indexOf("/app/templateapp/") > 0) {

    } else if (true) {
        console.log("to do")
    }
});