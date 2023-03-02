import { replaceProducts, fetchData } from './functions.js';


const form = document.getElementById("filter-form")
form.addEventListener("submit", event => {
    event.preventDefault();

    // Get the selected categories and price range
    const selectedCategories = Array.from(document.querySelectorAll(".category-checkbox:checked")).map(c => c.value);
    const selectedPrice = Array.from(document.querySelectorAll(".form-price-input:checked")).map(x => x.value);
    let dataToSend = { categories: selectedCategories, price: selectedPrice };
    let url = "https://nchoof.com/products/filter_home";
    // Make a POST request to the backend view
    fetchData(url, dataToSend).then(data => {
        // Handle the response data and update the product display
        // The server should return the filtered products as JSON
        // Clear the existing products from the page
        replaceProducts(data);
    });
});
const parentCategories = document.querySelectorAll(".category-parent");
parentCategories.forEach(element => {
    element.addEventListener("change", function () {
        let valueToLower = this.value.toLowerCase();
        let childCategory = document.querySelectorAll(`.${valueToLower}-child`);
        if (this.checked) {
            childCategory.forEach(e => {
                e.hidden = false;
            }

            )
        }
        else (
            childCategory.forEach(
                e => {
                    e.childNodes[1].checked = false;
                    e.hidden = true;
                }
            )
        )
    })
})