import { fetchData, replaceProducts } from  "./functions.js"
  
const form = document.getElementById("filter-form")
form.addEventListener("submit", event => {
    event.preventDefault();
    // Get the selected price range and category
    const selectedPrice = Array.from(document.querySelectorAll(".form-price-input:checked")).map(x => x.value);
    const categories = []
    const category = document.getElementById("category-h3").textContent.trim();
    categories.push(category);
    let dataToSend = { price: selectedPrice, categories: categories }
    let url = "http://localhost:8000/products/filter_home"
    // Make a POST request to the backend view
    fetchData(url, dataToSend).then(data => {
        // Handle the response data and update the product display
        // The server should return the filtered products as JSON
        // Clear the existing products from the page
        replaceProducts(data);
    });
})