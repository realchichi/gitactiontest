// Get references to DOM elements
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const searchHistory = document.getElementById('searchHistory');

// Event listener for search button click
searchButton.addEventListener('click', function() {
  const searchTerm = searchInput.value.trim();
  
  if (searchTerm !== '') {
    addToHistory(searchTerm);
    searchInput.value = ''; // Clear input field
  }
});

// Function to add search term to history
function addToHistory(term) {
  const searchItem = document.createElement('div');
  searchItem.textContent = term;
  searchItem.classList.add('search-item');
  searchHistory.appendChild(searchItem);
}

// Display search history when the page loads
document.addEventListener('DOMContentLoaded', function() {
  const savedHistory = JSON.parse(localStorage.getItem('searchHistory')) || [];
  savedHistory.forEach(term => addToHistory(term));
});

// Save search history to local storage when a new search is added
searchButton.addEventListener('click', function() {
  const searchTerm = searchInput.value.trim();
  
  if (searchTerm !== '') {
    addToHistory(searchTerm);
    saveHistory();
    searchInput.value = ''; // Clear input field
  }
});

// Function to save search history to local storage
function saveHistory() {
  const searchItems = Array.from(document.querySelectorAll('.search-item'));
  const searchTerms = searchItems.map(item => item.textContent);
  localStorage.setItem('searchHistory', JSON.stringify(searchTerms));
}
