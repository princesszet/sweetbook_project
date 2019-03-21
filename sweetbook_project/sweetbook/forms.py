# implement the necessary infrastructure that will allow users to add recipes
# and comments to the database via forms
import django
import datetime
from django import forms
from sweetbook.models import Recipe, Comment, UserProfile
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from registration.forms import RegistrationFormUniqueEmail
import datetime
from django.utils import timezone
from datetime import datetime

class RecipeForm(forms.ModelForm,):
    # user = models.ForeignKey(User)
    name = forms.CharField(max_length=50,
                           help_text="Please enter the recipe name.")
    recipe_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(help_text="You can add pictures of your recipe.",
                               required=False)
    ingredients = forms.CharField(max_length=200,
                                  help_text="Enter the ingredients.")
    description = forms.CharField(max_length=400,
                                  help_text="Enter the description.")
    # HOW TO DO IT SO THAT THE USERS CAN RATE RECIPES?
    # rating = models.DecimalField(decimal_pla
    cooktime = forms.IntegerField(initial=0,
                                  help_text="Enter the cooktime.")
    difficulty = forms.CharField(max_length=10, initial ="medium",
                                  help_text="Enter the difficulty level.")
    last_modified = forms.DateTimeField(widget=forms.HiddenInput(), initial=django.utils.timezone.now)

    # an inline class to provide additional information on the form.
    class Meta:
        model = Recipe
        # exclude foreign key and rating
        exclude = ("user", "rating", "rating_number",)

class CommentForm(forms.ModelForm):
    # user = models.ForeignKey(User)
    # recipe = models.ForeignKey(Recipe)
    date = forms.DateTimeField(widget=forms.HiddenInput(), initial=django.utils.timezone.now)
    description = forms.CharField(max_length=100,
                                  help_text="Enter your comment.")
    # an inline class to provide additional information on the form.
    class Meta:
        model = Comment
        # exclude foreign keys
        exclude = ("user", "recipe")


'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email','password')

class UserProfileForm(forms.ModelForm):

  # not sure if we need to write the fields, in the book they don t
  # check at testing
  #-------------fields--------#

    class Meta:
        model = UserProfile
        exclude = ('user',)

        '''

class UserProfileRegistrationForm(forms.ModelForm,):
    firstname = forms.CharField(max_length = 25,required=True)
    surname = forms.CharField(max_length = 25,required=True)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user','events',)
