from django.conf.urls import patterns, url

import views
import views_game
import views_user
import views_admin
import views_ws

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

     url(r'^((?P<lang>[\w-]+)/)?$', views.index, name='index'),

     url(r'^((?P<lang>[\w-]+)/)?user$', views_user.index),
     url(r'^((?P<lang>[\w-]+)/)?user/logout$', views_user.logout, name="user.logout"),

     url(r'^((?P<lang>[\w-]+)/)?user/nickname$', views_user.nickname, name="user.nickname"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquesta1$', views_user.enquesta1, name="user.enquesta1"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquesta2$', views_user.enquesta2, name="user.enquesta2"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinalintro$', views_user.enquestafinalintro, name="user.enquestafinalintro"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal1$', views_user.enquestafinal1, name="user.enquestafinal1"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal2$', views_user.enquestafinal2, name="user.enquestafinal2"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal3$', views_user.enquestafinal3, name="user.enquestafinal3"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal4$', views_user.enquestafinal4, name="user.enquestafinal4"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal5$', views_user.enquestafinal5, name="user.enquestafinal5"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal6$', views_user.enquestafinal6, name="user.enquestafinal6"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal7$', views_user.enquestafinal7, name="user.enquestafinal7"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquestafinal8$', views_user.enquestafinal8, name="user.enquestafinal8"),

     url(r'^((?P<lang>[\w-]+)/)?user/inici', views_user.inici, name="user.inici"),
     url(r'^((?P<lang>[\w-]+)/)?user/final_joc', views_user.final_joc, name="user.final_joc"),
     url(r'^((?P<lang>[\w-]+)/)?user/resultats_clima', views_user.resultats_clima, name="user.resultats_clima"),

     url(r'^((?P<lang>[\w-]+)/)?game$', views_game.index, name='game.index'),
     url(r'^((?P<lang>[\w-]+)/)?game/tutorial$', views_game.tutorial, name='game.tutorial'),

     url(r'^((?P<lang>[\w-]+)/)?admin$', views_admin.registre, name='admin.admin'),
     url(r'^((?P<lang>[\w-]+)/)?admin/registre$', views_admin.registre, name='admin.registre'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida$', views_admin.partida, name='admin.partida'),
     url(r'^((?P<lang>[\w-]+)/)?admin/stats$', views_admin.stats, name='admin.stats'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users$', views_admin.users, name='admin.users'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users/reset/(?P<user_id>\d+)$', views_admin.users_reset, name='admin.users_reset'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_list$', views_admin.partida_list, name='admin.partida_list'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_detail/(?P<num_partida>\d+)/$', views_admin.partida_detail, name='admin.partida_detail'),


     url(r'^((?P<lang>[\w-]+)/)?ws/usuaris_registrats/', views_ws.usuaris_registrats, name='ws.usuaris_registrats'),
     url(r'^((?P<lang>[\w-]+)/)?ws/estat_partida/', views_ws.estat_partida, name='ws.estat_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/llistat_partides/', views_ws.llistat_partides, name='ws.llistat_partides'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida/', views_ws.stats_partida, name='ws.stats_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/tancar_ronda/(?P<num_partida>\d+)/', views_ws.tancar_ronda, name='ws.tancar_ronda'),
     url(r'^((?P<lang>[\w-]+)/)?ws/tancar_partida/(?P<num_partida>\d+)/', views_ws.tancar_partida, name='ws.tancar_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_resultat_partida/', views_ws.demanar_resultat_partida, name='ws.demanar_resultat_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida_detail/(?P<num_partida>\d+)/', views_ws.stats_partida_detail, name='ws.stats_partida_detail'),


     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_dades/(?P<user_id>\d+)/', views_ws.demanar_dades, name='ws.demanar_dades'),
     url(r'^((?P<lang>[\w-]+)/)?ws/enviar_accio/(?P<user_id>\d+)/(?P<ronda_id>\d+)/(?P<result>[\w-]+)', views_ws.enviar_accio, name='ws.enviar_accio'),
     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_resultat/(?P<user_id>\d+)/(?P<ronda_id>\d+)/', views_ws.demanar_resultat, name='ws.demanar_resultat'),


)
