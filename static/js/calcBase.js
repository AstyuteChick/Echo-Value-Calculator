
const charDataEle=document.querySelector("#char-data");
const charData=JSON.parse(charDataEle.textContent); //Character.data

const echoDataEle=document.querySelector("#echo-data");
const echoData=JSON.parse(echoDataEle.textContent); //GameData.substat_names (ordered substat names, list)
const substatRollsEle=document.querySelector("#substat-rolls-data");
const substatRollsData=JSON.parse(substatRollsEle.textContent); //GameData.substat_rolls (dict -> statName: list of rolls)

const state={
    selectedChar: `Aemeath`, 
    isCharMenuOpen: false, 
    selectedTeam: null, 
    totEr: null
}

const elms={
    form: document.querySelector(".calcForm"), 
    selectedChar: document.querySelector(".selectedChar"), 
    searchChar: document.querySelector("#char-search"), 
    charOptsLst: document.querySelector(".charOptsLst"), 
    teamSlct: document.querySelector("#team-select"),
    totErIn: document.querySelector("#tot-er"), 
    resetBtn: document.querySelector(".allResetBtn"), 
    scoreVal: document.querySelector(".scoreVal"), 
    tierVal: document.querySelector(".tierVal"), 
    resultDivs: document.querySelectorAll(".resultDiv")
}

function validateBaseStateUI() {
    if (state["selectedChar"]!==elms["selectedChar"].children[1].textContent) return false;
    if (state["selectedTeam"]!==elms["teamSlct"].value) return false;
    if (state["totEr"]!==Number(elms["totErIn"].value)) return false;
    return true;
}

function validateEchoStateUI(echoState, echoElm, echoPickedStats, uidData, uidName) {
    for (const [ind, statVal] of echoState.entries()) {
        const statName=echoData[ind];
        if (!statVal) {
            for (const nameSlct of echoElm) {
                if (nameSlct.value===statName) return false;
            }
        } else {
            if (!echoPickedStats.includes(statName)) return false;
            let matchesFound=0;
            let uid="";
            for (const nameSlct of echoElm) {
                if (nameSlct.value===statName) {
                    matchesFound++;
                    uid=nameSlct.id.slice(uidData);
                }
            }
            if (matchesFound!==1 || uid==="") return false;
            const valSlct=document.getElementById(`${uidName}${uid}`);
            if (valSlct.value!==statVal) return false;
        }
    }
    return true;
}

function handleSubmit(event) {event.preventDefault();}

function renderCharOpts(searchInp="") {
    const normInp=searchInp.toLowerCase().trim();
    const charNames=Object.keys(charData);
    const filteredChars=charNames.filter(function(charName) {return charName.toLowerCase().includes(normInp);});
    if (filteredChars.length===0) {
        elms["charOptsLst"].innerHTML=`<li><span>No Characters Found</span></li>`;
        return;
    }
    elms["charOptsLst"].innerHTML=``;
    filteredChars.forEach(function (charName) {
        const li=document.createElement("li");
        const btn=document.createElement("button");
        const img=document.createElement("img");
        const spn=document.createElement("span");
        const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
        spn.textContent=charName;
        img.src=`${staticImgPath}Resonator_${cleanCharName}.webp`;
        img.classList.add("charPortrait");
        btn.type="button";
        btn.classList.add("btn", "charOptsBtn");
        btn.dataset.charName=charName;
        btn.appendChild(img);
        btn.appendChild(spn);
        li.appendChild(btn);
        elms["charOptsLst"].appendChild(li);
    });
}

function openCharMenu() {
    elms["charOptsLst"].hidden=false;
    state["isCharMenuOpen"]=true;
    renderCharOpts(elms["searchChar"].value);
}

function handleCharSearchFocus() {
    elms["searchChar"].value="";
    openCharMenu();
}

function handleCharSearchType() {renderCharOpts(elms["searchChar"].value);}

function closeCharMenu() {
    elms["charOptsLst"].hidden=true;
    elms["searchChar"].value=state.selectedChar;
    state["isCharMenuOpen"]=false;
}

function renderTeamOpts(charName) {
    elms["teamSlct"].innerHTML=`<option value="">Select your character's team</option>`;
    elms["teamSlct"].classList.remove("hasVal");
    const charTeams=Object.keys(charData[charName][1][0]);
    charTeams.forEach(function (team) {
        const opt=document.createElement("option");
        opt.value=team;
        opt.textContent=team;
        elms.teamSlct.appendChild(opt);
    });
    state["selectedTeam"]=null;
    elms["teamSlct"].value="";
}

