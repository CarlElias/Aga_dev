from django.conf.urls import handler404
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.shortcuts import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import random
from django.http import JsonResponse
from django.contrib import messages 
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import user_passes_test
from django.views.decorators.http import require_POST
import re
import traceback
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def user_page(Request):
    return render(Request, 'dash/user_page.html')

def logout_view(Request):
    logout(Request)
    return redirect('app:index')

def template(Request):
    return render(Request, 'dash/template.html')

#----------------------------------------------------------------> Gestion des messages

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def msg(Request):
    #liste des messages par ordre alphabetique du 'last_name' sauf ceux qui ont les permission de superutilisateur
    messages = message.objects.order_by('-date_ajout')
    return render(Request, 'dash/message.html', {'msg':messages})

def supprimer_msg(Request, id):
    msg = get_object_or_404(message, id=id)
    msg.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:msg')

#----------------------------------------------------------------> Gestion des utilisateurs

@user_passes_test(lambda u: u.is_superuser)
def gest_us(Request):
    #liste des utilsateurs par ordre alphabetique du 'last_name' sauf ceux qui ont les permission de superutilisateur
    users = User.objects.filter(is_superuser=False).order_by('last_name')
    return render(Request, 'dash/gestion_user.html', {'users':users})

@user_passes_test(lambda u: u.is_superuser)
def update_is_staff(request):
    #dans le fichier html, j'ai un code ajax qui est sensé envoye a la view un dictionnaire data contenant les valeurs user_id et is_staff, ecris le code recuperation des donnes dans le dictionnaire data 
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_id = request.POST.get('user_id')
        is_staff = request.POST.get('is_staff')
        
        
        # Utilisez les valeurs user_id et is_staff pour effectuer les opérations nécessaires
        try:
            user = User.objects.get(id=user_id)
            user.is_staff = is_staff == 'true'  # Convertir la chaîne en booléen
            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            #retourner l'erreur dans la variable erreur pourquel soir=t facciher dans un console log
            erreur = traceback.format_exc()
            return JsonResponse({'success': False, 'error': erreur})

    return JsonResponse({'success': False, 'error': 'Requête invalide.'})

@require_POST
def supprimer_us(Request, id):
    us = get_object_or_404(User, id=id)
    us.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:gest_us')

#----------------------------------------------------------------> Inspiration / Quotes

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def insp(Request):
    qt = quote.objects.all()
    themes = theme_biblique.objects.all()
    return render(Request, 'dash/quotes.html',  {'qt':qt, 'themes':themes}) 

@require_POST
def ajouter_insp(Request):
    themes_ids = Request.POST.getlist('themes')  # Récupère la liste des IDs des thèmes sélectionnés
    txt_quote = Request.POST.get('txt_quote')
    verset = Request.POST.get('verset')
    
    # Crée une instance d'étude biblique
    quote_c = quote.objects.create(txt_quote=txt_quote, verset=verset)


    # Associe les thèmes sélectionnés à l'inspirations
    themes = theme_biblique.objects.filter(id__in=themes_ids)
    quote_c.themes.set(themes)
    
    messages.success(Request, "Etude ajouter avec success !" )
    return redirect('dash:insp')

@require_POST
def supprimer_insp(Request, id):
    qt = get_object_or_404(quote, id=id)
    qt.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:insp')

@require_POST
def edit_insp(Request, id):
    if 'form_mod_edit_qt' in Request.POST and Request.method=='POST':
        # Récupère la liste des IDs des thèmes sélectionnés
        themes_ids = Request.POST.getlist('themes')
        txt_quote = Request.POST.get('txt_quote')
        verset = Request.POST.get('verset')
        
        # appliquer les modification
        qt = quote.objects.get(id=id)
        qt.txt_quote = txt_quote
        qt.verset = verset
        qt.save()
        
        # Associe les thèmes sélectionnés à l'étude biblique
        themes = theme_biblique.objects.filter(id__in=themes_ids)
        qt.themes.set(themes)
        
        messages.success(Request, "Inspiration modifier avec success !" )
        return redirect('dash:insp')
    qt = get_object_or_404(quote, id=id)
    themes = theme_biblique.objects.all()
    qt_themes = qt.themes.all()  # Récupérer les thèmes associés à l'étude biblique
    
    # Créer une liste de valeurs des thèmes associés
    themes_values = [theme.id for theme in qt_themes]
    return render(Request, 'dash/modification/edit_qt.html', {'qt':qt, 'themes':themes, 'themes_values': themes_values})

