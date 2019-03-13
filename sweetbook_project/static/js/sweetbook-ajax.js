//  the url for the rating button is add-rating
// and you"ll have to pass me the recipe id

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
$('#add-rating').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/sweetbook/like_recipe/', {recipe_id: recid}, function(data){
               $('#like_count').html(data);
               $('#add-rating').hide();

    });
});
