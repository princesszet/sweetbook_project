from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    picture = models.ImageField()
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return #what? eg. self.date

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    picture = models.ImageField()
    ingredient = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    rating = models.DecimalField(decimal_places=2, max_digits=1)
    cooktime = models.IntegerField()
    difficulty = models.CharField(max_length=10)

    def __str__(self):
        return #what? eg. self.date

class Event(models.Model):
    date = models.DateTimeField()
    decription = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return #what? eg. self.date

class Comment(models.Model):
    date = models.DateTimeField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return #what? eg. self.date
