
const charDataEle = document.querySelector("#char-data");
const charData = JSON.parse(charDataEle.textContent); //Character.data

const echoDataEle = document.querySelector("#echo-data");
const echoData = JSON.parse(echoDataEle.textContent); //GameData.substat_names (ordered substat names, list)
const substatRollsEle = document.querySelector("#substat-rolls-data");
const substatRollsData = JSON.parse(substatRollsEle.textContent); //GameData.substat_rolls (dict -> statName: list of rolls)

const state = {
    selectedChar: `Aemeath`, 
    isCharMenuOpen: false, 
    selectedTeam: null, 
    totEr: 100.0
};

const elms = {
    form: document.querySelector(".calcForm"), 
    selectedChar: document.querySelector(".selectedChar"), 
    searchChar: document.querySelector("#char-search"), 
    charOptsLst: document.querySelector(".charOptsLst"), 
    teamSlct: document.querySelector("#team-select"),
    totErIn: document.querySelector("#tot-er"), 
    scoreVal: document.querySelector(".scoreVal"), 
    tierVal: document.querySelector(".tierVal")
};

function renderCharOpts(searchInp=""){
    const normInp = searchInp.toLowerCase().trim();
    const charNames = Object.keys(charData);
    const filteredChars = charNames.filter(function(charName){return charName.toLowerCase().includes(normInp);});
    if (filteredChars.length===0){
        elms["charOptsLst"].innerHTML = `<li><span>No Characters Found</span></li>`;
        return;
    }
    elms["charOptsLst"].innerHTML = ``;
    filteredChars.forEach(function (charName){
        const li = document.createElement("li");
        const btn = document.createElement("button");
        const img = document.createElement("img");
        const spn = document.createElement("span");
        const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
        spn.textContent = charName;
        img.src = `${staticImgPath}Resonator_${cleanCharName}.webp`;
        img.classList.add("charPortrait");
        btn.type = "button";
        btn.classList.add("btn", "charOptsBtn");
        btn.dataset.charName = charName;
        btn.appendChild(img);
        btn.appendChild(spn);
        li.appendChild(btn);
        elms["charOptsLst"].appendChild(li);
    });
}

function renderTeamOpts(charName){
    elms["teamSlct"].innerHTML = `<option value="">Select your character's team</option>`;
    const charTeams = Object.keys(charData[charName][1][0]);
    charTeams.forEach(function (team){
        const opt = document.createElement("option");
        opt.value = team;
        opt.textContent = team;
        elms.teamSlct.appendChild(opt);
    });
    state["selectedTeam"] = null;
    elms["teamSlct"].value = "";
}

function handleSubmit(event){event.preventDefault();}

function handleCharSearchFocus(){
    if (elms["searchChar"].value) {elms["searchChar"].value = "";}
    openCharMenu();
}

function openCharMenu(){
    elms["charOptsLst"].hidden = false;
    state["isCharMenuOpen"] = true;
    renderCharOpts(elms["searchChar"].value);
}

function closeCharMenu(){
    elms["charOptsLst"].hidden = true;
    elms["searchChar"].value = state.selectedChar;
    state["isCharMenuOpen"] = false;
}

function handleCharSearchType(){renderCharOpts(elms["searchChar"].value);}

function selectChar(charName){
    if (!charName) return;
    state["selectedChar"] = charName;
    elms["searchChar"].value = charName;
    const img = document.createElement("img");
    const spn = document.createElement("span");
    const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
    img.src = `${staticImgPath}Resonator_${cleanCharName}.webp`;
    img.classList.add("charPortrait");
    spn.textContent = charName;
    elms["selectedChar"].innerHTML = ``;
    elms["selectedChar"].appendChild(img);
    elms["selectedChar"].appendChild(spn);
    closeCharMenu();
    renderTeamOpts(charName);
    state["totEr"]=100.0;
    elms["totErIn"].value="";
}

function handleCharSearchClick(event){
    const clickedBtn = event.target.closest(".charOptsBtn");
    if (!clickedBtn) return;
    selectChar(clickedBtn.dataset.charName);
}

function handleOutsideClick(event){
    const clickInCharOpts = event.target.closest(".charOptsLst");
    const clickInCharInp = event.target.closest(".charSearchInp");
    if (!clickInCharOpts && !clickInCharInp) {closeCharMenu();}
}

function handleTeamChange(event){
    const slctTeamVal = event.target.value;
    if (slctTeamVal === "") {
        state["selectedTeam"] = null;
    } else {
        state["selectedTeam"] = slctTeamVal;
    }
}

function handleTotErFocus(){
    if (elms["totErIn"].value) {elms["totErIn"].value="";}
}

function handleTotErType(){
    state["totEr"] = elms["totErIn"].value;
}

function setEventListeners(){
    elms["form"].addEventListener("submit", handleSubmit);
    elms["searchChar"].addEventListener("focus", handleCharSearchFocus);
    elms["searchChar"].addEventListener("input", handleCharSearchType);
    elms["charOptsLst"].addEventListener("click", handleCharSearchClick);
    elms["teamSlct"].addEventListener("change", handleTeamChange);
    elms["totErIn"].addEventListener("focus", handleTotErFocus);
    elms["totErIn"].addEventListener("input", handleTotErType);
    document.addEventListener("click", handleOutsideClick);
}

function setup(){
    selectChar(state["selectedChar"]);
}

setEventListeners();
setup();