#----------------------------------------------------------------> Etude Biblique

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def etude_b(Request):
    et_b = etude_biblique.objects.all()
    themes = theme_biblique.objects.all()
    return render(Request, 'dash/etude_b.html',  {'et_b':et_b, 'themes':themes}) 

@require_POST
def ajouter_et_b(Request):
    themes_ids = Request.POST.getlist('themes')  # Récupère la liste des IDs des thèmes sélectionnés
    titre = Request.POST.get('titre')
    sous_titre = Request.POST.get('sous_titre')
    contenu = Request.POST.get('contenu')
    verset = Request.POST.get('verset')
    lien_yt = Request.POST.get('lien_yt')
    
    # Gestion des retours à la ligne et des espaces
    #-->contenu = contenu.replace('\n', '<br>')  # Remplace les retours à la ligne par des balises <br>
    #-->contenu = contenu.replace('  ', '&nbsp;&nbsp;')  # Remplace les espaces doubles par des balises &nbsp;
    
    if lien_yt == "":
        video_id = ""
    else:
        # Récupère l'ID de la vidéo YouTube
        video_id = re.findall(r"v=([A-Za-z0-9_-]{11})", lien_yt)[0]

    # Crée une instance d'étude biblique
    etude = etude_biblique.objects.create(titre=titre, sous_titre=sous_titre, contenu=contenu, verset=verset, lien_yt=video_id)
    #typ_a = type_annonce(nom_type_annonce=nom_type_annonce)
    #typ_a.save()

    # Associe les thèmes sélectionnés à l'étude biblique
    themes = theme_biblique.objects.filter(id__in=themes_ids)
    etude.themes.set(themes)
    
    messages.success(Request, "Etude ajouter avec success !" )
    return redirect('dash:etude_b')
    #return HttpResponse(themes_ids)

@require_POST
def supprimer_etude_b(Request, id):
    et_b = get_object_or_404(etude_biblique, id=id)
    et_b.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:etude_b')

@require_POST
def edit_etude_b(Request, id):
    if 'form_mod_edit_etude_b' in Request.POST and Request.method=='POST':
        themes_ids = Request.POST.getlist('themes')  # Récupère la liste des IDs des thèmes sélectionnés
        titre = Request.POST.get('titre')
        sous_titre = Request.POST.get('sous_titre')
        contenu = Request.POST.get('contenu')
        verset = Request.POST.get('verset')
        lien_yt = Request.POST.get('lien_yt')
        
        
        # appliquer les modification
        etude = etude_biblique.objects.get(id=id)
        etude.titre = titre
        etude.sous_titre = sous_titre
        etude.verset = verset
        etude.lien_yt = lien_yt
        etude.contenu = contenu
        etude.save()
        
        # Associe les thèmes sélectionnés à l'étude biblique
        themes = theme_biblique.objects.filter(id__in=themes_ids)
        etude.themes.set(themes)

        
        messages.success(Request, "Etude Bilique modifier avec success !" )
        return redirect('dash:etude_b')
    et_b = get_object_or_404(etude_biblique, id=id)
    themes = theme_biblique.objects.all()
    et_b_themes = et_b.themes.all()  # Récupérer les thèmes associés à l'étude biblique

    # Créer une liste de valeurs des thèmes associés
    themes_values = [theme.id for theme in et_b_themes]
    return render(Request, 'dash/modification/edit_et_b.html', {'et_b':et_b, 'themes':themes, 'themes_values': themes_values})

#----------------------------------------------------------------> Pensee Biblique

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def pens_b(Request):
    pns_b = pensee_biblique.objects.all()
    themes = theme_biblique.objects.all()
    return render(Request, 'dash/pense_b.html',  {'pns_b':pns_b, 'themes':themes}) 

