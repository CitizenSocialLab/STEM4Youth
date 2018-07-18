$(function () {
    $(".bx-push")
        .on("touchstart", function(ev) {
            //console.log("pushed-touchstart");
            $(ev.target).addClass("start-push");
        })
        .on("touchend", function(ev) {
            //console.log("pushed-touchend");
            $(ev.target).trigger("pushed");
        })
        .on("click", function(ev) {
            //console.log("pushed-click");
//            var isiPad = navigator.userAgent.toLowerCase().indexOf("ipad");
//            console.log(isiPad);
            if (isiPad==-1) {
                //console.log("pushed-click-notipad");
                $(ev.target).trigger("pushed");
            }
        });

    $(".bx-tab")
        .on("touchstart", function(ev) {
            //console.log("tab-touchstart");
        })
        .on("touchend", function(ev) {
            //console.log("tab-touchend");
            $(ev.target).trigger("selected");
        })
        .on("click", function(ev) {
//            console.log("tab-click");
//            var isiPad = navigator.userAgent.toLowerCase().indexOf("ipad");
            //console.log(isiPad);
            if (isiPad==-1) {
                //console.log("pushed-click-notipad");
                $(ev.target).trigger("selected");
            }
        });

    $(".bx-option")
        .on("touchstart", function(ev) {
            //console.log("option-touchstart");

            $(ev.target).addClass("bx-option-hover");
        })
        .on("touchend", function(ev) {
            //console.log("option-touchend");

            var name = $(ev.target).attr("name");
            var value = $(ev.target).attr("value");
            $("input[name=" + name + "][type=hidden]").attr("value", value);
            $(".bx-option[name=" + name + "]").each(function() {
                $(this).removeClass("bx-option-selected");
            });

            $(ev.target)
                .removeClass("bx-option-hover")
                .addClass("bx-option-selected");
        })
        .on("click", function(ev) {
            //console.log("pushed-option");

            $(ev.target)
                .trigger("touchstart")
                .trigger("touchend")
                .trigger("selected")
        });
});

