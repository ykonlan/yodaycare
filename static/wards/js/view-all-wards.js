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