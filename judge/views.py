from .models import Problem,Solution,TestCase
from django.views import generic
from django.utils import timezone
import os,filecmp
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewUserForm
from django.contrib import messages
from django.core.files.base import ContentFile

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

def submission(request,problem_id):
	f=request.FILES["solution"] 
	with open("F:/OJ/judge/uploads/sol/solution%d.cpp" % problem_id,'wb+') as dest:
		for chunk in f.chunks():
			dest.write(chunk)
	os.system('g++ F:/OJ/judge/uploads/sol/solution%d.cpp' % problem_id)
	os.system('a.exe < F:/OJ/judge/uploads/input/problem_2/single_number_input.txt > F:/OJ/judge/uploads/output/problem_2/out%d.txt' % problem_id)

	out1='F:/OJ/judge/uploads/output/problem_2/out%d.txt' % problem_id
	out2='F:/OJ/judge/uploads/output/problem_2/single_number_output.txt'
	if(filecmp.cmp(out1,out2,shallow=False)):
		verdict='Accepted'
	else:
		verdict='Wrong Answer'

	solution=Solution()
	solution.problem=Problem.objects.get(pk=problem_id)
	solution.verdict=verdict
	solution.time_of_submission=timezone.now()
	solution.submitted_code='F:/OJ/judge/uploads/sol/solution.cpp'
	solution.save()
	return HttpResponseRedirect(reverse('judge:leaderboard'))	

def leaderboard(request):
	solutions=Solution.objects.all()
	return render(request,'judge/leaderboard.html',{'solutions': solutions})





















