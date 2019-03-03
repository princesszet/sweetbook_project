from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=50)
    event_slug = models.SlugField(unique=True)
    date = models.DateTimeField()
    decription = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class User(models.Model):
    # relationships:
    event = models.ManyToManyField(Event)
    # comment = models.ForeignKey(Comment)
    # recipe = models.ForeignKey(Recipe)
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
    recipe_slug = models.SlugField(unique=True)
    picture = models.ImageField(null=True) # 'users (...) must be able to upload their
                                           # recipes with or without pictures'
    ingredients = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    rating = models.DecimalField(decimal_places=2, max_digits=3)
    cooktime = models.IntegerField()
    difficulty = models.CharField(max_length=10)
    last_modified = models.DateTimeField()

    def __str__(self):
        return self.AuthenticationMiddleware

class Comment(models.Model):
    # relationships
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
    # fields
    date = models.DateTimeField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class SavedRecipe(models.Model):
    # relationships
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
