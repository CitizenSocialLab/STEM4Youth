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
        return redirect('user.inici')

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
        return redirect('user.inici')

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
            return redirect('user.inici')

        #Sino enviar-lo a l'enquesta
        except ObjectDoesNotExist:
            request.session['user'] = None
            request.session['nickname'] = nick
            # Eliminam l'avis a l'usuari, ja que tenim un altre tipus de consentiment
            # El check_1 No Aplica en aquest cas
            # return redirect(reverse('user.avis'))
            request.session['check_1'] = "NA"

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

        user.data_creacio = timezone.now()

        user.save()

        request.session['user'] = user

        return redirect('game.tutorial')


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
    pr3 = forms.CharField(max_length=100)


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
    enquesta_final_pr3 = form['pr3'].value()


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

            'pr3': enquesta_final_pr3,
            'pr3_danger': enquesta_final_pr3 is None or len(enquesta_final_pr3) == 0,
            'pr3_1_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r1' else '',
            'pr3_2_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r2' else '',
            'pr3_3_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r3' else '',
            'pr3_4_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r4' else '',
            'pr3_5_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r5' else '',
            'pr3_6_checked': 'bx-option-selected' if enquesta_final_pr3 == 'r6' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr1'] = enquesta_final_pr1
        request.session['pr2'] = enquesta_final_pr2
        request.session['pr3'] = enquesta_final_pr3

        return redirect('user.enquestafinal2')


#########################################################################################################
#########################################################################################################
# Enquesta Final 2
class SigninFormFinal2(forms.Form):
    
    pr4_r1 = forms.CharField(max_length=100, required=False)
    pr4_r2 = forms.CharField(max_length=100, required=False)
    pr4_r3 = forms.CharField(max_length=100, required=False)
    pr4_r4 = forms.CharField(max_length=100, required=False)
    pr4_r5 = forms.CharField(max_length=100, required=False)
    pr4_r6 = forms.CharField(max_length=100, required=False)


