let modal_box = document.querySelector("#modal");

let addstaffBtn = document.querySelector("#add-staff");

addstaffBtn.addEventListener("click", function(e) {
    modal_box.classList.add("show");
});

let closeModalBtn = document.querySelector("#close-modal");

closeModalBtn.addEventListener("click", function(e) {
    modal_box.classList.remove("show");
});

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