


function Game() {
}

Game.prototype = {

    update_cur_time: function(time) {
        this.curtime_ronda = time;
        var invtpc = this.curtime_ronda / this.dur_ronda;
        var tpc = (1 - invtpc);

        if (invtpc>0.66) {
            c3 = [0xf0, 0x66, 0x6b, 1];
        } else if (invtpc>0.33) {
            c3 = [220, 135, 0, 1];
        } else {
            c3 = [0x3f, 0xa9, 0xf5, 1];
        }

        $('#timer_progress')
            .css('width', (tpc * 100) + '%')
            .css('background-color', 'rgba(' + c3.join(',') + ')');
    },


    load_game: function(user_id, lang) {
        this.user_id = user_id;
        this.lang = lang;
    },

    start_game: function(data) {
        //console.log(data);
        console.log('Total rondes '+data.total_rondes);

        this.num_rondes = data.total_rondes;
        this.countdown_time = data.temps_inici;

        this.dur_ronda = data.temps_ronda;
        this.current_ronda = data.numero_ronda;
        this.diners_actuals = data.diners_inici_ronda;
        this.num_jugador = data.num_jugador;

        this.altres_jugadors = data.altres_jugadors;

        //console.log(this.altres_jugadors);

        this.timer_value = 100;
        this.resposta = false;

        this.temps_espera = data.temps_espera;
        $('#countdown_time').text(Math.ceil(this.countdown_time/1000));
        $('#countdown-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        $("#countdown_valor_ruleta").text(this.diners_actuals + ' ' + text_monedes).hide();
        $("#countdown_valor_jugador").text('JUGADOR '+this.num_jugador).show();

        $("#countdown_nom_j1").text('JUGADOR '+this.altres_jugadors[0][0]+':');
        $("#countdown_nom_j2").text('JUGADOR '+this.altres_jugadors[1][0]+':');
        $("#countdown_nom_j3").text('JUGADOR '+this.altres_jugadors[2][0]+':');
        $("#countdown_nom_j4").text('JUGADOR '+this.altres_jugadors[3][0]+':');
        $("#countdown_nom_j5").text('JUGADOR '+this.altres_jugadors[4][0]+':');

        $("#countdown_valor_j1").text(this.altres_jugadors[0][1] + ' ' + text_monedes);
        $("#countdown_valor_j2").text(this.altres_jugadors[1][1] + ' ' + text_monedes);
        $("#countdown_valor_j3").text(this.altres_jugadors[2][1] + ' ' + text_monedes);
        $("#countdown_valor_j4").text(this.altres_jugadors[3][1] + ' ' + text_monedes);
        $("#countdown_valor_j5").text(this.altres_jugadors[4][1] + ' ' + text_monedes);


        $("#countdown_titol").show();
        $("#countdown_time").show();
        $("#countdown_valor_ruleta").show();
        $("#countdown_valor_otros").show();

        //Setup timer and bind events
        var self = this;
        this.timer_ronda = new TimerInterval(
            function() {
                //Aquesta funcio es llança si s'ha arribat a final de ronda
                //Per tant demanem dades al server de resultat
                if(!game.resposta)
                    game.demanar_resultat();
            },
            this.dur_ronda,
            function(time) {  self.update_cur_time(time) },
            this.timer_value
        );


        var mytimer = this.countdown_time % 1000;
        this.countdown_time = this.countdown_time - mytimer;
        setTimeout(function(){game.countdown_inici()}, mytimer);
    },

    countdown_inici: function() {
        if (this.countdown_time>0) {
            $('#countdown_time').text(this.countdown_time/1000);
            this.countdown_time = this.countdown_time - 1000;
            setTimeout(function(){game.countdown_inici()}, 1000);
        } else {
            $("#countdown-modal").modal('hide');
            game.start_next_round();
        }
    },



    start_next_round: function() {
        //console.log(this.current_ronda);
        //console.log(this.rondes[this.current_ronda]);
        this.resposta = false;

        console.log("Inici ronda: " + this.current_ronda);
        this.timer_ronda.start_timer();

        $('#text-bucket').text(this.diners_actuals);
        $('#text-ronda').text(text_ronda+' '+this.current_ronda+' de 10');

        if(this.diners_actuals<4)  $("#button-4").hide();
        if(this.diners_actuals<3)  $("#button-3").hide();
        if(this.diners_actuals<2)  $("#button-2").hide();
        if(this.diners_actuals<1)  $("#button-1").hide();

        // Per a que mai puguem jugar la ronda 11
        if (this.current_ronda >= 11) {
            $('#final-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        }
    },


    end_round:function(data) {
        //console.log(data);

        //Si estava esperant amagar el dialeg
        $("#esperar-modal").modal('hide');     // dismiss the dialog


        this.next_round_time = data.temps_restant * 1000;
        this.current_ronda = data.numero_ronda;
        this.diners_actuals = data.diners_inici_ronda;

        this.contribucio_all_ronda = data.contribucions_ronda;
        this.ha_seleccionat = data.ha_seleccionat;

        this.contribucio_ronda_aggr = data.contribucions_ronda_aggr;
        this.diners_actuals_all_ronda = data.diners_actuals_all;
        this.diners_inicials_all_game = data.diners_inicials_all;

        this.total_contribucions = data.contribucions_partida;

        this.id_user = data.id_user;
        this.ids = data.ids;

        $('#ronda_imatge_refors').hide();
        $('#ronda_taula_resultats').show();


        if (!data.jugant || this.current_ronda>=11) {
            //Fem que el jocs'acabi en aquest torn
            $('#final-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
            return;
        }


        $('#ronda-modal').modal({backdrop: 'static', keyboard: true}).modal('show');

        //Engegar timer
        $('#nextround_time').text(Math.ceil(this.next_round_time / 1000));

        this.next_round_time = this.next_round_time - 1000;
        setTimeout(function () {
            game.countdown_next_round()
        }, 1000);

        $('#modal_ronda_msg').text(text_num_ronda + ' ' + (this.current_ronda - 1));

        for(i=0; i<6; i++)
        {
            if (this.id_user == this.ids[i]) {
                $('#player_'+(i+1)).css("font-weight", "bold").css("color", "#FF0000");
                $('#resultat_seleccio_'+(i+1)).css("font-weight", "bold").css("color", "#FF0000");
                $('#resultat_actual_'+(i+1)).css("font-weight", "bold").css("color", "#FF0000");
                $('#resultat_inicial_'+(i+1)).css("font-weight", "bold").css("color", "#FF0000");
            }

            if (this.ha_seleccionat[i]) robot = '';
            else robot = '*';

            $('#resultat_seleccio_'+(i+1)).text(this.contribucio_all_ronda[i]+robot);
            $('#resultat_actual_'+(i+1)).text(this.diners_actuals_all_ronda[i]);
            $('#resultat_inicial_'+(i+1)).text(this.diners_inicials_all_game[i]);

        }

        $('#resultat_total_contribucions').text(this.contribucio_ronda_aggr);
        $('#resultat_contribucio').text(this.total_contribucions);
    },




    countdown_next_round: function() {

        if (this.next_round_time>0) {
            $('#nextround_time').text(Math.ceil(this.next_round_time/1000));
            this.next_round_time = this.next_round_time - 1000;
            setTimeout(function(){game.countdown_next_round()}, 1000);
        } else {
            $("#ronda-modal").modal('hide');

            game.start_next_round();
        }
    },


    //////////////////////////////////////////////////////////////////////////////////////////
    /////////////////////////  FUNCIONS AJAX SERVER   ////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////

    // FUNCIO PER A RECOLLIR LES DADES DEL SERVER
    demanar_dades: function() {
        //console.log(this.user_id);
        $.ajax({
            url: '/es/ws/demanar_dades/'+this.user_id+'/',
            success: function(data) {
                if (data.jugant=="false") {
                    setTimeout(function(){game.demanar_dades();}, 1000);
                } else {
                    $("#welcome-modal").modal('hide');
                    game.start_game(data);
                }
            },
            error: function(data) {
                setTimeout(function(){game.demanar_dades();}, 1000);
            }
        });
    },

    //Funcio per a enviar el resultat de la ronda
    enviar_accio: function(user, ronda, accio) {
        $.ajax({
            url: '/es/ws/enviar_accio/'+user+'/'+ronda+'/'+accio+'/',
            success: function(data) {
                //console.log(data);
                if (data.saved == "ok") {
                } else {
                    game.enviar_accio(user, ronda, accio);
                }
            },
            error: function(){
                game.enviar_accio(user, ronda, accio);
            }
        });
    },


    //Funcio per a obtenir el resultat del torn
    demanar_resultat: function() {
        $.ajax({
            url: '/es/ws/demanar_resultat/'+this.user_id+'/'+game.current_ronda+'/',
            success: function(data) {
                //console.log(data);


                if (data.correcte && !data.jugant) {
                    $('#final-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
                } else if (data.correcte && data.ronda_acabada) {
                    game.end_round(data);
                } else {
                    setTimeout(function(){game.demanar_resultat()}, 500);
                }
            },
            error: function(data) {
                setTimeout(function(){game.demanar_resultat()}, 500);
            }
        });
    }
};



game = new Game();

$(document).ready(function() {

    $("#final-modal").on("shown.bs.modal", function() {    // wire up the OK button to dismiss the modal when shown
        $("#final-modal-fi").on("click", function(e) {
            $("#final-modal").modal('hide').on("hidden.bs.modal", function() {
                window.location.href = '/'+ game.lang + '/user/resultats_clima';
            });
        });
    });

    $("#button-0").on("pushed", function(e) {
        //enviar missatge al server que hem apretat C
        $('#esperar-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        game.resposta = true;
        game.enviar_accio(game.user_id,game.current_ronda,0);
        game.demanar_resultat();
    });


    $("#button-1").on("pushed", function(e) {
        //enviar missatge al server que hem apretat C
        $('#esperar-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        game.resposta = true;
        game.enviar_accio(game.user_id,game.current_ronda,1);
        game.demanar_resultat();
    });

    $("#button-2").on("pushed", function(e) {
        //enviar missatge al server que hem apretat C
        $('#esperar-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        game.resposta = true;
        game.enviar_accio(game.user_id,game.current_ronda,2);
        game.demanar_resultat();
    });



    $("#button-3").on("pushed", function(e) {
        //enviar missatge al server que hem apretat C
        $('#esperar-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        game.resposta = true;
        game.enviar_accio(game.user_id,game.current_ronda,3);
        game.demanar_resultat();
    });

    $("#button-4").on("pushed", function(e) {
        //enviar missatge al server que hem apretat C
        $('#esperar-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
        game.resposta = true;
        game.enviar_accio(game.user_id,game.current_ronda,4);
        game.demanar_resultat();
    });


    $('#welcome-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');
    game.demanar_dades();
});


