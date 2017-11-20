# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta, time
from django.contrib.sessions.models import Session
# Create your views here.
def index(request):
    return render(request, "meetup_app/index.html")

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")
    return redirect('/home')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/home')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    Session.objects.all().delete()
    return redirect('/')


def home(request):
    context = {
        "activities": Activity.objects.all(),
        "user": User.objects.get(id=request.session['id'])
    }
    
    return render(request, "meetup_app/home.html", context)

def new(request):
    return render(request, 'meetup_app/new.html')

def new_activity(request):
    errors = Activity.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/new')
    else:
        Activity.objects.create(title= request.POST['title'], 
        time= datetime.strptime(request.POST['time'],  "%H:%M").time(), 
        date= datetime.strptime(request.POST['date'], "%Y-%m-%d").date(), 
        duration_number= request.POST['duration_number'], 
        duration= request.POST['duration'], 
        description= request.POST['description'], 
        creator = User.objects.get(id=request.session['id']))
    return redirect('/home')

def activity(request, act_id):
    context={
        'activity': Activity.objects.get(id=act_id),
    }
    return render(request, 'meetup_app/activity.html', context)

def delete(request, act_id):
    Activity.objects.get(id=act_id).delete()
    return redirect('/home')

def join(request, act_id):
    Activity.objects.get(id=act_id).number_of_participants.add(User.objects.get(id=request.session['id']))
    return redirect('/home')
    
def leave(request, act_id):
    Activity.objects.get(id=act_id).number_of_participants.remove(User.objects.get(id=request.session['id']))
    return redirect('/home')