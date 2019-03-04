import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sweetbook_project.settings')

import django

from django.shortcuts import render
from django.db.models import Count
from sweetbook.models import User, Event, Recipe, SavedRecipe, Comment


def home(request):
    top_rated_recipes = Recipe.objects.order_by('-rating')[:10]
    most_commented_recipes= []
    context_dict = {}

    for recipe in Recipe.objects.order_by('last_modified')[:5]:
        comments_count = recipe.comment_set.count()
        most_commented_recipes.append([comments_count,recipe])
    most_commented_recipes.sort(key=lambda x: x[0])

    recipe_of_the_day = most_commented_recipes[0][1]

    latest_events = Event.objects.filter().order_by('date')[:10]
    context_dict ["toprated"] = top_rated_recipes
    context_dict ["recipeofday"] = recipe_of_the_day
    context_dict ["latestevents"] = latest_events
    return render(request, 'sweetbook/home.html', context_dict )


def recipes (request):
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
