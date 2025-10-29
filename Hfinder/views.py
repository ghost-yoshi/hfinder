# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime import datetime, date
from Hfinder.forms import LoginForm, userProfileForm, Person, AddFriendForm
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
        print('formulaire reçu !')
        form = LoginForm(request.POST)
        if form.is_valid():
            print('formulaire valide')
            user_mail = form.cleaned_data['email']
            logged_user = Person.objects.get(email=user_mail)
            print('sauvegarde de session en cours...')
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
            print("création d'un nouvel utilisateur...")
            form.save()
            print("utilisateur sauvegardé ! redirection vers le login...")
            return redirect('/login')
        else:
            print("error lors du remplissage du formulaire...")
            form = userProfileForm()
            return render (request, 'register.html', {'form': form})
    else:
        print("formulaire de création de compte envoyé !")
        form = userProfileForm()
        return render(request, 'register.html', {'form': form})
    
def add_friend(request):
    print(" verification de l'utilisateur")
    logged_user = get_logged_user_from_request(request)
    
    if logged_user:
        print("verification terminé: success")
        #test d'envoi du formulaire
        if request.method == 'POST':
        
            print("reception d'un formulaire")
            form = AddFriendForm(request.POST)

            if form.is_valid(): 
                print("formulaire d'ajout d'ami bien rempli. traitement...")
                new_friend_name = form.cleaned_data['name']
                print("recherche de l'utilisateur: ", new_friend_name)
                new_friend = Person.objects.get(first_name = new_friend_name)
                logged_user.friends.add(new_friend)
                logged_user.save()
                return redirect('/welcome')
            
            else:
                print("Quelque chose a mal tourné, l'ajout a echoué")
                return render(request, 'add_friend.html', { 'form':form})
        else:
            print("Demande d'ajout d'un ami")
            form = AddFriendForm()
            return render(request, 'add_friend.html', { 'form': form})
    else:
        return redirect('/login')




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