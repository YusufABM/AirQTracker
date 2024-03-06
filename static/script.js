'use strict';
// Initialize score
let score = 0;

// Get the modal


// Generate random arithmetic problem
function generateProblem() {
    let num1 = Math.floor(Math.random() * 10);
    let num2 = Math.floor(Math.random() * 10);
    let operator = ['+', '-', '*', '/'][Math.floor(Math.random() * 4)];

    document.getElementById('problem').textContent = `${num1} ${operator} ${num2}`;
    return {num1, num2, operator};
}

let currentProblem = generateProblem();

// Check answer when button is clicked
document.getElementById('check-answer').addEventListener('click', function() {
    let studentAnswer = parseFloat(document.getElementById('answer').value);
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

    if(studentAnswer === correctAnswer) {
        document.getElementById('feedback').textContent = 'Correct!';
        score++;
    } else {
        document.getElementById('feedback').textContent = 'Wrong!';
    }

    document.getElementById('score').textContent = `Score: ${score}`;
    currentProblem = generateProblem();
    document.getElementById('answer').value = '';
});


