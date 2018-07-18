from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import *

from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone

from game.models import *
from game.vars import *

import math

def user_exists_in_db(user):
    try:
        User.objects.get(pk=user.id)
        return True
    except:
        return False


def index(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        print user.email
        return redirect('user.registre')

    return redirect('user.nickname')





#########################################################################################################
#########################################################################################################
# Pantalla 1: Escollir un nickname
class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=300)

@csrf_exempt
def nickname(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        #print user.useremail_set.all()
        return redirect('user.registre')

    #Borrem el nickanme de la sessio
    if 'nickname' in request.session:
        del request.session['nickname']

    if request.method != 'POST':
        return render_to_response('nickname.html', {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))
    else:
        form = NicknameForm(request.POST)
        nick = form['nickname'].value()

        if not nick or len(nick) == 0:
            return render_to_response('nickname.html', {'lang': request.session['lang'], 'text': request.session['text']},
                                      context_instance=RequestContext(request))

        if len(nick) > 20:
            return render_to_response('nickname.html',
                                      {'nickname_error': False, 'nickname_error2': True, 'nickname': nick,
                                       'lang': request.session['lang'], 'text': request.session['text']},
                                      context_instance=RequestContext(request))

        #Si l'usuari ja existeix enviar-lo a la pantalla d'inici
        try:
            user = User.objects.get(nickname=nick)
            request.session['user'] = user
            request.session['nickname'] = nick
            return redirect('user.registre')

        #Sino enviar-lo a l'enquesta
        except ObjectDoesNotExist:
            request.session['user'] = None
            request.session['nickname'] = nick

            return redirect('user.enquesta1')






#########################################################################################################
#########################################################################################################
# Pantalla 5: Enquesta 1
class SigninForm1(forms.Form):
    genere = forms.CharField(max_length=100)
    rang_edat = forms.CharField(max_length=100)
    residencia = forms.CharField(max_length=100)
    codi_postal = forms.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(99999)])
    origen = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=100)


