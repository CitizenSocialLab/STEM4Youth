from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from game.models import User
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

    if user.partida.estat == "ACABADA" or user.partida.estat  == "ACABADA_MANUAL":
        return redirect('user.inici')


    #Mirem que la partida no estigui en marxa ja:
    if user.partida.estat == "JUGANT":
        date_now = timezone.now()
        date_start = user.partida.data_inicialitzacio
        temps_actual_joc = (date_now - date_start).total_seconds()

        #print "+++", date_now, date_start, temps_actual_joc, TEMPS_INICI_SEC
        if temps_actual_joc > TEMPS_INICI_SEC:
            return redirect('user.inici')


    #Si esta tot be passem a jugar amb els seguents parametres
    return render_to_response('game.html', {'user': request.session['user'],
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

    return render_to_response('tutorial.html', {'user': request.session['user'],
                                                'lang': request.session['lang'],
                                                'text': request.session['text'],
                                                'count':  6,
                                                'prefix': '/static/img/tutorial_',
                                                'provar_url': '/'+request.session['lang']+'/game/prova',
                                                'jugar_url': '/'+request.session['lang']+'/user/inici'})

