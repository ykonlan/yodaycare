let addMedBtn = document.querySelector("#add-med");
let addMealBtn = document.querySelector("#add-meal");
let addNapBtn = document.querySelector("#add-nap");

addMedBtn.addEventListener("click", function(e){
    let emptyFormDiv = document.querySelector("#empty-med-template").content.cloneNode(true);
    let formInput = document.querySelector("input[name='meds-TOTAL_FORMS']")
    let formNumber = Number(formInput.value)
    emptyFormDiv.querySelectorAll("*").forEach(element => {
        for(let attribute of element.attributes){
            element.setAttribute(attribute.name, attribute.value.replace("__prefix__", formNumber));
        }
    });
    document.querySelector("#med-form").appendChild(emptyFormDiv);
    formInput.value = formNumber + 1;

})

addMealBtn.addEventListener("click", function(e){
    let emptyFormDiv = document.querySelector("#empty-meal-template").content.cloneNode(true);
    let formInput = document.querySelector("input[name='meals-TOTAL_FORMS']")
    let formNumber = Number(formInput.value)
    emptyFormDiv.querySelectorAll("*").forEach(element => {
        for(let attribute of element.attributes){
            element.setAttribute(attribute.name, attribute.value.replace("__prefix__", formNumber));
        }
    });
    document.querySelector("#meal-form").appendChild(emptyFormDiv);
    formInput.value = formNumber + 1;

})

addNapBtn.addEventListener("click", function(e){
    let emptyFormDiv = document.querySelector("#empty-nap-template").content.cloneNode(true);
    let formInput = document.querySelector("input[name='naps-TOTAL_FORMS']")
    let formNumber = Number(formInput.value)
    emptyFormDiv.querySelectorAll("*").forEach(element => {
        for(let attribute of element.attributes){
            element.setAttribute(attribute.name, attribute.value.replace("__prefix__", formNumber));
        }
    });
    document.querySelector("#nap-form").appendChild(emptyFormDiv);
    formInput.value = formNumber + 1;

})

