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
    // Update the score
    document.getElementById('score').textContent = `Score: ${score}`;

    // Generate a new problem
    currentProblem = generateProblem();

    // Clear the input field
    document.querySelector('input[name="answer"]').value = '';
});

// Generate random arithmetic problem
function generateProblem() {
    let num1 = Math.floor(Math.random() * 10);
    let num2 = Math.floor(Math.random() * 10);
    let operator = ['+', '-', '*', '/'][Math.floor(Math.random() * 4)];

    // If the operator is division and num2 is 0, regenerate num2 until it's not 0
    while (operator === '/' && num2 === 0) {
    num2 = Math.floor(Math.random() * 10);
    }

    document.getElementById('problem').textContent = `${num1} ${operator} ${num2}`;
    return {num1, num2, operator};
}

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