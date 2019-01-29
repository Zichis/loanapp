$(document).ready(function () {
  $('#generate_account_no').click(function(e){
    e.preventDefault();
    let $random_number = Math.floor(Math.random() * (999999 - 100000) + 100000);
    $('#account_number').val("PB" + $random_number);
  });

  $('.alert').alert();
});