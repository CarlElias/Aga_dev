from django.urls import path
from django.conf.urls import handler404
from .views import *

app_name = 'dash'

urlpatterns = [
    path('', user_page, name='user_page'),
    path('logout', logout_view, name='logout'),
    path('template', template, name='template'),
#-------------------------------------------------------------------->Message
    path('message', msg, name="msg"),
    path('supprimer-message/<int:id>', supprimer_msg, name="supprimer_msg"),
#-------------------------------------------------------------------->Gestion des utilisateurs
    path('Utilisateurs', gest_us, name="gest_us"),
    path('update-is-staff/',update_is_staff, name='update_is_staff'),
    path('supprimer-utilisateur/<int:id>', supprimer_us, name="supprimer_us"),
#-------------------------------------------------------------------->Quotes / INspiration
    path('citation', insp, name="insp"),
    path('ajouter_citation', ajouter_insp, name="ajouter_insp"),
    path('edit-citation/<int:id>', edit_insp, name="edit_insp"),
    path('supprimer-citation/<int:id>', supprimer_insp, name="supprimer_insp"),
#-------------------------------------------------------------------->LifeStyle
    path('lifestyle', lifes, name="lifes"),
    path('ajouter_lifes', ajouter_lif, name="ajouter_lif"),
    path('edit-lifestyle/<int:id>', edit_lif, name="edit_lif"),
    path('supprimer-lifestyle/<int:id>', supprimer_lif, name="supprimer_lif"),
#-------------------------------------------------------------------->Etude Biblique
    path('etude-biblique', etude_b, name="etude_b"),
    path('ajouter_et_b', ajouter_et_b, name="ajouter_et_b"),
    path('edit-etude-biblique/<int:id>', edit_etude_b, name="edit_etude_b"),
    path('supprimer-etude-biblique/<int:id>', supprimer_etude_b, name="supprimer_etude_b"),
#-------------------------------------------------------------------->Annonce
    path('Annonce', annonce, name="ann"),
#-------------------------------------------------------------------->Type
    path('type-theme-biblique', typ_th_b, name='typ_th_b'),
    path('ajouter_th_b', ajouter_th_b, name="ajouter_th_b"),
    path('edit-theme-biblique/<int:id>', edit_typ_th_b, name="edit_typ_th_b"),
    path('supprimer-theme-biblique/<int:id>', supprimer_th_b, name="supprimer_th_b"),
    
    path('type-annonce', typ_a, name='typ_a'),
    path('ajouter_typ_a', ajouter_typ_a, name="ajouter_typ_a"),
    path('edit-type-annonce/<int:id>', edit_typ_a, name="edit_typ_a"),
    path('supprimer-type-annonce/<int:id>', supprimer_typ_a, name="supprimer_typ_a"),
    #-------------------------------------------------------------------->Settings
    path('Parametre', para, name="para"),
    path('Parametre-user-update/<int:id>', user_update, name="user_update"),
    path('Parametre-user-delete/<int:id>', mdp_change, name="mdp_change"),
    #-------------------------------------------------------------------->Commentaire
    path('commentaire', commentaire, name="comment"),
    path('commentaire-status', commentaire_st, name="comment_st"),
    path('commentaire-catgerie', commentaire_cat, name="comment_cat"),
    path('supprimer-commentaire/<int:id>', supprimer_commentaire, name="supprimer_commentaire"),
    
    
]

#gestion d'erreur 404
handler404 = 'app.views.handler404'