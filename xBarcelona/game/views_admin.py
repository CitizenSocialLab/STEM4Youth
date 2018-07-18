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
        ##############  CODI PER QUAN S'ESTA LLISTANT USUARIS ################
        ######################################################################

        partida_activa = partida_activa[0]
        usuaris = User.objects.filter(partida=partida_activa)

        # Si hi ha una partida registrant i es un POST, vol dir que hem de comensar la partida nova
        if request.method == 'POST':

                #ToDo: SI NO HI HA ALMENYS 6 USUARIS NO ES POT COMENSAR!!!! Ara el limit es 1
                #if len(usuaris)==0:
                if len(usuaris) < 6:
                    return redirect('admin.registre')


                partida_activa.estat = "GENERANT_DADES"
                partida_activa.save()

                #Creem usuaris fake, temporal mentres fem proves!!!
                if len(usuaris)<6:
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


                game_trust = []
                game_dictator = []
                game_prisoner = []
                # Cream els Trust per cada usuari
                for i in range(len(usuaris)):
                    trust = Trust()
                    trust.user = usuaris[i]
                    game_trust.append(trust)
                    trust.save()

                    dictator =  Dictator()
                    dictator.user = usuaris[i]
                    game_dictator.append(dictator)
                    dictator.save()

                    prisoner = Prisoner()
                    prisoner.user = usuaris[i]
                    game_prisoner.append(prisoner)
                    prisoner.save()

                # Assignem un numero als participants de l'experiment
                random.shuffle(NUMS_JUGADOR)
                # Public Goods - Valors inicials
                random.shuffle(VALORS_INICI)
                # Trust Game - Valors inicials
                random.shuffle(INVERSOR_EMPRESARI)
                # Dictator Game - Valors inicials
                random.shuffle(DICTATOR_PUNISHER)
                # Prisoner Game - Valors inicials
                random.shuffle(ADVANTAGE_DISADVANTAGE)


                # Trust Game - Llistat usuaris
                llista_trust_inversors1 = []
                llista_trust_inversors2 = []
                llista_trust_empresaris1 = []
                llista_trust_empresaris2 = []

                # Dictator Game - Llistat usuaris
                llista_dictator_dictator1 = []
                llista_dictator_dictator2 = []
                llista_dictator_punisher1 = []
                llista_dictator_punicher2 = []

                # Prisoner Dilemma - Llistat usuaris
                llista_prisoner1 = [] # JUGADORES IGUALES

                llista_prisoner_advantage2 = [] # JUGADORES A en la 2
                llista_prisoner_disavantage2 = [] # JUGADORES D en la 2

                llista_prisoner_advantage3 = [] # JUGADORES A en la 3
                llista_prisoner_disavantage3 = [] # JUGADORES D en la 3


                for i in range(len(usuaris)):
                    # Numero de jugador per cada usuari
                    usuaris[i].num_jugador = NUMS_JUGADOR[i]

                    # Public Goods - Diners inicials i actuals
                    usuaris[i].diners_inicials = 40
                    usuaris[i].diners_actuals = 40

                    # Trust Game - Donam el rol INVERSOR a la primera i EMPRESARI a las segona
                    if INVERSOR_EMPRESARI[i]=='I':
                        game_trust[i].rol1 = 'I'
                        game_trust[i].rol2 = 'E'
                        llista_trust_inversors1.append(game_trust[i])
                        llista_trust_empresaris2.append(game_trust[i])


                        if usuaris[i].is_robot:
                            game_trust[i].seleccio1 = random.choice([0,1,2,3,4,5,6,7,8,9,10])
                            game_trust[i].seleccio2 = random.choice([0,25,50,75,100])

                    # Trust Game - Donam el rol EMPRESARI a la primera i INVERSOR a la segona
                    else:
                        game_trust[i].rol1 = 'E'
                        game_trust[i].rol2 = 'I'

                        llista_trust_empresaris1.append(game_trust[i])
                        llista_trust_inversors2.append(game_trust[i])

                        if usuaris[i].is_robot:
                            game_trust[i].seleccio2 = random.choice([0,1,2,3,4,5,6,7,8,9,10])
                            game_trust[i].seleccio1 = random.choice([0,25,50,75,100])

                    # Dictator Game - Donam el rol DICTATOR a la primera i PUNISHER a las segona
                    if DICTATOR_PUNISHER[i]=='D':
                        game_dictator[i].rol1 = 'D'
                        game_dictator[i].rol2 = 'P'
                        llista_dictator_dictator1.append(game_dictator[i])
                        llista_dictator_punicher2.append(game_dictator[i])

                        if usuaris[i].is_robot:
                            game_dictator[i].seleccio1 = random.choice([0,1,2,3,4,5,6,7,8,9,10])
                            game_dictator[i].seleccio2 = random.choice([0,1,2,3,4,5])

                    # Dictator Game - Donam el rol DICTADOR a la primera i PUNISHER a la segona
                    else:
                        game_dictator[i].rol1 = 'P'
                        game_dictator[i].rol2 = 'D'

                        llista_dictator_punisher1.append(game_dictator[i])
                        llista_dictator_dictator2.append(game_dictator[i])

                        if usuaris[i].is_robot:
                            game_dictator[i].seleccio2 = random.choice([0,1,2,3,4,5,6,7,8,9,10])
                            game_dictator[i].seleccio1 = random.choice([0,1,2,3,4,5])


                    # Prisoner Game - Donam el rol ADVANTATGE a la primera i DISADVANTATGE a las segona
                    if ADVANTAGE_DISADVANTAGE[i]=='A':
                        game_prisoner[i].rol2 = 'A'
                        game_prisoner[i].rol3 = 'D'
                        llista_prisoner_advantage2.append(game_prisoner[i])
                        llista_prisoner_disavantage3.append(game_prisoner[i])


                        if usuaris[i].is_robot:
                            game_prisoner[i].seleccio2 = random.choice(["C","D"])
                            game_prisoner[i].seleccio3 = random.choice(["C","D"])

                    # Prisoner Game - Donam el rol ADVANTATGE a la primera i DISADVANTATGE a la segona
                    else:
                        game_prisoner[i].rol2 = 'D'
                        game_prisoner[i].rol3 = 'A'

                        llista_prisoner_disavantage2.append(game_prisoner[i])
                        llista_prisoner_advantage3.append(game_prisoner[i])

                        if usuaris[i].is_robot:
                            game_prisoner[i].seleccio2 = random.choice(["C","D"])
                            game_prisoner[i].seleccio3 = random.choice(["C","D"])



                    # Prisoner Dilemma

                    game_prisoner[i].rol1 = 'E'

                    if usuaris[i].is_robot:
                        print 'is_robot'
                        game_prisoner[i].seleccio1 = random.choice(['C','D'])

                    llista_prisoner1.append(game_prisoner[i])

                    usuaris[i].save()

                #Fem les parelles per als jocs
                while llista_prisoner1:
                    rand1_prisoner = pop_random(llista_prisoner1)
                    rand2_prisoner = pop_random(llista_prisoner1)
                    rand1_prisoner.rival1 = rand2_prisoner.user
                    rand2_prisoner.rival1 = rand1_prisoner.user
                    rand1_prisoner.save()
                    rand2_prisoner.save()

                while llista_prisoner_advantage2:
                    rand1_prisoner = pop_random(llista_prisoner_advantage2)
                    rand2_prisoner = pop_random(llista_prisoner_disavantage2)
                    rand1_prisoner.rival2 = rand2_prisoner.user
                    rand2_prisoner.rival2 = rand1_prisoner.user
                    rand1_prisoner.save()
                    rand2_prisoner.save()

                while llista_prisoner_advantage3:
                    rand1_prisoner = pop_random(llista_prisoner_advantage3)
                    rand2_prisoner = pop_random(llista_prisoner_disavantage3)
                    rand1_prisoner.rival3 = rand2_prisoner.user
                    rand2_prisoner.rival3 = rand1_prisoner.user
                    rand1_prisoner.save()
                    rand2_prisoner.save()

                #Fem les parelles per als jocs TRUST

                while llista_trust_inversors1:
                    rand1_trust = pop_random(llista_trust_inversors1)
                    rand2_trust = pop_random(llista_trust_empresaris1)
                    rand1_trust.rival1 = rand2_trust.user
                    rand2_trust.rival1 = rand1_trust.user
                    rand1_trust.save()
                    rand2_trust.save()

                while llista_trust_inversors2:
                    rand1_trust = pop_random(llista_trust_inversors2)
                    rand2_trust = pop_random(llista_trust_empresaris2)
                    rand1_trust.rival2 = rand2_trust.user
                    rand2_trust.rival2 = rand1_trust.user
                    rand1_trust.save()
                    rand2_trust.save()

                #Fem les parelles per als jocs DICTATOR

                while llista_dictator_dictator1:
                    rand1_dictator = pop_random(llista_dictator_dictator1)
                    rand2_dictator = pop_random(llista_dictator_punisher1)
                    rand1_dictator.rival1 = rand2_dictator.user
                    rand2_dictator.rival1 = rand1_dictator.user
                    rand1_dictator.save()
                    rand2_dictator.save()

                while llista_dictator_dictator2:
                    rand1_dictator = pop_random(llista_dictator_dictator2)
                    rand2_dictator = pop_random(llista_dictator_punicher2)
                    rand1_dictator.rival2 = rand2_dictator.user
                    rand2_dictator.rival2 = rand1_dictator.user
                    rand1_dictator.save()
                    rand2_dictator.save()

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
                partida_activa.estat = "NO_JUGA" # Si no volem jugar al clima

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

        partida = Partida.objects.create(num_partida=npartida,
                                         data_creacio=timezone.now(),
                                         estat="REGISTRANT",
                                         classe=EXPERIMENT,
                                         guanyen_igualment = True if random.randint(0,9) == 9 else False,
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
              'diners_trust': u.diners_trust,
              'diners_prisoner': u.diners_prisoner,
              'diners_dictator': u.diners_dictator,
              'diners_total': u.diners_total,
              'vals': u.vals,
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


