from django.contrib import admin
from .models import Produit

from .models import *
admin.site.register([Utilisateur, Client, Fournisseur, Commande, LigneCommande, MouvementStock, Categorie])


class ProduitAdmin(admin.ModelAdmin):
    exclude = ('reference',)  # ou utilise exclude = ('reference',) si tu veux le cacher
    list_display = ('designation', 'reference', 'prix_vente', 'quantite_stock')

# Puis enregistre-la comme ceci :
admin.site.register(Produit, ProduitAdmin)
