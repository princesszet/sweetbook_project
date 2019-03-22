// for rating recipes
$('#add-rating').click(function(mousevent){
    console.log("hi");
    var value;
    var x = mousevent.target.id;
    if (x == "rb-five") {
      value = 5;
    } else if (x == "rb-four") {
      value = 4;
    } else if (x == "rb-three") {
      value = 3;
    } else if (x == "rb-two") {
      value = 2;
    } else {
      value = 1;
    }
    console.log(value);
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/like-recipe/', {recipe_id: recid, recipe_value: value}, function(data){
               $('#like_count').html(data);
               // $('#add-rating').hide();
               // $('#text1').hide();
               $('#add-rating-box').hide();


    });
    // window.alert("Thank you for rating this recipe!");
});

// for saving recipes
$('#save-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/add-to-cookbook/', {recipe_id: recid}, function(data){
               $('#save-recipe').hide();

    });
    window.alert("Recipe saved!");
});



// for comments
// $('#submit').click(function(){
//     var recid;
//     recid = $(this).attr("data-recid");
//     var comment;
//     comment = String($("textarea").val());
//     $.post('/sweetbook/add-comment/', {recipe_id: recid, text: comment}, function(data){
//                $('#add-comment').hide();
//     });
// });

$('#submit').click(function(){
  var length = $(location).attr("href").split("/").length
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  $.ajax({
    type: "POST",
    url: "/"+$(location).attr("href").split("/").slice(length-4,length-1).join("/")+"/",
    data: {
          'recid': $(this).attr("data-recid"),
          'text': String($('textarea').val()),
          },
    success: function(data) {
      alert("success");
    },
    error: function(data) {
       alert("fail");
    }
  });
});


// for adding events to the calendar
$('#save-event').click(function(){
    var eventid;
    eventid = $(this).attr("data-eventid");
    $.get('/sweetbook/add-to-mycalendar/', {event_id: eventid}, function(data){
               $('#save-event').hide();
    });
});

// for deleting recipes
$('#delete-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/myrecipes/delete-recipe', {recipe_id: recid}, function(data){
               $('#delete_recipe').hide();

    });
    window.alert("Your recipe was deleted");
});

// -------------------------------------------------------------------------
// taken from https://docs.djangoproject.com/en/1.11/ref/csrf/
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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//---------------------------------------------------------------------------
