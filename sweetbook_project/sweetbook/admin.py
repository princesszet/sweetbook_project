from django.contrib import admin 
from sweetbook.models import User
from sweetbook.models import Comment
from sweetbook.models import Recipe
from sweetbook.models import SavedRecipe
from sweetbook.models import Event


admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(Event)