@require_POST
def ajouter_pens_b(Request):
    titre = Request.POST.get('titre')
    contenu = Request.POST.get('contenu')
    lien_youtube = Request.POST.get('lien_youtube')
    theme = Request.POST.get('theme')
    
    if lien_youtube == "":
        video_id = ""
    else:
        # Récupère l'ID de la vidéo YouTube
        video_id = re.findall(r"v=([A-Za-z0-9_-]{11})", lien_youtube)[0]
        
    pensee = pensee_biblique.objects.create(titre=titre, contenu=contenu, lien_youtube=video_id, theme_id=theme)

    messages.success(Request, "Pensee ajouter avec success !" )
    return redirect('dash:pens_b')

@require_POST
def supprimer_pens_b(Request, id):
    pns_b = get_object_or_404(pensee_biblique, id=id)
    pns_b.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:pens_b')

@require_POST
def edit_pens_b(Request, id):
    if 'form_mod_edit_pns_b' in Request.POST and Request.method=='POST':
        titre = Request.POST.get('titre')
        contenu = Request.POST.get('contenu')
        lien_youtube = Request.POST.get('lien_youtube')
        theme = Request.POST.get('theme')
            
        # appliquer les modification
        pens_b = pensee_biblique.objects.get(id=id)
        pens_b.titre = titre
        pens_b.contenu = contenu
        pens_b.lien_youtube = lien_youtube
        pens_b.theme_id = theme
        pens_b.save()
        
        messages.success(Request, "Pensee Bilique modifier avec success !" )
        return redirect('dash:pens_b')
    pns_b = get_object_or_404(pensee_biblique, id=id)
    themes = theme_biblique.objects.all()
    return render(Request, 'dash/modification/edit_p.html', {'pns_b':pns_b, 'themes':themes})

#----------------------------------------------------------------> lifestyle

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def lifes(Request):
    lifes = lifestyle.objects.order_by('date_ajout')
    #liste des themes_biblique par ordre
    themes = theme_biblique.objects.order_by('theme')
    return render(Request, 'dash/lifestyle.html', {'lifes':lifes, 'themes':themes}) 

@require_POST
def ajouter_lif(Request):
    themes_ids = Request.POST.getlist('themes')  # Récupère la liste des IDs des thèmes sélectionnés
    titre = Request.POST.get('titre')
    contenu = Request.POST.get('contenu')
    image = Request.FILES.get('image')

    # Crée une instance de lifestyle et inserer dans la bd
    lif = lifestyle.objects.create(titre=titre, contenu=contenu, image=image)

    # Associe les thèmes sélectionnés à l'étude biblique
    themes = theme_biblique.objects.filter(id__in=themes_ids)
    lif.themes.set(themes)
    
    messages.success(Request, "LifeStyle ajouter avec success !" )
    return redirect('dash:lifes')
    #return HttpResponse(themes_ids)

@require_POST
def supprimer_lif(Request, id):
    #supprimer le lifestyle de l'id et en supprimant, supprimer aussi l'image enregistrer 
    lif = get_object_or_404(lifestyle, id=id)
    lif.image.delete()
    lif.delete()

    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:lifes')    

@require_POST
def edit_lif(Request, id):
    if 'form_mod_edit_lif' in Request.POST and Request.method=='POST':
        themes_ids = Request.POST.getlist('themes')  # Récupère la liste des IDs des thèmes sélectionnés
        titre = Request.POST.get('titre')
        image = Request.FILES.get('image')
        contenu = Request.POST.get('contenu')
        
        #appliquer les modification en mettant une conditaion pour image si null
        lifS = lifestyle.objects.get(id=id)
        lifS.titre = titre
        if image:
            lifS.image.delete()
            lifS.image = image
        lifS.contenu = contenu
        lifS.save()    
        
        
        # Associe les thèmes sélectionnés à l'étude biblique
        themes = theme_biblique.objects.filter(id__in=themes_ids)
        lifS.themes.set(themes)
        
        messages.success(Request, "Lifestyle modifié avec success !" )
        return redirect('dash:lifes')
    lif = get_object_or_404(lifestyle, id=id)
    themes = theme_biblique.objects.all()
    lif_themes = lif.themes.all()  # Récupérer les thèmes associés à l'étude biblique

    # Créer une liste de valeurs des thèmes associés
    themes_values = [theme.id for theme in lif_themes]
    return render(Request, 'dash/modification/edit_life.html', {'lif':lif, 'themes':themes, 'themes_values': themes_values})

