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
    enquesta_final_pr10 = models.CharField(max_length=100, default="")
    enquesta_final_pr11 = models.CharField(max_length=100, default="")
    enquesta_final_pr12 = models.CharField(max_length=100, default="")
    enquesta_final_pr13 = models.CharField(max_length=1000, default="")

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

    #Variables diners
    diners_clima = models.IntegerField(default=0)

    diners_total = models.FloatField(default=0)

    val_abacus = models.IntegerField(default=0)
    bots = models.IntegerField(default=0)

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

