let modal_box = document.querySelector("#modal");
let addParentBtn = document.querySelector("#add-parent");
addParentBtn.addEventListener("click", function(e){
    modal_box.classList.add("show")
})

let closeModalBtn = document.querySelector("#close-modal");
closeModalBtn.addEventListener("click", function(e){
    modal_box.classList.remove("show");
    console.log(modal_box.className);
})

