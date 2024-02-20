function checkLength(input) {
    var username = input.value.trim(); // ตัดช่องว่างด้านหน้าและด้านหลัง
    var englishLetters = /^[A-Za-z]+$/; // regular expression สำหรับตรวจสอบภาษาอังกฤษ
  
    if (username.length < 6 ) {
      var alertContainer = document.getElementById('username');
      var alertMessage = document.createElement('div');
      alertMessage.className = 'alert';
      alertMessage.textContent = "Username must be at least 6 characters long !";
      alertContainer.innerHTML = '';
      alertContainer.appendChild(alertMessage);
    }else if(!englishLetters.test(username)){
        var alertContainer = document.getElementById('username');
      var alertMessage = document.createElement('div');
      alertMessage.className = 'alert';
      alertMessage.textContent = "Username must be in English !";
      alertContainer.innerHTML = '';
      alertContainer.appendChild(alertMessage);

    } 
   

  }