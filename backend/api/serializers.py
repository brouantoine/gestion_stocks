# api/serializers.py
from multiprocessing.connection import Client
from rest_framework import serializers
from .models import Produit
from django.core.validators import ValidationError

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'
        extra_kwargs = {
            'reference': {
                'read_only': True  # Empêche toute modification de la référence
            }
        }

    # Supprimez la méthode validate_reference qui cause le problème

    def validate_reference(self, value):
        if Produit.objects.filter(reference=value).exists():
            raise serializers.ValidationError("Cette référence existe déjà.")
        return value # api/serializers.py
from rest_framework import serializers
from .models import Produit
from django.core.validators import ValidationError

from rest_framework import serializers

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'
        extra_kwargs = {
            'reference': {
                'read_only': True  # Empêche la modification via l'API
            }
        }

from rest_framework import serializers
from .models import Commande, LigneCommande

class LigneCommandeSerializer(serializers.ModelSerializer):
     class Meta:
         model = LigneCommande
         fields = '__all__'
         read_only_fields = ('total_ligne_ht',)

from rest_framework import serializers
from .models import Commande

from rest_framework import serializers
from .models import Commande

class CommandeSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeSerializer(many=True, required=False, read_only=True)
    total_ht = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True,
        coerce_to_string=False  # Important pour les décimaux
    )
    nom_fournisseur = serializers.CharField(
        source='fournisseur.nom_fournisseur',
        read_only=True,
        allow_null=True  # Permet les valeurs nulles
    )

    class Meta:
        model = Commande
        fields = [
            'id',
            'numero',
            'date_creation',
            'date_validation',
            'statut',
            'notes',
            'remise_globale',
            'fournisseur',
            'nom_fournisseur',
            'utilisateur',
            'total_ht',
            'lignes'
        ]
        extra_kwargs = {
            'fournisseur': {'required': True},
            'utilisateur': {'read_only': True}
        }

    def validate(self, data):
        """Validation globale"""
        if data.get('remise_globale', 0) < 0 or data.get('remise_globale', 0) > 100:
            raise serializers.ValidationError({
                'remise_globale': 'Doit être entre 0 et 100'
            })
        return data
    
    def validate_fournisseur(self, value):
        if not value:
            raise serializers.ValidationError("Le fournisseur est obligatoire")
        return value
from rest_framework import serializers
from .models import Fournisseur

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'

from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'nom_client',
            'adresse',
            'code_postal',
            'ville',
            'pays',
            'telephone',
            'email',
            'siret',
            'date_creation',
            'notes'
        ]
        read_only_fields = ['id', 'date_creation']
        extra_kwargs = {
            'email': {'required': False},
            'siret': {'required': False},
            'notes': {'required': False}
        }

    def validate_telephone(self, value):
        """Validation personnalisée du numéro de téléphone"""
        if len(value) < 10:
            raise serializers.ValidationError("Le numéro de téléphone doit contenir au moins 10 chiffres")
        return value

    def validate_siret(self, value):
        """Validation du SIRET si fourni"""
        if value and len(value) != 14:
            raise serializers.ValidationError("Le SIRET doit contenir exactement 14 chiffres")
        return value