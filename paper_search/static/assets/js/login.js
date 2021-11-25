function function1(){
    username = document.getElementById("user").value;
    password = document.getElementById("pass").value;
    if(username && password){
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Wrong Password',
      })
    }
    else if(username){
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Enter Password',
        
      })
    }
    else{
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Enter Username',
        
      })
    }
    }

function function2(){
  username = document.getElementById("user1").value;
  password = document.getElementById("pass1").value;
  email = document.getElementById("email").value;
  if(ValidateEmail(email)){
    if(username && password){
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(password))
      {
          alert("sucess");
      }
      else{
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'password requierments not met',
          
          });
      }
       
    }
    else if(username){
      Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Enter Password',
      
      })
    }
    else{
      Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Enter Username',
      
      })
    }
  }
  else{
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Enter Valid Email',
      
      })
  }
}


function ValidateEmail(mail) 
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  {
    return (true)
  }
    
    return (false)
}

