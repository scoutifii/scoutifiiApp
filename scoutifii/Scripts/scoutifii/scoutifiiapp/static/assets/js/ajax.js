$(function(){
        $('#search').keyup(function(){
            const csrftoken = getCookie('csrftoken');
            $.ajax({
                type: "POST",
                url: "{% url 'searching' %}",
                data: {
                    'search_term': $('#search').val(),
                    "X-CSRFToken": csrftoken
                },
                success: searchSuccess,
                dataType: "html"
            });
        });
    });

function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data);
}

 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie name begin with the name you want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');