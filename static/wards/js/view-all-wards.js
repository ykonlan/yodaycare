let modal_box = document.querySelector("#modal");
let addWardBtn = document.querySelector("#add-ward");
addWardBtn.addEventListener("click", function(e){
    modal_box.classList.add("show")
})

let closeModalBtn = document.querySelector("#close-modal");
closeModalBtn.addEventListener("click", function(e){
    modal_box.classList.remove("show");
    console.log(modal_box.className);
})

modal_box.addEventListener("click", function(e) {
    if (e.target === modal_box) {
        modal_box.classList.remove("show");
    }
});

document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
        modal_box.classList.remove("show");
    }
});

let emptyFormTemplate = document.querySelector("#empty-allergy-forms");
let allergyBtn = document.querySelector("#add-allergy");
let totalFormsInput = document.querySelector("input[name='allergies-TOTAL_FORMS']");
let allergyForms = document.querySelector("#allergy-forms");


allergyBtn.addEventListener("click", function(e){
    const formIndex = Number(totalFormsInput.value);
    const newForm = emptyFormTemplate.content.cloneNode(true);

    newForm.querySelectorAll("*").forEach(element => {
        for(const attribute of element.attributes){
            element.setAttribute(attribute.name, attribute.value.replaceAll("__prefix__", formIndex))
        }
    });

    allergyForms.appendChild(newForm);
    totalFormsInput.value = formIndex + 1;
});