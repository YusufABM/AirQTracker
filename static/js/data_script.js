'use strict';

const dataContainer = document.getElementById('data-container');
const prevBtn = document.getElementById('prev-page');
const nextBtn = document.getElementById('next-page');
const currentPageSpan = document.getElementById('current-page');
let cardElement = document.getElementById('card');
let currentPage = 1;
const itemsPerPage = 20;


function fetchData(page) {
  // Fetch data from the server using AJAX or fetch API,
  // filtering for the specified page and number of items
  // (implementation details based on your backend)
  fetch(`/store/sensor?page=<span class="math-inline">\{page\}&limit\=</span>{itemsPerPage}`)
    .then(response => response.json())
    .then(data => {
      populateData(data);
      updatePagination(data.length < itemsPerPage);
    })
    .catch(error => console.error(error));
}

function populateData(data) {
  dataContainer.innerHTML = ''; // Clear existing content
  for (const item of data) {
    const card = document.createElement('div');
    card.classList.add('data-card');
    // Build the card content using item properties (e.g., eCO2, TVOC, timestamp)
    card.innerHTML = `
      <h3>eCO2: ${item.eCO2_value}</h3>
      <h3>TVOC: ${item.TVOC_value}</h3>
      <p>Timestamp: ${item.timestamp}</p>
    `;
    dataContainer.appendChild(card);
  }
  if(date == null){
    console.log("date is null");
  } else {
    console.log("date is not null");
  }
}

function updatePagination(isLastPage) {
  currentPageSpan.textContent = `Page ${currentPage}`;
  prevBtn.disabled = currentPage === 1;
  nextBtn.disabled = isLastPage;
}
