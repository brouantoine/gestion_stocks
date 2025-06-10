# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class Taxe(models.Model):
    nom = models.CharField(max_length=50)
    taux = models.DecimalField(max_digits=5, decimal_places=2)  # 20.00 pour 20%
    code_comptable = models.CharField(max_length=20, blank=True)
    
class Utilisateur(AbstractUser):
    ROLES = (
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire de stock'),
        ('vendeur', 'Vendeur'),
        ('caissier', 'Caissier'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='vendeur')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)
    modules = models.ManyToManyField('Module',blank=True)
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
    image = models.ImageField(upload_to='produits/', blank=True)
    code_barre = models.CharField(max_length=50, blank=True)
    tva = models.ForeignKey(Taxe, on_delete=models.PROTECT, null=True)

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
    # Ajouter dans les deux modèles
    tva = models.ForeignKey(Taxe, on_delete=models.PROTECT)
    date_echeance = models.DateField(blank=True, null=True)  # Pour paiement
    
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
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, related_name='lignecommandes')
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
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, related_name='mouvements')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type_mouvement} de {self.quantite} {self.produit.unite_mesure} pour {self.produit}"

class Statistique(models.Model):
    date = models.DateField(auto_now_add=True)
    total_commandes = models.IntegerField(default=0)
    total_clients = models.IntegerField(default=0)
    total_fournisseurs = models.IntegerField(default=0)
    total_produits = models.IntegerField(default=0)
    ca_ht = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Statistiques du {self.date}"
from django.db import models
from django.contrib.auth import get_user_model

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Connexion'),
        ('LOGOUT', 'Déconnexion'),
        ('CREATE', 'Création'),
        ('UPDATE', 'Mise à jour'),
        ('DELETE', 'Suppression'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Log d'activité"
        verbose_name_plural = "Logs d'activité"

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} à {self.timestamp}"
    
class Vente(models.Model):
    STATUS_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('VALIDEE', 'Validée'),
        ('PAYEE', 'Payée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_vente = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BROUILLON')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    numero_facture = models.CharField(max_length=20, unique=True, blank=True)
    # Ajouter dans les deux modèles
    tva = models.ForeignKey(Taxe, on_delete=models.PROTECT)
    date_echeance = models.DateField(blank=True, null=True)  # Pour paiement

class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

class Inventaire(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(Utilisateur, on_delete=models.PROTECT)
    complet = models.BooleanField(default=False)

class LigneInventaire(models.Model):
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite_theorique = models.IntegerField()
    quantite_reelle = models.IntegerField()
    ecart = models.IntegerField(default=0)

class Parametres(models.Model):
    seuil_alerte_defaut = models.IntegerField(default=5)
    tva_par_defaut = models.ForeignKey(Taxe, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='logos/', blank=True)


class Emplacement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()

class StockProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)


from django.db import models
from django.core.validators import MinValueValidator

class CommandeClient(models.Model):
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon (panier non validé)'),
        ('VALIDEE', 'Validée par le client'),
        ('EN_PREPARATION', 'En préparation'),
        ('PRETE', 'Prête pour retrait/livraison'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]

    MODE_RETRAIT = [
        ('MAGASIN', 'Retrait en magasin'),
        ('LIVRAISON', 'Livraison à domicile'),
    ]

    # Identifiant unique (ex: "CMD-2023-001")
    numero_commande = models.CharField(max_length=20, unique=True, blank=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, related_name='commandes')
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.PROTECT, null=True, blank=True)  # Vendeur/Caissier
    
    # Logistique
    mode_retrait = models.CharField(max_length=10, choices=MODE_RETRAIT, default='MAGASIN')
    adresse_livraison = models.TextField(blank=True)  # Si livraison
    date_creation = models.DateTimeField(auto_now_add=True)
    date_livraison_prevue = models.DateTimeField(null=True, blank=True)
    date_livraison_reelle = models.DateTimeField(null=True, blank=True)
    
    # État
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='BROUILLON')
    est_payee = models.BooleanField(default=False)
    
    # Financier
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Remise globale en %
    tva = models.ForeignKey('Taxe', on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    total_commande = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)  # Total TTC
    class Meta:
        verbose_name = "Commande client"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commande {self.numero_commande} - {self.client.nom_client}"

    def save(self, *args, **kwargs):
        """Sauvegarde la commande sans essayer de calculer le total immédiatement"""
        if not self.numero_commande:
            prefix = "CMD"
            last_id = CommandeClient.objects.order_by('-id').values_list('id', flat=True).first() or 0
            self.numero_commande = f"{prefix}-{str(last_id + 1).zfill(3)}"
        
        # Sauvegarde d'abord pour obtenir un ID
        super().save(*args, **kwargs)
        
        # Calcule le total seulement si la commande existe déjà
        if self.pk:
            self.total_commande = self.total_ttc
            super().save(update_fields=['total_commande'])

    @property
    def total_ht(self):
        if not self.pk:  # Si la commande n'est pas encore sauvegardée
            return 0
        return sum(ligne.sous_total_ht for ligne in self.lignes.all())

    @property
    def total_ttc(self):
        if not self.pk or not hasattr(self, 'tva'):  # Si pas sauvegardé ou pas de TVA
            return 0
        return self.total_ht * (1 + self.tva.taux / 100)
    

class LigneCommandeClient(models.Model):
    commande = models.ForeignKey(CommandeClient, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('Produit', on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de la commande
    remise_ligne = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Remise en % par produit

    def __str__(self):
        return f"{self.quantite}x {self.produit.designation}"

    @property
    def sous_total_ht(self):
        try:
            quantite = self.quantite if self.quantite is not None else 0
            prix = self.prix_unitaire if self.prix_unitaire is not None else 0
            remise = self.remise_ligne if self.remise_ligne is not None else 0
            return (quantite * prix) * (1 - remise / 100)
        except (TypeError, AttributeError):
            return 0

from django.db import models

class Module(models.Model):
    """
    Système modulaire pour gérer les accès fonctionnels
    """
    CODE_CHOICES = [
        ('PRODUCTS', 'Produits'),
        ('SALES', 'Ventes'),
        ('CAISSE', 'Caisse'),
        ('CUSTOMERS', 'Clients'),
        ('ORDERS', 'Commandes'),
        ('ADMIN', 'Administration'),
        ('REPORTS', 'Statistiques'),
        ('INVENTORY', 'Inventaire'),
        ('SETTINGS', 'Paramètres'),
        ('LOGS', 'Logs')
    ]

    code = models.CharField(
        max_length=20,
        choices=CODE_CHOICES,
        unique=True
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    route = models.CharField(max_length=100, default='/')
    allowed_roles = models.CharField(max_length=200, default='admin')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def roles_list(self):
        return [r.strip() for r in self.allowed_roles.split(',')]