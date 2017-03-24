function validateForm() {

  // password == confirm_password validation
  var pass = document.forms["signupform"]["password"].value;
  var conf_pass = document.forms["signupform"]["confirm_password"].value;
  if (pass != conf_pass) {
    alert("Password is not matched");
    document.forms["signupform"]["password"].style.borderColor = "#E34234";
    document.forms["signupform"]["confirm_password"].style.borderColor = "#E34234";
    return false;
  }


  // phone-number validation
  var phon = document.forms["signupform"]["mobile_number"].value;

  if(!phon.match(/^[789]\d{9}$/)){
    alert("Please enter proper formated mobile number.....");
    return false;
  }

}

function go(){
  var usr = document.forms["signupform"]["user_type"].value;
  if(usr == "Customer"){
    $('#hidden_div').addClass("hidden_data");
  }
  else{
    $('#hidden_div').removeClass("hidden_data");
  }

}
