
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function searchCriteriaCollection(share) {
    var result = {};
    $("input.form-control").each(function (index) {
        var key = $(this).attr('id')
        if (typeof key === "undefined") {
            return
        }
        key = key.slice(3,key.length)

         //avoid empty shadowed parameters
         if($(this).val() != ''){
            result[key] = $(this).val();
         }
    });

    $( "select.form-control" ).each(function( index ) {
      var key = $(this).attr('id')
        if (typeof key === "undefined") {
            return
        }
        key = key.slice(3,key.length)

         //avoid empty shadowed parameters
         if($(this).val() ){
            result[key] = $(this).val();
         }
    });

    result['csrfmiddlewaretoken'] = getCookie('csrftoken');
    return result;
}
