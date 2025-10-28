# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime import datetime, date
from Hfinder.forms import LoginForm, userProfileForm, Person
from Hfinder.models import Message

def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        if len(Person.objects.filter(id=logged_user_id)) ==1:
            return Person.objects.get(id=logged_user_id)
        else : 
            return None
        
    else :
        return None
    
def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if 'newMessage' in request.GET and request.GET['newMessage'] != '':
            newMessage = Message(author=logged_user,
                                 content = request.GET['newMessage'],
                                 publication_date = date.today())
            newMessage.save()
            
        friendMessages = Message.objects.filter(author__friends=logged_user).order_by('-publication_date')
        return render(request, 'welcome.html', 
                      {'firstname': logged_user.first_name,
                       'lastname': logged_user.last_name,
                       'phone_number': logged_user.phone_number,
                       'register_date': logged_user.register_date,
                       'friendMessages': friendMessages,
                       'logged_user': logged_user})
    else:
        print('non logged user detected:', logged_user)
        return redirect('/login')
def login(request):

    if len(request.POST) > 0:
        print (request.session)
        form = LoginForm(request.POST)
        if form.is_valid():
            user_mail = form.cleaned_data['email']
            logged_user = Person.objects.get(email=user_mail)
            request.session['logged_user_id'] = logged_user.id
            print('utilisateur: ', logged_user.first_name, ' sauvegardé')
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