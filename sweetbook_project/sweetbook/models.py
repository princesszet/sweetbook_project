Skip to content

Search or jump to…

Pull requests
Issues
Marketplace
Explore
 @princesszet Sign out
3
0 0 princesszet/sweetbook_project
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights  Settings
sweetbook_project/sweetbook_project/sweetbook/models.py
@elenasoare elenasoare Added population script, models, views, admin
b74a97f  3 hours ago
@luciacangarova @elenasoare
68 lines (55 sloc)  2.21 KB

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=50,unique=True)
    event_slug = models.SlugField()
    date = models.DateTimeField()
    description = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class User(models.Model):
    # relationships:
    events = models.ManyToManyField(Event)
    # fields:
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    picture = models.ImageField(null=True) # user might not have a profile picture
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Recipe(models.Model):
    # relationships:
    user = models.ForeignKey(User)
    # fields:
    name = models.CharField(max_length=50, unique=True)
    recipe_slug = models.SlugField()
    picture = models.ImageField(null=True) # 'users (...) must be able to upload their
                                           # recipes with or without pictures'
    ingredients = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default = 0, blank=True)
    cooktime = models.IntegerField(default = 0)
    difficulty = models.CharField(max_length=10, default ="medium")
    last_modified = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.name

class Comment(models.Model):
    # relationships
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)


    date = models.DateTimeField(default = timezone.now() )
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class SavedRecipe(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
    def __str__(self):
        return self.user.username + " saves " +recipe.name
