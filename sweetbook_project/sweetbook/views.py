import os
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sweetbook_project.settings')

import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django import forms
from django.contrib.auth.models import User
from sweetbook.models import User, Event, Recipe, SavedRecipe, Comment
from sweetbook.forms import CommentForm, RecipeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from sweetbook.forms import UserProfileRegistrationForm
from sweetbook.models import UserProfile
from datetime import datetime
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt,csrf_protect,ensure_csrf_cookie
'''
Cookies helper functions which help storing cookies on the server side
Number of cookies are stored and displayed in the home page

'''

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # get cookies from the last day
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits']= visits


'''
Home view returns to the template:
- a list of 10 top rated recipes
- the recipe of the day ( count a recently added recipe with the biggest number of comments)
- the latest events, in the date order (the first event is the closest to present moment)

'''
def home(request):

    top_rated_recipes = Recipe.objects.order_by('rating')[::-1][:10]      # top rated recipes

    # find out the most commented recipe from the last 5 recipes added recently
    most_commented_recipes= []
    context_dict = {}

    for recipe in Recipe.objects.order_by('last_modified')[:5]:
        comments_count = recipe.comment_set.count()                       # add the recipes to a list containing the number of comments as well
        most_commented_recipes.append([comments_count,recipe])
    most_commented_recipes.sort(key=lambda x: x[0])                       # sort the list

    if len(most_commented_recipes) > 0:
        recipe_of_the_day = most_commented_recipes[0][1]                  # get the first element of the sorted list
        context_dict ["recipeofday"] = recipe_of_the_day

    latest_events = Event.objects.filter().order_by('date')[:10]

    # add to context dictionary
    context_dict ["toprated"] = top_rated_recipes
    context_dict ["latestevents"] = latest_events

    # count the visits
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # let tamplate handle the presentation of data
    response = render(request, 'sweetbook/home.html', context=context_dict)
    return response


'''
Recipes view will return to template:

- a list of the recently added(or modified) recipes

'''
def recipes(request):

    context_dict={}
    last_recipes = Recipe.objects.order_by('last_modified')[:20]
    context_dict["recipes"] = last_recipes

    return render(request, 'sweetbook/recipes.html', context_dict)

'''
chosen-recipe view will return to template:

- the recipe that the user wants to access
- the comments that other users made on the recipe
- the user that created the recipe

'''
@csrf_exempt
def chosen_recipe(request, recipe_slug):

    context_dict = {}
    try:
        # get the information about recipe, comments, user
        recipe = Recipe.objects.get(recipe_slug=recipe_slug)
        comments = Comment.objects.filter (recipe = recipe)
        user = User.objects.filter ( recipe = recipe)

        # store them in the context dictionary,if found
        context_dict['comments'] = comments
        context_dict['recipe'] = recipe
    except Recipe.DoesNotExist:
        context_dict['comments'] = None
        context_dict['recipe'] = None

    return render (request, 'sweetbook/chosen_recipe.html', context_dict)

'''
contactus view will return to template and empty dictionary

'''
def contactus(request):
	return render (request, 'sweetbook/contactus.html',{})


'''
add-comment view which will deal with receives a POST request and stores the given details in the database

'''
@login_required
# @requires_csrf_token
@csrf_exempt
@ensure_csrf_cookie
def add_comment(request, recipe_slug):
    try:
        # get the recipe from the recipe slug
        recipe = Recipe.objects.get(recipe_slug = recipe_slug)
    except Recipe.DoesNotExist:
        recipe = None
        user = None

    # get the user
    if request.user.is_authenticated():
        user = request.user

    if request.method == 'POST':

        # if it was  POST request, get the text message and save the new comment
        comment_text = request.POST.get('text')
        if recipe and user:
            comment = Comment.get_or_create(user = user, recipe = recipe, description = text)
            comment.save()
            # return chosen_recipe(request, recipe_slug)
            #return render (request, 'sweetbook/ad.html', context_dict)
            return chosen_recipe(request, recipe.recipe_slug)

    context_dict = {'form':form, 'recipe':recipe}
    return render (request, 'sweetbook/add_comment.html', context_dict)

'''
add-new-recipe view gets a form from the user, and saves a the recipe in the database

'''
@login_required
def add_new_recipe(request):
    user = None
    if request.user.is_authenticated():
        user = request.user

    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save (commit=False)
            recipe.user = user
            recipe.save()
            return chosen_recipe(request, recipe.recipe_slug)
        else:
            print(form.errors)

    context_dict = {'form':form}
    return render (request, 'sweetbook/new_recipe.html', context_dict)

'''
events view - returns to the template:
    - a list of all events, ordered by date

'''
def events (request):
    context_dict = {}
    latest_events = Event.objects.order_by('date')[:10]
    context_dict["events"] = latest_events
    return render(request, 'sweetbook/events.html', context_dict)


'''
chosen-event view - returns to the template:
    - the event that is requested using the event_slug
'''

def chosen_event(request, event_slug):
    context_dict = {}
    try:
        event = Event.objects.get(event_slug=event_slug)
        context_dict['event'] = event
    except Category.DoesNotExist:
        context_dict['event'] = None
    return render (request, 'sweetbook/chosen_event.html', context_dict)


