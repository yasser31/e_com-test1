let imageField = document.querySelectorAll(".clearablefileinput");
  let defaultFields = document.querySelectorAll(".form-check");
  defaultFields.forEach(e => {
    e.hidden = true;
  })
  imageField.forEach(element => {
    element.addEventListener("change", function(){
      if (element.id.trim() === "id_product_images-0-image"){
        let defaultField = document.getElementById("div_id_product_images-0-default");
        let deleteField = document.getElementById("div_id_product_images-0-DELETE");
        defaultField.hidden = false;
        deleteField.hidden = false;
      }
      else if (element.id.trim() === "id_product_images-1-image"){
        let defaultField = document.getElementById("div_id_product_images-1-default");
        let deleteField = document.getElementById("div_id_product_images-1-DELETE");
        defaultField.hidden = false;
        deleteField.hidden = false;
      }
      else if (element.id.trim() === "id_product_images-2-image"){
        let defaultField = document.getElementById("div_id_product_images-2-default");
        let deleteField = document.getElementById("div_id_product_images-2-DELETE");
        defaultField.hidden = false;
        deleteField.hidden = false;
      }
      else if (element.id.trim() === "id_product_images-3-image"){
        let defaultField = document.getElementById("div_id_product_images-3-default");
        let deleteField = document.getElementById("div_id_product_images-3-DELETE");
        defaultField.hidden = false;
        deleteField.hidden = false;
      }
    });
  })