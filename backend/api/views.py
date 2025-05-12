# api/views.py

from warnings import filters
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import Produit
from api.serializers import ProduitSerializer
from api.models import Produit
from api.serializers import ProduitSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .models import Commande, LigneCommande
from .serializers import CommandeSerializer, LigneCommandeSerializer
from rest_framework import viewsets
from .models import Fournisseur
from .serializers import FournisseurSerializer




class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Ne pas permettre la modification de la référence
        if 'reference' in request.data:
            request.data.pop('reference')
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    
class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            


class CommandeViewSet(viewsets.ModelViewSet):
     queryset = Commande.objects.prefetch_related('lignes', 'fournisseur').all() 
     serializer_class = CommandeSerializer

     @action(detail=True, methods=['post'])
     def valider(self, request, pk=None):
         commande = self.get_object()
         commande.statut = 'VALIDEE'
         commande.save()
         return Response({'status': 'Commande validée'})
     @action(detail=False, methods=['get'])
     def stats(self, request):
         aujourdhui = datetime.now()
         debut_mois = aujourdhui.replace(day=1)
        
         stats = {
             'mois_courant': Commande.objects.filter(
                 date_creation__gte=debut_mois
             ).count(),
             'en_attente': Commande.objects.filter(
                 statut='BROUILLON'
             ).count(),
             'ca_ht': Commande.objects.filter(
                 statut='VALIDEE'
             ).aggregate(
                 total=Sum('total_ht')
             )['total'] or 0,
             'fournisseurs_actifs': Commande.objects.values(
                 'fournisseur'
             ).distinct().count(),
         }
        
         return Response(stats)

class LigneCommandeViewSet(viewsets.ModelViewSet):
     queryset = LigneCommande.objects.all()
     serializer_class = LigneCommandeSerializer,
    

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    
from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all().order_by('-date_creation')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['ville', 'pays']
    search_fields = ['nom_client', 'email', 'telephone', 'siret']
    ordering_fields = ['nom_client', 'date_creation']
    ordering = ['-date_creation']

    def perform_create(self, serializer):
        """Ajoute des logs ou traitement supplémentaire à la création"""
        serializer.save()
        # Exemple: logger.info(f"Nouveau client créé: {serializer.data['nom_client']}")

    def get_queryset(self):
        """Optionnel: Filtrage supplémentaire"""
        queryset = super().get_queryset()
        # Exemple de filtre supplémentaire:
        # if self.request.query_params.get('actifs'):
        #     queryset = queryset.filter(actif=True)
        return queryset