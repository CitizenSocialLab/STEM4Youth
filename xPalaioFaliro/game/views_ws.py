from django.views.decorators.csrf import csrf_exempt

from game.models import *
from game.vars import *

import math


import datetime
from django.utils import timezone

import json
from django.http import HttpResponse


import random
random.seed(datetime.datetime.now())


@csrf_exempt
def demanar_dades(request, **kwargs):
    user_id = kwargs.get('user_id', None)

    response_data={}
    jugant = "false"

    user = None
    try:
        # partida que juga aquest usuari
        user = User.objects.get(id=user_id)
    except:
        print "Usuari "+str(user_id)+" no existeix"

    # status de la partida actual
    if user.partida.status == "PLAYING":
        altres_users = user.partida.user_set.all().exclude(id=user_id).order_by('num_jugador')

        jugant = "true"

        date_now = timezone.now()
        #print(date_now)
        date_start = user.partida.date_start+datetime.timedelta(0, TEMPS_INICI_SEC)
        #print(date_start)

        # control resta
        temps = (date_start - date_now).total_seconds()
        #print temps*1000
        if temps > 0:
            response_data["temps_inici"] = temps*1000
            response_data["partida_en_joc"] = False
        else:
            response_data["temps_inici"] = 0
            response_data["partida_en_joc"] = True

        response_data["temps_ronda"] = TEMPS_RONDA
        response_data["temps_espera"] = TEMPS_ESPERA

        response_data["total_rondes"] = NUM_ROUNDS
        response_data["numero_ronda"] = 1
        response_data["diners_inici_ronda"] = user.endowment_current
        response_data["num_jugador"] = user.num_jugador
        response_data["altres_jugadors"] = [(u.num_jugador, u.endowment_initial) for u in altres_users]
        response_data["threshold"] = THRESHOLD
        response_data["control_wealth"] = user.partida.control_wealth
        response_data["residence"] = user.residence
        response_data["residence_name"] = Pollution.objects.get(tag=user.residence).district
        response_data["NO2"] = Pollution.objects.get(tag=user.residence).NO2
        response_data["school"] = Pollution.objects.get(tag=user.residence).school
        response_data["num_schools"] = Pollution.objects.get(tag=user.residence).num_schools
        response_data["quality"] = Pollution.objects.get(tag=user.residence).quality

        response_data["experiment"] = EXPERIMENT


    response_data["jugant"] = jugant
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def enviar_accio(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    num_ronda = kwargs.get('ronda_id', None)
    result = kwargs.get('result', None)

    # Update de les dades. Falta controlar si hi ha errors
    userronda = UserRonda.objects.filter(user_id=user_id, ronda__num_ronda=num_ronda).order_by('-id')

    if len(userronda) > 0:
        if userronda[0].seleccio is None:
            userronda[0].ha_seleccionat = True
            userronda[0].seleccio = int(result)
            userronda[0].temps_seleccio = timezone.now()
            userronda[0].save()

            userronda[0].user.num_seleccions = userronda[0].user.num_seleccions + 1
            userronda[0].user.save()

        response_data = {"saved":"ok"}
    else:
        response_data = {"saved":"error"}

    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def calculs_ronda(partida_activa, num_ronda):

    # The game is FINISHED or FINISHED_MANUALLY
    if partida_activa.status == "FINISHED" or partida_activa.status == "FINISHED_MANUALLY":
        return

    temps_actual = timezone.now()

    # Closing current round (not a previous or posterior)
    if num_ronda != partida_activa.ronda_actual:
        return

    print "FINISHING ROUND:", num_ronda

    partida_activa.ronda_actual = partida_activa.ronda_actual + 1
    partida_activa.data_fi_ronda = temps_actual + datetime.timedelta(seconds=TEMPS_ESPERA_SEC+TEMPS_RONDA_SEC)
    partida_activa.save()

    ronda_acabada = partida_activa.ronda_set.get(num_ronda=partida_activa.ronda_actual-1)

    bucket_final_ronda = 0

    # Calculate the round results
    for ur in ronda_acabada.userronda_set.all():
        # No user's selection - random selection
        if not ur.ha_seleccionat:
            ur.user.bots = ur.user.bots + 1
            if ur.ronda.num_ronda == 1:
                ur.seleccio = 2
            else:
                ur_anterior = UserRonda.objects.filter(user=ur.user, ronda__num_ronda=ur.ronda.num_ronda-1).order_by('-id')[0]
                tmp = random.randint(0,5)
                if tmp==4:  # 20% probability to increase
                    ur.seleccio = ur_anterior.seleccio + 2
                elif tmp==3: # 20% probability to decrement
                    ur.seleccio = ur_anterior.seleccio - 2
                else:
                    ur.seleccio = ur_anterior.seleccio

            if ur.seleccio < 0: ur.seleccio = 0
            if ur.seleccio > 4: ur.seleccio = 4
            ur.save()

        # Control the selection is in the range
        if ur.user.endowment_current - ur.seleccio < 0:
            ur.seleccio = ur.user.endowment_current
            ur.save()

        # Total contributed
        gastat = 0
        for userronda in UserRonda.objects.filter(user_id=ur.user, ronda__partida__id=partida_activa.id , seleccio__isnull=False):
            gastat = gastat + userronda.seleccio

        ur.user.endowment_current = ur.user.endowment_initial - gastat
        ur.user.status = "PLAYING"
        ur.user.save()

        bucket_final_ronda = bucket_final_ronda + gastat

    ronda_acabada.bucket_final_ronda = THRESHOLD - bucket_final_ronda
    ronda_acabada.temps_final_ronda = temps_actual
    ronda_acabada.calculada = True
    ronda_acabada.save()

    # Check if the game is finished
    if partida_activa.ronda_actual > partida_activa.num_rondes:
        # Check if the contributions are greater than the goal
        if (ronda_acabada.bucket_final_ronda <= 0):
            partida_activa.objectiu_aconseguit = True

        partida_activa.status = "FINISHED"
        partida_activa.date_end = timezone.now()
        partida_activa.save()

    # Next round
    else:

        ronda_seguent = partida_activa.ronda_set.get(num_ronda=partida_activa.ronda_actual)
        ronda_seguent.bucket_inici_ronda = THRESHOLD - bucket_final_ronda
        ronda_seguent.temps_inici_ronda = temps_actual + datetime.timedelta(seconds=TEMPS_ESPERA_SEC)

        ronda_seguent.save()

@csrf_exempt
def demanar_resultat(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    num_ronda = kwargs.get('ronda_id', None)

    # The participant is playing?
    user_ronda = UserRonda.objects.filter(user_id=user_id, ronda__num_ronda=num_ronda).order_by('-id')
    if len(user_ronda) == 0:
        # The participant is not playing
        return HttpResponse(json.dumps({"correcte": False}), content_type="application/json")

    user_ronda = user_ronda[0]
    user = user_ronda.user
    partida_activa = user.partida

    # Current round is equal or lower than the participant's round
    # Is changing to the next round?
    if partida_activa.ronda_actual == user_ronda.ronda.num_ronda:

        # Refresh data of the current round
        temps_restant = (partida_activa.data_fi_ronda - timezone.now()).total_seconds()

        # Calculate the results of the round
        if temps_restant <= 0:
            calculs_ronda(partida_activa, partida_activa.ronda_actual)

        # All the player have contribute
        else:
            num_players = User.objects.filter(partida=partida_activa, is_robot=False).count()
            num_respostes = UserRonda.objects.filter(seleccio__isnull=False, ronda__partida = partida_activa, ronda__num_ronda=num_ronda).count()

            if num_players == num_respostes and int(partida_activa.ronda_actual) == int(num_ronda):
                calculs_ronda(partida_activa, partida_activa.ronda_actual)


    # If game is not PLAYING return the data to the participants
    if partida_activa.status != "PLAYING":
        return HttpResponse(json.dumps({"correcte": True, "jugant": False}), content_type="application/json")

    # If round is finished
    if user_ronda.ronda.num_ronda < partida_activa.ronda_actual and user_ronda.ronda.calculada:

        game_users = User.objects.filter(partida_id=partida_activa.id).order_by('num_jugador')

        user = user_ronda.user
        response_data = {
            "correcte": True, #Per confirmar que les dades son correctes
            "ronda_acabada": True,
            "jugant": True if partida_activa.status == "PLAYING" else False,
            "has_elegit": user_ronda.ha_seleccionat,
            "contribucio": user_ronda.seleccio,
            "endowment_initial": user_ronda.user.endowment_initial,
            "id_user": user_ronda.user.id,
            "ids": [gu.id for gu in game_users],
            "contribucions_ronda": [ur.seleccio for ur in user_ronda.ronda.userronda_set.all().order_by('user__num_jugador')],
            "ha_seleccionat": [ur.ha_seleccionat for ur in user_ronda.ronda.userronda_set.all().order_by('user__num_jugador')],
            "contribucions_ronda_aggr": user_ronda.ronda.bucket_inici_ronda - user_ronda.ronda.bucket_final_ronda,
            "contribucions_partida": THRESHOLD - user_ronda.ronda.bucket_final_ronda,
            "numero_ronda": partida_activa.ronda_actual,
            "diners_inici_ronda": user.endowment_current,
            "endowment_current_all": [ur.user.endowment_current for ur in user_ronda.ronda.userronda_set.all().order_by('user__num_jugador')],
            "endowment_initial_all": [ur.user.endowment_initial for ur in user_ronda.ronda.userronda_set.all().order_by('user__num_jugador')],
            "temps_restant": (partida_activa.data_fi_ronda - timezone.now()).total_seconds() - TEMPS_RONDA_SEC,
            "temps_canvi_imatge": TEMPS_ESPERA_SEC,
            "threshold": THRESHOLD,
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"ronda_acabada": False}), content_type="application/json")