'''
add-to-cookbook view
    - take the recipe_id from GET request
    - finds out the recipe associated with it
    - uses the SavedRecipe method to store it in the database
(SavedRecipe contains the recipes created by other users, but which want to be stored by the current user on his profile)

'''
@login_required
def add_to_cookbook(request):
	# add a recipe to the user cookbook
    user = None

    if request.user.is_authenticated():
        user = request.user

    recipe_id = None
    if request.method == "GET" and user:
        recipe_id = request.GET['recipe_id']                    # get the recipe_id
        if recipe_id:
            recipe = Recipe.objects.get(id = int(recipe_id))
            if recipe:
                # save the recipe in the database
                saved_recipe = SavedRecipe.objects.get_or_create(recipe = recipe, user=user)[0]
                saved_recipe.save()

    return HttpResponse(saved_recipe)


'''
add-to-mycalendar view:
    - takes an event_id using the GET request
    - find out what the current event is
    - stores the event in the current users' s profile ( visible in the /mycalendar/ page)

'''

@login_required
def add_to_mycalendar(request):
    user = None
    user_profile = None

    if request.user.is_authenticated():
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)

    event_id = None
    if request.method == "GET" and user:
        event_id = request.GET['event_id']
        if event_id:
            event = Event.objects.get(id = int(event_id))
            if event:
                user_profile.events.add(event)
                user_profile.save()
    return HttpResponse(event)


'''
like-recipe view:
    - get the receipe_id using the GET request
    - gets the value given also through the GET request (which is either 1,2,3,4,5)
    - computes the average

'''
@login_required
def like_recipe(request):
    rec_id = None
    if request.method == 'GET':
        rec_id = request.GET['recipe_id']
        rec_value = request.GET['recipe_value']

    rating = 0

    if rec_id:
        rec = Recipe.objects.get(id=int(rec_id))
        if rec:

            # if the rating of the recipe is 0, the rating average will be the first rating
            if rating == 0:
                rating = float(rec_value)
            else:
                rating = (float(rec.rating) + float(rec_value))/2
            rec.rating =  rating
            rec.save()

    return HttpResponse(rating)


'''
myaccount view - returns to the template:
    - the information about the user (username)
    - the information about his profile (surname, firstname, picture)
'''

@login_required
def myaccount(request):
    user = None
    context_dict = {}

    if request.user.is_authenticated():
        user = request.user

    context_dict["user"] = user
    context_dict["userprofile"] = get_object_or_404(UserProfile, user=user)
    return render(request, 'sweetbook/myaccount.html', context_dict)


'''
delete_myaccount view:
    - finds out the user who is authenticated and deletes him
    - redirect to the home page

'''

@login_required
def delete_myaccount(request):

    user = None

    if request.user.is_authenticated():
        user = request.user
    user.delete()

    return HttpResponseRedirect(reverse('home'))


'''
mybakebook view - returns to the template:
    - the list of recipes that the user saved for him to lookup later

'''
@login_required
def mybakebook(request):

    user = None
    context_dict = {}
    mybakebook = []

    if request.user.is_authenticated():
        user = request.user

    for saved_recipe in SavedRecipe.objects.all():
        if saved_recipe.user == user:

            myrecipe = saved_recipe.recipe
            mybakebook.append(myrecipe)

    context_dict["mybakebook"] = mybakebook
    return render(request, 'sweetbook/mybakebook.html', context_dict)



'''
myrecipes view - returns to the template:
    - a list of recipes that the user created/ added to the website

'''
@login_required
def myrecipes(request):
    user = None
    context_dict = {}
    myrecipes = []                    # list of recipes that the user has created

    if request.user.is_authenticated():
        user = request.user

    for recipe in Recipe.objects.all():
        if recipe.user == user:
            myrecipes.append(recipe)

    context_dict["myrecipes"] = myrecipes
    return render(request, 'sweetbook/myrecipes.html', context_dict)


'''
delete view:
    - get the recipe-id frm the GET request
    - delete the recipe and return to myaccount page

'''
@login_required
def delete_recipe(request):
    rec_id = None
    if request.method == 'GET':
        rec_id = request.GET['recipe_id']

    if rec_id:
        rec = get_object_or_404(Recipe, id=int(rec_id))
        if rec:
            rec.delete()
            #return HttpResponseRedirect(reverse('sweetbook:myaccount'))
            return myaccount(request)
    return render_to_response (request, 'sweetbook/myrecipes.html', context_dict)


'''
mycalendar view returns to the template:
    - a list of the events that the user is interested in participating

'''
@login_required
def mycalendar(request):

    user = None
    context_dict = {}
    myevents = []

    if request.user.is_authenticated():
        user = request.user

    userprofile = get_object_or_404(UserProfile, user=user)
    myevents = userprofile.events

    context_dict["myevents"] = userprofile.events.order_by('date')
    return render(request, 'sweetbook/myevents.html', context_dict)


'''
views which handle the user login, logout and registrations templates

'''
@login_required
def restricted(request):
    return render(request, 'sweetbook/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def register_profile(request):
    form = UserProfileRegistrationForm()

    if request.method == 'POST':
        form = UserProfileRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('home')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'sweetbook/profile_registration.html', context_dict)
