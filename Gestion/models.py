from django.db import models
class Classe(models.Model):
    libele = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.libele 
    def all(self):
        return self.eleves.all
class Eleves(models.Model):
    nom = models.CharField(max_length=30, blank=True)
    prenom = models.CharField(max_length=30, blank=True)
    sexe = models.CharField(max_length=30, choices=[("Masculin", "masculin"), ("Feminin", "feminin")], blank=True)
    date_nais = models.DateField(blank=True, null = True)
    adresse = models.CharField(max_length=30, default=None, blank=True)
    telephone = models.CharField(max_length=30, default=None, blank=True)
    statut = models.BooleanField(default=False, blank=True)
    classe = models.ForeignKey(Classe, on_delete = models.CASCADE, default=None, related_name="eleves")
    class Meta:
        ordering = ['nom']

class Paiement(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    montant = models.IntegerField()
    date_paiement = models.DateField(null = True, auto_now_add=True)
# class TypePaiement(models.Model):
#     type_paiement = models.CharField(max_length=30, choices=[("A", "NURSERY"),("B", "PRIMAIRE")])
    def __str__(self) -> str:
        return str(self.eleve.nom)

class TranchePaiement(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    montant_tranche = models.IntegerField()
    date_limite = models.DateField()
    # type_paiement = models.ForeignKey("TypePaiement", on_delete=models.CASCADE, related_name="tranches")  
    classe = models.ForeignKey("Classe", on_delete=models.CASCADE, related_name="tranches", blank = True, null=True)
    def __str__(self) -> str:
        return str(self.montant_tranche)
# Create your models here.
class Enseignant(models.Model):
    nom = models.CharField(max_length=50)
    cni = models.IntegerField()
    conctact = models.CharField(max_length=50)
    def __str__(self) -> str:
        return str(self.nom)
