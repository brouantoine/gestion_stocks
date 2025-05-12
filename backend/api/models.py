# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class Utilisateur(AbstractUser):
    ROLES = (
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire de stock'),
        ('vendeur', 'Vendeur'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='vendeur')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Client(models.Model):
    nom_client = models.CharField(max_length=255)
    adresse = models.TextField()
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="France")
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    siret = models.CharField(max_length=14, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom_client

class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=255)
    adresse = models.TextField()
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="France")
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    siret = models.CharField(max_length=14)
    date_creation = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom_fournisseur

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

from django.db import models

from django.db import models

class Produit(models.Model):
    UNITE_CHOICES = (
        ('unite', 'Unité'),
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('l', 'Litre'),
        ('m', 'Mètre'),
    )
    
    categorie = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    designation = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=5)
    unite_mesure = models.CharField(max_length=10, choices=UNITE_CHOICES, default='unite')
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reference'],
                name='unique_reference'
            )
        ]

    def save(self, *args, **kwargs):
        """Génère automatiquement la référence à la création uniquement"""
        if not self.pk and not self.reference:
            prefix = "PRD"
            last_id = Produit.objects.order_by('-id').values_list('id', flat=True).first() or 0
            self.reference = f"{prefix}{str(last_id + 1).zfill(5)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.designation} ({self.reference})"
class Commande(models.Model):
    STATUS_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('VALIDEE', 'Validée'),
        ('EN_PREPARATION', 'En préparation'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.PROTECT, related_name='commandes' )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BROUILLON')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    remise_globale = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Commande {self.numero} - {self.fournisseur}"
    
    @property
    def total_ht(self):
        return sum(ligne.total_ligne_ht for ligne in self.lignes.all())
    
    @property
    def total_ttc(self):
        return self.total_ht  # Ajouter taxes si nécessaire

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    remise_ligne = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_livraison_prevue = models.DateField(null=True, blank=True)
    statut_livraison = models.CharField(max_length=20, default='A_LIVRER')
    
    def __str__(self):
        return f"{self.quantite}x {self.produit}"
    
    @property
    def total_ligne_ht(self):
        return (self.quantite * self.prix_unitaire) * (1 - self.remise_ligne / 100)
    
    
class MouvementStock(models.Model):
    TYPE_MOUVEMENT = (
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('ajustement', 'Ajustement'),
    )
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type_mouvement} de {self.quantite} {self.produit.unite_mesure} pour {self.produit}"

