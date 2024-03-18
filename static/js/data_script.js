'use strict';

const dataContainer = document.getElementById('data-container');
const prevBtn = document.getElementById('prev-page');
const nextBtn = document.getElementById('next-page');
const currentPageSpan = document.getElementById('current-page');
let cardElement = document.getElementById('card');
let currentPage = 1;
const itemsPerPage = 20;

// Fetch the first page of data when the page loads
fetchData(currentPage);

// Add event listeners for pagination buttons
nextBtn.addEventListener('click', () => {
  currentPage++;
  fetchData(currentPage);
});

prevBtn.addEventListener('click', () => {
  if (currentPage > 1) {
    currentPage--;
    fetchData(currentPage);
  }
});

document.getElementById("backButton").addEventListener("click", function() {
  console.log("backButton");
  window.location.href = '/';
});



function fetchData(page) {
  console.log(`Fetching data for page ${page}`);
  currentPage = page;

  // Calculate the offset for pagination
  const offset = (page - 1) * itemsPerPage;

  // Fetch data from the server with pagination parameters
  fetch(`/store/sensor/all?page=${currentPage}`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // **Ensure correct total_pages handling (if provided by the backend):**
      if (data.total_pages !== undefined) {
        updatePagination(data.total_pages === currentPage); // Update pagination based on total_pages
      } else {
        console.warn('total_pages not provided by server. Pagination might not work as expected.');
      }
      populateData(data.data); // Assuming data object has 'data' key for actual content
      console.log(data.total_pages); // Log the received total_pages (if available)
    })
    .catch(error => console.error(error));
}


function populateData(data) {
  console.log(`Populating data: ${data}`);
  const dataContainer = document.getElementById("data-container");
  dataContainer.innerHTML = ''; // Clear existing content

  //Check if data is an iterable array
  if (!Array.isArray(data)) {
    console.error('Data is not an array');
    return;
  }
  // Iterate over the data (assuming data is an array of arrays)
  for (let row of data) {
    // Parse the timestamp
    let date = new Date(row[3]); // Assuming timestamp is at index 3
    let formattedTimestamp = `${date.getHours()}:${date.getMinutes()} ${date.getDate()}/${date.getMonth() + 1}`;

    // Create a new card element
    let card = document.createElement('div');
    card.className = 'card card2'; // Add a class for styling

    // Create a table element for the data
    let table = document.createElement('table');

    // Create the row for the timestamp (single column)
    let timestampRow = document.createElement('tr');
    let timestampCell = document.createElement('td');
    timestampCell.colSpan = 2; // Span across both columns
    timestampCell.textContent = formattedTimestamp;
    timestampRow.appendChild(timestampCell);
    table.appendChild(timestampRow);

    // Create data rows for TVOC and eCO2
    let tvocRow = document.createElement('tr');
    let tvocCell = document.createElement('td');
    tvocCell.textContent = 'eCO2';
    tvocRow.appendChild(tvocCell);
    let tvocValueCell = document.createElement('td');
    tvocValueCell.innerHTML = '<h4>' + row[1] + '</h4>'; // Use <h4> for TVOC value
    tvocRow.appendChild(tvocValueCell);
    table.appendChild(tvocRow);

    let eco2Row = document.createElement('tr');
    let eco2Cell = document.createElement('td');
    eco2Cell.textContent = 'TVOC';
    eco2Row.appendChild(eco2Cell);
    let eco2ValueCell = document.createElement('td');
    eco2ValueCell.innerHTML = '<h4>' + row[2] + '</h4>'; // Use <h4> for eCO2 value
    eco2Row.appendChild(eco2ValueCell);
    table.appendChild(eco2Row);

    // Add the table to the card and the card to the container
    card.appendChild(table);
    dataContainer.appendChild(card);
  }
}

setInterval(updateTable, 10000);



function updatePagination(isLastPage) {
  console.log(`Updating pagination, isLastPage: ${isLastPage}`);
  currentPageSpan.textContent = `Page ${currentPage}`;
  console.log(currentPage==1);
  prevBtn.disabled = false;
  nextBtn.disabled = isLastPage;
}
