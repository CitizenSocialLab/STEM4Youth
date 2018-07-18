function Tutorial() {
    this.current = 0;
    this.count = 0;
    this.prefix = '';
    this.provar_url = '';
    this.jugar_url = '';
}

Tutorial.prototype = {

    load: function(count, prefix, provar_url, jugar_url, lang) {
        this.current = 0;
        this.count = count;
        this.prefix = prefix;
        this.provar_url = provar_url;
        this.jugar_url = jugar_url;
        this.lang = lang;
    },

    start: function() {
        this.show_slide(0);
    },

    show_slide: function(id) {
        this.current = id;
        $('.slide').attr('src', this.prefix + id + '_' + this.lang + '.png');
        $('.page_button_right').hide();
        if (this.current == 0) {
            $('.prev-button').attr('disabled',true);
            $('#arrow_left').attr('src','/static/img/arrow_left_clara.png');
        } else {
            $('.prev-button').attr('disabled',false);
            $('#arrow_left').attr('src','/static/img/arrow_left.png');
        }
        if (this.current == this.count - 1) {
            $('.page_button_right').show();
            $('.next-button').attr('disabled',true);
            $('#arrow_right').attr('src','/static/img/arrow_right_clara.png');
        } else {
            $('.next-button').attr('disabled',false);
            $('#arrow_right').attr('src','/static/img/arrow_right.png');
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
