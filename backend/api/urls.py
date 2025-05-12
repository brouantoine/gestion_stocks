from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FournisseurViewSet, ProduitViewSet, ClientViewSet
from .views import ProduitViewSet, CommandeViewSet, LigneCommandeViewSet


router = DefaultRouter()
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'commandes', CommandeViewSet, basename='commande')
router.register(r'lignes-commande', LigneCommandeViewSet, basename='lignecommande')
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'clients', ClientViewSet, basename='client')
urlpatterns = [
    path('', include(router.urls)),  # <- Changement ici (supprimé 'api/')
]  

# urlpatterns = [
#     path('api/', include(router.urls)),  # Toutes les URLs auront le préfixe /api/
# ]