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
    // value = $('input:radio[name='rate']:checked','#add-rating').val();
    // value = $('id').val();
    $.get('/sweetbook/like_recipe/', {recipe_id: recid, recipe_value: value}, function(data){
               $('#like_count').html(data);
               $('#add-rating').hide();
               $('#text1').hide();

    });
    window.alert("Thank you for rating this recipe!");
});


$('#save-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/add_to_cookbook/', {recipe_id: recid}, function(data){
               // $('#like_count').html(data);
               $('#save-recipe').hide();

    });
    window.alert("Recipe saved!");
});

// $('#submit').click(function(){
//     var recid;
//     recid = $(this).attr("data-recid");
//     var text;
//     text = String($("textarea").val());
//     $.get('/sweetbook/add_to_cookbook/', {recipe_id: recid, comment_text: text}, function(data){
//                // $('#like_count').html(data);
//                $('#add-comment').hide();
//     });
// });

$('#search').keyup(function(){
  var query;
  query = $(this).val();
  console.log(query);
  $.get('/sweetbook/search/', {search: query}, function(data){
    $('#recs').html(data);
  });
});
