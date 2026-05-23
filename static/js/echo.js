
function resetEchoState() {
    state["echoData"]=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    state["usefulStats"]=[];
    state["pickedStats"]=[];
    elms["scoreVal"].innerHTML="[Your Echo Score]";
    elms["tierVal"].innerHTML="[Your Echo Tier]";
}

function setEchoElements() {
    elms["allEchoNameSlct"]=document.querySelectorAll(".statNameSlct");
    elms["allEchoValSlct"]=document.querySelectorAll(".statValueSlct");
}

function renderEchoSubstats() {
    // Also updates state of usefulstats
    elms["allEchoNameSlct"].forEach(function (nameSlct) {
        nameSlct.innerHTML=`<option value="noVal">Select Substat</option>`;
        nameSlct.classList.remove("hasVal");
    });
    charData[state["selectedChar"]][0].forEach(function (relVal, ind) {
        if (!relVal) return;
        const statName=echoData[ind];
        elms["allEchoNameSlct"].forEach(function (nameSlct) {
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            nameSlct.appendChild(opt);
        });
        state["usefulStats"].push(statName);
    });
}

function resetEchoVals() {
    elms["allEchoValSlct"].forEach(function (valSlct) {
        valSlct.innerHTML=`<option value="noVal">Select Roll</option>`;
        valSlct.classList.remove("hasVal");
    });
}

function handleEchoCharClick() {
    resetEchoState();
    renderEchoSubstats();
    resetEchoVals();
}

function updateEchoStateEr(erReq) {
    if (erReq>100) {
        if (!state["usefulStats"].includes("ER(%)")) {state["usefulStats"].push("ER(%)");}
    } else {
        if (state["usefulStats"].includes("ER(%)")) {state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1);}
        if (state["pickedStats"].includes("ER(%)")) {state["pickedStats"].splice(state["pickedStats"].indexOf("ER(%)"), 1);}
        state["echoData"][12]=0;
    }
}

function updateEchoSubstats() {
    elms["allEchoNameSlct"].forEach(function (nameSlct) {
        const curStat=nameSlct.value;
        nameSlct.innerHTML=`<option value="noVal">Select Substat</option>`;
        state["usefulStats"].forEach(function (stat) {
            if (state["pickedStats"].includes(stat) && curStat!==stat) return;
            const opt=document.createElement("option");
            opt.value=stat;
            opt.textContent=stat;
            nameSlct.appendChild(opt);
        });
        if (state["pickedStats"].includes(curStat)) {
            nameSlct.value=curStat;
            nameSlct.classList.add("hasVal");
        }
        else {
            nameSlct.value="noVal";
            nameSlct.classList.remove("hasVal");
        }
    });
}

function updateEchoVals() {
    // Assumes substats are updated first, and value options are refreshed after every substat change
    elms["allEchoValSlct"].forEach(function (valSlct) {
        const curVal=valSlct.value;
        const nameSlct=document.getElementById(`stat-name-${valSlct.id.slice(-1)}`);
        const statName=nameSlct.value;
        valSlct.innerHTML=`<option value="noVal">Select Roll</option>`;
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

function handleEchoTeamChange(event) {
    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    let erReq=0;
    if (teamName!=="noVal"){erReq=charData[state["selectedChar"]][1][0][teamName];}
    updateEchoStateEr(erReq);
    updateEchoSubstats();
    updateEchoVals();
}

function updateEchoStateStats(prevStat, curStat) {
    if (prevStat!=="noVal") {state["pickedStats"].splice(state["pickedStats"].indexOf(prevStat), 1);}
    if (curStat!=="noVal") {state["pickedStats"].push(curStat);}
}

function renderEchoVals(uid, curStat) {
    // Only renders for the specific substat
    const valSlct=document.getElementById(`stat-value-${uid}`);
    valSlct.innerHTML=`<option value="noVal">Select Roll</option>`;
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

function handleEchoSubstatChange(event) {
    const statSlct=event.currentTarget;
    const prevStat=statSlct.dataset.prevVal;
    const curStat=statSlct.value;
    statSlct.dataset.prevVal=curStat;
    const uid=statSlct.id.slice(-1);
    updateEchoStateStats(prevStat, curStat);
    renderEchoVals(uid, curStat);
    updateEchoSubstats();
}

function handleEchoValChange(event) {
    const valSlct=event.currentTarget;
    const statSlct=document.getElementById(`stat-name-${valSlct.id.slice(-1)}`);
    const statInd=echoData.indexOf(statSlct.value);
    state["echoData"][statInd]=valSlct.value==="noVal"?0:valSlct.value;
}

function updateEchoResults(result) {
    elms["scoreVal"].innerHTML=result.score;
    elms["tierVal"].innerHTML=result.tier;
}

async function calcEchoResults() {
    try {
        const response=await fetch("/calcEcho", {
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({
                char: state.selectedChar, 
                team: state.selectedTeam, 
                totEr: state.totEr, 
                ssr: state.echoData
            })
        });
        if (!response.ok) {throw new Error("Server Error");}
        const result = await response.json();
        updateEchoResults(result);
    } catch (error) {
        console.error("Submit Failed: ", error)
    }
}

function echoDebugger() {
    console.log(state["selectedChar"]);
    console.log(state["selectedTeam"]);
    console.log(state["totEr"]);
    console.log(state["echoData"]);
}

function setEchoEventListeners() {
    elms["charOptsLst"].addEventListener("click", handleEchoCharClick);
    elms["teamSlct"].addEventListener("change", handleEchoTeamChange);
    elms["allEchoNameSlct"].forEach(function (slct) {
        slct.dataset.prevVal=slct.value;
        slct.addEventListener("change", handleEchoSubstatChange);
        slct.addEventListener("change", controlStyles)
    });
    elms["allEchoValSlct"].forEach(function (slct) {
        slct.addEventListener("change", handleEchoValChange);
        slct.addEventListener("change", controlStyles)
    });
    elms["form"].addEventListener("submit", calcEchoResults);

    document.addEventListener("click", echoDebugger);
}

resetEchoState();
setEchoElements();
setEchoEventListeners();
handleEchoCharClick();
