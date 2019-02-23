from django.conf.urls import url 
from sweetbook import views 

app_name = 'sweetbook'

urlpatterns = [ 
	url(r'^$', views.home, name='home'),
]