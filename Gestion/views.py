from django.shortcuts import render, redirect, reverse, resolve_url
from .models import Classe, Eleves, Paiement, TranchePaiement
import locale
from django.contrib.auth.decorators import login_required
locale.setlocale(locale.LC_ALL,"fr-us")

# Create your views here.
@login_required(login_url='/admin/login/')
def Home(request):  
    nb_eleves = Eleves.objects.all().count
    eleves = Eleves.objects.all()
    montant_total_payements = sum(Paiement.objects.all().values_list('montant', flat=True))
    montant_total_payements = str(locale.format_string("%d", montant_total_payements, grouping=True))
    data = []
    nb_tranche_1 = 0
    nb_tranche_2 = 0
    nb_tranche_3 = 0
    for i in eleves:
        montant_total_paye = sum(Paiement.objects.filter(eleve=i.pk).values_list('montant', flat=True))
        tranche_1 = TranchePaiement.objects.get(classe = i.classe.id, numero = 1)
        tranche_2 = TranchePaiement.objects.get(classe = i.classe.id, numero = 2)
        tranche_3 = TranchePaiement.objects.get(classe = i.classe.id, numero = 3)
        stat_1 =  tranche_1.montant_tranche
        # print(stat_1)
        stat_2 =  tranche_2.montant_tranche
        stat_3 =  tranche_3.montant_tranche
        if montant_total_paye >= stat_1 :
            nb_tranche_1= nb_tranche_1 + 1
        if montant_total_paye >= (stat_1 + stat_2) :
            nb_tranche_2 = nb_tranche_2 + 1
        if montant_total_paye >= (stat_1 + stat_2 + stat_3):
            nb_tranche_3 = nb_tranche_3 + 1
    context = {
        'eleves': nb_eleves,
        'nb_tranche_1':nb_tranche_1,
        'nb_tranche_2':nb_tranche_2,
        'nb_tranche_3':nb_tranche_3,
        'total':montant_total_payements

    }
    return render(request, 'index.html', context)

@login_required(login_url='/admin/login/')
def Classes(request):
    classes = Classe.objects.all()
    eleves = Eleves.objects.all()

    data = []
    cpt = 0
    for i in classes:
        for j in eleves:
            if j.classe.id == i.pk:
                cpt = cpt + 1
        tmp = {
            'classe':i,
            'nb_eleve':cpt,
        }
        data.append(tmp)
        cpt = 0
    
    context={
        'classes': data,
        
    }
    return render(request, 'classes.html', context)

@login_required(login_url='/admin/login/')
def Eleves_salle(request, pk):
    classe = Classe.objects.get(pk = pk)
    eleves = Eleves.objects.filter(classe = pk)
    data = []
    data2 = []
    data3 = []
    j = 0
    j3 = 0
    c= 0
    c3= 0
    data_2 = []
    numero = 0

    for i in eleves:
        montant_total_paye = sum(Paiement.objects.filter(eleve=i.pk).values_list('montant', flat=True))
        tranche_1 = TranchePaiement.objects.get(classe = classe.id, numero = 1)
        tranche_2 = TranchePaiement.objects.get(classe = classe.id, numero = 2)
        tranche_3 = TranchePaiement.objects.get(classe = classe.id, numero = 3)
        stat_1 =  tranche_1.montant_tranche
        stat_2 =  tranche_2.montant_tranche
        stat_3 =  tranche_3.montant_tranche
       
        # print(stat_1)
        #ceux qui  n'ont pas fini de payer la 2e tranche