#----------------------------------------------------------------> Annonce

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def ann(Request):
    annonces = annonce.objects.order_by('-date_ajout')
    ty_a = type_annonce.objects.all()
    return render(Request, 'dash/annonce.html', {'annonces':annonces, 'ty_a':ty_a})

@require_POST
def aj_ann(Request):
    type_annonces = Request.POST.get('type_annonce')
    titre = Request.POST.get('titre')
    txt_annonce = Request.POST.get('txt_annonce')
    image_annonce = Request.FILES.get('image_annonce')
    #theme = Request.POST.get('theme')
    
    type_annonce_obj = type_annonce.objects.get(pk=type_annonces)
    
    # Crée une instance de lifestyle et inserer dans la bd
    ann = annonce.objects.create(titre=titre, type_annonce=type_annonce_obj, image_annonce=image_annonce, txt_annonce=txt_annonce)
    ann.save()
    
    messages.success(Request, "Annonce Enregistrée avec success !" )
    return redirect('dash:ann')

@require_POST
def edit_ann(Request, id):
    if 'form_mod_edit_ann' in Request.POST and Request.method=='POST':
        type_annonces = Request.POST.get('type_annonce')
        titre = Request.POST.get('titre')
        txt_annonce = Request.POST.get('txt_annonce')
        image_annonce = Request.FILES.get('image_annonce')
        type_annonce_obj_hidden = Request.POST.get('type_annonce_hidden')
        
        #type_annonce_obj = type_annonce.objects.get(pk=type_annonces)
        
        annon = annonce.objects.get(id=id)
        id_ty_ann = annon.type_annonce
        """
        print(annon)
        print(id_ty_ann)
        print(type(id_ty_ann))
        print('-------')
        """
        
        if type_annonces is None:
            type_annonce_obj = id_ty_ann
        else:
            type_annonce_obj = type_annonce.objects.get(pk=type_annonces)          

        #print(type_annonce_obj)
        #print(type(type_annonce_obj))
        
        
        #appliquer les modification en mettant une conditaion pour image si null
        Ann = annonce.objects.get(id=id)
        Ann.titre = titre
        if image_annonce:
            Ann.image_annonce.delete()
            Ann.image_annonce = image_annonce
        Ann.txt_annonce = txt_annonce
        Ann.type_annonce = type_annonce_obj
        Ann.save()
        
        
        messages.success(Request, "Anonnce modifier avec success !" )
        return redirect('dash:ann')
    an = get_object_or_404(annonce, id=id)
    ty_a = type_annonce.objects.all()
    return render(Request, 'dash/modification/edit_ann.html', {'an':an, 'ty_a':ty_a})
        

@require_POST
def supprimer_ann(Request, id):
    #supprimer le l'annonce de l'id et en supprimant, supprimer aussi l'image enregistrer 
    ann = get_object_or_404(annonce, id=id)
    ann.image_annonce.delete()
    ann.delete()

    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:ann')

#----------------------------------------------------------------> Solidarity Chain

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def sld(Request):
    sld_ch = sld_chain.objects.order_by('-date_ajout')
    return render(Request, 'dash/sld_chain.html', {'sld_ch':sld_ch})

def aj_sld_chain(Request):
    titre = Request.POST.get('titre')
    montant = Request.POST.get('montant')
    type_annonce = "Solidarity Chain"
    
    # Crée une instance de lifestyle et inserer dans la bd
    sl = sld_chain.objects.create(titre=titre, type_annonce=type_annonce, montant=montant)
    sl.save()
    
    messages.success(Request, "Solidarity Chain Enregistrée avec success !" )
    return redirect('dash:sld_chain')

@require_POST
def edit_sld_chain(Request, id):
    if 'form_mod_edit_sld' in Request.POST and Request.method=='POST':
        titre = Request.POST.get('titre')  
        montant = Request.POST.get('montant')
        
        #modifier le theme de l'id 
        objet = sld_chain.objects.get(id=id)
        objet.titre = titre
        objet.montant = montant
        objet.save()
        
        messages.success(Request, "Solidarity Chain modifier avec success !" )
        return redirect('dash:sld_chain')
    sl = get_object_or_404(sld_chain, id=id)
    return render(Request, 'dash/modification/edit_sld_chain.html', {'sl':sl})

