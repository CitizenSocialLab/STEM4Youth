from django.db import models


#### USUARIS D'ADMINISTRACIO
class AdminUser(models.Model):
    email = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300) # guardar md5



class Partida(models.Model):
    num_partida = models.IntegerField()
    data_creacio = models.DateTimeField()
    data_inicialitzacio = models.DateTimeField(null=True)
    data_finalitzacio = models.DateTimeField(null=True)

    estat = models.CharField(max_length=20, default="INACTIVA") # INACTIVA, REGISTRANT, COMPLETA, ENJOC, ACABADA

    classe = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides

    num_rondes = models.IntegerField(null=True)

    ronda_actual = models.IntegerField(null=True)
    data_fi_ronda = models.DateTimeField(null=True)

    usuaris_registrats = models.IntegerField(default=0)

    guanyen_igualment = models.BooleanField(default=False) # Aquesta variable indica si es guanyen els diners si no
                                                           # s'arriba a recollir els diners objectius

    comentari = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides

    objectiu_aconseguit = models.BooleanField(default=False)

    control = models.BooleanField(default=True) # Per sabre si esteim amb el setup CONTROL o EXPERIMENTAL


#### INFORMACIO SOBRE UN JUGADOR
class User(models.Model):
    is_robot = models.BooleanField(default=False)

    # Enquesta inicial
    nickname = models.CharField(max_length=100, default="")
    codi_postal = models.CharField(max_length=6, default="")
    genere = models.CharField(max_length=1, default="")
    rang_edat = models.CharField(max_length=100, default="")
    nivell_estudis = models.CharField(max_length=100, default="")
    situacio_laboral = models.CharField(max_length=100, default="")
    estat_civil = models.CharField(max_length=100, default="")
    residencia = models.CharField(max_length=100, default="")
    origen = models.CharField(max_length=100, default="")
    pais = models.CharField(max_length=100, default="")
    ####################

    # Enquesta final
    enquesta_final_pr1 = models.CharField(max_length=100, default="")
    enquesta_final_pr2 = models.CharField(max_length=100, default="")
    enquesta_final_pr3 = models.CharField(max_length=100, default="")
    enquesta_final_pr4 = models.CharField(max_length=100, default="")
    enquesta_final_pr5 = models.CharField(max_length=100, default="")
    enquesta_final_pr6 = models.CharField(max_length=100, default="")
    enquesta_final_pr7 = models.CharField(max_length=100, default="")
    enquesta_final_pr8 = models.CharField(max_length=100, default="")
    enquesta_final_pr9 = models.CharField(max_length=100, default="")

    ####################

    num_jugador = models.IntegerField(null=True)

    data_registre = models.DateTimeField(null=True)
    data_creacio = models.DateTimeField()
    data_finalitzacio = models.DateTimeField(null=True)

    acabat = models.BooleanField(default=False)

    diners_inicials = models.IntegerField(null=True)
    diners_actuals = models.IntegerField(null=True)

    num_seleccions = models.IntegerField(default=0)
    guany_final = models.IntegerField(default=0)

    partida = models.ForeignKey(Partida, null=True)


    #Variables joc inversor
    #rol_joc_inversor1 = models.CharField(max_length=100)
    #rol_joc_inversor2 = models.CharField(max_length=100)
    #seleccio_joc_inversor1 = models.IntegerField(default=-1)
    #seleccio_joc_inversor2 = models.IntegerField(default=-1)
    #rival_joc_inversor1 = models.ForeignKey('self',null=True,blank=True, related_name='rival_inv1')
    #rival_joc_inversor2 = models.ForeignKey('self',null=True,blank=True, related_name='rival_inv2')
    #is_robot_joc_inversor1 = models.BooleanField(default=True)
    #is_robot_joc_inversor2 = models.BooleanField(default=True)
    #data_seleccio_inversor1 = models.DateTimeField(null=True)
    #data_seleccio_inversor2 = models.DateTimeField(null=True)

    # Variables joc premi
    # seleccio_joc_premi = models.CharField(max_length=1, default="")
    # guess_joc_premi = models.CharField(max_length=1, default="")
    # rival_joc_premi = models.ForeignKey('self', null=True, blank=True, related_name='rival_pres')
    # is_robot_joc_premi = models.BooleanField(default=True)
    # data_seleccio_premi = models.DateTimeField(null=True)
    # data_seleccio_guess_premi = models.DateTimeField(null=True)

    #Variables diners
    diners_clima = models.IntegerField(default=0)
    diners_trust = models.FloatField(default=0)
    diners_dictator = models.FloatField(default=0)
    diners_prisoner = models.FloatField(default=0)

    diners_total = models.FloatField(default=0)

    vals = models.IntegerField(default=0)



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

class Trust(models.Model):
    user = models.ForeignKey(User)

    # Primera tirada
    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_trust1')
    rol1 = models.CharField(max_length=100)
    seleccio1 = models.IntegerField(default=-1)
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)


    # Segona tirada
    rival2 = models.ForeignKey(User,null=True,blank=True, related_name='rival_trust2')
    rol2 = models.CharField(max_length=100)
    seleccio2 = models.IntegerField(default=-1)
    is_robot2 = models.BooleanField(default=True)
    data_seleccio2 = models.DateTimeField(null=True)
    diners_guanyats2 = models.FloatField(default=0)


class Dictator(models.Model):
    user = models.ForeignKey(User)

    # Primera tirada
    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_dictator1')
    rol1 = models.CharField(max_length=100)
    seleccio1 = models.FloatField(default=-1)
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)


    # Segona tirada
    rival2 = models.ForeignKey(User,null=True,blank=True, related_name='rival_dictator2')
    rol2 = models.CharField(max_length=100)
    seleccio2 = models.FloatField(default=-1)
    is_robot2 = models.BooleanField(default=True)
    data_seleccio2 = models.DateTimeField(null=True)
    diners_guanyats2 = models.FloatField(default=0)


class Prisoner(models.Model):
    user = models.ForeignKey(User)

    # Primera tirada
    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_prisoner1')
    guess1 = models.CharField(max_length=1, default="")
    rol1 = models.CharField(max_length=100, default="") # ADVANTAGE OR DISVANTAGE
    seleccio1 = models.CharField(max_length=1, default="")
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    data_guess1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)

    # Segona tirada
    rival2 = models.ForeignKey(User,null=True,blank=True, related_name='rival_prisoner2')
    guess2 = models.CharField(max_length=1, default="")
    rol2 = models.CharField(max_length=100, default="") # ADVANTAGE OR DISVANTAGE
    seleccio2 = models.CharField(max_length=1, default="")
    is_robot2 = models.BooleanField(default=True)
    data_seleccio2 = models.DateTimeField(null=True)
    data_guess2 = models.DateTimeField(null=True)
    diners_guanyats2 = models.FloatField(default=0)

    # Tercera tirada
    rival3 = models.ForeignKey(User,null=True,blank=True, related_name='rival_prisoner3')
    guess3 = models.CharField(max_length=1, default="")
    rol3 = models.CharField(max_length=100, default="") # ADVANTAGE OR DISVANTAGE
    seleccio3 = models.CharField(max_length=1, default="")
    is_robot3 = models.BooleanField(default=True)
    data_seleccio3 = models.DateTimeField(null=True)
    data_guess3 = models.DateTimeField(null=True)
    diners_guanyats3 = models.FloatField(default=0)




