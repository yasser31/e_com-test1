export function replaceProducts(data) {
    let contextMessages = document.querySelector('.message-section');
    contextMessages.innerHTML = "";
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => card.remove());
    const productContainer = document.getElementById('cards-row');
    productContainer.innerHTML = '';
    if (data.products.length === 0) {
        const message = document.createElement("p");
        message.classList.add("filter-message");
        message.classList.add("btn-danger");
        const messageTextNode = document.createTextNode("Aucun produit ne correspond à votre recherche/filtre");
        message.appendChild(messageTextNode);
        productContainer.appendChild(message);
    }
    else {
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
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function fetchData(url, dataObj) {
    const csrftoken = getCookie('csrftoken');
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(dataObj)
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response data and update the product display
            // The server should return the filtered products as JSON
            // Clear the existing products from the page
            return data;
        });
}

export function getData(url) {
    return fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response data and update the product display
            // The server should return the filtered products as JSON
            // Clear the existing products from the page
            return data;
        });
}