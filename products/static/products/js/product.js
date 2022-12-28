document.addEventListener("DOMContentLoaded", function() {
  const checkboxes = document.querySelectorAll("input[type='checkbox']");
  const addToCartButton = document.getElementById("add-to-cart-button");

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
      const variationInput = document.getElementById("variation");
      const selectedCheckboxes = document.querySelectorAll("input[type='checkbox']:checked");
      let variationIds = [];

      selectedCheckboxes.forEach(function(selectedCheckbox) {
        variationIds.push(selectedCheckbox.value);
      });

      variationInput.value = variationIds.join(",");
    });
  });
});
