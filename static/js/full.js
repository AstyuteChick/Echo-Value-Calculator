
function resetFullState() {
    state["fullData"]=[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ];
    state["usefulStats"] = [];
    state["pickedStats"] = [
        [], [], [], [], []
    ];
    elms["scoreVal"].innerHTML="[Your Full Score]";
    elms["tierVal"].innerHTML="[Your Full Tier]";
}

function setFullElements() {
    elms["allEchoesNameSlct"]=document.querySelectorAll(".fsEchoStatSlct");
    elms["allEchoesValSlct"]=document.querySelectorAll(".fsEchoValSlct");
}

function renderFullSubstats() {
    // Also updates state
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        nameSlct.innerHTML=`<option value="noVal">Substat</option>`;
        nameSlct.classList.remove("hasVal");
    });
    charData[state["selectedChar"]][0].forEach(function (relVal, ind) {
        if (!relVal) return;
        const statName=echoData[ind];
        state["usefulStats"].push(statName);
        elms["allEchoesNameSlct"].forEach(function (nameSlct) {
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            nameSlct.appendChild(opt);
        });
    });
}

function resetFullVals() {
    elms["allEchoesValSlct"].forEach(function (valSlct) {
        valSlct.innerHTML=`<option value="noVal">Rolls</option>`;
        valSlct.classList.remove("hasVal");
    });
}

function handleFullCharClick() {
    resetFullState();
    renderFullSubstats();
    resetFullVals();
}

function updateFullStateEr(erReq) {
    if (erReq>100) {
        if (!state["usefulStats"].includes("ER(%)")) {state["usefulStats"].push("ER(%)");}
    } else {
        if (state["usefulStats"].includes("ER(%)")) {state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1);}
        state["pickedStats"].forEach(function (echo, ind) {
            if (echo.includes("ER(%)")) {state["pickedStats"][ind].splice(echo.indexOf("ER(%)"), 1);}
        });
        state["fullData"].forEach(function (echo, ind) {state["fullData"][ind][12]=0;});
    }
}

function updateFullSubstats() {
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        const curStat=nameSlct.value;
        const echoInd=Number(nameSlct.id[5])-1;
        nameSlct.innerHTML=`<option value="noVal">Substat</option>`;
        state["usefulStats"].forEach(function (stat) {
            if (state["pickedStats"][echoInd].includes(stat) && stat!==curStat) return;
            const opt=document.createElement("option");
            opt.value=stat;
            opt.textContent=stat;
            nameSlct.appendChild(opt);
        });
        if (state["pickedStats"][echoInd].includes(curStat)) {
            nameSlct.value=curStat;
            nameSlct.classList.add("hasVal");
        }
        else {
            nameSlct.value="noVal";
            nameSlct.classList.remove("hasVal");
        }
    });
}

function updateFullVals() {
    // Assumes substats are updated first, and value options are refreshed after every substat change
    elms["allEchoesValSlct"].forEach(function (valSlct) {
        const curVal=valSlct.value;
        const nameSlct=document.getElementById(`stat-${valSlct.id.slice(-2)}`);
        const statName=nameSlct.value;
        valSlct.innerHTML=`<option value="noVal">Rolls</option>`;
        if (statName==="noVal") {
            valSlct.value="noVal";
            valSlct.classList.remove("hasVal");
            return;
        }
        substatRollsData[statName].forEach(function (roll) {
            const opt=document.createElement("option");
            opt.value=roll;
            opt.textContent=roll;
            valSlct.appendChild(opt);
        });
        valSlct.value=curVal;
        if (curVal!=="noVal") {valSlct.classList.add("hasVal");}
        else {valSlct.classList.remove("hasVal");}
    });
}

function handleFullTeamChange(event) {
    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    let erReq=0;
    if (teamName!==""){erReq=charData[state["selectedChar"]][1][0][teamName];}
    updateFullStateEr(erReq);
    updateFullSubstats();
    updateFullVals();
}

function updateFullStateStats(prevStat, curStat, echoInd) {
    if (prevStat!=="noVal" && state["pickedStats"][echoInd].includes(prevStat)) {
        state["pickedStats"][echoInd].splice(state["pickedStats"][echoInd].indexOf(prevStat), 1);
        const prevStatInd=echoData.indexOf(prevStat);
        state["fullData"][echoInd][prevStatInd]=0;
    }
    if (curStat!=="noVal") {state["pickedStats"][echoInd].push(curStat);}
}

function renderFullVals(uid, curStat) {
    // Only renders for the specific substat
    const valSlct=document.getElementById(`val-${uid}`);
    valSlct.innerHTML=`<option value="noVal">Rolls</option>`;
    if (curStat!=="noVal") {
        substatRollsData[curStat].forEach(function (roll) {
            const opt=document.createElement("option");
            opt.value=roll;
            opt.textContent=roll;
            valSlct.appendChild(opt);
        });
    }
    valSlct.value="noVal"
    valSlct.classList.remove("hasVal");
}

function handleFullSubstatChange(event) {
    const statSlct=event.currentTarget;
    const prevStat=statSlct.dataset.prevVal;
    const curStat=statSlct.value;
    statSlct.dataset.prevVal=curStat;
    const echoInd=Number(statSlct.id[5])-1;
    const uid=statSlct.id.slice(-2);
    updateFullStateStats(prevStat, curStat, echoInd);
    renderFullVals(uid, curStat);
    updateFullSubstats();
}

function handleFullValChange(event) {
    const valSlct=event.currentTarget;
    const echoInd=Number(valSlct.id[4])-1;
    const statSlct=document.getElementById(`stat-${valSlct.id.slice(-2)}`);
    const statInd=echoData.indexOf(statSlct.value);
    state["fullData"][echoInd][statInd]=valSlct.value==="noVal"?0:valSlct.value;
}

function updateFullResults(result) {
    elms["scoreVal"].textContent=result.score;
    elms["tierVal"].textContent=result.tier;
}

async function calcFullResults() {
    if (!elms["form"].reportValidity()) return;
    try {
        const response = await fetch("/calcFull", {
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({
                char: state.selectedChar, 
                team: state.selectedTeam, 
                totEr: state.totEr, 
                ssr: state.fullData
            })
        });
        if (!response.ok) {throw new Error("Server Error");}
        const result = await response.json();
        updateFullResults(result);
    } catch (error) {
        console.error("Submit Failed: ", error)
    }
}

function setFullEventListeners() {
    elms["charOptsLst"].addEventListener("click", handleFullCharClick);
    elms["teamSlct"].addEventListener("change", handleFullTeamChange);
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        nameSlct.dataset.prevVal="noVal";
        nameSlct.addEventListener("change", handleFullSubstatChange);
        nameSlct.addEventListener("change", controlStyles)
    });
    elms["allEchoesValSlct"].forEach(function (valSlct) {
        valSlct.addEventListener("change", handleFullValChange);
        valSlct.addEventListener("change", controlStyles)
    });
    elms["form"].addEventListener("submit", calcFullResults);
}

resetFullState();
setFullElements();
setFullEventListeners();
handleFullCharClick();
