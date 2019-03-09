from django.conf.urls import url 
from sweetbook import views 

app_name = 'sweetbook'

urlpatterns = [ 
    url(r'^$', views.home, name='home'),
    url(r'^recipes/(?P<recipe_slug>[\w\-]+)/$',
    	  views.chosen_recipe, name = 'chosen_recipe'),
    url(r'^events/(?P<event_slug>[\w\-]+)/$',
    	  views.chosen_event, name = 'chosen_event'),
    url (r'^recipes/', views.recipes, name = 'recipes'),
    url (r'^events/', views.events, name = 'events'),
    url(r'^add-to-cookbook', views.add_to_cookbook, name='add_to_cookbook'),
    url(r'^recipes/(?P<recipe_slug>[\w\-]+)/add-comment/$',
    	  views.add_comment, name = 'add_comment'),
    url (r'^register/$', views.register, name='register'),
        
    url (r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name='logout'),
]
