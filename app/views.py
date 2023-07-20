from django.conf.urls import handler404
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.shortcuts import *
from .models import *
from dash.models import *
from django.http import HttpResponse, HttpResponseRedirect
import random
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST

def index(Request):
    quotes = quote.objects.order_by('?')[:3]
    q_0 = quotes[0]
    q_1 = quotes[1]
    q_2 = quotes[2]
    themes = theme_biblique.objects.all()
    #recuperer l'etude_biblique par oredre de date dj'aout le plus recent 
    etudeb = etude_biblique.objects.order_by('-date_ajout')[:3]
    return render(Request, 'app/index.html', {'themes':themes, 'etudeb':etudeb, 'q_0':q_0, 'q_1':q_1, 'q_2':q_2})

def etudeb_view(Request, id, slug):
    #recuperer l'etude en fonction de l'id
    etudeb = etude_biblique.objects.get(id=id)
    #return vers la page 'app/bible-study.html
    return render(Request, 'app/bible-study.html', {'etudeb':etudeb})

def list_et(Request):
    #recupere tout etude_biblique et fais un return vers 'app/bible-studies.html'
    etudeb = etude_biblique.objects.all()
    return render(Request, 'app/bible-studies.html', {'etudeb':etudeb})

def login_view(Request):
    #si utilisateur authentifié redirgier vers la page d'acceuil
    if Request.user.is_authenticated:
        #retourné vers la ^page d'acceuil
        return HttpResponseRedirect(reverse('app:index'))
    else:
        if Request.method=='POST' :
            username = Request.POST.get('username')
            password = Request.POST.get('password')
            user = authenticate(Request,username=username,password=password)
            #faire une authentification, creer une session d'utilisateur et rediriger sur la page index avec le nom de l'user
            if user is not None:
                login(Request, user)
                #faire un return sur la view 'user_page' de dash.vew
                return redirect('app:index')
            else:
                return render(Request, 'app/auth.html', {'error':'Nom d\'utilisateur ou mot de passe incorrect'})
    return render(Request, 'app/auth.html') 

def register(Request):
    if Request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:index')) 
    else:
        if Request.method=='POST':
            username = Request.POST.get('username')
            email = Request.POST.get('email')
            password1 = Request.POST.get('password1')
            password2 = Request.POST.get('password2')
            last_name = Request.POST.get('last_name')
            first_name = Request.POST.get('first_name')
        
            if password1==password2:
                #verification de l'existence de l'user
                if User.objects.filter(username=username).exists():
                    return render(Request, 'app/register.html', {'error':'Ce nom d\'utilisateur existe déjà'})
                else:
                    if User.objects.filter(email=email).exists():
                        return render(Request, 'app/register.html', {'error':'Cet email existe déjà'})
                    else:
                        #creation de l'user
                        user = User.objects.create_user(username=username, email=email, password=password1, last_name=last_name, first_name=first_name)
                        #enregistrement de l'user
                        user.save()
                        return render(Request, 'app/auth.html', {'success':'Votre inscription a bien été prise en compte. Vous pouvez vous connecter'})

            else:
                return render(Request, 'app/register.html', {'error':'Les mots de passe ne correspondent pas'}) 
        return render(Request, 'app/register.html')