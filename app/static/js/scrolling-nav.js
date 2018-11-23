(function($) {
  "use strict"; // Start of use strict

  // Scrolling navigation bar
  $(window).scroll(function() {
    if($(window).scrollTop() > 80){
      $('.mainNav').css({'padding' : '0px'});
      $('.myLogo').css({'height': '60px', 'width' : '60px', 'margin-left' : '5px'});
      $('.nav-link').css({'margin' : '8px'});
      $('.LoginButton').css({'margin-right' : '8px'});
      $('.SignOutButton').css({'margin-right' : '8px'});
     }else{
      $('.mainNav').css({'padding' : '28px'});
      $('.myLogo').css({'height': '80px', 'width' : '80px', 'margin-left' : '10px'});
      $('.nav-link').css({'margin-left' : '40px', 'margin-right' : '40px'});
     }
   });

  $('a.pricingLink').click(function () {
        $('.overlay, .popup').toggle('fast');
        $('.overlay, .popup').fadeOut(1400);
        return false;
      });

  $('.ShowEdit').click(function(){
      $('.UpdateForm').show(500);
      $('.ShowEdit').hide(500);
  });
  
  $('.UpdateButton').click(function(){
      $('.UpdateForm').hide(1000);
      $('.ShowEdit').show(1000);
  });

})(jQuery); // End of use strict