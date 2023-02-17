const form = document.getElementById("filter-form")
form.addEventListener("submit", event => {
    event.preventDefault();
    // Get the selected price range and category
    const selectedPrice = Array.from(document.querySelectorAll(".form-price-input:checked")).map(x => x.value);
    const categories = []
    const category = document.getElementById("category-h3").textContent.trim();
    categories.push(category);
    // Make a GET request to the backend view
    fetch("http://localhost:8000/products/filter_home", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': document.querySelector("input[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify({ price: selectedPrice, categories: categories })
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