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
      $('.nav-link').css({'margin' : '15px'});
     }
   });

  // var email = $('#email').val();
  // var password = $('#password').val();

  // // Don't close modal if invalid email or password
  // $('.submitAction').click(function() {
  //   if( email == "" || password == "" || password.length < 8){
  //       //$('#showError').show();
  //       return false;
  //   }
  //   else{
  //     return true;
  //   }
  // });

// // Function for check email format 
// function isEmail(email) {
//   var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
//   if (regex.test(email)){
//     return true;
//   }
//   else{
//     return false;
//   }
// }

})(jQuery); // End of use strict