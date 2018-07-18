function Slideshow() {
    this.prefix = '';
    this.active = 'slide1';
    this.prev_milis = 100;
}

Slideshow.prototype = {

    start: function(prefix) {
        this.prefix = prefix;

        var self = this;
        $.ajax({data: null,
                url: '/admin/slidenext',
                type: 'get',
                success: function(resp) {
                    //console.log('success');
                    $('.slide1').css('backgroundImage', 'url(' + self.prefix + resp.name + '.png)');
                    self.prev_milis = resp.millis;
                },
                error: function(resp) {
                    console.log('error');
                }
        });

        $.ajax({data: null,
                url: '/admin/slidenext',
                type: 'get',
                success: function(resp) {
                    //console.log('success');
                    $('.slide2').css('backgroundImage', 'url(' + self.prefix + resp.name + '.png)');
                    self.prev_milis = resp.millis;
                },
                error: function(resp) {
                    console.log('error');
                }
        });

        $('#slider2').css('opacity',0);
        $('#slider1').css('opacity',1);
        this.show_next_slide();
    },

    show_next_slide: function() {
        if(this.active=='slide1') {
            $('#slider2').css('opacity',1);
            $('#slider1').css('opacity',0);
            this.active='slide2';
        } else {
            $('#slider1').css('opacity',1);
            $('#slider2').css('opacity',0);
            this.active='slide1';
        }

        var self = this;
        $.ajax({data: null,
                url: '/admin/slidenext',
                type: 'get',
                success: function(resp) {
                    //console.log('success');
                    if(self.active=='slide1') {
                        $('.slide2').css('backgroundImage', 'url(' + self.prefix + resp.name + '.png)');
                    } else {
                        $('.slide1').css('backgroundImage', 'url(' + self.prefix + resp.name + '.png)');
                    }
                    self.start_timeout(self.prev_milis);
                    self.prev_milis = resp.millis;
                },
                error: function(resp) {
                    console.log('error');
                    self.start_timeout(1000);
                }
        });
    },

    start_timeout: function(t) {
        var self = this;
        this.timer = setTimeout(function() {
            self.show_next_slide();
        }, t);
    }

};

slideshow = new Slideshow();
