from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm , PostForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request,'home.html',{'posts':posts})


def about(request):
    return render(request, 'about.html')

# @login_required
def contact(request):
    return render(request, 'contact.html')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/signin/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('/')
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request, "Account has been created")
            return redirect('signin')
    form = SignUpForm()
    return render(request, 'signup.html',{'form':form})

def signout(request):
    logout(request)
    return redirect('/')

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:  # Handle the GET request
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

    

def update_post(request, id):
    if request.user.is_authenticated:
        pi = Post.objects.get(pk=id)
        if request.method=='POST':
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = PostForm(instance=pi)
            return render(request,'update.html',{'form':form})
    else:
        return HttpResponseRedirect('/signin/')


def delete_post(request, id):
    if request.user.is_authenticated:
        pi = Post.objects.get(pk=id)
        pi.delete()
        return redirect('dashboard')
    else:
        return HttpResponseRedirect('/signin/')