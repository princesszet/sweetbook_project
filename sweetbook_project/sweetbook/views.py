from django.shortcuts import render

def home(request):
	return render(request, 'sweetbook/base.html', {"username":"Lucy"})
