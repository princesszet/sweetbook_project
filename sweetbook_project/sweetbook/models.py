from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from datetime import datetime
import django
from PIL import Image
from django.utils.six import StringIO


'''
Event - contains the name, drescription, place, postcode and url(Maps API)

'''
class Event(models.Model):
    name = models.CharField(max_length=50,unique=True)
    event_slug = models.SlugField(default="")
    date = models.DateTimeField(null=True)
    description = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    url = models.CharField(max_length=200, default="")

    def save(self, *args, **kwargs):
        self.event_slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


'''
    UserProfile contains
        - 1:1 relationship with the imported User
        - a list of events he is interested in
        - firstname, surname and a profile picture

'''
class UserProfile(models.Model):
    #required
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # relationships:
    events = models.ManyToManyField(Event)
    # fields:
    firstname = models.CharField(max_length = 25, blank = False)
    surname = models.CharField(max_length = 25, blank = False)
    picture = models.ImageField(upload_to='profile_images', blank=True) # user might not have a profile picture

    def __str__(self):
        return self.user.username

'''
    Recipe contains:
        - the user that created the recipe
        - ingredients, description, rating, cooktime, difficulty
        - the date of the last modification

'''
class Recipe(models.Model):
    # relationships:
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    # fields:
    name = models.CharField(max_length=50, unique=True)
    recipe_slug = models.SlugField()
    picture = models.ImageField(blank=True, upload_to ='recipes_images', default=None) # 'users (...) must be able to upload their
                                           # recipes with or without pictures'
    ingredients = models.CharField(max_length=200)
    description = models.CharField(max_length=400)

    rating = models.FloatField(default=0)
    # OTHER POSSIBLE OPTIONS:
    # rating = models.DecimalField(decimal_places=2, max_digits=3, default = 0, blank=True)
    rating_number = models.IntegerField(default = 0)
    cooktime = models.IntegerField(default = 0)
    difficulty = models.CharField(max_length=10, default ="medium")
    last_modified = models.DateTimeField(default = django.utils.timezone.now)

    def save(self, *args, **kwargs):
        self.recipe_slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


'''
    Comment contains:
        - the user that commented, and the recipe that he commented on
        - the date (the default is used, and it is now)
        - the description

'''
class Comment(models.Model):
    # relationships
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE, default=None)

    date = models.DateTimeField(default =django.utils.timezone.now)
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.description


'''
    SavedRecipe:
        - the user that saved a recipe
        - the recipe that he has saved
'''
class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,)
    def __str__(self):
        return self.user.username + " saves " + self.recipe.name