@csrf_exempt
def enquestafinal2(request, **kwargs):

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
        return render_to_response('enquestafinal2.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'pr3': request.session['pr3']},

                                  context_instance=RequestContext(request))

    form = SigninFormFinal2(request.POST)

    pr4_r1 = form['pr4_r1'].value()
    pr4_r2 = form['pr4_r2'].value()
    pr4_r3 = form['pr4_r3'].value()
    pr4_r4 = form['pr4_r4'].value()
    pr4_r5 = form['pr4_r5'].value()
    pr4_r6 = form['pr4_r6'].value()
    
    enquesta_final_pr4 = ""

    if pr4_r1 == 'r1': enquesta_final_pr4 = enquesta_final_pr4 +'r1 '
    if pr4_r2 == 'r2': enquesta_final_pr4 = enquesta_final_pr4 +'r2 '
    if pr4_r3 == 'r3': enquesta_final_pr4 = enquesta_final_pr4 +'r3 '
    if pr4_r4 == 'r4': enquesta_final_pr4 = enquesta_final_pr4 +'r4 '
    if pr4_r5 == 'r5': enquesta_final_pr4 = enquesta_final_pr4 +'r5 '
    if pr4_r6 == 'r6': enquesta_final_pr4 = enquesta_final_pr4 +'r6 '
    
    if not form.is_valid():
        return render_to_response('enquestafinal2.html', {
            'pr4': enquesta_final_pr4,
            'pr4_danger': enquesta_final_pr4 is None or len(enquesta_final_pr4) == 0,
            'lang': request.session['lang'], 'text': request.session['text'], 'pr3': request.session['pr3']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr4'] = enquesta_final_pr4

        return redirect('user.enquestafinal3')


#########################################################################################################
#########################################################################################################
# Enquesta Final 3
class SigninFormFinal3(forms.Form):
    pr5 = forms.CharField(max_length=100)


@csrf_exempt
def enquestafinal3(request, **kwargs):

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
        return render_to_response('enquestafinal3.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal3(request.POST)
    enquesta_final_pr5 = form['pr5'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal3.html', {
            'pr5': enquesta_final_pr5,
            'pr5_danger': enquesta_final_pr5 is None or len(enquesta_final_pr5) == 0,
            'pr5_1_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r1' else '',
            'pr5_2_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r2' else '',
            'pr5_3_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r3' else '',



            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr5'] = enquesta_final_pr5


        if enquesta_final_pr5 == 'r1':
            request.session['pr6'] = 'na'
            return redirect('user.enquestafinal5')
        else :
            return redirect('user.enquestafinal4')



# Enquesta Final 4
class SigninFormFinal4(forms.Form):

    pr6_r1 = forms.CharField(max_length=100, required=False)
    pr6_r2 = forms.CharField(max_length=100, required=False)
    pr6_r3 = forms.CharField(max_length=100, required=False)
    pr6_r4 = forms.CharField(max_length=100, required=False)
    pr6_r5 = forms.CharField(max_length=100, required=False)
    pr6_r6 = forms.CharField(max_length=100, required=False)
    pr6_r7 = forms.CharField(max_length=100, required=False)
    pr6_r8 = forms.CharField(max_length=100, required=False)
    pr6_r9 = forms.CharField(max_length=100, required=False)
    pr6_r10 = forms.CharField(max_length=100, required=False)
    pr6_r11 = forms.CharField(max_length=100, required=False)

@csrf_exempt
def enquestafinal4(request, **kwargs):

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
        return render_to_response('enquestafinal4.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal4(request.POST)

    pr6_r1 = form['pr6_r1'].value()
    pr6_r2 = form['pr6_r2'].value()
    pr6_r3 = form['pr6_r3'].value()
    pr6_r4 = form['pr6_r4'].value()
    pr6_r5 = form['pr6_r5'].value()
    pr6_r6 = form['pr6_r6'].value()
    pr6_r7 = form['pr6_r7'].value()
    pr6_r8 = form['pr6_r8'].value()
    pr6_r9 = form['pr6_r9'].value()
    pr6_r10 = form['pr6_r10'].value()
    pr6_r11 = form['pr6_r11'].value()

    enquesta_final_pr6 = ""

    if pr6_r1 == 'r1': enquesta_final_pr6 = enquesta_final_pr6 +'r1 '
    if pr6_r2 == 'r2': enquesta_final_pr6 = enquesta_final_pr6 +'r2 '
    if pr6_r3 == 'r3': enquesta_final_pr6 = enquesta_final_pr6 +'r3 '
    if pr6_r4 == 'r4': enquesta_final_pr6 = enquesta_final_pr6 +'r4 '
    if pr6_r5 == 'r5': enquesta_final_pr6 = enquesta_final_pr6 +'r5 '
    if pr6_r6 == 'r6': enquesta_final_pr6 = enquesta_final_pr6 +'r6 '
    if pr6_r7 == 'r7': enquesta_final_pr6 = enquesta_final_pr6 +'r7 '
    if pr6_r8 == 'r8': enquesta_final_pr6 = enquesta_final_pr6 +'r8 '
    if pr6_r9 == 'r9': enquesta_final_pr6 = enquesta_final_pr6 +'r9 '
    if pr6_r10 == 'r10': enquesta_final_pr6 = enquesta_final_pr6 +'r10 '
    if pr6_r11 == 'r11': enquesta_final_pr6 = enquesta_final_pr6 +'r11 '


    if not form.is_valid():
        return render_to_response('enquestafinal4.html', {
            'pr6_danger': enquesta_final_pr6 is None or len(enquesta_final_pr6) == 0,
            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr6'] = enquesta_final_pr6
        return redirect('user.enquestafinal5')

#########################################################################################################
#########################################################################################################
# Enquesta Final 5
class SigninFormFinal5(forms.Form):
    pr7 = forms.CharField(max_length=100)


@csrf_exempt
def enquestafinal5(request, **kwargs):

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
        return render_to_response('enquestafinal5.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal5(request.POST)
    enquesta_final_pr7 = form['pr7'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal5.html', {
            'pr7': enquesta_final_pr7,
            'pr7_danger': enquesta_final_pr7 is None or len(enquesta_final_pr7) == 0,
            'pr7_1_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r1' else '',
            'pr7_2_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r2' else '',
            'pr7_3_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r3' else '',
            'pr7_4_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r4' else '',
            'pr7_5_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r5' else '',
            'pr7_6_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r6' else '',
            'pr7_7_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r7' else '',
            'pr7_8_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r8' else '',
            'pr7_9_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r9' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr7'] = enquesta_final_pr7

        return redirect('user.enquestafinal6')


#########################################################################################################
#########################################################################################################

#########################################################################################################
#########################################################################################################
# Enquesta Final 6
class SigninFormFinal6(forms.Form):
    pr8 = forms.CharField(max_length=100)
    pr9 = forms.CharField(max_length=100)
    pr10 = forms.CharField(max_length=100)


@csrf_exempt
def enquestafinal6(request, **kwargs):

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
        return render_to_response('enquestafinal6.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal6(request.POST)
    enquesta_final_pr9 = form['pr9'].value()
    enquesta_final_pr8 = form['pr8'].value()
    enquesta_final_pr10 = form['pr10'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal6.html', {
            'pr8': enquesta_final_pr8,
            'pr8_danger': enquesta_final_pr8 is None or len(enquesta_final_pr8) == 0,
            'pr8_1_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r1' else '',
            'pr8_2_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r2' else '',
            'pr8_3_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r3' else '',
            'pr8_4_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r4' else '',
            'pr8_5_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r5' else '',
            'pr8_6_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r6' else '',

            'pr9': enquesta_final_pr9,
            'pr9_danger': enquesta_final_pr9 is None or len(enquesta_final_pr9) == 0,
            'pr9_1_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r1' else '',
            'pr9_2_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r2' else '',
            'pr9_3_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r3' else '',
            'pr9_4_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r4' else '',
            'pr9_5_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r5' else '',
            'pr9_6_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r6' else '',
            
            'pr10': enquesta_final_pr10,
            'pr10_danger': enquesta_final_pr10 is None or len(enquesta_final_pr10) == 0,
            'pr10_1_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r1' else '',
            'pr10_2_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r2' else '',
            'pr10_3_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r3' else '',
            'pr10_4_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r4' else '',
            'pr10_5_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r5' else '',
            'pr10_6_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r6' else '',



            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr9'] = enquesta_final_pr9
        request.session['pr8'] = enquesta_final_pr8
        request.session['pr10'] = enquesta_final_pr10

        return redirect('user.enquestafinal7')


#########################################################################################################
#########################################################################################################


#########################################################################################################
#########################################################################################################
# Enquesta Final 7
class SigninFormFinal7(forms.Form):
    pr11 = forms.CharField(max_length=100)
    pr12_r1 = forms.CharField(max_length=100, required=False)
    pr12_r2 = forms.CharField(max_length=100, required=False)
    pr12_r3 = forms.CharField(max_length=100, required=False)
    pr12_r4 = forms.CharField(max_length=100, required=False)
    pr12_r5 = forms.CharField(max_length=100, required=False)
    pr12_r6 = forms.CharField(max_length=100, required=False)

@csrf_exempt
def enquestafinal7(request, **kwargs):

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
        return render_to_response('enquestafinal7.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal7(request.POST)
    enquesta_final_pr11 = form['pr11'].value()
    
    pr12_r1 = form['pr12_r1'].value()
    pr12_r2 = form['pr12_r2'].value()
    pr12_r3 = form['pr12_r3'].value()
    pr12_r4 = form['pr12_r4'].value()
    pr12_r5 = form['pr12_r5'].value()
    pr12_r6 = form['pr12_r6'].value()
    
    enquesta_final_pr12 = ""

    if pr12_r1 == 'r1': enquesta_final_pr12 = enquesta_final_pr12 +'r1 '
    if pr12_r2 == 'r2': enquesta_final_pr12 = enquesta_final_pr12 +'r2 '
    if pr12_r3 == 'r3': enquesta_final_pr12 = enquesta_final_pr12 +'r3 '
    if pr12_r4 == 'r4': enquesta_final_pr12 = enquesta_final_pr12 +'r4 '
    if pr12_r5 == 'r5': enquesta_final_pr12 = enquesta_final_pr12 +'r5 '
    if pr12_r6 == 'r6': enquesta_final_pr12 = enquesta_final_pr12 +'r6 '



    if not form.is_valid():
        return render_to_response('enquestafinal7.html', {
            'pr11': enquesta_final_pr11,
            'pr11_danger': enquesta_final_pr11 is None or len(enquesta_final_pr11) == 0,
            'pr11_1_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r1' else '',
            'pr11_2_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r2' else '',
            'pr11_3_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r3' else '',
            'pr11_4_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r4' else '',
            'pr11_5_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r5' else '',
            'pr11_6_checked': 'bx-option-selected' if enquesta_final_pr11 == 'r6' else '',

            'pr12': enquesta_final_pr12,
            'pr12_danger': enquesta_final_pr12 is None or len(enquesta_final_pr12) == 0,
            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr11'] = enquesta_final_pr11
        request.session['pr12'] = enquesta_final_pr12

        return redirect('user.enquestafinal8')


#########################################################################################################
#########################################################################################################


#########################################################################################################
#########################################################################################################
# Enquesta Final 8
class SigninFormFinal8(forms.Form):
    pr13 = forms.CharField(max_length=1000)


@csrf_exempt
def enquestafinal8(request, **kwargs):

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
        return render_to_response('enquestafinal8.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal8(request.POST)
    enquesta_final_pr13 = form['pr13'].value()
    print(len(enquesta_final_pr13) == 1)

    if not form.is_valid():
        return render_to_response('enquestafinal8.html', {
            'pr13': enquesta_final_pr13,
            'pr13_danger': enquesta_final_pr13 is None or len(enquesta_final_pr13) == 0,
            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr13'] = enquesta_final_pr13

        user = User.objects.get(id=request.session['user'].id)

        user.enquesta_final_pr1 = request.session['pr1']
        user.enquesta_final_pr2 = request.session['pr2']
        user.enquesta_final_pr3 = request.session['pr3']
        user.enquesta_final_pr4 = request.session['pr4']
        user.enquesta_final_pr5 = request.session['pr5']
        user.enquesta_final_pr6 = request.session['pr6']
        user.enquesta_final_pr7 = request.session['pr7']
        user.enquesta_final_pr8 = request.session['pr8']
        user.enquesta_final_pr9 = request.session['pr9']
        user.enquesta_final_pr10 = request.session['pr10']
        user.enquesta_final_pr11 = request.session['pr11']
        user.enquesta_final_pr12 = request.session['pr12']
        user.enquesta_final_pr13 = request.session['pr13']

        user.acabat = True
        user.data_finalitzacio = timezone.now()

        user.save()

        return redirect('user.resultats_clima')


#########################################################################################################
#########################################################################################################




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

    # Vals
    # Vals que han guanyat
    val_abacus = int(math.floor(resultat_total/FACTOR_VALS)) + 1

    # No han arribat a objectiu i no guanyen
    if not user.partida.objectiu_aconseguit and user.partida.guanyen_igualment == 0:
        val_abacus = 0

    # El robot ha contestat mes de 2 vegades
    if num_seleccions < 9:
        val_abacus = 0



    user.diners_clima = resultat_clima
    user.diners_total = resultat_total
    user.val_abacus = val_abacus
    user.bots = 10 - num_seleccions
    user.save()


    return render_to_response('resultats_clima.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                        'user': request.session['user'],
                                                        'num_partida': request.session['user'].partida.num_partida},
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

    print user.partida
    print user.diners_clima
    #FALTA ACTIVAR-HO
    del request.session['user']
    return render_to_response('final_joc.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'resultat_clima': user.diners_clima,
                                                 'resultat_total': user.diners_total,
                                                 'val_abacus': user.val_abacus,
                                                 'username': user.nickname,
                                                 },
                              context_instance=RequestContext(request))