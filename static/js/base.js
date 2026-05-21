
const darkModeToggle=document.querySelector("#dark-mode");

function toggleDarkMode(event) {
    const dm=event.currentTarget.checked;
    if (dm) {document.documentElement.classList.remove("lightMode");}
    else {document.documentElement.classList.add("lightMode");}
}

darkModeToggle.addEventListener("change", toggleDarkMode);
