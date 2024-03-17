'use strict';

// Generate the first problem
let currentProblem = generateProblem();


// Function to fetch new data and update the table
function updateTable() {
  // Fetch new data from the Python backend
  fetch('/path/to/your/api')
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