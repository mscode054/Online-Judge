from math import hypot
from .models import Problem,Solution,TestCase
from django.views import generic
from datetime import datetime
from django.utils import timezone
import os,filecmp
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect
from django.urls import reverse
import subprocess
import sys
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewUserForm
from django.contrib import messages



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
				return redirect("/problems/")
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
	
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

def problems(request):
    p=Problem.objects.all()
    context={'p':p}
    return render(request,'judge/problem_list.html',context)

class DetailView(generic.DetailView):
    model = Problem
    template_name = 'judge/problem_desc.html'

def submission(request,problem_id):
	f=request.FILES["solution"] 
	date = str(datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p"))
	username=request.user.get_username()
	with open("F:/OJ/solution_%d_%s_%s.cpp" % (problem_id,username,date),'wb+') as dest:
		for chunk in f.chunks():
			dest.write(chunk)
   
	subprocess.call("docker run gcc tail -f /dev/null",shell=True)
	output=subprocess.check_output(['docker','ps'],universal_newlines=True)
	x=output.split('\n')
	container_id=""
	for i in x:
		if i.__contains__("gcc"):
			container_id=i[:12]
   
	container_id_with_path=container_id+":/tmp"
	subprocess.call(["docker", "cp", "/root/solution_%d_%s_%s.cpp" % (problem_id,username,date), container_id_with_path])
	subprocess.call(["docker", "cp", "/root/input_%d.txt" % (problem_id), container_id_with_path])
	subprocess.call(['docker','exec', container_id,'g++','/root/solution_%d_%s_%s.cpp'% (problem_id,username,date)])
	subprocess.call(['docker','exec', container_id+'./a.out'> "/root/input_%d.txt" % (problem_id) < "/root/out_%d_%s_%s.txt" % (problem_id,username,date) ])
	
	# subprocess.call(["docker", "cp",  container_id_with_path+"/out_%d_%s_%s.txt" % (problem_id,username,date), "/root/"])
   
	# os.system('g++ F:/OJ/judge/uploads/sol/solution_%d_%s_%s.cpp' % (problem_id,username,date))
	# os.system('a.exe < F:/OJ/judge/uploads/input/problem_%d/single_number_input.txt > F:/OJ/judge/uploads/output/problem_2/out_%d_%s_%s.txt' % (problem_id,problem_id,username,date))

	out1='F:/OJ/out_%d_%s_%s.txt' %(problem_id,problem_id,username,date)
	out2='F:/OJ/judge/uploads/output/problem_%d/single_number_output.txt' %(problem_id)
	if(filecmp.cmp(out1,out2,shallow=False)):
		verdict='Accepted'
	else:
		verdict='Wrong Answer'

	solution=Solution()
	solution.problem=Problem.objects.get(pk=problem_id)
	solution.verdict=verdict
	solution.time_of_submission=timezone.now()
	solution.submitted_code='F:/OJ/judge/uploads/sol/solution_%d_%s_%s.cpp' % (problem_id,username,date)
	solution.save()
	return HttpResponseRedirect(reverse('judge:leaderboard'))	

def leaderboard(request):
	solutions=Solution.objects.all()
	return render(request,'judge/leaderboard.html',{'solutions': solutions})





















