
const baseState={
    isMenuOpen: false,
    darkMode: true
}

const baseElems={
    menuBtn: document.querySelector("#prof-btn"), 
    menuToggle: document.querySelector(".menuCont"), 
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

function handleMenuToggleClick() {
    if (baseState["isMenuOpen"]) {
        baseState["isMenuOpen"]=false;
        baseElems["menuToggle"].hidden=true;
    } else {
        baseState["isMenuOpen"]=true;
        baseElems["menuToggle"].hidden=false;
    }
}

function handleBaseOutsideClick(event) {
    const clickInProfMenu=event.target.closest(".menuCont");
    const clickOnProfBtn=event.target.closest("#prof-btn");
    if (!clickInProfMenu && !clickOnProfBtn) {
        baseState["isMenuOpen"]=false;
        baseElems["menuToggle"].hidden=true;
    }
}

function setBaseState() {
    const theme=localStorage.getItem("theme")||"dark";
    if (theme==="dark") {toggleDarkMode(true);}
    else {toggleDarkMode(false);}
}

function setBaseEventListeners() {
    baseElems["darkModeToggle"].addEventListener("change", handleDarkModeChange);
    baseElems["menuBtn"].addEventListener("click", handleMenuToggleClick);
    document.addEventListener("click", handleBaseOutsideClick);
}

setBaseEventListeners();
setBaseState();
