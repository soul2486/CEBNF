from django.contrib import admin

from .models import Classe, Eleves, Paiement, TranchePaiement

# Register your models here.
class elevesAdmin(admin.ModelAdmin): 
  list_display =['nom', 'prenom', 'sexe', 'classe']
# class classeAdmin(admin.ModelAdmin):
#   list_display = ['libele']

admin.site.register(Eleves,elevesAdmin)
# admin.site.register(Classe,classeAdmin)

class ÉlèveInline(admin.TabularInline):
    model = Eleves
    extra = 0

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('libele',)
    inlines = [ÉlèveInline]

class TranchePaiementAdmin(admin.ModelAdmin):
  list_display = ('numero', 'montant_tranche', 'date_limite', 'classe')
class PaiementAdmin(admin.ModelAdmin):
  list_display = ('eleve', 'montant', 'date_paiement')

admin.site.register(Paiement, PaiementAdmin)
admin.site.register(TranchePaiement, TranchePaiementAdmin)