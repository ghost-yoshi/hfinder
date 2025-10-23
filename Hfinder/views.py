# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime import datetime
from Hfinder.forms import LoginForm, userProfileForm, Person

def welcome(request):
    return render(request,'welcome.html', {
    'Nom':'YOSHi',
    'Date': datetime.now,
    'ville': 'Douala'
    })

def login(request):

    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/welcome') 
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm ()
        return render(request, 'login.html', {'form': form})

def register(request):
    if len(request.GET)>0:
        form = userProfileForm(request.GET)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            form = userProfileForm()
            return render (request, 'user_profile.html', {'form': form})
    else:
        form = userProfileForm()
        return render(request, 'user_profile.html', {'form': form})




"""  if len(request.POST) > 0:
        if 'email' not in request.POST or 'password' not in request.POST:
            error = "Veuillez Saisir une adresse mail et un mot de passe valide"
            return render(request, 'login.html', {'error': error})
        else:
            email = request.POST['email']
            password = request.POST['password']

            if password != 'yoshi' or email != 'Yoshi@gmail.com':
                error = " Adresse mail ou mot de passe erroné. "
                return render(request, 'login.html', {'error': error})
            else:
                return redirect('/login/')
    else:
        return render(request, 'login.html')"""
   
# return render(request, 'login.html')