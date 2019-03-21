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

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits']= visits


def home(request):

    # request.session.set_test_cookie()
    top_rated_recipes = Recipe.objects.order_by('rating')[::-1][:10]
    most_commented_recipes= []
    context_dict = {}

    for recipe in Recipe.objects.order_by('last_modified')[:5]:
        comments_count = recipe.comment_set.count()
        most_commented_recipes.append([comments_count,recipe])
    most_commented_recipes.sort(key=lambda x: x[0])
    if len(most_commented_recipes) > 0:
        recipe_of_the_day = most_commented_recipes[0][1]
        context_dict ["recipeofday"] = recipe_of_the_day

    latest_events = Event.objects.filter().order_by('date')[:10]

    context_dict ["toprated"] = top_rated_recipes
    context_dict ["latestevents"] = latest_events
    
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    print(context_dict['visits'])
    response = render(request, 'sweetbook/home.html', context=context_dict)

    return response

def recipes(request):
    context_dict={}
    last_recipes = Recipe.objects.order_by('last_modified')[:20]
    context_dict["recipes"] = last_recipes
    return render(request, 'sweetbook/recipes.html', context_dict)

def chosen_recipe(request, recipe_slug):
    context_dict = {}
    try:
        recipe = Recipe.objects.get(recipe_slug=recipe_slug)
        comments = Comment.objects.filter (recipe = recipe)
        user = User.objects.filter ( recipe = recipe)
        context_dict['comments'] = comments
        context_dict['recipe'] = recipe
    except Recipe.DoesNotExist:
        context_dict['comments'] = None
        context_dict['recipe'] = None
    return render (request, 'sweetbook/chosen_recipe.html', context_dict)

def contactus(request):
	return render (request, 'sweetbook/contactus.html',{})

# ELI'S VERSION:
@login_required
def add_comment(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(recipe_slug = recipe_slug)
    except Recipe.DoesNotExist:
        recipe = None
        user = None

    if request.user.is_authenticated():
        user = request.user

    # form = CommentForm()
    if request.method == 'POST':
        comment_text = request.POST.get('text')
        if recipe and user:
            comment = Comment.get_or_create(user = user, recipe = recipe, description = text)
            comment.save()
            return chosen_recipe(request, recipe_slug)
        else:
            print(form.errors)


    # context_dict = {'form':form, 'comment':comment}
    context_dict = {'form':form, 'recipe':recipe}
    return render (request, 'sweetbook/add_comment.html', context_dict)

@login_required
def add_new_recipe(request):
    user = None
    if request.user.is_authenticated():
        user = request.user

    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save (commit=False)
            recipe.user = user
            recipe.save()
            return chosen_recipe(request, recipe.recipe_slug)
        else:
            print(form.errors)

    context_dict = {'form':form}
    return render (request, 'sweetbook/new_recipe.html', context_dict)


    # context_dict = {'form':form, 'comment':comment}
    context_dict = {'form':form, 'recipe':recipe}
    return render (request, 'sweetbook/add_comment.html', context_dict)

def events (request):
    context_dict = {}
    latest_events = Event.objects.order_by('date')[:10]
    context_dict["events"] = latest_events
    return render(request, 'sweetbook/events.html', context_dict)

def chosen_event(request, event_slug):
    context_dict = {}
    try:
        event = Event.objects.get(event_slug=event_slug)
        context_dict['event'] = event
    except Category.DoesNotExist:
        context_dict['event'] = None
    return render (request, 'sweetbook/chosen_event.html', context_dict)

@login_required
def add_to_cookbook(request):
	# add a recipe to the user cookbook
    user = None

    if request.user.is_authenticated():
        user = request.user
    recipe_id = None
    if request.method == "GET" and user:
        recipe_id = request.GET['recipe_id']
        print(recipe_id)
        if recipe_id:
            recipe = Recipe.objects.get(id = int(recipe_id))
            if recipe:
                saved_recipe = SavedRecipe.objects.get_or_create(recipe = recipe, user=user)[0]
                saved_recipe.save()
    return HttpResponse(saved_recipe)

# not yet tested
@login_required
def add_to_mycalendar(request):
    user = None
    user_profile = None

    if request.user.is_authenticated():
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)

    print(user, user_profile)

    event_id = None
    if request.method == "GET" and user:
        event_id = request.GET['event_id']
        print(event_id)
        if event_id:
            event = Event.objects.get(id = int(event_id))
            print(event)
            if event:
                user_profile.events.add(event)
                user_profile.save()
    print(event_id+"EVEEEENT")
    return HttpResponse(event)

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
            rating = (float(rec.rating) + float(rec_value))/2
            rec.rating =  rating
            rec.save()

    return HttpResponse(rating)

# not yet tested
@login_required
def myaccount(request):

    user = None
    context_dict = {}
    if request.user.is_authenticated():
        user = request.user

    # !!!! for the implementatin ih HTML the user has username, userprofile has the other information(surname, lastname,profile picture)
    context_dict["user"] = user
    context_dict["userprofile"] = get_object_or_404(UserProfile, user=user)
    return render(request, 'sweetbook/myaccount.html', context_dict)

# not yet tested
@login_required
def delete_myaccount(request):

    user = None

    if request.user.is_authenticated():
        user = request.user
    user.delete()
    return HttpResponseRedirect(reverse('home'))

# TESTED - It works
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


# TESTED - It works
@login_required
def myrecipes(request):

    user = None
    context_dict = {}
    myrecipes = []

    if request.user.is_authenticated():
        user = request.user

    for recipe in Recipe.objects.all():
        if recipe.user == user:
            myrecipes.append(recipe)

    context_dict["myrecipes"] = myrecipes
    return render(request, 'sweetbook/myrecipes.html', context_dict)

@login_required
def delete_recipe(request):
    rec_id = None
    if request.method == 'GET':
        rec_id = request.GET['recipe_id']

    if rec_id:
        rec = get_object_or_404(Recipe, id=int(rec_id))
        if rec:
            rec.delete()
            return HttpResponseRedirect(reverse('myrecipes'))


# TESTED - It works
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

# not yet tested
@login_required
def myBakebook(request):

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
    return render(request, 'sweetbook/myBakebook.html', context_dict)


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
