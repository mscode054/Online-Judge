from .models import User,Problem,Solution,TestCase
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

class ProblemView(generic.ListView):
    model = Problem
    # template_name = 'polls/details.html'


def login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, '/user/problem_list.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'judge/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, '/')


def register(request):
    # if this is a POST request we need to process the form data
    template = 'judge/register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.save()
        
                # login(request, user)
               
                # redirect to accounts page:
                return HttpResponseRedirect('/')

   # No post data availabe, let's just show the page.
    else:
        form = UserCreationForm()

    return render(request, template, {'form': form})


def problems(request):
    p=Problem.objects.all()
    context={'p':p}
    return render(request,'judge/problem_list.html',context)

class DetailView(generic.DetailView):
    model = Problem
    template_name = 'judge/problem_desc.html'

def verdict(request,problem_id):
    return HttpResponse("Success")












