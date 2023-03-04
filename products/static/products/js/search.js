import { replaceProducts, fetchData, getData } from './functions.js';

const searchForm = document.getElementById("search-form");
searchForm.addEventListener("submit", function (e) {
    e.preventDefault();
    let inputElement = document.getElementById("search-input");
    let Q = inputElement.value;
    if (Q.length > 0) {
        let url = `https://www.nchoof.com/search/${Q}`;
        getData(url).then(data => {
            replaceProducts(data);
        })
    }
    else {
        inputElement.setCustomValidity("Veuillez taper une recherche");
    }
})