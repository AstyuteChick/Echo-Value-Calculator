
const charDataEle = document.querySelector("#char-data");
const charData = JSON.parse(charDataEle.textContent);

const state = {
    selectedChar: null, 
    selectedTeam: null, 
    isCharMenuOpen: false
};

const elms = {
    form: document.querySelector(".calcForm"), 
    selectedChar: document.querySelector(".selectedChar"), 
    searchChar: document.querySelector("#char-search"), 
    charOptsLst: document.querySelector(".charOptsLst")
};

function setEventListeners(){
    if (!elms.form) return;
    elms.form.addEventListener("submit", handleSubmit);
    elms.searchChar.addEventListener("focus", openCharMenu);
    elms.searchChar.addEventListener("input", handleCharSearchType);
    elms.charOptsLst.addEventListener("click", handleCharSearchClick);
    document.addEventListener("click", handleOutsideClick);
};

function renderCharOpts(searchInp=""){
    const normInp = searchInp.toLowerCase().trim();
    const charNames = Object.keys(charData);
    const filteredChars = charNames.filter(function(charName){
        return charName.toLowerCase().includes(normInp);
    });
    if (filteredChars.length===0){
        elms.charOptsLst.innerHTML = `<li><span>No Characters Found</span></li>`;
        return;
    } else {
        elms.charOptsLst.innerHTML = ``;
    }
    filteredChars.forEach(function (charName){
        const li = document.createElement("li");
        const btn = document.createElement("button");
        const img = document.createElement("img");
        const spn = document.createElement("span");
        const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
        spn.textContent = charName;
        img.src = `${staticImgPath}Resonator_${cleanCharName}.webp`;
        img.classList.add("charPortrait")
        btn.type = "button";
        btn.classList.add("btn", "charOptsBtn");
        btn.dataset.charName = charName;
        btn.appendChild(img);
        btn.appendChild(spn);
        li.appendChild(btn);
        elms.charOptsLst.appendChild(li);
    });
}

function handleSubmit(event){event.preventDefault();}

function openCharMenu(){
    state.isCharMenuOpen = true;
    elms.charOptsLst.hidden = false;
    renderCharOpts(elms.searchChar.value);
}

function closeCharMenu(){
    state.isCharMenuOpen = false;
    elms.charOptsLst.hidden = true;
}

function handleCharSearchType(){
    const inpVal = elms.searchChar.value;
    openCharMenu();
    renderCharOpts(inpVal);
}

function selectChar(charName){
    if (!charName) return;
    console.log(charName);
    state.selectedChar = charName;
    elms.searchChar.value = charName;
    const img = document.createElement("img");
    const spn = document.createElement("span");
    const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
    img.src = `${staticImgPath}Resonator_${cleanCharName}.webp`;
    img.classList.add("charPortrait");
    spn.textContent = charName;
    elms.selectedChar.innerHTML = ``;
    elms.selectedChar.appendChild(img);
    elms.selectedChar.appendChild(spn);
    closeCharMenu();
}

function handleCharSearchClick(event){
    const clickedBtn = event.target.closest(".charOptsBtn");
    if (!clickedBtn) return;
    const charName = clickedBtn.dataset.charName;
    selectChar(charName);
}

function handleOutsideClick(event){
    const clickInCharOpts = event.target.closest(".charOptsLst");
    const clickInCharInp = event.target.closest(".charSearchInp");
    if (!clickInCharOpts && !clickInCharInp) {closeCharMenu();}
}

function setState(){
    if (state.isCharMenuOpen===false){
        closeCharMenu();
    } else {
        openCharMenu();
    }
    selectChar(state.selectedChar);
}

setEventListeners();

setState();
