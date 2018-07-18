from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django import forms

from game.models import *
from django.shortcuts import redirect
import random
from django.utils import timezone

from game.vars import *

import datetime

random.seed(datetime.datetime.now())



def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

@csrf_exempt
def registre(request, **kwargs):

    partida_activa = Partida.objects.filter(estat="REGISTRANT")
    if len(partida_activa)>0:

        ######################################################################
        ##############  CODI PER QUAN S'ESTA LLISTANT USUARIS
        partida_activa = partida_activa[0]
        usuaris = User.objects.filter(partida=partida_activa)

        # Si hi ha una partida registrant i es un POST, vol dir que hem de comensar la partida nova
        if request.method == 'POST':

                #if len(usuaris)==0:
                if len(usuaris)<6:
                    return redirect('admin.registre')


                partida_activa.estat = "GENERANT_DADES"
                partida_activa.save()


                if len(usuaris)<6:
                    #Creem usuaris fake, temporal mentres fem proves!!!
                    for i in range(6-len(usuaris)):
                        user = User()
                        user.is_robot = True
                        user.nickname = "ROBOT "+str(i+1)
                        user.genere = "N"
                        user.rang_edat = -1
                        user.nivell_estudis = "N"
                        user.codi_postal = -1
                        user.diners_inicials = 0
                        user.diners_actuals = 0
                        user.data_creacio = timezone.now()
                        user.partida = partida_activa
                        user.save()
                    usuaris = User.objects.filter(partida=partida_activa)

                #Assignem diners inicials i numeros de jugador als participants
                random.shuffle(NUMS_JUGADOR)
                random.shuffle(VALORS_INICI)



                for i in range(len(usuaris)):
                    usuaris[i].num_jugador = NUMS_JUGADOR[i]

                    usuaris[i].diners_inicials = 40
                    usuaris[i].diners_actuals = 40

                    usuaris[i].save()



                #Generar les dades que necessitem de la partida
                partida_activa.num_rondes = 10
                for num_ronda in range(partida_activa.num_rondes):
                    ronda = Ronda.objects.create(partida=partida_activa, num_ronda=num_ronda+1)

                    for user in usuaris:
                        UserRonda.objects.create(user=user,
                                                 ronda=ronda,
                                                 ha_seleccionat=False)

                #I... ENGEGO LA PARTIDA!!!!
                partida_activa.estat = "JUGANT"

                partida_activa.ronda_actual=1
                partida_activa.data_inicialitzacio = timezone.now()
                partida_activa.data_fi_ronda = timezone.now() +  datetime.timedelta(seconds=TEMPS_INICI_SEC+TEMPS_RONDA_SEC)

                partida_activa.save()

                ronda_actual = partida_activa.ronda_set.get(num_ronda=1)
                ronda_actual.bucket_inici_ronda = 120
                ronda_actual.temps_inici_ronda = partida_activa.data_inicialitzacio +  datetime.timedelta(seconds=TEMPS_INICI_SEC)
                ronda_actual.save()

                return redirect('admin.partida')

        #Sino obtinc el llistat d'usuaris registrats en aquesta partida
        return render_to_response('admin_registre.html', {'registre_iniciat': True,
                                                         'usuaris': usuaris,
                                                         'partida': partida_activa,
                                                         'pagina': 'registre',
                                                         'lang': request.session['lang'],
                                                         'text': request.session['text']},
                                  context_instance=RequestContext(request))


    ######################################################################
    ##############  CODI PER QUAN NO HI HA REGISTER OBERT
    #Si no hi ha registre i rebem un post, en creem una de nova!!
    if request.method == 'POST':
        results = Partida.objects.all().order_by('-num_partida')
        npartida = 1
        #Si hi ha mes d'un result, mirem quin es el seguent num de partida
        if len(results) > 0:
            npartida = results[0].num_partida+1

        #### random.randint(0,1) == 1 50%
        #### random.randint(0,9) == 9 10%

        partida = Partida.objects.create(num_partida=npartida,
                                         data_creacio=timezone.now(),
                                         estat="REGISTRANT",
                                         classe="VILADECANS",
                                         guanyen_igualment = True if random.randint(0,1) == 1 else False,
                                         num_rondes=10)
        partida.save()
        return redirect('admin.registre')

    #Sino es un post, ensenyem el boto per crear registre nou
    return render_to_response('admin_registre.html', {
                                        'registre_iniciat': False,
                                         'lang': request.session['lang'],
                                         'pagina': 'registre',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))





@csrf_exempt
def partida(request, **kwargs):
    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def stats(request, **kwargs):
    #Sino es un post, ensenyem el boto per crear registre nou
    return render_to_response('admin_stats.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'stats',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))



@csrf_exempt
def partida_detail(request, **kwargs):
    num_partida = kwargs.get('num_partida', None)

    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida_detail.html', {
                                         'lang': request.session['lang'],
                                         'num_partida': num_partida,
                                         'pagina': 'partida_detail',
                                         'text': request.session['text']},
                                        context_instance=RequestContext(request))



@csrf_exempt
def users(request, **kwargs):
    users = [{'nickname': u.nickname,
              'partida': u.partida_id,
              'diners_clima': u.diners_clima,
              'diners_inversor': u.diners_inversor,
              'diners_empresari': u.diners_empresari,
              'diners_premi': u.diners_premi,
              'diners_total': u.diners_total,
              'val_abacus': u.val_abacus,
              'id': u.id} for u in User.objects.filter(is_robot=False).order_by('-data_creacio')]
    users_1 = users[0:18]
    users_2 = users[18:36]

    print users

    return render_to_response('admin_users.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'users',
                                         'text': request.session['text'],
                                         'users_1': users_1,
                                         'users_2': users_2},
                          context_instance=RequestContext(request))


@csrf_exempt
def users_reset(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    print "Reseting user", user_id
    if user_id is not None:
        user = User.objects.get(id=user_id)
        if user is not None:
            user.partida=None
            user.save()
    return redirect('admin.users')


@csrf_exempt
def partida_list(request, **kwargs):
    partides = [{'num_partida': p.num_partida,
                 'classe': p.classe,
                 'data_creacio': p.data_creacio,
                 'users': [{'nickname': u.nickname} for u in p.user_set.all()[0:2]]}
                for p in Partida.objects.filter(estat__in=("ACABADA", "ACABADA_MANUAL")).order_by('-data_finalitzacio')[0:20]]
    partides_1 = partides[0:10]
    partides_2 = partides[10:20]
    return render_to_response('admin_partida_list.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida_list',
                                         'text': request.session['text'],
                                         'partides_1': partides_1,
                                         'partides_2': partides_2},
                          context_instance=RequestContext(request))


