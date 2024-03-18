'use strict';

// Button to change page
document.getElementById("datapage").addEventListener("click", function() {
    window.location.href = "/datapage";
});


// Function to update a table cell and flash it if the data is new
function updateTableCell(newData, elementId) {
  const element = document.getElementById(elementId);

  // Convert the new data and the current data to strings before comparing them
  const newDataStr = String(newData);
  const currentDataStr = String(element.textContent);

  // Only update the table cell if the new data is different from the current data
  if (newDataStr !== currentDataStr) {
    // Update the table cell with the new data
    element.textContent = newData;

    // Add the 'flash' class to the table cell
    element.classList.add('flash');

    // Remove the 'flash' class after the animation has completed
    setTimeout(() => {
      element.classList.remove('flash');
    }, 2000);  // 2000ms = 2s, the duration of the flash animation
  }
}

// Function to fetch new data and update the table
function updateTable() {
    // Fetch new data from the Python backend
    fetch('/store/sensor')
      .then(response => response.json())
      .then(data => {
        // Update the table with the new data
        updateTableCell(data.eCO2.min, 'eCO2_min');
        updateTableCell(data.eCO2.max, 'eCO2_max');
        updateTableCell(data.eCO2.latest, 'eCO2_latest');
        updateTableCell(data.TVOC.min, 'TVOC_min');
        updateTableCell(data.TVOC.max, 'TVOC_max');
        updateTableCell(data.TVOC.latest, 'TVOC_latest');
      });
  }

// Call the function to update the table
updateTable();
// Update the table every 5 seconds
setInterval(updateTable, 5000);







