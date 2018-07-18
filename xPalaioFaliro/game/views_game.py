from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from game.models import User
from game.models import Partida
from game.vars import *

from game.views_user import user_exists_in_db
from django.utils import timezone

@csrf_exempt
def index(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('login')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except:
        return redirect('user.login')

    #Comprovar que l'usuari esta realment a dins d'una partida
    #I que aquesta partida no s'hagi acabat ja
    if not user.partida:
        return redirect('user.inici')

    if user.partida.status == "FINISHED" or user.partida.status  == "FINISHED_MANUALLY":
        return redirect('user.inici')


    #Mirem que la partida no estigui en marxa ja:
    if user.partida.status == "PLAYING":
        date_now = timezone.now()
        date_start = user.partida.date_start
        temps_actual_joc = (date_now - date_start).total_seconds()

        #print "+++", date_now, date_start, temps_actual_joc, TEMPS_INICI_SEC
        if temps_actual_joc > TEMPS_INICI_SEC:
            return redirect('user.inici')


    #Si esta tot be passem a jugar amb els seguents parametres
    return render_to_response('game.html', {'xAire': True if EXPERIMENT == 'xAire' else False,
                                            'Athens': True if EXPERIMENT == 'Athens' else False,
                                            'user': request.session['user'],
                                            'lang': request.session['lang'],
                                            'text': request.session['text'],})

@csrf_exempt
def tutorial(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('login')
    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('login')

    partida_activa = Partida.objects.filter(status="REGISTERING")
    if len(partida_activa) == 0:
        return redirect('game.tutorial_inici')

    else:
        partida_activa = partida_activa[0]
        return render_to_response('tutorial.html', {'user': request.session['user'],
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'count':  4,
                                                    'control_reward': partida_activa.control_reward,
                                                    'prefix': '/static/img/tutorial/base/tutorial_red/'+request.session['lang']+'/'+EXPERIMENT+'/tutorial_',
                                                    'provar_url': '/'+request.session['lang']+'/game/prova',
                                                    'jugar_url': '/'+request.session['lang']+'/user/inici',
                                                    'verification_url': '/'+request.session['lang']+'/user/verification'})

@csrf_exempt
def tutorial_inici(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('login')
    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('login')

    partida_activa = Partida.objects.filter(status="REGISTERING")
    if len(partida_activa) > 0:
        partida_activa = partida_activa[0]
        try:
            #Todo: Controlling number of users
            print 'usuaris registrat: ' + str(partida_activa.usuaris_registrats)
            if partida_activa.usuaris_registrats < NUM_PLAYERS:
                # If the user not have game
                if not user.partida:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()
                    print "Partida", partida_activa.num_partida,"- usuaris registrats:", partida_activa.usuaris_registrats
                    user.partida = partida_activa
                    user.date_tutorial = timezone.now()
                    user.status = "TUTORIAL"
                    user.save()
            else:
                return render_to_response('tutorial_inici.html', {'user': user,
                             'lang': request.session['lang'],
                             'text': request.session['text'],
                             'error_partida':True})

            #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
            return redirect('game.tutorial')
        except:
            #Si hi ha hagut error tornem a la pagina
            return redirect('game.tutorial_inici')

    return render_to_response('tutorial_inici.html', {'user': user,
                             'lang': request.session['lang'],
                             'text': request.session['text'],
                             'error_partida':True})

@csrf_exempt
def logos(request, **kwargs):
    return render_to_response('logos.html',
                              {'lang': request.session['lang'],
                               'text': request.session['text']})

