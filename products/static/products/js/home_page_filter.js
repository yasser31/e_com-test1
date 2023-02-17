const form = document.getElementById("filter-form")
form.addEventListener("submit", event => {
    event.preventDefault();

    // Get the selected categories and price range
    const selectedCategories = Array.from(document.querySelectorAll(".category-checkbox:checked")).map(c => c.value);
    const selectedPrice = Array.from(document.querySelectorAll(".form-price-input:checked")).map(x => x.value);
    // Make a GET request to the backend view
    fetch("http://localhost:8000/products/filter_home", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': document.querySelector("input[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify({ categories: selectedCategories, price: selectedPrice })
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response data and update the product display
            // The server should return the filtered products as JSON
            // Clear the existing products from the page
            const cards = document.querySelectorAll('.product-card');
            cards.forEach(card => card.remove());
            let productContainer = document.getElementById('cards-row');
            for (let i = 0; i < data.products.length; i++) {
                let imageUrl = null;
                let product = data.products[i];
                let productCard = document.createElement("div");
                productCard.classList.add("col-md-3");
                productCard.classList.add("product-card");
                if (product.images.length === 0) {
                    imageUrl = "/static/products/img/no-image.jpg";
                }
                else {
                    for (let i = 0; i < product.images.length; i++) {
                        let image = product.images[i];
                        if (image.default === true) {
                            imageUrl = image.url;
                        }
                    }
                }

                productCard.innerHTML = `<div class="card-sl">
              <img src="${imageUrl}" id="card-img">
              <div class="card-heading">
                 ${product.name}
              </div>
              <div class="card-text">
                 Contact : ${product.contact}
                 <br>
                  ${product.price} DA
              </div>
              <a href="products/${product.id}" class="card-button">Détails</a>
              </div>`;
                productContainer.appendChild(productCard)
            }
        });
})
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