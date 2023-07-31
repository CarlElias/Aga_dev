from django.contrib import admin
from .models import *

# Register your models here.   

class AdminTheme_biblique(admin.ModelAdmin):
    list_display = ('theme', 'date_ajout')
    
class AdminType_annonce(admin.ModelAdmin):
    list_display = ('nom_type_annonce', 'date_ajout')

class AdminQuote(admin.ModelAdmin):
    list_display = ('id', 'txt_quote', 'verset', 'date_ajout')
    list_filter = ('themes',)  # Ajout de la virgule pour créer un tuple
    
class AdminAnnonce(admin.ModelAdmin):
    list_display = ('type_annonce', 'titre', 'txt_annonce', 'date_ajout')
    
class AdminContact(admin.ModelAdmin):
    list_display = ('nom', 'mail', 'message', 'contact', 'date_ajout')

class AdminEtude_biblique(admin.ModelAdmin):
    list_display = ('id', 'titre', 'sous_titre', 'verset', 'date_ajout')
    list_filter = ('themes',)  # Ajout de la virgule pour créer un tuple
    
class AdminePensee_biblique(admin.ModelAdmin):
    list_display = ('theme', 'titre', 'date_ajout')
    list_filter = ('theme',)  # Ajout de la virgule pour créer un tuple
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contenu', 'statut', 'date_ajout')
    list_filter = ('statut', 'table')
    
class lifestyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'date_ajout')
    list_filter = ('themes',)  # Ajout de la virgule pour créer un tuple
    
class AdminPriere_louange(admin.ModelAdmin):
    list_display = ('verset','theme', 'type', 'date_ajout')
    #filtrer par theme et type
    list_filter = ('theme', 'type')  # Ajout de la virgule pour créer un tuple
    
class messageAdmin(admin.ModelAdmin):
    list_display = ('nom','email','objet','contact','contenu','date_ajout')
    
class sld_chainAdmin(admin.ModelAdmin):
    list_display = ('titre','montant','date_ajout')
    
admin.site.register(type_annonce, AdminType_annonce)
admin.site.register(theme_biblique, AdminTheme_biblique)
admin.site.register(quote, AdminQuote)
admin.site.register(annonce, AdminAnnonce)
admin.site.register(contact, AdminContact)
admin.site.register(lifestyle, lifestyleAdmin)
admin.site.register(etude_biblique, AdminEtude_biblique)
admin.site.register(pensee_biblique, AdminePensee_biblique)
admin.site.register(comment, CommentAdmin)
admin.site.register(priere_louange, AdminPriere_louange)
admin.site.register(message, messageAdmin)
admin.site.register(sld_chain, sld_chainAdmin)