@csrf_exempt
def enquesta1(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        # print user.useremail_set.all()
        return redirect('user.registre')

    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta1.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm1(request.POST)
    genere = form['genere'].value()
    rang_edat = form['rang_edat'].value()
    residencia = form['residencia'].value()
    codi_postal = form['codi_postal'].value()
    origen = form['origen'].value()
    pais = form['pais'].value()

    print(pais)

    if not form.is_valid():
        return render_to_response('enquesta1.html', {
            'genere': genere,
            'genere_danger': genere is None or len(genere) == 0,
            'genere_0_checked': 'bx-option-selected' if genere == 'M' else '',
            'genere_1_checked': 'bx-option-selected' if genere == 'F' else '',

            'rang_edat': rang_edat,
            'rang_edat_danger': rang_edat is None or len(rang_edat) == 0,
            'rang_edat_1_checked': 'bx-option-selected' if rang_edat == 'r1' else '',
            'rang_edat_2_checked': 'bx-option-selected' if rang_edat == 'r2' else '',
            'rang_edat_3_checked': 'bx-option-selected' if rang_edat == 'r3' else '',
            'rang_edat_4_checked': 'bx-option-selected' if rang_edat == 'r4' else '',
            'rang_edat_5_checked': 'bx-option-selected' if rang_edat == 'r5' else '',
            'rang_edat_6_checked': 'bx-option-selected' if rang_edat == 'r6' else '',
            'rang_edat_7_checked': 'bx-option-selected' if rang_edat == 'r7' else '',
            'rang_edat_8_checked': 'bx-option-selected' if rang_edat == 'r8' else '',

            'residencia': residencia,
            'residencia_danger': residencia is None or len(residencia) == 0,
            'residencia_0_checked': 'bx-option-selected' if residencia == 'r1' else '',
            'residencia_1_checked': 'bx-option-selected' if residencia == 'r2' else '',

            'codi_postal': codi_postal,
            'codi_postal_danger': codi_postal is None or len(codi_postal) == 0 or not codi_postal.isdigit()
                                  or int(codi_postal) < 0 or int(codi_postal) >= 99999,

            'origen': origen,
            'origen_danger': origen is None or len(origen) == 0,
            'origen_0_checked': 'bx-option-selected' if origen == 'r1' else '',
            'origen_1_checked': 'bx-option-selected' if origen == 'r2' else '',

            'pais': pais,
            'pais_danger': pais is None or len(pais) == 0,

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['genere'] = genere
        request.session['rang_edat'] = rang_edat
        request.session['residencia'] = residencia
        request.session['codi_postal'] = codi_postal
        request.session['origen'] = origen
        request.session['pais'] = pais


        return redirect('user.enquesta2')


#########################################################################################################
#########################################################################################################
# Pantalla 6: Enquesta part 2
class SigninForm2(forms.Form):
    nivell_estudis = forms.CharField(max_length=100)
    estat_civil = forms.CharField(max_length=100)
    situacio_laboral = forms.CharField(max_length=100)

@csrf_exempt
def enquesta2(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        # print user.useremail_set.all()
        return redirect('user.registre')

    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta2.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm2(request.POST)
    print(form)
    situacio_laboral = form['situacio_laboral'].value()
    nivell_estudis = form['nivell_estudis'].value()
    estat_civil = form['estat_civil'].value()

    if not form.is_valid():
        return render_to_response('enquesta2.html', {

            'situacio_laboral': situacio_laboral,
            'situacio_laboral_danger': situacio_laboral is None or len(situacio_laboral) == 0,
            'situacio_laboral_0_checked': 'bx-option-selected' if situacio_laboral == 'r1' else '',
            'situacio_laboral_1_checked': 'bx-option-selected' if situacio_laboral == 'r2' else '',
            'situacio_laboral_2_checked': 'bx-option-selected' if situacio_laboral == 'r3' else '',

            'estat_civil': estat_civil,
            'estat_civil_danger': estat_civil is None or len(estat_civil) == 0,
            'estat_civil_0_checked': 'bx-option-selected' if estat_civil == 'r1' else '',
            'estat_civil_1_checked': 'bx-option-selected' if estat_civil == 'r2' else '',
            'estat_civil_2_checked': 'bx-option-selected' if estat_civil == 'r3' else '',
            'estat_civil_3_checked': 'bx-option-selected' if estat_civil == 'r4' else '',
            'estat_civil_4_checked': 'bx-option-selected' if estat_civil == 'r5' else '',
            'estat_civil_5_checked': 'bx-option-selected' if estat_civil == 'r6' else '',

            'nivell_estudis': nivell_estudis,
            'nivell_estudis_danger': nivell_estudis is None or len(nivell_estudis) == 0,
            'nivell_estudis_0_checked': 'bx-option-selected' if nivell_estudis == 'r1' else '',
            'nivell_estudis_1_checked': 'bx-option-selected' if nivell_estudis == 'r2' else '',
            'nivell_estudis_2_checked': 'bx-option-selected' if nivell_estudis == 'r3' else '',
            'nivell_estudis_3_checked': 'bx-option-selected' if nivell_estudis == 'r4' else '',
            'nivell_estudis_4_checked': 'bx-option-selected' if nivell_estudis == 'r5' else '',
            'nivell_estudis_5_checked': 'bx-option-selected' if nivell_estudis == 'r6' else '',
            'nivell_estudis_6_checked': 'bx-option-selected' if nivell_estudis == 'r7' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))


    else:
        request.session['situacio_laboral'] = situacio_laboral
        request.session['estat_civil'] = estat_civil
        request.session['nivell_estudis'] = nivell_estudis

        user = User()
        user.nickname = request.session['nickname']
        user.genere = request.session['genere']
        user.rang_edat = request.session['rang_edat']
        user.residencia = request.session['residencia']
        user.situacio_laboral = request.session['situacio_laboral']
        user.nivell_estudis = request.session['nivell_estudis']
        user.estat_civil = request.session['estat_civil']
        user.origen = request.session['origen']
        user.codi_postal = request.session['codi_postal']
        user.pais = request.session['pais']

        user.diners_inicials = 0
        user.diners_actuals = 0

        #user.source = "WEB"
        user.data_creacio = timezone.now()

        user.save()

        request.session['user'] = user

        #return redirect('game.tutorial')
        return redirect('user.registre')


#########################################################################################################
#########################################################################################################
# Enquesta Final Intro

@csrf_exempt
def enquestafinalintro(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('user.login')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    return render_to_response('enquestafinalintro.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text']},
                                  context_instance=RequestContext(request))

#########################################################################################################
#########################################################################################################
# Enquesta Final 1
class SigninFormFinal1(forms.Form):
    pr1 = forms.CharField(max_length=100)
    pr2 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal1(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('user.login')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal1.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal1(request.POST)
    enquesta_final_pr1 = form['pr1'].value()
    enquesta_final_pr2 = form['pr2'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal1.html', {
            'pr1': enquesta_final_pr1,
            'pr1_danger': enquesta_final_pr1 is None or len(enquesta_final_pr1) == 0,
            'pr1_1_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r1' else '',
            'pr1_2_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r2' else '',
            'pr1_3_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r3' else '',
            'pr1_4_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r4' else '',
            'pr1_5_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r5' else '',

            'pr2': enquesta_final_pr2,
            'pr2_danger': enquesta_final_pr1 is None or len(enquesta_final_pr2) == 0,
            'pr2_1_checked': 'bx-option-selected' if enquesta_final_pr2 == 'r1' else '',
            'pr2_2_checked': 'bx-option-selected' if enquesta_final_pr2 == 'r2' else '',
            'pr2_3_checked': 'bx-option-selected' if enquesta_final_pr2 == 'r3' else '',
            'pr2_4_checked': 'bx-option-selected' if enquesta_final_pr2 == 'r4' else '',
            'pr2_5_checked': 'bx-option-selected' if enquesta_final_pr2 == 'r5' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr1'] = enquesta_final_pr1
        request.session['pr2'] = enquesta_final_pr2

        return redirect('user.enquestafinal2')

#########################################################################################################
#########################################################################################################
# Enquesta Final 2
class SigninFormFinal2(forms.Form):
    pr3 = forms.CharField(max_length=100)
    pr4 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal2(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('user.login')




    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal2.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal2(request.POST)
    enquesta_final_pr3 = form['pr3'].value()
    enquesta_final_pr4 = form['pr4'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal2.html', {
            'pr3': enquesta_final_pr3,
            'pr3_danger': enquesta_final_pr3 is None or len(enquesta_final_pr3) == 0,
            'pr3_1_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r1' else '',
            'pr3_2_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r2' else '',
            'pr3_3_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r3' else '',
            'pr3_4_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r4' else '',
            'pr3_5_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r5' else '',

            'pr4': enquesta_final_pr4,
            'pr4_danger': enquesta_final_pr4 is None or len(enquesta_final_pr4) == 0,
            'pr4_1_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r1' else '',
            'pr4_2_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r2' else '',
            'pr4_3_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r3' else '',
            'pr4_4_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r4' else '',
            'pr4_5_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r5' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr3'] = enquesta_final_pr3
        request.session['pr4'] = enquesta_final_pr4

        return redirect('user.enquestafinal3')

#########################################################################################################
#########################################################################################################
# Enquesta Final 3
class SigninFormFinal3(forms.Form):
    pr5 = forms.CharField(max_length=100)
    pr6 = forms.CharField(max_length=100)


@csrf_exempt
def enquestafinal3(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('user.login')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal3.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal3(request.POST)
    enquesta_final_pr5 = form['pr5'].value()
    enquesta_final_pr6 = form['pr6'].value()

    if not form.is_valid():
        return render_to_response('enquestafinal3.html', {
            'pr5': enquesta_final_pr5,
            'pr5_danger': enquesta_final_pr5 is None or len(enquesta_final_pr5) == 0,
            'pr5_1_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r1' else '',
            'pr5_2_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r2' else '',
            'pr5_3_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r3' else '',
            'pr5_4_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r4' else '',
            'pr5_5_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r5' else '',

            'pr6': enquesta_final_pr6,
            'pr6_danger': enquesta_final_pr6 is None or len(enquesta_final_pr6) == 0,
            'pr6_1_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r1' else '',
            'pr6_2_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r2' else '',
            'pr6_3_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r3' else '',
            'pr6_4_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r4' else '',
            'pr6_5_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r5' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr5'] = enquesta_final_pr5
        request.session['pr6'] = enquesta_final_pr6

        return redirect('user.enquestafinal4')


#########################################################################################################
#########################################################################################################
# Enquesta Final 3
class SigninFormFinal4(forms.Form):
    pr7 = forms.CharField(max_length=100)
    pr8 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal4(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.login')

    user = request.session['user']
    if not user_exists_in_db(user):
        del request.session['user']
        return redirect('user.login')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal4.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal4(request.POST)
    enquesta_final_pr7 = form['pr7'].value()
    enquesta_final_pr8 = form['pr8'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal4.html', {
            'pr7': enquesta_final_pr7,
            'pr7_danger': enquesta_final_pr7 is None or len(enquesta_final_pr7) == 0,
            'pr7_1_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r1' else '',
            'pr7_2_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r2' else '',
            'pr7_3_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r3' else '',

            'pr8': enquesta_final_pr8,
            'pr8_danger': enquesta_final_pr8 is None or len(enquesta_final_pr8) == 0,
            'pr8_1_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r1' else '',
            'pr8_2_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r2' else '',
            'pr8_3_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r3' else '',
            'pr8_4_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r4' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr7'] = enquesta_final_pr7
        request.session['pr8'] = enquesta_final_pr8

        user = User.objects.get(id=request.session['user'].id)

        user.enquesta_final_pr1 = request.session['pr1']
        user.enquesta_final_pr2 = request.session['pr2']
        user.enquesta_final_pr3 = request.session['pr3']
        user.enquesta_final_pr4 = request.session['pr4']
        user.enquesta_final_pr5 = request.session['pr5']
        user.enquesta_final_pr6 = request.session['pr6']
        user.enquesta_final_pr7 = request.session['pr7']
        user.enquesta_final_pr8 = request.session['pr8']

        user.acabat = True
        user.data_finalitzacio = timezone.now()

        user.save()

        return redirect('user.final_joc')

#########################################################################################################
#########################################################################################################
@csrf_exempt
def logout(request, **kwargs):
    if 'user' in request.session and request.session['user'] is not None:
        del request.session['user']
    return redirect('index')


#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

#Pantalla 2:Seleccio de l'experiment si ja hi ha un usuari a la sessio
@csrf_exempt
def inici(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    if user.data_finalitzacio:
        return redirect('user.final_joc')

    # si l'usuari no te cap partida assignada
    if not user.partida:
        #Mirem si ens estan demanant d'entrar a partida o encara no
        if request.method != 'POST':
            return render_to_response('inici.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False},
                                      context_instance=RequestContext(request))

        # Si demanem entrar a partida, primer mirem si n'hi ha una d'activa
        partida_activa = Partida.objects.filter(estat="REGISTRANT")
        if len(partida_activa) > 0:
            # Si es aixi registrem a l'usuari
            partida_activa = partida_activa[0]
            #print partida_activa.num_partida

            try:
                #Controlem que nomes hi hagi 6 usuaris a la partida!!
                if partida_activa.usuaris_registrats < 6:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()
                    print "Partida", partida_activa.num_partida,"// usuaris registrats:", partida_activa.usuaris_registrats

                    user.partida = partida_activa
                    user.data_registre = timezone.now()
                    user.save()
                else:
                    return redirect('user.inici')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('game.index')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.inici')


        return render_to_response('inici.html', {'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'error_partida':True},
                                  context_instance=RequestContext(request))

    # Si l'usuari te partida assignada
    else:
        #Si l'usuari ja te una partida assignada i aquesta encara esta registrant
        if user.partida and user.partida.estat == "REGISTRANT":
            return redirect('game.index')


        #Si l'usuari ja te una partida assignada i aquesta no ha comensat a jugar
        if user.partida and user.partida.estat == "JUGANT":
            date_now = timezone.now()
            date_start = user.partida.data_inicialitzacio
            temps_actual_joc = (date_now - date_start).total_seconds()

            #print date_now, date_start, temps_actual_joc, TEMPS_INICI_SEC
            if temps_actual_joc < TEMPS_INICI_SEC:
                return redirect('game.index')

            else :
                 #return redirect('game.index')
                return redirect('user.inici')


        #Si la partida on ha participat l'usuari ja esta acabada, l'envio als resultats
        if user.partida and (user.partida.estat == "ACABADA" or user.partida.estat == "ACABADA_MANUAL"):
            return redirect('user.resultats_clima')

        return redirect('user.inici')

#####################################################################################################
########################################### REGISTRE ################################################
#####################################################################################################

@csrf_exempt
def registre(request, **kwargs):

    print request.session['lang']
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    #if user.data_finalitzacio:
    #    return redirect('user.final_joc')

    # si l'usuari no te cap partida assignada
    print 'user partida: '+str(user.partida)
    if not user.partida:
        #Mirem si ens estan demanant d'entrar a partida o encara no
        if request.method != 'POST':
            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'waiting':0},
                                      context_instance=RequestContext(request))

        # Si demanem entrar a partida, primer mirem si n'hi ha una d'activa
        partida_activa = Partida.objects.filter(estat="REGISTRANT")
        print 'partida activa: '+ str(partida_activa)
        if len(partida_activa) > 0:
            # Si es aixi registrem a l'usuari
            partida_activa = partida_activa[0]
            print partida_activa.num_partida

            try:
                #Controlem que nomes hi hagi 6 usuaris a la partida!!
                if partida_activa.usuaris_registrats < 6:
                   partida_activa.usuaris_registrats += 1
                   partida_activa.save()
                   print "Partida", partida_activa.num_partida,"// usuaris registrats:", partida_activa.usuaris_registrats

                   user.partida = partida_activa
                   user.data_registre = timezone.now()
                   user.save()
                else:
                   return redirect('user.registre')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('user.registre')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.registre')


        return render_to_response('registre.html', {'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'error_partida':True,
                                                 'waiting':0},
                                  context_instance=RequestContext(request))

    else:
        # En caso de que la partida de clima este acabada, vamos a los resultados
        if user.partida and (user.partida.estat == "ACABADA" or user.partida.estat == "ACABADA_MANUAL"):
            return redirect('user.resultats_clima')

        if user.partida and (user.partida.estat == "NO_JUGA"):
            #ToDo: Primer Joc al que Jugam

            #return redirect('user.joc_inversor1')
            return redirect('user.joc_dictator1')
            #return redirect('user.joc_prisoner1')


        return render_to_response('registre.html', {'user': user,
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'error_partida':False,
                                                    'waiting':1},
                                  context_instance=RequestContext(request))


@csrf_exempt
def resultats_clima(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Actualitzem el premi de l'usuari si l'ha guanyat
    resultat_clima = 0

    #Comprovem que s'hagi arribat al bote
    if user.partida.objectiu_aconseguit or user.partida.guanyen_igualment:
        resultat_clima = user.diners_actuals

    #Comprovem si ha escollit almenys 8 vegades
    num_seleccions = UserRonda.objects.filter(user=user, ha_seleccionat = True).count()
    if num_seleccions<9:
        resultat_clima = 0

    resultat_total = resultat_clima
    vals = int(math.floor(resultat_total/10))

    user.diners_clima = resultat_clima
    user.diners_total = resultat_total
    user.vals = vals
    user.save()


    return render_to_response('resultats_clima.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                     'user': request.session['user'],
                                                     'num_partida': request.session['user'].partida.num_partida},
                              context_instance=RequestContext(request))


######################################################################################
################################### DICTATOR GAME ####################################
######################################################################################

@csrf_exempt
def joc_dictator1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    user_dictator = Dictator.objects.get(user=user.id)
    user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_dictator.seleccio1 >=0 and user_dictator_rival.seleccio1  >=0:
            return redirect('user.joc_dictator3')

    print(request.session['lang'])
    return render_to_response('joc_dictator1.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                     'user': request.session['user']},
                              context_instance=RequestContext(request))


@csrf_exempt
def joc_dictator2(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    user_dictator = Dictator.objects.get(user=user.id)
    user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_dictator.seleccio1 >=0 and user_dictator_rival.seleccio1  >=0:
            # Redirigim a la seguent pantalla
            return redirect('user.joc_dictator3')


    request.session['factor_punisher'] = FACTOR_PUNISHER
    request.session['diners_dictador'] = DINERS_DICTATOR

    if user_dictator.rol1 == 'D':
        #L'enviem a la pantalla del dictator
        return render_to_response('joc_dictator2_dictator.html', {'lang': request.session['lang'],
                                                            'text': request.session['text'],
                                                         'user': request.session['user'],
                                                         'diners_dictator': request.session['diners_dictador'],
                                                         'factor_punisher': request.session['factor_punisher']},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('joc_dictator2_punisher.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user'],
                                                         'diners_dictator': request.session['diners_dictador'],
                                                         'factor_punisher': request.session['factor_punisher']},
                                  context_instance=RequestContext(request))


@csrf_exempt
def joc_dictator3(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    user_dictator = Dictator.objects.get(user=user.id)
    user_dictator_rival = Dictator.objects.get(user=user_dictator.rival2.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_dictator.seleccio2 >=0 and user_dictator_rival.seleccio2  >=0:
            # Redirigim al seguent joc
            return redirect('user.joc_prisoner1')

    request.session['factor_punisher'] = FACTOR_PUNISHER
    request.session['diners_dictador'] = DINERS_DICTATOR

    if user_dictator.rol2 == 'D':
        #L'enviem a la pantalla de l'inversor
        return render_to_response('joc_dictator3_dictator.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user'],
                                                         'diners_dictator': request.session['diners_dictador'],
                                                         'factor_punisher': request.session['factor_punisher']},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('joc_dictator3_punisher.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user'],
                                                         'diners_dictator': request.session['diners_dictador'],
                                                         'factor_punisher': request.session['factor_punisher']},
                                  context_instance=RequestContext(request))

######################################################################################
###################################### TRUST GAME ####################################
######################################################################################

@csrf_exempt
def joc_inversor1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game

    user_trust = Trust.objects.get(user=user.id)
    user_trust_rival = Trust.objects.get(user=user_trust.rival1.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_trust.seleccio1 >=0 and user_trust_rival.seleccio1  >=0:
            return redirect('user.joc_inversor3')

    return render_to_response('joc_inversor1.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                     'user': request.session['user']},
                              context_instance=RequestContext(request))


@csrf_exempt
def joc_inversor2(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    user_trust = Trust.objects.get(user=user.id)
    user_trust_rival = Trust.objects.get(user=user_trust.rival1.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_trust.seleccio1 >=0 and user_trust_rival.seleccio1  >=0:
            return redirect('user.joc_inversor3')

    if user_trust.rol1 == 'I':
        #L'enviem a la pantalla de l'inversor
        return render_to_response('joc_inversor2_inv.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user']},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('joc_inversor2_emp.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user']},
                                  context_instance=RequestContext(request))



@csrf_exempt
def joc_inversor3(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    user_trust = Trust.objects.get(user=user.id)
    user_trust_rival = Trust.objects.get(user=user_trust.rival2.id)

    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_trust.seleccio2 >=0 and user_trust_rival.seleccio2  >=0:
            return redirect('user.enquestafinalintro')


    if user_trust.rol2 == 'I':
        #L'enviem a la pantalla de l'inversor
        return render_to_response('joc_inversor3_inv.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user']},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response('joc_inversor3_emp.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                         'user': request.session['user']},
                                  context_instance=RequestContext(request))


######################################################################################
################################### PRISONER GAME ####################################
######################################################################################

@csrf_exempt
def joc_prisoner1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id)

    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner2_asimetric')

    return render_to_response('joc_prisoner1.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                     'user': request.session['user']},
                              context_instance=RequestContext(request))



@csrf_exempt
def joc_prisoner2_simetric(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id)

    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner2_asimetric')

    return render_to_response('joc_prisoner2_simetric.html', {'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'user': request.session['user']},
                              context_instance=RequestContext(request))




@csrf_exempt
def joc_prisoner3_simetric(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id)

    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner2_asimetric')

    return render_to_response('joc_prisoner3_simetric.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                     'user': request.session['user']},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner2_asimetric(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id)
        request.session['user_prisoner'] = user_prisoner

    except Exception as e:
        return redirect('user.nickname')



    #Check if he has played this game
    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_prisoner.seleccio2 != "" and user_prisoner.seleccio3 != "":
            return redirect('user.joc_inversor1')

    request.session['matrix'] = MATRIX2

    if user_prisoner.seleccio2 == "":

        request.session['tirada'] = 2

        return render_to_response('joc_prisoner2_asimetric.html', {'lang': request.session['lang'],
                                                                'text': request.session['text'],
                                                                'user': request.session['user'],
                                                                'user_prisoner': request.session['user_prisoner'],
                                                                'matrix': request.session['matrix'],
                                                                'tirada': request.session['tirada']},
                              context_instance=RequestContext(request))

    elif user_prisoner.seleccio3 == "":

        request.session['tirada'] = 3

        return render_to_response('joc_prisoner2_asimetric.html', {'lang': request.session['lang'],
                                                                'text': request.session['text'],
                                                                'user': request.session['user'],
                                                                'user_prisoner': request.session['user_prisoner'],
                                                                'matrix': request.session['matrix'],
                                                                'tirada': request.session['tirada']},
                              context_instance=RequestContext(request))


@csrf_exempt
def joc_prisoner3_asimetric(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id)
        request.session['user_prisoner'] = user_prisoner

    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    if user.partida.estat == 'ACABADA' or user.partida.estat == 'ACABADA_MANUAL' or user.partida.estat == 'NO_JUGA':
        if user_prisoner.seleccio2 != "" and user_prisoner.seleccio3 != "":
            return redirect('user.joc_inversor1')

    request.session['matrix'] = MATRIX2

    if user_prisoner.seleccio2 == "":

        request.session['tirada'] = 2

        return render_to_response('joc_prisoner3_asimetric.html', {'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'user': request.session['user'],
                                                     'user_prisoner': request.session['user_prisoner'],
                                                     'matrix': request.session['matrix'],
                                                     'tirada': request.session['tirada']},
                              context_instance=RequestContext(request))

    elif user_prisoner.seleccio3 == "":

        request.session['tirada'] = 3

        return render_to_response('joc_prisoner3_asimetric.html', {'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'user': request.session['user'],
                                                     'user_prisoner': request.session['user_prisoner'],
                                                     'matrix': request.session['matrix'],
                                                     'tirada': request.session['tirada']},
                              context_instance=RequestContext(request))






@csrf_exempt
def final_joc(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')


    #FALTA ACTIVAR-HO
    del request.session['user']
    return render_to_response('final_joc.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'resultat_clima': user.diners_clima,
                                                 'resultat_dictator': user.diners_dictator,
                                                 'resultat_prisoner': user.diners_prisoner,
                                                 'resultat_trust': user.diners_trust,
                                                 'resultat_total': user.diners_total,
                                                 'vals': user.vals,

                                                 },
                              context_instance=RequestContext(request))