@require_POST
def supprimer_sld_ch(Request, id):
    #supprimer le l'annonce de l'id et en supprimant, supprimer aussi l'image enregistrer 
    sl = get_object_or_404(sld_chain, id=id)
    sl.delete()

    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:sld_chain')

#----------------------------------------------------------------> Type Theme Biblique
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def typ_th_b(Request):
    themes = theme_biblique.objects.order_by('-date_ajout')
    return render(Request, 'dash/type_th_b.html', {'themes':themes})

@require_POST
def ajouter_th_b(Request):
    theme = Request.POST.get('theme')
    new_th = theme_biblique(theme=theme)
    new_th.save()
    messages.success(Request, "Thème ajouter avec success !" )
    return redirect('dash:typ_th_b')

@require_POST
def supprimer_th_b(Request, id):
    th_b = get_object_or_404(theme_biblique, id=id)
    th_b.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:typ_th_b')

@require_POST
def edit_typ_th_b(Request, id):
    if 'form_mod_edit_typ_th_b' in Request.POST and Request.method=='POST':
        theme = Request.POST.get('theme')  
        
        #modifier le theme de l'id 
        objet = theme_biblique.objects.get(id=id)
        objet.theme = theme
        objet.save()
        
        messages.success(Request, "Theme modifier avec success !" )
        return redirect('dash:typ_th_b')
    th_b = get_object_or_404(theme_biblique, id=id)
    return render(Request, 'dash/modification/edit_th_b.html', {'th_b':th_b}) 

#----------------------------------------------------------------> Type annonce
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def typ_a(Request):
    tp_a = type_annonce.objects.order_by('-date_ajout')
    return render(Request, 'dash/type_a.html', {'tp_a':tp_a})

@require_POST
def ajouter_typ_a(Request):
    nom_type_annonce = Request.POST.get('nom_type_annonce')
    typ_a = type_annonce(nom_type_annonce=nom_type_annonce)
    typ_a.save()
    messages.success(Request, "Type Annonce ajouter avec success !" )
    return redirect('dash:typ_a')

@require_POST
def supprimer_typ_a(Request, id):
    typ_a = get_object_or_404(type_annonce, id=id)
    typ_a.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:typ_a')

@require_POST
def edit_typ_a(Request, id):
    if 'form_mod_edit_typ_a' in Request.POST and Request.method=='POST':
        nom_type_annonce = Request.POST.get('nom_type_annonce')  
        
        #modifier le nom_type_annonce de l'id 
        objet = type_annonce.objects.get(id=id)
        objet.nom_type_annonce = nom_type_annonce
        objet.save()
        
        messages.success(Request, "Type Annonce modifier avec success !" )
        return redirect('dash:typ_a')
    typ_a = get_object_or_404(type_annonce, id=id)
    return render(Request, 'dash/modification/edit_type_a.html', {'typ_a':typ_a}) 

#----------------------------------------------------------------> Parametre

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def para(Request):
    return render(Request, 'dash/settings.html')

def user_update(Request, id):
    #modifier le last_name, first_name, emain, username de l'id puis retourner avec message success
    last_name = Request.POST.get('last_name')
    first_name = Request.POST.get('first_name')
    email = Request.POST.get('email')
    username = Request.POST.get('username')
        
    #modifier des informations de l'utilisateur 
    objet = User.objects.get(id=id)
    objet.last_name = last_name
    objet.first_name = first_name
    objet.email = email
    objet.username = username
    objet.save()
            
    messages.success(Request, "Information modifié avec success !" )
    return redirect('dash:para')

def mdp_change(Request, id):
    #recuperer le password, password1, password2
    password = Request.POST.get('password')
    password1 = Request.POST.get('password1')
    password2 = Request.POST.get('password2')
    
    #verifier que le password est en accord avec le mot de passe dans la base de données, si oui proceder au changement si non retourner un message d'erreur
    user = User.objects.get(id=id)
    if user.check_password(password):
        user.set_password(password1)
        user.save()
        messages.success(Request, "Mot de passe modifié avec success !" )
        #se login
        user = authenticate(username=user.username, password=password1)
        login(Request, user)
        return redirect('dash:para')
    else:
        messages.error(Request, "Mot de passe actuel incorrect !" )
        return redirect('dash:para')

