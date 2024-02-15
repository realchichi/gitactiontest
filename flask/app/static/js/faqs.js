document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll('.faq li .question');
  
    questions.forEach(function(question) {
      question.addEventListener('click', function() {
        this.querySelector('.plus-minus-toggle').classList.toggle('collapsed');
        this.parentElement.classList.toggle('active');
      });
    });
  });