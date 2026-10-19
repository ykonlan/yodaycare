let modal_box = document.querySelector("#modal");
let addstaffBtn = document.querySelector("#add-staff");
addstaffBtn.addEventListener("click", function(e){
    modal_box.classList.add("show")
})

let closeModalBtn = document.querySelector("#close-modal");
closeModalBtn.addEventListener("click", function(e){
    modal_box.classList.remove("show");
    console.log(modal_box.className);
})