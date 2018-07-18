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


####################
# USER STATUS

def user_exists_in_db(user):
    try:
        User.objects.get(pk=user.id)
        return True
    except:
        return False

#######################
#### Initial Modul ####
#######################

## Interface Index
@csrf_exempt
def index(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        # Check valid user in the db
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

    return redirect('user.nickname')

## Interface Nickname
class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=300)

@csrf_exempt
def nickname(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        # Check valid user in the db
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        #Todo: Distribute user when start
        if user_exists_in_db(user):
            if user.status == 'AVIS':
                return redirect('user.avis')
            elif user.status == 'SOCIODEMO':
                if EXPERIMENT == 'Athens':
                    return redirect('user.enquesta1_Athens')
                if EXPERIMENT == 'xAire':
                    return redirect('user.enquesta1_xAire')
            elif user.status == 'FRAME':
                return redirect('user.frame')
            elif user.status == 'TUTORIAL_WAITING':
                return redirect('game.tutorial_inici')
            elif user.status == 'TUTORIAL':
                return redirect('game.tutorial')
            elif user.status == 'VERIFICATION':
                return redirect('user.verification')
            elif user.status == 'START':
                return redirect('user.inici')
            elif user.status == 'SURVEY_FINAL':
                return redirect('user.enquestafinal1_xAire')

    # Delete nickname
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

        # If the user exist distribute in the game or show an alert message
        #Todo: Distribute user when start or show a message
        try:
            user = User.objects.get(nickname=nick)
            request.session['user'] = user

            if user.status == 'AVIS':
                return redirect('user.avis')
            elif user.status == 'SOCIODEMO':
                if EXPERIMENT == 'Athens':
                    return redirect('user.enquesta1_Athens')
                if EXPERIMENT == 'xAire':
                    return redirect('user.enquesta1_xAire')
            elif user.status == 'FRAME':
                return redirect('user.frame')
            elif user.status == 'TUTORIAL_WAITING':
                return redirect('game.tutorial_inici')
            elif user.status == 'TUTORIAL':
                return redirect('game.tutorial')
            elif user.status == 'VERIFICATION':
                return redirect('user.verification')
            elif user.status == 'START':
                return redirect('user.inici')
            elif user.status == 'SURVEY_FINAL':
                return redirect('user.enquestafinal1_xAire')
            else: return redirect('user.inici')

        # If user not exist send to survey
        except ObjectDoesNotExist:
            request.session['user'] = None
            request.session['nickname'] = nick

            user = User()
            user.date_creation = timezone.now()
            user.nickname = request.session['nickname']
            user.status = "AVIS"
            user.save()

            request.session['user'] = user
            return redirect('user.avis')

#########################################################################################################

###########################
### Pantalla avis legal ###
###########################

class AvisForm(forms.Form):
    check_1 = forms.CharField(max_length=20)

@csrf_exempt
def avis(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')


    if request.method != 'POST':
        return render_to_response('avis.html',  {'lang': request.session['lang'], 'text': request.session['text']},
                              context_instance=RequestContext(request))
    else:
        form = AvisForm(request.POST)
        request.session['consent'] = True

        user = User.objects.get(id=request.session['user'].id)
        user.status = "SOCIODEMO"
        user.consent = request.session['consent']
        user.save()

        if EXPERIMENT == 'Athens':
            return redirect('user.enquesta1_Athens')
        if EXPERIMENT == 'xAire':
            return redirect('user.enquesta1_xAire')


######################
### Surveys Athens ###
######################

class SigninForm1_Athens(forms.Form):
    gender = forms.CharField(max_length=100)
    age_range = forms.CharField(max_length=100)
    residence = forms.CharField(max_length=100)

@csrf_exempt
def enquesta1_Athens(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('enquesta1_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))
    # Control Experiment Athens
    form = SigninForm1_Athens(request.POST)
    gender = form['gender'].value()
    age_range = form['age_range'].value()
    residence = form['residence'].value()

    if not form.is_valid():
        return render_to_response('enquesta1_Athens.html', {
            'gender': gender,
            'gender_danger': gender is None or len(gender) == 0,
            'gender_1_checked': 'bx-option-selected' if gender == 'M' else '',
            'gender_2_checked': 'bx-option-selected' if gender == 'F' else '',
            'gender_3_checked': 'bx-option-selected' if gender == 'N' else '',

            'age_range': age_range,
            'age_range_danger': age_range is None or len(age_range) == 0,
            'age_range_1_checked': 'bx-option-selected' if age_range == 'r1' else '',
            'age_range_2_checked': 'bx-option-selected' if age_range == 'r2' else '',
            'age_range_3_checked': 'bx-option-selected' if age_range == 'r3' else '',
            'age_range_4_checked': 'bx-option-selected' if age_range == 'r4' else '',
            'age_range_5_checked': 'bx-option-selected' if age_range == 'r5' else '',
            'age_range_6_checked': 'bx-option-selected' if age_range == 'r6' else '',
            'age_range_7_checked': 'bx-option-selected' if age_range == 'r7' else '',

            'residence': residence,
            'residence_danger': residence is None or len(residence) == 0,
            'residence_0_checked': 'bx-option-selected' if residence == 'r1' else '',
            'residence_1_checked': 'bx-option-selected' if residence == 'r2' else '',
            'residence_2_checked': 'bx-option-selected' if residence == 'r3' else '',
            'residence_3_checked': 'bx-option-selected' if residence == 'r4' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['gender'] = gender
        request.session['age_range'] = age_range
        request.session['residence'] = residence

    return redirect('user.enquesta2_Athens')

class SigninForm2_Athens(forms.Form):
    economic_status = forms.CharField(max_length=100)
    educational_level = forms.CharField(max_length=100)
    working_status = forms.CharField(max_length=100)

@csrf_exempt
def enquesta2_Athens(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('enquesta2_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm2_Athens(request.POST)
    economic_status = form['economic_status'].value()
    educational_level = form['educational_level'].value()
    working_status = form['working_status'].value()

    if not form.is_valid():
        return render_to_response('enquesta2_Athens.html', {

            'economic_status': economic_status,
            'economic_status_danger': economic_status is None or len(economic_status) == 0,
            'economic_status_0_checked': 'bx-option-selected' if economic_status == 'r1' else '',
            'economic_status_1_checked': 'bx-option-selected' if economic_status == 'r2' else '',
            'economic_status_2_checked': 'bx-option-selected' if economic_status == 'r3' else '',
            'economic_status_3_checked': 'bx-option-selected' if economic_status == 'r4' else '',
            'economic_status_4_checked': 'bx-option-selected' if economic_status == 'r5' else '',

            'educational_level': educational_level,
            'educational_level_danger': educational_level is None or len(educational_level) == 0,
            'educational_level_0_checked': 'bx-option-selected' if educational_level == 'r1' else '',
            'educational_level_1_checked': 'bx-option-selected' if educational_level == 'r2' else '',
            'educational_level_2_checked': 'bx-option-selected' if educational_level == 'r3' else '',
            'educational_level_3_checked': 'bx-option-selected' if educational_level == 'r4' else '',
            'educational_level_4_checked': 'bx-option-selected' if educational_level == 'r5' else '',

            'working_status': working_status,
            'working_status_danger': working_status is None or len(working_status) == 0,
            'working_status_0_checked': 'bx-option-selected' if working_status == 'r1' else '',
            'working_status_1_checked': 'bx-option-selected' if working_status == 'r2' else '',
            'working_status_2_checked': 'bx-option-selected' if working_status == 'r3' else '',
            'working_status_3_checked': 'bx-option-selected' if working_status == 'r4' else '',
            'working_status_4_checked': 'bx-option-selected' if working_status == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))
    else:
        request.session['economic_status'] = economic_status
        request.session['working_status'] = working_status
        request.session['educational_level'] = educational_level

    user = User.objects.get(id=request.session['user'].id)
    user.gender = request.session['gender']
    user.age_range = request.session['age_range']
    user.residence = request.session['residence']
    user.economic_status = request.session['economic_status']
    user.working_status = request.session['working_status']
    user.educational_level = request.session['educational_level']
    user.consent = request.session['consent']
    user.endowment_initial = 0
    user.endowment_current = 0

    user.status = "FRAME"
    user.save()

    request.session['user'] = user

    return redirect('user.frame')


#####################
### Surveys xAire ###
#####################

class SigninForm1_xAire(forms.Form):
    gender = forms.CharField(max_length=100)
    age_range = forms.CharField(max_length=100)
    economic_status = forms.CharField(max_length=100)

@csrf_exempt
def enquesta1_xAire(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('enquesta1_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm1_xAire(request.POST)
    gender = form['gender'].value()
    age_range = form['age_range'].value()
    economic_status = form['economic_status'].value()

    if not form.is_valid():
        return render_to_response('enquesta1_xAire.html', {
            'gender': gender,
            'gender_danger': gender is None or len(gender) == 0,
            'gender_1_checked': 'bx-option-selected' if gender == 'M' else '',
            'gender_2_checked': 'bx-option-selected' if gender == 'F' else '',
            'gender_3_checked': 'bx-option-selected' if gender == 'O' else '',
            'gender_4_checked': 'bx-option-selected' if gender == 'N' else '',

            'age_range': age_range,
            'age_range_danger': age_range is None or len(age_range) == 0,
            'age_range_1_checked': 'bx-option-selected' if age_range == 'r1' else '',
            'age_range_2_checked': 'bx-option-selected' if age_range == 'r2' else '',
            'age_range_3_checked': 'bx-option-selected' if age_range == 'r3' else '',
            'age_range_4_checked': 'bx-option-selected' if age_range == 'r4' else '',
            'age_range_5_checked': 'bx-option-selected' if age_range == 'r5' else '',
            'age_range_6_checked': 'bx-option-selected' if age_range == 'r6' else '',
            'age_range_7_checked': 'bx-option-selected' if age_range == 'r7' else '',

            'economic_status': economic_status,
            'economic_status_danger': economic_status is None or len(economic_status) == 0,
            'economic_status_0_checked': 'bx-option-selected' if economic_status == 'r1' else '',
            'economic_status_1_checked': 'bx-option-selected' if economic_status == 'r2' else '',
            'economic_status_2_checked': 'bx-option-selected' if economic_status == 'r3' else '',
            'economic_status_3_checked': 'bx-option-selected' if economic_status == 'r4' else '',
            'economic_status_4_checked': 'bx-option-selected' if economic_status == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['gender'] = gender
        request.session['age_range'] = age_range
        request.session['economic_status'] = economic_status


    return redirect('user.enquesta2_xAire')

class SigninForm2_xAire(forms.Form):
    educational_level = forms.CharField(max_length=100)
    working_status = forms.CharField(max_length=100)

@csrf_exempt
def enquesta2_xAire(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('enquesta2_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm2_xAire(request.POST)
    educational_level = form['educational_level'].value()
    working_status = form['working_status'].value()

    if not form.is_valid():
        return render_to_response('enquesta2_xAire.html', {
            'educational_level': educational_level,
            'educational_level_danger': educational_level is None or len(educational_level) == 0,
            'educational_level_0_checked': 'bx-option-selected' if educational_level == 'r1' else '',
            'educational_level_1_checked': 'bx-option-selected' if educational_level == 'r2' else '',
            'educational_level_2_checked': 'bx-option-selected' if educational_level == 'r3' else '',
            'educational_level_3_checked': 'bx-option-selected' if educational_level == 'r4' else '',

            'working_status': working_status,
            'working_status_danger': working_status is None or len(working_status) == 0,
            'working_status_0_checked': 'bx-option-selected' if working_status == 'r1' else '',
            'working_status_1_checked': 'bx-option-selected' if working_status == 'r2' else '',
            'working_status_2_checked': 'bx-option-selected' if working_status == 'r3' else '',
            'working_status_3_checked': 'bx-option-selected' if working_status == 'r4' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['working_status'] = working_status
        request.session['educational_level'] = educational_level


    return redirect('user.enquesta3_xAire')

class SigninForm3_xAire(forms.Form):
    residence = forms.CharField(max_length=100)

@csrf_exempt
def enquesta3_xAire(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('enquesta3_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm3_xAire(request.POST)
    residence = form['residence'].value()

    if not form.is_valid():
        return render_to_response('enquesta3_xAire.html', {
            'residence': residence,
            'residence_danger': residence is None or len(residence) == 0,
            'residence_0_checked': 'bx-option-selected' if residence == 'r1' else '',
            'residence_1_checked': 'bx-option-selected' if residence == 'r2' else '',
            'residence_2_checked': 'bx-option-selected' if residence == 'r3' else '',
            'residence_3_checked': 'bx-option-selected' if residence == 'r4' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['residence'] = residence


    user = User.objects.get(id=request.session['user'].id)
    user.gender = request.session['gender']
    user.age_range = request.session['age_range']
    user.residence = request.session['residence']
    user.economic_status = request.session['economic_status']
    user.working_status = request.session['working_status']
    user.educational_level = request.session['educational_level']

    user.pollution = Pollution.objects.get(tag=user.residence)

    user.endowment_initial = 0
    user.endowment_current = 0

    user.status = "FRAME"
    user.save()

    request.session['user'] = user

    return redirect('user.frame')

## Interfaces Survey Framed
class SigninForm4_Athens(forms.Form):
    pr_framed1 = forms.CharField(max_length=100)
    pr_framed2 = forms.CharField(max_length=100)

class SigninForm4_xAire(forms.Form):
    pr_framed1 = forms.CharField(max_length=100)
    pr_framed2 = forms.CharField(max_length=100)
    pr_framed3 = forms.CharField(max_length=100)

@csrf_exempt
def frame(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    # Check POST
    if request.method != 'POST':
        return render_to_response('frame_'+EXPERIMENT+'.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    if EXPERIMENT == 'Athens':

        form = SigninForm4_Athens(request.POST)
        frame_pr1 = form['pr_framed1'].value()
        frame_pr2 = form['pr_framed2'].value()

        if not form.is_valid():
            return render_to_response('frame_'+EXPERIMENT+'.html', {

                'pr_framed1': frame_pr1,
                'pr_framed1_danger': frame_pr1 is None or len(frame_pr1) == 0,
                'pr_framed1_0_checked': 'bx-option-selected' if frame_pr1 == 'r1' else '',
                'pr_framed1_1_checked': 'bx-option-selected' if frame_pr1 == 'r2' else '',
                'pr_framed1_2_checked': 'bx-option-selected' if frame_pr1 == 'r3' else '',

                'pr_framed2': frame_pr2,
                'pr_framed2_danger': frame_pr2 is None or len(frame_pr2) == 0,
                'pr_framed2_0_checked': 'bx-option-selected' if frame_pr2 == 'r1' else '',
                'pr_framed2_1_checked': 'bx-option-selected' if frame_pr2 == 'r2' else '',
                'pr_framed2_2_checked': 'bx-option-selected' if frame_pr2 == 'r3' else '',

                'lang': request.session['lang'], 'text': request.session['text']
            }, context_instance=RequestContext(request))

        else:
            request.session['pr_framed1'] = frame_pr1
            request.session['pr_framed2'] = frame_pr2

    if EXPERIMENT == 'xAire':
        form = SigninForm4_xAire(request.POST)
        frame_pr1 = form['pr_framed1'].value()
        frame_pr2 = form['pr_framed2'].value()
        frame_pr3 = form['pr_framed3'].value()

        if not form.is_valid():
            return render_to_response('frame_'+EXPERIMENT+'.html', {

                'pr_framed1': frame_pr1,
                'pr_framed1_danger': frame_pr1 is None or len(frame_pr1) == 0,
                'pr_framed1_0_checked': 'bx-option-selected' if frame_pr1 == 'r1' else '',
                'pr_framed1_1_checked': 'bx-option-selected' if frame_pr1 == 'r2' else '',
                'pr_framed1_2_checked': 'bx-option-selected' if frame_pr1 == 'r3' else '',

                'pr_framed2': frame_pr2,
                'pr_framed2_danger': frame_pr2 is None or len(frame_pr2) == 0,
                'pr_framed2_0_checked': 'bx-option-selected' if frame_pr2 == 'r1' else '',
                'pr_framed2_1_checked': 'bx-option-selected' if frame_pr2 == 'r2' else '',
                'pr_framed2_2_checked': 'bx-option-selected' if frame_pr2 == 'r3' else '',

                'pr_framed3': frame_pr3,
                'pr_framed3_danger': frame_pr3 is None or len(frame_pr3) == 0,
                'pr_framed3_0_checked': 'bx-option-selected' if frame_pr3 == 'r1' else '',
                'pr_framed3_1_checked': 'bx-option-selected' if frame_pr3 == 'r2' else '',

                'lang': request.session['lang'], 'text': request.session['text']
            }, context_instance=RequestContext(request))


        else:
            request.session['pr_framed1'] = frame_pr1
            request.session['pr_framed2'] = frame_pr2
            request.session['pr_framed3'] = frame_pr3

    user = User.objects.get(id=request.session['user'].id)

    user.frame_pr1 = request.session['pr_framed1']
    user.frame_pr2 = request.session['pr_framed2']

    if EXPERIMENT == 'Athens': user.frame_pr3 = '-1'
    if EXPERIMENT == 'xAire': user.frame_pr3 = request.session['pr_framed3']

    user.status = "TUTORIAL_WAITING"

    request.session['user'] = user

    user.save()

    return redirect('game.tutorial_inici')

## Interfaces Verificacio
class SigninForm5(forms.Form):
    pr_verification1 = forms.CharField(max_length=100)
    pr_verification2 = forms.CharField(max_length=100)
    pr_verification3 = forms.CharField(max_length=100)

@csrf_exempt
def verification(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    user = User.objects.get(id=request.session['user'].id)
    user.status = 'VERIFICATION'
    user.save()

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('verification.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninForm5(request.POST)
    verification_pr1 = form['pr_verification1'].value()
    verification_pr2 = form['pr_verification2'].value()
    verification_pr3 = form['pr_verification3'].value()

    #ToDo: verification correct answer
    correct_answers = verification_pr1 == 'r2' and verification_pr2 == 'r2' and verification_pr3 == 'r1'

    if not form.is_valid() or not correct_answers:
        return render_to_response('verification.html', {

            'pr_verification1': verification_pr1,
            'pr_verification1_danger': verification_pr1 is None or len(verification_pr1) == 0,
            'pr_verification1_0_checked': 'bx-option-selected' if verification_pr1 == 'r1' else '',
            'pr_verification1_1_checked': 'bx-option-selected' if verification_pr1 == 'r2' else '',
            'pr_verification1_2_checked': 'bx-option-selected' if verification_pr1 == 'r3' else '',
            'pr_verification1_3_checked': 'bx-option-selected' if verification_pr1 == 'r4' else '',

            'pr_verification2': verification_pr2,
            'pr_verification2_danger': verification_pr2 is None or len(verification_pr2) == 0,
            'pr_verification2_0_checked': 'bx-option-selected' if verification_pr2 == 'r1' else '',
            'pr_verification2_1_checked': 'bx-option-selected' if verification_pr2 == 'r2' else '',
            'pr_verification2_2_checked': 'bx-option-selected' if verification_pr2 == 'r3' else '',

            'pr_verification3': verification_pr3,
            'pr_verification3_danger': verification_pr3 is None or len(verification_pr3) == 0,
            'pr_verification3_0_checked': 'bx-option-selected' if verification_pr3 == 'r1' else '',
            'pr_verification3_1_checked': 'bx-option-selected' if verification_pr3 == 'r2' else '',
            'pr_verification3_2_checked': 'bx-option-selected' if verification_pr3 == 'r3' else '',

            'pr_verification_error': not correct_answers,

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))


    else:
        request.session['pr_verification1'] = verification_pr1
        request.session['pr_verification2'] = verification_pr2
        request.session['pr_verification3'] = verification_pr3

        user = User.objects.get(id=request.session['user'].id)

        user.verification_pr1 = request.session['pr_verification1']
        user.verification_pr2 = request.session['pr_verification2']
        user.verification_pr3 = request.session['pr_verification3']
        user.status = "START"

        user.save()

        return redirect('user.inici')

##################
### Game Modul ###
##################

## Logout game action
@csrf_exempt
def logout(request, **kwargs):
    if 'user' in request.session and request.session['user'] is not None:
        del request.session['user']
    return redirect('index')

## Start game action
@csrf_exempt
def inici(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        print 'user not in request'
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        print 'user in request and in database'
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        print 'user in request not in database'
        return redirect('user.nickname')

    #Todo: Message in Nickname that this user exist and choose a new nickname
    # User - END
    if user.date_end:
        print 'user end'
        return redirect('user.final_joc')

    # User - WITHOUT PARTIDA
    if not user.partida:
        print 'user no game'
        return  redirect('game.tutorial_inici')

    # User - WITHOUT REGISTER
    if not user.date_register:
        print 'user not registered'
        # Check POST
        if request.method != 'POST':
            return render_to_response('inici.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'control_reward_economic': user.partida.control_reward == 'ECONOMIC',
                                                     'control_reward_social': user.partida.control_reward == 'SOCIAL'},
                                      context_instance=RequestContext(request))

        try:
            if user.partida.usuaris_registrats <= NUM_PLAYERS:
                print "Game ", user.partida.num_partida,"- Users Registered: ", user.partida.usuaris_registrats
                user.date_register = timezone.now()
                user.status = "REGISTERED"
                user.save()
            else:
                return redirect('user.tutorial_inici')

            # REGISTERED to GAME INDEX
            return redirect('game.index')
        except:
            # TRY AGAIN
            return redirect('user.inici')


        return render_to_response('inici.html', {'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'error_partida':True,
                                                 'control_reward_economic': user.partida.control_reward == 'ECONOMIC',
                                                 'control_reward_social': user.partida.control_reward == 'SOCIAL'},
                                  context_instance=RequestContext(request))


    # User REGISTERED
    else:
        print 'user registered'
        # User with GAME - REGISTERED and Game REGISTERING
        if user.partida and user.status == "REGISTERED" and user.partida.status == "REGISTERING":
            print 'user registered and game registering'
            return redirect('game.index')


        # User with GAME - REGISTERED and GAME PLAYING
        if user.partida and user.status == "REGISTERED" and user.partida.status == "PLAYING":
            print 'user registered and game playing'
            date_now = timezone.now()
            date_start = user.partida.date_start
            temps_actual_joc = (date_now - date_start).total_seconds()

            # Rounds DO NOT STARTED
            if temps_actual_joc < TEMPS_INICI_SEC:
                return redirect('game.index')

            # Rounds STARTED
            else :
                return redirect('user.inici')

        # User and Game PLAYING - But User EXIT GAME
        if user.partida and user.status == "PLAYING" and user.partida.status == "PLAYING":
            print 'You has quitted of the game and can not enter again.'
            #Todo: Send to results or nickname with a error message
            return redirect('user.resultats_clima')

        if user.partida and user.date_register and not user.date_end and user.partida.status == "REGISTERING":
            print 'player start and game registering'
            user = User.objects.get(id=request.session['user'].id)
            user.status = "REGISTERED"
            user.save()
            return redirect('game.index')

        if user.partida and (user.partida.status == "FINISHED" or user.partida.status == "FINISHED_MANUALLY"):
            return redirect('user.resultats_clima')


        return redirect('user.inici')

## Results game
@csrf_exempt
def resultats_clima(request, **kwargs):

    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    try:
        ronda = Ronda.objects.filter(partida_id=user.partida.id).order_by('bucket_final_ronda')[0]
    except Exception as e:
        return redirect('user.nickname')

    # Compute the results
    num_selections = UserRonda.objects.filter(user=user, ha_seleccionat = True).count()

    savings_public_goods = user.endowment_current
    contributed_public_goods = user.endowment_initial - user.endowment_current

    if ronda.bucket_final_ronda:
        contributed_total = THRESHOLD-ronda.bucket_final_ronda
    else:
        contributed_total = 0
    user.partida.total_contributed = contributed_total
    user.partida.save()

    #
    # Check if the goal is achieved
    if user.partida.objectiu_aconseguit or user.partida.always_win:
        if user.partida.control_reward == 'SOCIAL':
            winnings_public_goods = savings_public_goods
            user.partida.total_social_action = contributed_total
            user.partida.save()

        if user.partida.control_reward == 'ECONOMIC':
            winnings_public_goods = round(savings_public_goods + ((contributed_total*FACTOR_RETURN)/NUM_PLAYERS),0)
            user.partida.total_social_action = contributed_total*FACTOR_RETURN
            user.partida.save()

        coins_total = winnings_public_goods
        tickets = int(math.floor(coins_total/FACTOR_TICKETS)) + 1

    else:
        winnings_public_goods = 0
        tickets = 1
        coins_total = 0

    # Check the number of bots no wins no tickets
    if user.bots >= 2:
        winnings_public_goods = 0
        tickets = 0
        coins_total = 0


    user.contributed_public_goods = contributed_public_goods
    user.savings_public_goods = savings_public_goods
    user.winnings_public_goods = winnings_public_goods
    user.tickets = tickets
    user.coins_total = coins_total
    user.status = "RESULTS"
    user.save()

    return render_to_response('resultats_clima.html', {'lang': request.session['lang'],
                                                        'text': request.session['text'],
                                                        'user': request.session['user'],
                                                        'num_partida': request.session['user'].partida.num_partida},
                              context_instance=RequestContext(request))

## Final game
@csrf_exempt
def final_joc(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        user.status = "END"
        user.save()

        request.session['user'] = user

    except Exception as e:
        return redirect('user.nickname')

    #ToDo: Work in the last screen
    #del request.session['user']

    return render_to_response('final_joc.html', {'xAire': True if EXPERIMENT == 'xAire' else False,
                                                 'Athens': True if EXPERIMENT == 'Athens' else False,
                                                 'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'winnings_public_goods': user.winnings_public_goods,
                                                 'tickets': user.tickets,
                                                 'username': user.nickname,
                                                 'goal': "achieved" if user.partida.objectiu_aconseguit else "no_achieved",
                                                 'bot': user.bots
                                                 },
                              context_instance=RequestContext(request))

#####################
### Survey xAire  ###
#####################

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

class SigninFormFinal1_xAire(forms.Form):
    pr1 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal1_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    user = User.objects.get(id=request.session['user'].id)
    user.status = "SURVEY_FINAL"
    user.save()

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal1_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal1_xAire(request.POST)
    enquesta_final_pr1 = form['pr1'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal1_xAire.html', {
            'pr1': enquesta_final_pr1,
            'pr1_danger': enquesta_final_pr1 is None or len(enquesta_final_pr1) == 0,
            'pr1_1_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r1' else '',
            'pr1_2_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r2' else '',
            'pr1_3_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r3' else '',
            'pr1_4_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r4' else '',
            'pr1_5_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr1'] = enquesta_final_pr1

        return redirect('user.enquestafinal2_xAire')

class SigninFormFinal2_xAire(forms.Form):
    pr2 = forms.CharField(max_length=100)
    pr3 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal2_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal2_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal2_xAire(request.POST)
    enquesta_final_pr2 = form['pr2'].value()
    enquesta_final_pr3 = form['pr3'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal2_xAire.html', {

            'pr2': enquesta_final_pr2,
            'pr2_danger': enquesta_final_pr2 is None or len(enquesta_final_pr2) == 0,
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


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr2'] = enquesta_final_pr2
        request.session['pr3'] = enquesta_final_pr3

        return redirect('user.enquestafinal3_xAire')

class SigninFormFinal3_xAire(forms.Form):
    pr4 = forms.CharField(max_length=100)
    pr5 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal3_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal3_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal3_xAire(request.POST)
    enquesta_final_pr4 = form['pr4'].value()
    enquesta_final_pr5 = form['pr5'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal3_xAire.html', {

            'pr4': enquesta_final_pr4,
            'pr4_danger': enquesta_final_pr4 is None or len(enquesta_final_pr4) == 0,
            'pr4_1_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r1' else '',
            'pr4_2_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r2' else '',
            'pr4_3_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r3' else '',
            'pr4_4_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r4' else '',
            'pr4_5_checked': 'bx-option-selected' if enquesta_final_pr4 == 'r5' else '',

            'pr5': enquesta_final_pr5,
            'pr5_danger': enquesta_final_pr5 is None or len(enquesta_final_pr5) == 0,
            'pr5_1_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r1' else '',
            'pr5_2_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r2' else '',
            'pr5_3_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r3' else '',
            'pr5_4_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r4' else '',
            'pr5_5_checked': 'bx-option-selected' if enquesta_final_pr5 == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr4'] = enquesta_final_pr4
        request.session['pr5'] = enquesta_final_pr5

        return redirect('user.enquestafinal4_xAire')

class SigninFormFinal4_xAire(forms.Form):
    pr6 = forms.CharField(max_length=100)
    pr7 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal4_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal4_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal4_xAire(request.POST)
    enquesta_final_pr6 = form['pr6'].value()
    enquesta_final_pr7 = form['pr7'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal4_xAire.html', {

            'pr6': enquesta_final_pr6,
            'pr6_danger': enquesta_final_pr6 is None or len(enquesta_final_pr6) == 0,
            'pr6_1_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r1' else '',
            'pr6_2_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r2' else '',
            'pr6_3_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r3' else '',
            'pr6_4_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r4' else '',
            'pr6_5_checked': 'bx-option-selected' if enquesta_final_pr6 == 'r5' else '',

            'pr7': enquesta_final_pr7,
            'pr7_danger': enquesta_final_pr7 is None or len(enquesta_final_pr7) == 0,
            'pr7_1_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r1' else '',
            'pr7_2_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r2' else '',
            'pr7_3_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r3' else '',


            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr6'] = enquesta_final_pr6
        request.session['pr7'] = enquesta_final_pr7

        return redirect('user.enquestafinal5_xAire')

class SigninFormFinal5_xAire(forms.Form):
    pr8 = forms.CharField(max_length=100)
    pr9 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal5_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal5_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal5_xAire(request.POST)
    enquesta_final_pr8 = form['pr8'].value()
    enquesta_final_pr9 = form['pr9'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal5_xAire.html', {

            'pr8': enquesta_final_pr8,
            'pr8_danger': enquesta_final_pr8 is None or len(enquesta_final_pr8) == 0,
            'pr8_1_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r1' else '',
            'pr8_2_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r2' else '',
            'pr8_3_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r3' else '',
            'pr8_4_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r4' else '',
            'pr8_5_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r5' else '',

            'pr9': enquesta_final_pr9,
            'pr9_danger': enquesta_final_pr9 is None or len(enquesta_final_pr9) == 0,
            'pr9_1_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r1' else '',
            'pr9_2_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r2' else '',
            'pr9_3_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r3' else '',
            'pr9_4_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r4' else '',
            'pr9_5_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr8'] = enquesta_final_pr8
        request.session['pr9'] = enquesta_final_pr9

        return redirect('user.enquestafinal6_xAire')

class SigninFormFinal6_xAire(forms.Form):
    pr10 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal6_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal6_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal6_xAire(request.POST)
    enquesta_final_pr10 = form['pr10'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal6_xAire.html', {

            'pr10': enquesta_final_pr10,
            'pr10_danger': enquesta_final_pr10 is None or len(enquesta_final_pr10) == 0,
            'pr10_1_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r1' else '',
            'pr10_2_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r2' else '',
            'pr10_3_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r3' else '',
            'pr10_4_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r4' else '',
            'pr10_5_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr10'] = enquesta_final_pr10

        return redirect('user.enquestafinal7_xAire')

class SigninFormFinal7_xAire(forms.Form):
    pr11 = forms.CharField(max_length=1000)

@csrf_exempt
def enquestafinal7_xAire(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal7_xAire.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal7_xAire(request.POST)
    enquesta_final_pr11 = form['pr11'].value()

    if not form.is_valid():
        return render_to_response('enquestafinal7_xAire.html', {
            'pr11': enquesta_final_pr11,
            'pr11_danger': enquesta_final_pr11 is None or len(enquesta_final_pr11) == 0,
            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr11'] = enquesta_final_pr11

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

        user.acabat = True
        user.date_end = timezone.now()
        user.status = "SURVEY_FINAL"

        user.save()

        return redirect('user.resultats_clima')


######################
### Survey Athens  ###
######################

class SigninFormFinal1_Athens(forms.Form):
    pr1 = forms.CharField(max_length=100)
    pr2 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal1_Athens(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    user = User.objects.get(id=request.session['user'].id)
    user.status = "SURVEY_FINAL"
    user.save()

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal1_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal1_Athens(request.POST)
    enquesta_final_pr1 = form['pr1'].value()
    enquesta_final_pr2 = form['pr2'].value()

    if not form.is_valid():
        return render_to_response('enquestafinal1_Athens.html', {
            'pr1': enquesta_final_pr1,
            'pr1_danger': enquesta_final_pr1 is None or len(enquesta_final_pr1) == 0,
            'pr1_1_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r1' else '',
            'pr1_2_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r2' else '',
            'pr1_3_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r3' else '',
            'pr1_4_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r4' else '',
            'pr1_5_checked': 'bx-option-selected' if enquesta_final_pr1 == 'r5' else '',

            'pr2': enquesta_final_pr2,
            'pr2_danger': enquesta_final_pr2 is None or len(enquesta_final_pr2) == 0,
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

        return redirect('user.enquestafinal2_Athens')

class SigninFormFinal2_Athens(forms.Form):
    pr3 = forms.CharField(max_length=100)
    pr4 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal2_Athens(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal2_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal2_Athens(request.POST)
    enquesta_final_pr3 = form['pr3'].value()
    enquesta_final_pr4 = form['pr4'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal2_Athens.html', {

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

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr3'] = enquesta_final_pr3
        request.session['pr4'] = enquesta_final_pr4

        return redirect('user.enquestafinal3_Athens')

class SigninFormFinal3_Athens(forms.Form):
    pr5 = forms.CharField(max_length=100)
    pr6 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal3_Athens(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal3_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal3_Athens(request.POST)
    enquesta_final_pr5 = form['pr5'].value()
    enquesta_final_pr6 = form['pr6'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal3_Athens.html', {

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

        return redirect('user.enquestafinal4_Athens')

class SigninFormFinal4_Athens(forms.Form):
    pr7 = forms.CharField(max_length=100)
    pr8 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal4_Athens(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal4_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal4_Athens(request.POST)
    enquesta_final_pr7 = form['pr7'].value()
    enquesta_final_pr8 = form['pr8'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal4_Athens.html', {

            'pr7': enquesta_final_pr7,
            'pr7_danger': enquesta_final_pr7 is None or len(enquesta_final_pr7) == 0,
            'pr7_1_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r1' else '',
            'pr7_2_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r2' else '',
            'pr7_3_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r3' else '',
            'pr7_4_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r4' else '',
            'pr7_5_checked': 'bx-option-selected' if enquesta_final_pr7 == 'r5' else '',

            'pr8': enquesta_final_pr8,
            'pr8_danger': enquesta_final_pr8 is None or len(enquesta_final_pr8) == 0,
            'pr8_1_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r1' else '',
            'pr8_2_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r2' else '',
            'pr8_3_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r3' else '',
            'pr8_4_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r4' else '',
            'pr8_5_checked': 'bx-option-selected' if enquesta_final_pr8 == 'r5' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr7'] = enquesta_final_pr7
        request.session['pr8'] = enquesta_final_pr8

        return redirect('user.enquestafinal5_Athens')

class SigninFormFinal5_Athens(forms.Form):
    pr9 = forms.CharField(max_length=100)
    pr10 = forms.CharField(max_length=100)

@csrf_exempt
def enquestafinal5_Athens(request, **kwargs):

    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')

    if user.acabat:
        return redirect('user.final_joc')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquestafinal5_Athens.html',
                                  {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))

    form = SigninFormFinal5_Athens(request.POST)
    enquesta_final_pr9 = form['pr9'].value()
    enquesta_final_pr10 = form['pr10'].value()


    if not form.is_valid():
        return render_to_response('enquestafinal5_Athens.html', {

            'pr9': enquesta_final_pr9,
            'pr9_danger': enquesta_final_pr9 is None or len(enquesta_final_pr9) == 0,
            'pr9_1_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r1' else '',
            'pr9_2_checked': 'bx-option-selected' if enquesta_final_pr9 == 'r2' else '',

            'pr10': enquesta_final_pr10,
            'pr10_danger': enquesta_final_pr10 is None or len(enquesta_final_pr10) == 0,
            'pr10_1_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r1' else '',
            'pr10_2_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r2' else '',
            'pr10_3_checked': 'bx-option-selected' if enquesta_final_pr10 == 'r3' else '',

            'lang': request.session['lang'], 'text': request.session['text']
        }, context_instance=RequestContext(request))

    else:
        request.session['pr9'] = enquesta_final_pr9
        request.session['pr10'] = enquesta_final_pr10

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

        user.acabat = True
        user.date_end = timezone.now()
        user.status = "SURVEY_FINAL"

        user.save()

        return redirect('user.resultats_clima')