function selectChar(charName) {
    if (!charName) return;
    state["selectedChar"]=charName;
    elms["searchChar"].value=charName;
    const img=document.createElement("img");
    const spn=document.createElement("span");
    const cleanCharName=charName.split('(')[0].trim().split(' ')[0].trim();
    img.src=`${staticImgPath}Resonator_${cleanCharName}.webp`;
    img.classList.add("charPortrait");
    spn.textContent=charName;
    elms["selectedChar"].innerHTML=``;
    elms["selectedChar"].appendChild(img);
    elms["selectedChar"].appendChild(spn);
    closeCharMenu();
    renderTeamOpts(charName);
    state["totEr"]=null;
    elms["totErIn"].value="";
    setConsColor("");
    triggerAni();
}

function handleCharSearchClick(event) {
    const clickedBtn=event.target.closest(".charOptsBtn");
    if (!clickedBtn) return;
    selectChar(clickedBtn.dataset.charName);
}

function handleOutsideClick(event) {
    const clickInCharOpts=event.target.closest(".charOptsLst");
    const clickInCharInp=event.target.closest(".charSearchInp");
    if (!clickInCharOpts && !clickInCharInp) {closeCharMenu();}
}

function handleTeamChange(event) {
    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    if (teamName==="") {
        state["selectedTeam"]=null;
    } else {
        state["selectedTeam"]=teamName;
    }
}

function handleTotErFocus() {
    if (elms["totErIn"].value) {
        state["totEr"]=null;
        elms["totErIn"].value="";
    }
}

function handleTotErType() {state["totEr"]=Number(elms["totErIn"].value);}

function controlStyles(event) {
    const elem=event.currentTarget;
    let hasVal;
    if (!elem.value) {
        if (elem.textContent) {hasVal=true;}
        else {hasVal=false;}
    } else {
        if (elem.value==="noVal") {hasVal=false;}
        else {hasVal=true;}
    }
    if (hasVal===true) {elem.classList.add("hasVal");}
    else {elem.classList.remove("hasVal");}
}

function setConsColor(tier) {
    switch (tier) {
        case "Godly": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--godly)";
                div.style.color="hsl(0, 0%, 4%)";
            });
            break;
        case "Extreme": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--extreme)";
                div.style.color="hsl(0, 0%, 4%)";
            });
            break;
        case "High Investment": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--high)";
                div.style.color="hsl(0, 0%, 96%)";
            });
            break;
        case "Well Built": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--well)";
                div.style.color="hsl(0, 0%, 96%)";
            });
            break;
        case "Decent": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--decent)";
                div.style.color="hsl(0, 0%, 4%)";
            });
            break;
        case "Base Level": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--base)";
                div.style.color="hsl(0, 0%, 96%)";
            });
            break;
        case "Error": 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--error)";
                div.style.color="hsl(0, 0%, 96%)";
            });
            break;
        default: 
            elms["resultDivs"].forEach(function (div) {
                div.style.backgroundColor="var(--b2)";
                div.style.color="var(--txt)";
            });
    }
}

function triggerAni() {
    elms["resultDivs"].forEach(function (div) {
        div.classList.remove("otshine");
        void div.offsetWidth;
        div.classList.add("otshine");
    })
}

function handleAniEnd(event) {
    if (event.animationName==="result-shine") {
        elms["resultDivs"].forEach(function (div) {div.classList.remove("otshine")});
    }
}

function setEventListeners() {
    elms["form"].addEventListener("submit", handleSubmit);
    elms["searchChar"].addEventListener("focus", handleCharSearchFocus);
    elms["searchChar"].addEventListener("input", handleCharSearchType);
    elms["charOptsLst"].addEventListener("click", handleCharSearchClick);
    document.addEventListener("click", handleOutsideClick);
    elms["teamSlct"].addEventListener("change", handleTeamChange);
    elms["totErIn"].addEventListener("focus", handleTotErFocus);
    elms["totErIn"].addEventListener("input", handleTotErType);
    elms["teamSlct"].addEventListener("change", controlStyles);
    elms["totErIn"].addEventListener("input", controlStyles);
    elms["resultDivs"].forEach(function (div) {
        div.addEventListener("animationend", handleAniEnd);
    });
    elms["resetBtn"].addEventListener("click", function () {selectChar(state["selectedChar"]);});
}

function setup() {selectChar(state["selectedChar"]);}

setEventListeners();
setup();