# ceux qui n'ont pas payer la 3e tranche inclus la deuxieme 
        if montant_total_paye < (stat_1 + stat_2 + stat_3) :
            reste = (stat_1 + stat_2 + stat_3 ) - montant_total_paye
            numero = numero + 1
            total = str(locale.format_string("%d",montant_total_paye, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1 + stat_2 + stat_3, grouping=True))
            reste = " - " + str(locale.format_string("%d", reste, grouping=True)) + "FCFA  / (" + str(locale.format_string("%d", stat_1 + stat_2 + stat_3 , grouping=True)) + "FCFA )"
            tmp_2 = {
            'eleve': i,
            'reste': reste,
            'num': numero,
            'total': total,
        }
            data_2.append(tmp_2)




        if montant_total_paye <= stat_1:
            tranche_1 = str(locale.format_string("%d", montant_total_paye, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1,grouping=True))
            tranche_2 = str(0) + "FCFA/ " + str(locale.format_string("%d",stat_2,grouping=True))
            tranche_3 = str(0) + "FCFA/ " + str(locale.format_string("%d",stat_3,grouping=True))
            # total = str(montant_total_paye) + "FCFA/ " + str(stat_1 + stat_2 + stat_2) 
            total = str(locale.format_string("%d",montant_total_paye, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1 + stat_2 + stat_3, grouping=True)) 

            c= c+1
            tmp2 = {
                'numero':c,
                'eleve':i,
                'total':total
            }
            data2.append(tmp2)
        else:

            if montant_total_paye > stat_1 and montant_total_paye <= (stat_1 + stat_2) : 
                tranche_1 = str(locale.format_string("%d",stat_1, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1, grouping=True))
                tranche_2 = str(locale.format_string("%d",montant_total_paye - stat_1, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_2,grouping=True))
                tranche_3 = str(0) + "FCFA/ " + str(locale.format_string("%d",stat_3,grouping=True))
                total = str(locale.format_string("%d",montant_total_paye, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1 + stat_2 + stat_3, grouping=True)) 

                c3= c3+1
                tmp3 = {
                    'numero':c3,
                    'eleve':i,
                    'total':total
            }
                data3.append(tmp3)
            else:
                tranche_1 = str(locale.format_string("%d",stat_1,grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1,grouping=True))
                tranche_2 = str(locale.format_string("%d",stat_2, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_2,grouping=True))
                tranche_3 = str(locale.format_string("%d",montant_total_paye - stat_1 - stat_2,grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_3,grouping=True))
        total = str(locale.format_string("%d",montant_total_paye, grouping=True)) + "FCFA/ " + str(locale.format_string("%d",stat_1 + stat_2 + stat_3, grouping=True)) 
        total_form = montant_total_paye
        tranches = {
            '1': tranche_1,
            '2': tranche_2,
            '3': tranche_3,
            'total': total,
            'total_form':total_form
        }
        j = j+1
        tmp = {
            'eleve': i,
            'tranche':tranches,
            'numero':j
        }
        data.append(tmp)
    context = {
        'eleves':data,
        'classe':classe,
        'etat_2':data2,
        'etat_3':data3,
        'non_2':data_2,
    }
    return render(request, 'eleves_classe.html', context)

@login_required(login_url='/admin/login/')
def Historique(request, pk):
    if request.method == 'POST':
        montant = request.POST.get('montant')
        date = request.POST.get('datePaiement')
        eleve = Eleves.objects.get(pk = pk)
        data = {
            'eleve':eleve,
            'montant':montant,
            'date_paiement':date
        }
        Paiement.objects.create(**data)
        # return render()
        return redirect('Eleves_salle', pk = eleve.classe.pk)
        # Eleves_salle(request=request, pk = eleve.classe.pk)
    eleve = Eleves.objects.get(pk = pk)
    paiements = Paiement.objects.filter(eleve = eleve)
    data = []
    for x in paiements:
        montant = locale.format_string("%d", x.montant,grouping=True)
        tmp = {
            'paiements':x,
            'montant':montant,
        }
        data.append(tmp)
    montant_total_paye = sum(Paiement.objects.filter(eleve= pk).values_list('montant', flat=True))
    montant_total_paye = locale.format_string("%d", montant_total_paye, grouping=True)
    context = {
        'eleve':eleve,
        'paiements':data,
        'total':montant_total_paye
    }
    return render(request, 'historique.html', context)


@login_required(login_url='/admin/login/')
def premiere_tranche(request):
    nb_eleves = Eleves.objects.all().count
    eleves = Eleves.objects.all()
    montant_total_payements = sum(Paiement.objects.all().values_list('montant', flat=True))
    montant_total_payements = str(locale.format_string("%d", montant_total_payements, grouping=True))
    data = []
    nb_tranche_1 = 0
    nb_tranche_2 = 0
    nb_tranche_3 = 0
    j=0
    for i in eleves:
        montant_total_paye = sum(Paiement.objects.filter(eleve=i.pk).values_list('montant', flat=True))
        tranche_1 = TranchePaiement.objects.get(classe = i.classe.id, numero = 1)
        tranche_2 = TranchePaiement.objects.get(classe = i.classe.id, numero = 2)
        tranche_3 = TranchePaiement.objects.get(classe = i.classe.id, numero = 3)
        stat_1 =  tranche_1.montant_tranche
        # print(stat_1)
        stat_2 =  tranche_2.montant_tranche
        stat_3 =  tranche_3.montant_tranche
        if montant_total_paye >= stat_1 :
            j = j + 1
            tmp = {
                'eleve':i,
                'total':montant_total_paye,
                'numero': j,
            }
            data.append(tmp)
    context = {
       'data':data

    }
    return render(request, 'premiere_tranche.html', context)

#Historique de paiement journaliere:

@login_required(login_url='/admin/login/')
def HistoriqueDay(request):
    DatePaiement = Paiement.objects.all()
    data = []
    c = 0
    for x in DatePaiement:
        if data.__contains__(x.date_paiement):
        #    c = c+ 1
            print("already")

        else:
            data.append(x.date_paiement)
            c = c+1
    print(c)
    data.sort(reverse = True)
    context = {
        'date': data
    }
    print(DatePaiement)
    return render(request, 'historique_day.html' , context)