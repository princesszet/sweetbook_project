from django.conf.urls import url
from sweetbook import views

app_name = 'sweetbook'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^recipes/(?P<recipe_slug>[\w\-]+)/$',
    	  views.chosen_recipe, name = 'chosen_recipe'),
    url(r'^events/(?P<event_slug>[\w\-]+)/$',
    	  views.chosen_event, name = 'chosen_event'),
    url(r'^recipes/', views.recipes, name = 'recipes'),
    url(r'^events/', views.events, name = 'events'),
    url(r'^add-to-cookbook', views.add_to_cookbook, name='add_to_cookbook'),
    url(r'^recipes/(?P<recipe_slug>[\w\-]+)/add-comment/$',views.add_comment, name = 'add_comment'),
    url(r'^myaccount/$', views.myaccount, name='myaccount'),
    url(r'^myaccount/delete-myaccount$', views.delete_myaccount, name='delete_myaccount'),
    url(r'^mybakebook/$', views.mybakebook, name='mybakebook'),
    url(r'^mycalendar/$', views.mycalendar, name='mycalendar'),
    url(r'^myrecipes/$', views.myrecipes, name='myrecipes'),
    url(r'^myrecipes/new-recipe/$', views.add_new_recipe, name='new_recipe'),
    url(r'^myrecipes/delete-recipe$', views.delete_recipe, name='delete_recipe'),
    url(r'^like-recipe/$', views.like_recipe, name='like_recipe'),
    url(r'^add-to-mycalendar', views.add_to_mycalendar, name='add_to_mycalendar'),
    url(r'^restricted/',views.restricted, name='restricted'),
    url(r'^register-profile/$', views.register_profile, name='register_profile'),
    url(r'^contactus/', views.contactus, name = 'contactus'),
]
