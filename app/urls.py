from django.urls import path
from django.conf.urls import handler404
from .views import *

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('etudeb/<int:id>/<slug:slug>', etudeb_view, name='etudeb_view'),
    path('list_et', list_et, name='list_et'),
    path('login', login_view, name='login_view'),
    path('register', register, name='register'),
    #path('etudeb/<int:id>/<slug:slug>', etudeb_view, name='etudeb_view'),
    #path('contact_view/', contact_view, name='contact_view'),
    #path('login', login_view, name='login'),
    #path('register', register, name='sign'),
    #path('logout', logout_view, name='logout'),
]

#gestion d'erreur 404
handler404 = 'app.views.handler404'