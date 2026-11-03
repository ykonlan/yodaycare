let modal_box = document.querySelector("#modal");

let addParentBtn = document.querySelector("#add-parent");

addParentBtn.addEventListener("click", function() {
    modal_box.classList.add("show");
});

let closeModalBtn = document.querySelector("#close-modal");

closeModalBtn.addEventListener("click", function() {
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