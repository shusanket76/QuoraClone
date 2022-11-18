from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import Room, Topic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from . forms import RoomForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            return HttpResponse("USER NOT FOUND")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            return HttpResponse("error")
    context={'page':page}
    return render(request, 'shusanket/login-register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.username=user.username.lower()
            user.save()
            return redirect('loginpage')

        else:
            return HttpResponse("ERRORRRRRRR")

    context={'form':form}
    return render(request,  'shusanket/login-register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)



                                )
    roomcount= rooms.count()
    topic = Topic.objects.all()
    context =  {'rooms': rooms, 'topics':topic, 'roomcount':roomcount}
    return render(request, "shusanket/home.html", context)



def room(request, pk):
    rooms = Room.objects.get(id=pk)
    rmessage=rooms.message_set.all()
    context = {'room':rooms, 'rmessage':rmessage}
    return render(request, 'shusanket/room.html', context)


@login_required(login_url='loginpage')
def cform(request):
    form = RoomForm
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'shusanket/form.html',{'form':form})


@login_required(login_url='loginpage')

def update(request, pk):


    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("not allowed mf")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={"form":form}

    return render(request, 'shusanket/update.html',context)


@login_required(login_url='loginpage')
def delete(request, pk):
    room = Room.objects.get(id=pk)


    if request.user != room.host:
        return HttpResponse("not allowed mf")
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'room':room}

    return render(request, 'shusanket/delete.html', context)


