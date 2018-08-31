//**********************  Start with disable/enable scroll function  **********************
// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36

var keys = [37, 38, 39, 40];

function preventDefault(e) {
    e = e || window.event;
    if (e.preventDefault)
        e.preventDefault();
    e.returnValue = false;
}

function keydown(e) {
    for (var i = keys.length; i--;) {
        if (e.keyCode === keys[i]) {
            preventDefault(e);
            return;
        }
    }
}

function wheel(e) {
    preventDefault(e);
}

function disable_scroll() {
    if (window.addEventListener) {
        window.addEventListener('DOMMouseScroll', wheel, false);
    }
    window.onmousewheel = document.onmousewheel = wheel;
    document.onkeydown = keydown;
}

function enable_scroll() {
    if (window.removeEventListener) {
        window.removeEventListener('DOMMouseScroll', wheel, false);
    }
    window.onmousewheel = document.onmousewheel = document.onkeydown = null;
}

//**********************  End with disable/enable scroll function  **********************



jQuery(function($) {

        $(".sidebar-dropdown > a").click(function(){
	        $(".sidebar-submenu").slideUp(250);
        	if ($(this).parent().hasClass("active")){
 		         $(".sidebar-dropdown").removeClass("active");
 		         $(this).parent().removeClass("active");
        	}else{
        		$(".sidebar-dropdown").removeClass("active");
        		$(this).next(".sidebar-submenu").slideDown(250);
        	 	$(this).parent().addClass("active");

        	}

        });

        $("#toggle-sidebar").click(function(){
	         $(".page-wrapper").toggleClass("toggled");
             if($('.black_overlay').css('display') === 'block'){
                $('.black_overlay').css('display','none');
                // $("body").removeClass('hide_scrollbar');
                enable_scroll();
                
             }
             else{
                $('.black_overlay').css('display','block');
                // $("body").addClass('hide_scrollbar');
                disable_scroll();
             }
       	 });

        $(".sidebar-menu textarea").mousewheel(function(e,delta){
            enable_scroll();
            if($(".sidebar-menu textarea").scrollTop() + $(".sidebar-menu textarea").height()+5 >= $('.sidebar-menu textarea').prop('scrollHeight')) {
                if(delta < 0) {  
                    e.preventDefault();
                    return false;
                }
            }
            if($(".sidebar-menu textarea").scrollTop() === 0) {
                if(delta > 0) {
                   e.preventDefault();
                   return false;
                }
            }
        })

        $(".sidebar-menu textarea").mouseleave(function(){
            disable_scroll();
        })

        $(".black_overlay").click(function(){ 
            $("#toggle-sidebar").trigger('click');
        });

        $(".page-content").animate({left:'250px'});

        if(! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            $(".sidebar-content").mCustomScrollbar({
                            axis:"y",
                            autoHideScrollbar: true,
                            scrollInertia:300
            });
            $(".sidebar-content").addClass("desktop");
        }

});
