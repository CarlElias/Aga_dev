from django.db import models
from django.contrib.auth.models import User
    
#model type_annonce avec le nom du type_annonce
class type_annonce(models.Model):
    nom_type_annonce = models.CharField(max_length=500)
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom_type_annonce

#model theme_biblique avec le nom
class theme_biblique(models.Model):
    theme = models.CharField(max_length=500)
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.theme
    
class quote(models.Model):
    themes = models.ManyToManyField(theme_biblique)
    txt_quote = models.CharField(max_length=2000)
    verset = models.CharField(max_length=500)
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.verset

#model annonce
class annonce(models.Model):
    type_annonce = models.ForeignKey(type_annonce, on_delete=models.CASCADE, null=True)
    titre = models.CharField(max_length=500)
    txt_annonce = models.TextField()
    image_annonce = models.ImageField(upload_to='images_upload/annonce')
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.titre
    
#model pour contact avec nom, mail, message, contact, date
class contact(models.Model):
    nom = models.CharField(max_length=500)
    mail = models.CharField(max_length=500)
    message = models.TextField()
    contact = models.CharField(max_length=500)
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
#model etude_biblique avec le theme lié a la table theme_biblique
class etude_biblique(models.Model):
    themes = models.ManyToManyField(theme_biblique)
    titre = models.CharField(max_length=500)
    sous_titre = models.CharField(max_length=500)
    verset = models.CharField(max_length=500)
    contenu = models.TextField()
    lien_yt = models.CharField(max_length=500, blank=True)
    date_ajout = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    
#model pensee_biblique avec le theme lié a la table theme_biblique, le contenu, un lien youtube
class pensee_biblique(models.Model):
    theme = models.ForeignKey(theme_biblique, on_delete=models.CASCADE, null=True)
    titre = models.CharField(max_length=500)
    contenu = models.TextField()
    lien_youtube = models.CharField(max_length=500)
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.titre
      
#model lifestyle, lie a plusieurs theme biblique, ayant un titre, du contenu, une image et une date d'ajout
class lifestyle(models.Model):
    themes = models.ManyToManyField(theme_biblique)
    titre = models.CharField(max_length=500)
    contenu = models.TextField()
    image = models.ImageField(upload_to='images_upload/lifestyle')
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.titre

#model pour les comment, qui a un contenu, qui est appartien a un utilisateur
class comment(models.Model):
    contenu = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #un champ statut contenant trois option : validé, pre-validé et non-valider
    STATUT = (
        ('validé', 'validé'),
        ('pre-validé', 'pre-validé'),
        ('non-validé', 'non-validé'),
    )
    statut = models.CharField(max_length=500, choices=STATUT, default='non-valider')
    id_sujet = models.IntegerField()
    #un champ pour valider de quel table le commantaire s'agit 
    TABLE = (
        ('etude_biblique', 'etude_biblique'),
        ('pensee_biblique', 'pensee_biblique'),
        ('lifestyle', 'lifestyle'),
    )
    table = models.CharField(max_length=500, choices=TABLE, default='etude_biblique')
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Commentaire {self.pk} - Auteur: {self.user.username}, Contenu: {self.contenu[:50]}..."



#model Priere/louange avec verset, theme lié a theme biblique, contenu, type soit louange ou priere
class priere_louange(models.Model):
    verset = models.CharField(max_length=500)
    theme = models.ForeignKey(theme_biblique, on_delete=models.CASCADE, null=True)
    lien_yt = models.CharField(max_length=500, blank=True)
    contenu = models.TextField()
    TYPE = (
        ('louange', 'louange'),
        ('priere', 'priere'),
    )
    type = models.CharField(max_length=500, choices=TYPE, default='louange')
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.verset
    
#model message avec nom, prenom, email, contact, cintenu
class message(models.Model):
    nom = models.CharField(max_length=500)
    prenom = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    objet = models.CharField(max_length=500)
    contact = models.CharField(max_length=500)
    contenu = models.TextField()
    date_ajout = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom