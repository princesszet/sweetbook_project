from django.conf.urls import url 
from sweetbook import views 

app_name = 'sweetbook'

urlpatterns = [ 
	url(r'^$', views.home, name='home'),
	url (r'^recipes/', views.recipes, name = 'recipes'),
    url(r'^recipes/(?P<recipe_slug>[\w\-]+)/$',
    	  views.chosen_recipe, name = 'chosen_recipe'),
    url (r'^events/', views.events, name = 'events'),
    url(r'^events/(?P<event_slug>[\w\-]+)/$',
    	  views.chosen_event, name = 'chosen_event'),
]