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


function fetchData(page) {
  // Fetch data from the server using AJAX or fetch API,
  // filtering for the specified page and number of items
  // (implementation details based on your backend)
  fetch(`/store/sensor/all`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      populateData(data);
      // updatePagination(data.length < itemsPerPage);  // Remove or modify this line
    })
    .catch(error => console.error(error));
}

function populateData(data) {
  // Clear the data container
  dataContainer.innerHTML = '';

  //Check if data is an iterable array
  if (!Array.isArray(data)) {
    console.error('Data is not an array');
    return;
  }
  // Iterate over the rows of data
  for (let row of data) {
    // Create a new card for each row
    let card = document.createElement('div');
    card.className = 'card card2';

    // Parse the timestamp and format it
    let date = new Date(row[3]);
    let formattedTimestamp = `${date.getHours()}:${date.getMinutes()} ${date.getDate()}/${date.getMonth() + 1}`;

    // Add the formatted timestamp to the card
    let timestamp = document.createElement('h3');
    timestamp.textContent = formattedTimestamp;
    card.appendChild(timestamp);

    // Add the TVOC title and value to the card
    let tvoc = document.createElement('h4');
    tvoc.innerHTML = '<span class="title">TVOC:</span> <span class="data">' + row[0] + '</span>';  // TVOC is the first element in the row
    card.appendChild(tvoc);

    // Add the eCO2 title and value to the card
    let eco2 = document.createElement('h4');
    eco2.innerHTML = '<span class="title">eCO2:</span> <span class="data">' + row[1] + '</span>';  // eCO2 is the second element in the row
    card.appendChild(eco2);

    // Add the card to the data container
    dataContainer.appendChild(card);
  }
}


function updatePagination(isLastPage) {
  currentPageSpan.textContent = `Page ${currentPage}`;
  prevBtn.disabled = currentPage === 1;
  nextBtn.disabled = isLastPage;
  console.log("updatePagination");
}
