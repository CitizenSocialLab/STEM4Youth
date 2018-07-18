
function TimerInterval(timeout_callback, timeout_milis, interval_callback, interval_milis) {
	this.timeout_cb = timeout_callback;
	this.timeout_milis = timeout_milis;
	this.int_cb = interval_callback;
	this.int_milis = interval_milis;
	this.timer_id = null;
	this.remaining_time = 0;
    this.paused_history = 0;
}


TimerInterval.prototype = {
	start_timer: function() {
		//Prevent double initiation.
		if(this.timer_id)
			this.stop_timer();
		this.remaining_time = this.timeout_milis;
        this.paused_history = 0;
		var self = this;
		this.timer_id = setInterval(function() { self.do_interval() }, this.int_milis);
	},


	pause_timer: function() {
        if (this.timer_id) {
    		clearTimeout(this.timer_id);
	    	this.timer_id = null;
        }
        this.paused_history ++;
	},

	resume_timer: function() {
        this.paused_history--;
        if (this.paused_history <= 0 && !this.timer_id) {
    		var self = this;
            this.paused_history = 0;
	    	this.timer_id = setInterval(function() { self.do_interval() }, this.int_milis);
        }
	},

	stop_timer: function() {
		clearTimeout(this.timer_id);
		this.timer_id = null;
        this.paused_history = 0;
	},

	do_interval: function() {
		//Calculate remaining time
		this.remaining_time -= this.int_milis;

		if(this.remaining_time <= 0) {
			//If the time expired -> invoke the timeout function
			this.stop_timer();
			this.timeout_cb();
		} else {
			this.int_cb(this.timeout_milis - this.remaining_time);
		}
	}
};
