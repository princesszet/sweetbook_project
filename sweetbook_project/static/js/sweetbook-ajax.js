// @login_required
// def add_rating(request):
//
//     rec_id = None
//     if request.method == "GET":
//         rec_id = request.GET['recipe_id']
//         ratings = 0
//         rating = 0
//         if rec_id:
//             rec = Recipe.objects.get(id=int(rec_id))
//             if rec:
//                 ratings = rec.ratings + 1
//                 rec.ratings = ratings
//                 total = rec.rating
//                 rec.total = total
//                 rating = total / ratings
//                 rec.rating = rating
//                 rec.save()
//     return HttpResponse(ratings, rating)

//
// Lucy, the button to make this work has to be something like this (although I'm not sure!):
// <button id="add_rating" data-recipeid="{{recipe.id}}">Rate the recipe</button>

//GOOD WORKING
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

    });
});

// def add_to_cookbook(request):
// 	# add a recipe to the user cookbook
//     user = None
//
//     if request.user.is_authenticated():
//         user = request.user
//
//     recipe_id = None
//     if request.method == "GET" and user:
//         cat_id = request.GET['recipe_id']
//         if recipe_id:
//             recipe = Recipe.objects.get(id = int(recipe_id))
//             if recipe:
//                 saved_recipe = SavedRecipe.objects.get_or_create(recipe = recipe, user=user)
//                 saved_recipe.save()
//     returnHttpResponse(saved_recipe)

$('#save-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/add_to_cookbook/', {recipe_id: recid}, function(data){
               // $('#like_count').html(data);
               $('#save-recipe').hide();
    });
});