#################################
### WEBSERVICES ADMINISTRACIO ###
#################################

@csrf_exempt
def usuaris_registrats(request, **kwargs):
    response_data = {}

    partida_activa = Partida.objects.filter(status="REGISTERING")
    if len(partida_activa) > 0:
        response_data['registering'] = True

        partida_activa = partida_activa[0]

        all_users = []

        for usuari in User.objects.filter(partida=partida_activa):
            if usuari.date_tutorial is not None: date = usuari.date_tutorial.strftime("%a,  %d/%m/%Y - %H:%M:%S")
            if usuari.date_register is not None: date = usuari.date_register.strftime("%a,  %d/%m/%Y - %H:%M:%S")
            data_users = {"id_user": usuari.id,
                          "id_game": usuari.partida.id,
                           "nom": usuari.nickname,
                           "status": usuari.status,
                           "pollution": str(usuari.pollution.NO2) +' ('+ str(usuari.pollution.level)+' level)' if usuari.pollution else '-',
                           "date": date}

            all_users.append(data_users)
        response_data['usuaris'] = all_users

    else:
        response_data['registering'] = False

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def status_partida(request, **kwargs):
    response_data = {'partides': []}

    for partida in Partida.objects.filter(status="PLAYING"):

        #Info de la partida
        users = User.objects.filter(partida__num_partida = partida.num_partida)

        data = {'num_partida': partida.num_partida,
                'date_creation': partida.date_creation.strftime("%a,  %d/%m/%Y - %H:%M:%S"),
                'data_inici': partida.date_start.strftime("%a,  %d/%m/%Y - %H:%M:%S"),
                'always_win': partida.always_win,
                }

        # Mirem si hem d'de tancar la ronda actual
        temps_restant = (partida.data_fi_ronda - timezone.now()).total_seconds()
        if temps_restant <= 0 and partida.ronda_actual <= partida.num_rondes:
            calculs_ronda(partida, partida.ronda_actual)

        ronda_data = []
        for i in range(1,partida.ronda_actual+1):
            num_players = User.objects.filter(partida=partida).count()

            num_respostes = UserRonda.objects.filter(seleccio__isnull=False, ronda__partida = partida, ronda__num_ronda=i).count()
            ronda_data.append({"ronda": i, "num_respostes": num_respostes, "num_jugadors": num_players})

        data["ronda_data"] = ronda_data

        if partida.ronda_actual > partida.num_rondes:
            data['status'] = "Se han jugado todas las rondas"

        elif partida.ronda_actual == 1:
            if temps_restant > TEMPS_RONDA_SEC:
                data['status'] = "Partida empieza en: "+str(int(round(temps_restant-TEMPS_RONDA_SEC)))+"sec."

            else:
                data['status'] = "Ronda 1 jugando: <BR /> Quedan "+str(int(math.ceil(temps_restant)))+ " secs"

        else:
            if temps_restant > TEMPS_RONDA_SEC:
                data['status'] = "Ronda "+str(partida.ronda_actual-1)+" resultados: <BR /> Quedan "\
                                         +str(int(round(temps_restant-TEMPS_RONDA_SEC)))+" secs"

            else :
                data['status'] = "Ronda "+str(partida.ronda_actual)+" jugando: <BR /> Quedan "\
                                         +str(int(math.ceil(temps_restant)))+ " secs"

        response_data['partides'].append(data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def tancar_ronda(request, **kwargs):

    response_data = {}
    num_partida = kwargs.get('num_partida', None)
    partida = Partida.objects.get(num_partida=num_partida)
    calculs_ronda(partida, partida.ronda_actual)

    response_data["correcte"] = False
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def tancar_partida(request, **kwargs):

    response_data = {}
    num_partida = kwargs.get('num_partida', None)
    partida = Partida.objects.get(num_partida=num_partida)
    if partida.status == "PLAYING":
        partida.status = "FINISHED_MANUALLY"
        partida.date_end = timezone.now()
        partida.save()

    response_data["correcte"] = False
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def llistat_partides(request, **kwargs):

    response_data = {}

    all_partides = []
    for partida in Partida.objects.filter().order_by('-id')[:15]:

        users = User.objects.filter(partida__num_partida = partida.num_partida)
        #print(partida.date_end)
        data_partida = {"num_partida": partida.num_partida,
                        "guanys": [up.tickets for up in users],
                        "always_win": partida.always_win,
                        "objectiu_aconseguit": partida.objectiu_aconseguit,
                        "date_creation": partida.date_creation.strftime("%a, %H:%M:%S"),
                        "wealth": partida.control_wealth,
                        "reward": partida.control_reward,
                        "date_end": partida.date_end.strftime("%a, %H:%M:%S") if partida.date_end else '-',
                        "status": partida.status
        }

        all_partides.append(data_partida)

    response_data["partida"] = all_partides

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def stats_partida(request, **kwargs):

    response_data = {}

    all_partides = []

    games = [p for p in Partida.objects.filter(status="FINISHED").filter(experiment="xAire").order_by('-id')]
    participants = User.objects.filter(acabat=1)

    response_data["total_games"] = len(games)

    response_data["total_games_economic"] = len([g for g in games if g.control_reward == "ECONOMIC"])
    response_data["total_games_economic_equal"] = len([g for g in games if g.control_reward == "ECONOMIC" and g.control_wealth == "EQUAL"])
    response_data["total_games_economic_unequal_low"] = len([g for g in games if g.control_reward == "ECONOMIC" and g.control_wealth == "UNEQUAL-L"])
    response_data["total_games_economic_unequal_high"] = len([g for g in games if g.control_reward == "ECONOMIC" and g.control_wealth == "UNEQUAL-H"])

    response_data["total_games_social"] = len([g for g in games if g.control_reward == "SOCIAL"])
    response_data["total_games_social_equal"] = len([g for g in games if g.control_reward == "SOCIAL" and g.control_wealth == "EQUAL"])
    response_data["total_games_social_unequal_low"] = len([g for g in games if g.control_reward == "SOCIAL" and g.control_wealth == "UNEQUAL-L"])
    response_data["total_games_social_unequal_high"] = len([g for g in games if g.control_reward == "SOCIAL" and g.control_wealth == "UNEQUAL-H"])

    response_data["total_games_achieved"] = len([g for g in games if g.objectiu_aconseguit])
    response_data["total_participants"] = len(participants)
    response_data["tickets_laie"] = sum([(p.tickets) for p in participants])

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def delete_user(request, **kwargs):

    response_data = {}
    id_user = kwargs.get('id_user', None)

    user = User.objects.get(id=id_user)

    # NO_VALID and NO_GAME
    user.partida.usuaris_registrats -= 1
    user.partida.save()
    user.status = 'NO_VALID'
    user.partida = None
    user.save()

    response_data["correcte"] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def stats_partida_detail(request, **kwargs):

    num_partida = kwargs.get('num_partida', None)

    partida = Partida.objects.filter(num_partida=num_partida)[0]
    users_partida = User.objects.filter(partida_id=partida.id).order_by('num_jugador')

    if partida.date_end is None: dc = '-'
    else: dc = partida.date_end.strftime("%a,  %d/%m/%Y - %H:%M:%S")

    response_data = {
        "num_partida": num_partida,
        "num_players": NUM_PLAYERS,
        "threshold": THRESHOLD,
        "status_partida": partida.status,
        "always_win": partida.always_win,
        "control_reward": partida.control_reward,
        "control_wealth": partida.control_wealth,
        "factor_return": FACTOR_RETURN,
        "guanys": [up.winnings_public_goods for up in users_partida],
        "edad": [up.age_range for up in users_partida],
        "date_creacio": partida.date_creation.strftime("%a,  %d/%m/%Y - %H:%M:%S"),
        "date_inici": partida.date_start.strftime("%a,  %d/%m/%Y - %H:%M:%S"),
        "date_final": dc,
        "user_ids": [up.id for up in users_partida],
        "nicknames": [up.nickname for up in users_partida],
        "endowment_initial": [up.endowment_initial for up in users_partida],
        "diners_contribuits": [up.endowment_initial - up.endowment_current for up in users_partida],
        "bots": [up.bots for up in users_partida],
        "winnings_public_goods": [up.winnings_public_goods for up in users_partida],
        "savings_public_goods": [up.savings_public_goods for up in users_partida],
        "coins_total": [up.coins_total for up in users_partida],
        "tickets": [up.tickets for up in users_partida],
        "wealth": partida.control_wealth,
    }

    # Rondes de tots els users de la partida
    user_ronda_seleccio = []
    robot_seleccio = []
    for up in users_partida:
        user_ronda =  UserRonda.objects.filter(user_id=up.id).order_by('ronda_id')
        user_ronda_seleccio.append([ur.seleccio for ur in user_ronda])
        robot_seleccio.append([ur.ha_seleccionat for ur in user_ronda])
    response_data["rondes"] = user_ronda_seleccio
    response_data["robot"] = robot_seleccio

    return HttpResponse(json.dumps(response_data), content_type="application/json")

