


function Game() {
}

Game.prototype = {

    update_cur_time: function(time) {
        this.curtime_ronda = time;
        var invtpc = this.curtime_ronda / this.dur_ronda;
        var tpc = (1 - invtpc);

        if (invtpc>0.66) {
            c3 = [0x3D, 0x07, 0x07, 1];
        } else if (invtpc>0.33) {
            c3 = [0x7B, 0x0F, 0x0F, 1];
        } else {
            c3 = [0xCD, 0x19, 0x19, 1];
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

        console.log('Total rondes '+data.total_rondes);

        this.num_rondes = data.total_rondes;
        this.countdown_time = data.temps_inici;
        this.control_wealth = data.control_wealth;
        this.dur_ronda = data.temps_ronda;
        this.current_ronda = data.numero_ronda;
        this.endowment_current = data.diners_inici_ronda;
        this.num_jugador = data.num_jugador;
        this.altres_jugadors = data.altres_jugadors;
        this.timer_value = 100;
        this.resposta = false;
        this.temps_espera = data.temps_espera;
        this.experiment = data.experiment;
        this.residence = data.residence;
        this.residence_name = data.residence_name;
        this.NO2 = data.NO2;
        this.school = data.school;
        this.num_schools = data.num_schools;
        this.quality = data.quality;


        console.log(this.school)
        console.log(this.NO2)
        console.log(this.residence_name)
        console.log(this.num_schools)
        console.log(this.quality)

        $('#countdown_time').text(Math.ceil(this.countdown_time/1000));
        $('#countdown-modal').modal({ backdrop: 'static', keyboard: true }).modal('show');

        if (this.experiment != "xAire"){

            $("#countdown_text_player").html("<span class='bold_countdown'>" + text_number_player + ' ' + "</span><span class='bold_countdown_color'>" + text_player + ' ' + this.num_jugador + "</span>");
            $("#countdown_text_endowment").html("<span class='bold_countdown'>" + text_endowment + ' ' + "</span><span class='bold_countdown_color'>" +  this.endowment_current + ' ' + text_monedes + "</span>");

            if (this.control_wealth == "UNEQUAL"){
                $("#countdown_text_wealth").html(text_unequal)
            }

            if (this.control_wealth == "EQUAL"){
                $("#countdown_text_wealth").html(text_equal)
            }

            $("#countdown_j1").html("<span class='bold_countdown'>" + text_player + ' ' +this.altres_jugadors[0][0]+ "</span>"+ ': ' + this.altres_jugadors[0][1] + ' ' + text_monedes);
            $("#countdown_j2").html("<span class='bold_countdown'>" + text_player + ' ' +this.altres_jugadors[1][0]+ "</span>"+ ': ' + this.altres_jugadors[1][1] + ' ' + text_monedes);
            $("#countdown_j3").html("<span class='bold_countdown'>" + text_player + ' ' +this.altres_jugadors[2][0]+ "</span>"+ ': ' + this.altres_jugadors[2][1] + ' ' + text_monedes);
            $("#countdown_j4").html("<span class='bold_countdown'>" + text_player + ' ' +this.altres_jugadors[3][0]+ "</span>"+ ': ' + this.altres_jugadors[3][1] + ' ' + text_monedes);
            $("#countdown_j5").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[4][0]+ "</span>"+ ': ' + this.altres_jugadors[4][1] + ' ' + text_monedes);

        }

        if (this.experiment == "xAire"){


            $("#countdown_text_player").html("<span class='bold_countdown'>" + text_number_player + ' ' + "</span>" +
                                             "<span class='bold_countdown_color'>" + text_player + ' ' + this.num_jugador + "</span>" + ' ' +
                                             "<span class='bold_countdown'>" + text_endowment + ' ' + "</span>" + ' ' +
                                             "<span class='bold_countdown_color'>" +  this.endowment_current + ' ' + text_monedes + "</span>");


            text_school = '';
            qualitat = '';

            if (this.num_schools == 1){
                text_school = text_school_1.replace('{school}', this.school);
            }

            if (this.num_schools == 2){
                text_school = text_school_2.replace('{school}', this.school);
            }

            if (this.lang == 'ca'){
                if (this.quality == 'Poor'){
                  qualitat = ' ('+ text_quality + ' pobra' + ').'
                }

            }
            if (this.lang == 'es'){
                if (this.quality == 'Poor'){
                  qualitat = ' ('+ text_quality + ' pobre' + ').'
                }
                if (this.quality == 'Regular'){
                  qualitat = ' ('+ text_quality + ' regular' + ').'
                }
            }
            if (this.lang == 'en'){
                if (this.quality == 'Poor'){
                  qualitat = ' (poor ' + text_quality + ').'
                }
                if (this.quality == 'Regular'){
                  qualitat = ' (regular ' + text_quality + ').'
                }
            }

            if (this.residence == "r11"){

                $("#countdown_text_endowment").html("<span class='bold_countdown'>" + text_live_barcelona + ' ' + "</span>" +
                                                "<span class='bold_countdown_color'>" +  this.NO2 + "</span>" + ' ' +
                                                "<span class='bold_countdown'>" + text_NO2_units + qualitat + "</span>" );


            }else{



                $("#countdown_text_endowment").html("<span class='bold_countdown'>" + text_school + ' ' + text_know + ' ' + "</span>" +
                                                "<span class='bold_countdown'>" + text_in + ' ' + "</span>" +
                                                "<span class='bold_countdown_color'>" + this.residence_name + "</span>" + ' '+
                                                "<span class='bold_countdown'>" + text_NO2 + ' ' + "</span>"+' '+
                                                "<span class='bold_countdown_color'>" +  this.NO2 + "</span>" + ' ' +
                                                "<span class='bold_countdown'>" + text_NO2_units + qualitat + "</span>");

            }


            $("#countdown_text_wealth").html(text_wealth)

            console.log(this.altres_jugadors)

            $("#countdown_j1").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[0][0] + "</span>" + ' ' + text_have + ' ' + "<span class='bold_countdown'>" + this.altres_jugadors[0][1] + ' ' + text_monedes);
            $("#countdown_j2").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[1][0] + "</span>" + ' ' + text_have + ' ' + "<span class='bold_countdown'>" + this.altres_jugadors[1][1] + ' ' + text_monedes);
            $("#countdown_j3").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[2][0] + "</span>" + ' ' + text_have + ' ' + "<span class='bold_countdown'>" + this.altres_jugadors[2][1] + ' ' + text_monedes);
            $("#countdown_j4").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[3][0] + "</span>" + ' ' + text_have + ' ' + "<span class='bold_countdown'>" + this.altres_jugadors[3][1] + ' ' + text_monedes);
            $("#countdown_j5").html("<span class='bold_countdown'>" + text_player + ' ' + this.altres_jugadors[4][0] + "</span>" + ' ' + text_have + ' ' + "<span class='bold_countdown'>" + this.altres_jugadors[4][1] + ' ' + text_monedes);

        }


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

        this.resposta = false;

        console.log("Inici ronda: " + this.current_ronda);
        this.timer_ronda.start_timer();

        var savings = this.endowment_current
        text_bucket_complete =  text_bucket.replace("{savings}","<span class='bold_savings'>"+ savings +"</span>")
        $('#text-bucket').html(text_bucket_complete);

        text_ronda_round = text_ronda.replace("{round}", this.current_ronda)
        text_ronda_round = text_ronda_round.replace("{total_round}",this.num_rondes)

        $('#text-ronda').text(text_ronda_round);

        if(this.endowment_current<4)  $("#button-4").hide();
        if(this.endowment_current<3)  $("#button-3").hide();
        if(this.endowment_current<2)  $("#button-2").hide();
        if(this.endowment_current<1)  $("#button-1").hide();

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
        this.endowment_current = data.diners_inici_ronda;

        this.contribucio_all_ronda = data.contribucions_ronda;
        this.ha_seleccionat = data.ha_seleccionat;

        this.contribucio_ronda_aggr = data.contribucions_ronda_aggr;
        this.endowment_current_all_ronda = data.endowment_current_all;
        this.endowment_initial_all_game = data.endowment_initial_all;

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
        $('#resultat_objectiu').text(data.threshold)

        for(i=0; i<6; i++)
        {
            if (this.id_user == this.ids[i]) {
                $('#player_'+(i+1)).css("font-weight", "bold").css("color", "#CD1919");
                $('#resultat_seleccio_'+(i+1)).css("font-weight", "bold").css("color", "#CD1919");
                $('#resultat_actual_'+(i+1)).css("font-weight", "bold").css("color", "#CD1919");
                $('#resultat_inicial_'+(i+1)).css("font-weight", "bold").css("color", "#CD1919");
            }

            if (this.ha_seleccionat[i]) robot = '';
            else robot = '*';

            $('#resultat_seleccio_'+(i+1)).text(this.contribucio_all_ronda[i]+robot);
            $('#resultat_actual_'+(i+1)).text(this.endowment_current_all_ronda[i]);
            $('#resultat_inicial_'+(i+1)).text(this.endowment_initial_all_game[i]);

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
                // ToDo: once the game finished go to survey or results
                if (game.experiment == 'xAire') {
                    window.location.href = '/' + game.lang + '/user/enquestafinal1_xAire';
                }else if (game.experiment == 'Athens'){
                    window.location.href = '/' + game.lang + '/user/enquestafinal1_Athens';
                }else{
                    window.location.href = '/'+ game.lang + '/user/resultats_clima';
                }
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


