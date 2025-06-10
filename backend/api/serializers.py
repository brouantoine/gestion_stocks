# api/serializers.py
from multiprocessing.connection import Client
from rest_framework import serializers
from .models import Produit, Taxe
from django.core.validators import ValidationError




from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'  # Ou spécifiez les champs explicitement




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
    
from rest_framework import serializers
from .models import Utilisateur

from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Utilisateur.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'vendeur'),
            telephone=validated_data.get('telephone', ''),
            est_actif=validated_data.get('est_actif', True)
        )
        return user




from rest_framework import serializers
from .models import CommandeClient, LigneCommandeClient

class LigneCommandeClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneCommandeClient
        fields = '__all__'

# serializers.py
class LigneCommandeClientSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())
    
    class Meta:
        model = LigneCommandeClient
        fields = ['produit', 'quantite', 'prix_unitaire', 'remise_ligne']  # Retirer 'tva' si présent
        extra_kwargs = {
            'quantite': {'required': True},
            'prix_unitaire': {'required': True}
        }

class CommandeClientSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeClientSerializer(many=True)
    
    class Meta:
        model = CommandeClient
        fields = '__all__'
        read_only_fields = ('total_commande',)  # Le total sera calculé côté serveur

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes', [])
        
        # Création basique de la commande sans les lignes
        commande = CommandeClient.objects.create(**validated_data)
        
        # Les lignes seront ajoutées dans la vue
        return commande