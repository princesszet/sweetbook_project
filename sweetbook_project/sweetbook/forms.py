# implement the necessary infrastructure that will allow users to add recipes
# and comments to the database via forms

from django import forms
from rango.models import Recipe, Comment

class RecipeForm(forms.ModelForm):
    # user = models.ForeignKey(User)
    name = forms.CharField(max_length=50,
                           help_text="Please enter the recipe name.")
    recipe_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(help_text="You can add pictures of your recipe.",
                               required=False) '
    ingredients = forms.CharField(max_length=200,
                                  help_text="Enter the ingredients.")
    description = forms.CharField(max_length=400,
                                  help_text="Enter the description.")
    # HOW TO DO IT SO THAT THE USERS CAN RATE RECIPES?
    # rating = models.DecimalField(decimal_pla
    cooktime = forms.IntegerField(default=0,
                                  help_text="Enter the cooktime.")
    difficulty = forms.CharField(max_length=10, default ="medium",
                                  help_text="Enter the difficulty level.")
    last_modified = forms.DateTimeField(widget=forms.HiddenInput(), default=timezone.now())

    # an inline class to provide additional information on the form.
    class Meta:
        model = Recipe
        # exclude foreign key and rating
        exclude = ("user", "rating")

class CommentForm(forms.ModelForm):
    # user = models.ForeignKey(User)
    # recipe = models.ForeignKey(Recipe)
    date = forms.DateTimeField(widget=forms.HiddenInput(), default=timezone.now())
    description = forms.CharField(max_length=100,
                                  help_text="Enter your comment.")
    # an inline class to provide additional information on the form.
    class Meta:
        model = Comment
        # exclude foreign keys
        exclude = ("user", "recipe")
