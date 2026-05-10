
const charData = {};

const state = {};

const elms = {
    form : document.querySelector(".calcForm")
}

function handleSubmit(event){
    event.preventDefault();
    console.log("works");
}

if (elms.form){
    elms.form.addEventListener("submit", handleSubmit);
}
