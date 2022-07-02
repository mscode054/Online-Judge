from .models import User,Problem,Solution,TestCase
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render,redirect
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewUserForm
from django.contrib import messages

class ProblemView(generic.ListView):
    model = Problem
    # template_name = 'polls/details.html'


def login_req(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				# return redirect("problems/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="judge/login.html", context={"login_form":form})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/problems")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="judge/register.html", context={"register_form":form})
	

def problems(request):
    p=Problem.objects.all()
    context={'p':p}
    return render(request,'judge/problem_list.html',context)

class DetailView(generic.DetailView):
    model = Problem
    template_name = 'judge/problem_desc.html'

def verdict(request,problem_id):
    return HttpResponse("Success")












