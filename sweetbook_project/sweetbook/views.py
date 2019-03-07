import os
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sweetbook_project.settings')

import django

from django.shortcuts import render
from django.db.models import Count
from sweetbook.models import User, Event, Recipe, SavedRecipe, Comment
from sweetbook.forms import CommentForm, RecipeForm

def home(request):
    request.session.set_test_cookie()
    top_rated_recipes = Recipe.objects.order_by('rating')[::-1][:10]
    most_commented_recipes= []
    context_dict = {}
    for recipe in Recipe.objects.order_by('last_modified')[:5]:
        comments_count = recipe.comment_set.count()
        most_commented_recipes.append([comments_count,recipe])
    most_commented_recipes.sort(key=lambda x: x[0])

    if len(most_commented_recipes) > 0:
        recipe_of_the_day = most_commented_recipes[0][1]
        context_dixt ["recipe of the day"] = recipe_of_the_day
    latest_events = Event.objects.filter().order_by('date')[:10]
    context_dict ["top rated recipes"] = top_rated_recipes
    context_dict ["latest events"] = latest_events

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'sweetbook/home.html', context=context_dict)
    return response

def recipes (request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
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
    except Category.DoesNotExist:
        context_dict['comments'] = None
        context_dict['recipe'] = None
    return render (request, 'sweetbook/chosen_recipe.html', context_dict)

"""

not yet finished - need forms
def add_comment(request, recipe_slug):

    try:
        recipe = Recipe.objects.get(recipe_slug = recipe_slug)
    except Recipe.DoesNotExist:
        recipe = None

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if recipe:
                comment = form.save (commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category':category}
    return render (request, 'rango/add_page.html', context_dict)

"""
def events (request):
	latest_events = Event.objects.order_by('date')[:10]
	context_dict["events"] = latest_events
	return render(request, 'sweetbook/events.html', context_dict)

def chosen_event(request, event_slug):
    context_dict = {}
    try:
        event = Event.objects.get(event_slug=event_slug)
        context_dict['event'] = category
    except Category.DoesNotExist:
        context_dict['event'] = None
    return render (request, 'sweetbook/chosen_event.html', context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits
