'use strict';

// Generate the first problem
let currentProblem = generateProblem();


// Initialize the score and display it
let score = 0;
document.getElementById('score').textContent = `Score: ${score}`;
let scoreElement = document.getElementById('score');
let cardElement = document.getElementById('card');

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from being submitted in the traditional way
    var answer = document.querySelector('input[name="answer"]').value;
    // Check if the answer is not a number
    if (isNaN(answer)) {
        console.log('Please enter a valid number');
        return;  // Exit the function
    }

    if (checkAnswer(answer)) {
        score++;
        scoreElement.classList.add('correct');

        // Remove the class after the animation completes
        setTimeout(() => {
        scoreElement.classList.remove('correct');
        }, 1000); // 1000ms = 1s, which is the duration of the animation

    }else {
        score--;
        if (score < 0) {
            score = 0;
        }
        cardElement.classList.add('wrong');
        setTimeout(() => {
          cardElement.classList.remove('wrong');
        }, 300); // 500ms = 0.5s, which is the duration of the animation
    }
    updateTable();
});

// Function to fetch new data and update the table
function updateTable() {
    // Fetch new data from the Python backend
    fetch('/store/sensor')
      .then(response => response.json())
      .then(data => {
        // Update the table with the new data
        document.getElementById("eCO2_min").textContent = data.eCO2.min;
        document.getElementById("eCO2_max").textContent = data.eCO2.max;
        document.getElementById("eCO2_latest").textContent = data.eCO2.latest;
        document.getElementById("TVOC_min").textContent = data.TVOC.min;
        document.getElementById("TVOC_max").textContent = data.TVOC.max;
        document.getElementById("TVOC_latest").textContent = data.TVOC.latest;
      });
  }

  // Call the function to update the table
  updateTable();
  // Update the table every 5 seconds
  setInterval(updateTable, 5000);


function checkAnswer(data) {

    let studentAnswer = parseFloat(data.replace(',', '.'));
    let correctAnswer;


    switch(currentProblem.operator) {
        case '+':
            correctAnswer = currentProblem.num1 + currentProblem.num2;
            break;
        case '-':
            correctAnswer = currentProblem.num1 - currentProblem.num2;
            break;
        case '*':
            correctAnswer = currentProblem.num1 * currentProblem.num2;
            break;
        case '/':
            correctAnswer = currentProblem.num1 / currentProblem.num2;
            break;
    }

    // Round the correct answer to 2 decimal points
    correctAnswer = parseFloat(correctAnswer.toFixed(2));

    if(studentAnswer === correctAnswer) {
        return true;
    } else {
        return false;
    }
};