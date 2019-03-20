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
    $.get('/sweetbook/like_recipe/', {recipe_id: recid, recipe_value: value}, function(data){
               $('#like_count').html(data);
               $('#add-rating').hide();
               $('#text1').hide();

    });
    window.alert("Thank you for rating this recipe!");
});

// for saving recipes
$('#save-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/add_to_cookbook/', {recipe_id: recid}, function(data){
               $('#save-recipe').hide();

    });
    window.alert("Recipe saved!");
});

// for comments
$('#submit').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    var text;
    text = String($("textarea").val());
    $.get('/sweetbook/add_to_cookbook/', {recipe_id: recid, comment_text: text}, function(data){
               $('#add-comment').hide();
    });
});

// for adding events to the calendar
$('#save-event').click(function(){
    var eventid;
    eventid = $(this).attr("data-eventid");
    $.get('events/(?P<event_slug>[\w\-]+)/add_to_mycalendar/', {event_id: eventid}, function(data){
               $('#save-event').hide();
    });
});
