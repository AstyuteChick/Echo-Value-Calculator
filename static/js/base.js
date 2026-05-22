
const baseState={
    isMenuOpen: false,
    darkMode: true
}

const baseElems={
    darkModeToggle: document.querySelector("#dark-mode")
}

function toggleDarkMode(state) {
    if (state) {
        baseState["darkMode"]=true;
        document.documentElement.classList.remove("lightMode");
        baseElems["darkModeToggle"].checked=true;
        localStorage.setItem("theme", "dark");
    }
    else {
        baseState["darkMode"]=false;
        document.documentElement.classList.add("lightMode");
        baseElems["darkModeToggle"].checked=false;
        localStorage.setItem("theme", "light");
    }
}

function handleDarkModeChange(event) {
    const dm=event.currentTarget.checked;
    toggleDarkMode(dm);
}

function setBaseState() {
    const theme=localStorage.getItem("theme")||"dark";
    if (theme==="dark") {toggleDarkMode(true);}
    else {toggleDarkMode(false);}
}

function setBaseEventListeners() {baseElems["darkModeToggle"].addEventListener("change", handleDarkModeChange);}

setBaseEventListeners();
setBaseState();