#----------------------------------------------------------------> Commentaire

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def commentaire(Request):
    #recuper tout de la table comment sauf les element dont status=validé
    comments = comment.objects.exclude(statut='validé').order_by('date_ajout').filter(table="lifestyle")
    #comments = comment.objects.exclude(statut='validé').order_by('date_ajout').filter(table="lifestyle")
    
    for com in comments:
        com.user = User.objects.get(id=com.user_id)

        # Récupérer le titre du sujet en fonction de la table et de l'id_sujet
        if com.table == 'lifestyle':
            sujet = lifestyle.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'pensee_biblique':
            sujet = pensee_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'etude_biblique':
            sujet = etude_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre

    context = {'comments': comments}
    return render(Request, 'dash/comment.html', context)

    
    """
    #en cas de gestion de tout les commentaires 
    @user_passes_test(lambda u: u.is_superuser or u.is_staff)
    def commentaire(request):
        #recuper tout de la table comment sauf les element dont status=validé
        comments = comment.objects.exclude(statut='validé').order_by('-date_ajout')
        for com in comments:
            com.user = User.objects.get(id=com.user_id)

            # Récupérer le titre du sujet en fonction de la table et de l'id_sujet
            if com.table == 'lifestyle':
                sujet = lifestyle.objects.get(id=com.id_sujet)
                com.titre_sujet = sujet.titre
            elif com.table == 'pensee_biblique':
                sujet = pensee_biblique.objects.get(id=com.id_sujet)
                com.titre_sujet = sujet.titre
            elif com.table == 'etude_biblique':
                sujet = etude_biblique.objects.get(id=com.id_sujet)
                com.titre_sujet = sujet.titre

        context = {'comments': comments}
        return render(request, 'dash/comment.html', context)
    """

@user_passes_test(lambda u: u.is_superuser)
def update_statut(request):
    #dans le fichier html, j'ai un code ajax qui est sensé envoye a la view un dictionnaire data contenant les valeurs comment_id et statut, ecris le code recuperation des donnes dans le dictionnaire data 
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment_id = request.POST.get('comment_id')
        statut = request.POST.get('statut')
        
        #print(comment_id)
        #print(statut)
        
        # Utilisez les valeurs comment_id et statut pour effectuer les opérations nécessaires
        try:
            comment_obj = comment.objects.get(id=comment_id)
            
            # Convertir la valeur booléenne en chaîne de caractères "validé" ou "non-validé"
            comment_obj.statut = 'validé' if statut == 'true' else 'non-validé'
            
            comment_obj.save()
            
            return JsonResponse({'success': True})
        except comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Le commentaire n\'existe pas.'})
        except Exception as e:
            erreur = traceback.format_exc()
            return JsonResponse({'success': False, 'error': erreur})

    return JsonResponse({'success': False, 'error': 'Requête invalide.'})
    
@require_POST
def supprimer_commentaire(Request, id):
    comments = get_object_or_404(comment, id=id)
    comments.delete()
    messages.success(Request, "Suppresion effectué avec succes !" )
    #faire un return redirect
    return redirect('dash:comment')

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def commentaire_st(request):
    pass
    """
    #recuper tout de la table comment sauf les element dont status=validé
    comments = comment.objects.exclude(statut='validé').order_by('statut', '-date_ajout')
    for com in comments:
        com.user = User.objects.get(id=com.user_id)

        # Récupérer le titre du sujet en fonction de la table et de l'id_sujet
        if com.table == 'lifestyle':
            sujet = lifestyle.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'pensee_biblique':
            sujet = pensee_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'etude_biblique':
            sujet = etude_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre

    context = {'comments': comments}
    return render(request, 'dash/comment-status.html', context)
    """

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def commentaire_cat(request):
    pass
    """
    #recuper tout de la table comment sauf les element dont status=validé
    comments = comment.objects.exclude(statut='validé').order_by('table', '-date_ajout')
    for com in comments:
        com.user = User.objects.get(id=com.user_id)

        # Récupérer le titre du sujet en fonction de la table et de l'id_sujet
        if com.table == 'lifestyle':
            sujet = lifestyle.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'pensee_biblique':
            sujet = pensee_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre
        elif com.table == 'etude_biblique':
            sujet = etude_biblique.objects.get(id=com.id_sujet)
            com.titre_sujet = sujet.titre

    context = {'comments': comments}
    return render(request, 'dash/comment-cate.html', context)
    """


    
    