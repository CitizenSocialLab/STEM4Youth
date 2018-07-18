from django.db import models


#### USUARIS D'ADMINISTRACIO
class AdminUser(models.Model):
    email = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300) # guardar md5


class Pollution(models.Model):
    district = models.CharField(max_length=100, null=True)
    NO2 = models.FloatField(default=0)
    tag = models.CharField(max_length=10, null=False)
    level = models.CharField(max_length=10, null=True)
    school = models.CharField(max_length=100, null=True)
    num_schools = models.IntegerField(null=True)
    quality = models.CharField(max_length=100, null=True)


####
class Partida(models.Model):
    num_partida = models.IntegerField()

    date_creation = models.DateTimeField()
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    status = models.CharField(max_length=20, default="INACTIVA") # INACTIVA, REGISTERING, COMPLETA, ENJOC, ACABADA

    experiment = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides

    num_rondes = models.IntegerField(null=True)

    ronda_actual = models.IntegerField(null=True)
    data_fi_ronda = models.DateTimeField(null=True)

    usuaris_registrats = models.IntegerField(default=0)

    # Varibles de control
    control_reward = models.CharField(max_length=10, null=False, default='SOCIAL') # SOCIAL vs ECONOMIC
    control_wealth = models.CharField(max_length=10, null=False, default='EQUAL') # EQUAL vs UNEQUAL
    control_uncertainly = models.IntegerField(default=0) # UNCERTAINLY value

    always_win = models.BooleanField(default=False)

    comentari = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides

    objectiu_aconseguit = models.BooleanField(default=False)
    total_contributed = models.IntegerField(null=True)
    total_social_action = models.IntegerField(null=True)

class User(models.Model):
    is_robot = models.BooleanField(default=False)

    # Initial survey
    nickname = models.CharField(max_length=100, default="")
    consent = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, default="")
    age_range = models.CharField(max_length=100, default="")
    educational_level = models.CharField(max_length=100, default="")
    economic_status = models.CharField(max_length=100, default="")
    working_status = models.CharField(max_length=100, default="")
    residence = models.CharField(max_length=100, default="")
    pollution = models.ForeignKey(Pollution, null=True)


    # Framing

    frame_pr1 = models.CharField(max_length=100, default="")
    frame_pr2 = models.CharField(max_length=100, default="")
    frame_pr3 = models.CharField(max_length=100, default="")

    # Verification

    verification_pr1 = models.CharField(max_length=100, default="")
    verification_pr2 = models.CharField(max_length=100, default="")
    verification_pr3 = models.CharField(max_length=100, default="")
    verification_pr4 = models.CharField(max_length=100, default="")

    # Final survey
    enquesta_final_pr1 = models.CharField(max_length=100, default="")
    enquesta_final_pr2 = models.CharField(max_length=100, default="")
    enquesta_final_pr3 = models.CharField(max_length=100, default="")
    enquesta_final_pr4 = models.CharField(max_length=100, default="")
    enquesta_final_pr5 = models.CharField(max_length=100, default="")
    enquesta_final_pr6 = models.CharField(max_length=100, default="")
    enquesta_final_pr7 = models.CharField(max_length=100, default="")
    enquesta_final_pr8 = models.CharField(max_length=100, default="")
    enquesta_final_pr9 = models.CharField(max_length=100, default="")
    enquesta_final_pr10 = models.CharField(max_length=100, default="")
    enquesta_final_pr11 = models.CharField(max_length=1000, default="")

    ####################
    partida = models.ForeignKey(Partida, null=True)

    status = models.CharField(max_length=100, default="")

    num_jugador = models.IntegerField(null=True)

    date_tutorial = models.DateTimeField(null=True)
    date_register = models.DateTimeField(null=True)
    date_creation = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    acabat = models.BooleanField(default=False)
    num_seleccions = models.IntegerField(default=0)
    bots = models.IntegerField(default=0)

    endowment_initial = models.IntegerField(default=0,null=True)
    endowment_current = models.IntegerField(default=0,null=True)
    contributed_public_goods = models.IntegerField(default=0,null=True)
    winnings_public_goods = models.IntegerField(default=0,null=True)
    savings_public_goods = models.IntegerField(default=0,null=True)
    coins_total = models.FloatField(default=0)
    tickets = models.IntegerField(default=0,null=True)

    comment = models.CharField(max_length=1000, default="")


class Ronda(models.Model):
    partida = models.ForeignKey(Partida)
    num_ronda = models.IntegerField()

    bucket_inici_ronda = models.IntegerField(null=True)
    bucket_final_ronda = models.IntegerField(null=True)

    temps_inici_ronda = models.DateTimeField(null=True)
    temps_final_ronda = models.DateTimeField(null=True)

    calculada = models.BooleanField(default=False)

class UserRonda(models.Model):
    ronda = models.ForeignKey(Ronda)
    #Afegir dummy
    user = models.ForeignKey(User)

    ha_seleccionat = models.BooleanField(default=False)
    seleccio = models.IntegerField(null=True)
    temps_seleccio = models.DateTimeField(null=True)

