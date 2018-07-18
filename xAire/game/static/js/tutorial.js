function Tutorial() {
    this.current = 0;
    this.count = 0;
    this.prefix = '';
    this.provar_url = '';
    this.jugar_url = '';
}

Tutorial.prototype = {

    load: function(count, prefix, provar_url, jugar_url, lang, control_reward) {
        this.current = 0;
        this.count = count;
        this.prefix = prefix;
        this.provar_url = provar_url;
        this.jugar_url = jugar_url;
        this.lang = lang;
        this.control_reward = control_reward;
    },

    start: function() {
        this.show_slide(0);
    },

    show_slide: function(id) {
        this.current = id;
        console.log(this.current)
        if (this.current == 3){
            $('.slide').attr('src', this.prefix + id + '_' + this.lang + '_' + this.control_reward + '.png');
        }else{
            $('.slide').attr('src', this.prefix + id + '_' + this.lang+ '.png');
        }

        $('.page_button_right').hide();
        if (this.current == 0) {
            $('.prev-button').attr('disabled',true);
            $('#arrow_left').attr('src','/static/img/tutorial/arrow_left_empty.png');
        } else {
            $('.prev-button').attr('disabled',false);
            $('#arrow_left').attr('src','/static/img/tutorial/arrow_left_full.png');
        }
        if (this.current == this.count - 1) {
            $('.page_button_right').show();
            $('.next-button').attr('disabled',true);
            $('#arrow_right').attr('src','/static/img/tutorial/arrow_right_empty.png');
        } else {
            $('.next-button').attr('disabled',false);
            $('#arrow_right').attr('src','/static/img/tutorial/arrow_right_full.png');
        }
    },

    show_next: function() {
        if (this.current + 1 < this.count)
            this.show_slide(this.current + 1);
    },

    show_prev: function() {
        if (this.current > 0)
            this.show_slide(this.current - 1);
    },

    provar: function() {
        window.location.href = this.provar_url;
    },

    jugar: function() {
        window.location.href = this.jugar_url;
    }
};

tutorial = new Tutorial();
