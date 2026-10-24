let emptyFormDiv = document.querySelector("#empty-form-template").content;
let allergiesDiv = document.querySelector("#allergy-formset");


let addAllergyBtn = document.querySelector("#add-allergy");
addAllergyBtn.addEventListener("click", function(e){
    let emptyFormClone = emptyFormDiv.cloneNode(true);
    totalFormsInput = document.querySelector("input[name='allergies-TOTAL_FORMS']");
    let allergyFormNumber = Number(totalFormsInput.value);
    emptyFormClone.querySelectorAll("*").forEach(element => {
        for(let attrib of element.attributes){
            element.setAttribute(attrib.name, attrib.value.replace("__prefix__", allergyFormNumber));
        }
    });
    totalFormsInput.value = allergyFormNumber + 1;
    document.querySelector("#allergy-formset").appendChild(emptyFormClone);

})