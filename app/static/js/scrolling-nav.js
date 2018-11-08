(function($) {
  "use strict"; // Start of use strict

  $(window).scroll(function() {
    if($(window).scrollTop() > 80){
      $('#mainNav').css({'padding' : '0px'});
      $('#myLogo').css({'height': '60px', 'width' : '60px', 'margin-left' : '5px'});
      $('#nav-link').css({'margin' : '8px'});
      $('#LoginButton').css({'margin-right' : '8px'});
     }else{
      $('#mainNav').css({'padding' : '28px'});
      $('#myLogo').css({'height': '80px', 'width' : '80px'});
      $('#nav-link').css({'margin' : '15px'});
     }
   });

})(jQuery); // End of use strict