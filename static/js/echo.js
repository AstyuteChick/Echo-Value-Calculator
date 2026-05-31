
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
        state["usefulStats"].push(statName);
        elms["allEchoNameSlct"].forEach(function (nameSlct) {
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            nameSlct.appendChild(opt);
        });
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
        nameSlct.dataset.prevVal=nameSlct.value;
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
    if (teamName!==""){erReq=charData[state["selectedChar"]][1][0][teamName];}
    updateEchoStateEr(erReq);
    updateEchoSubstats();
    updateEchoVals();
}

function updateEchoStateStats(prevStat, curStat) {
    if (prevStat!=="noVal" && state["pickedStats"].includes(prevStat)) {
        state["pickedStats"].splice(state["pickedStats"].indexOf(prevStat), 1);
        const prevStatInd=echoData.indexOf(prevStat);
        state["echoData"][prevStatInd]=0;
    }
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
    if (statInd===-1) {
        const result={score: `001: Invalid Stat found - ${statSlct.value}`, tier: "Error"};
        updateEchoResults(result);
        tagEchoResult(result);
        return;
    }
    state["echoData"][statInd]=valSlct.value==="noVal"?0:valSlct.value;
}

function tagEchoResult(result) {
    if (typeof gtag !== "function") return;
    const tagData={
        result_source: "echo",
        character_name: state.selectedChar,
        team_name: state.selectedTeam,
        result_tier: result.tier
    }
    const validResult=Number.isFinite(Number(result.score));
    if (validResult) {tagData["result_score"]=Number(result.score);}
    gtag("event", "echo_result", tagData);
}

function updateEchoResults(result) {
    elms["scoreVal"].textContent=result.score;
    elms["tierVal"].textContent=result.tier;
    setConsColor(result.tier);
    triggerAni();
}

async function calcEchoResults() {
    if (
        !elms["form"].reportValidity() || 
        !validateBaseStateUI() || 
        !validateEchoStateUI(state["echoData"], elms["allEchoNameSlct"], state["pickedStats"], -1, `stat-value-`)
    ) {
        const result={score: "State-UI Mismatch", tier: "Error"}
        updateEchoResults(result);
        tagEchoResult(result);
        return;
    }
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
        if (!response.ok) {throw new Error("Server Error: \nPlease refresh the page and try again. \nIf Error persists, please report the conditions that caused this error at: echovaluecalc@gmail.com");}
        const result = await response.json();
        updateEchoResults(result);
        tagEchoResult(result);
    } catch (error) {
        console.error("Submit Failed: ", error);
        const result={score: `Submit Failed: ${error}`, tier: "Error"}
        updateEchoResults(result);
        tagEchoResult(result);
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
        slct.addEventListener("change", controlStyles);
    });
    elms["allEchoValSlct"].forEach(function (slct) {
        slct.addEventListener("change", handleEchoValChange);
        slct.addEventListener("change", controlStyles);
    });
    elms["form"].addEventListener("submit", calcEchoResults);
    elms["resetBtn"].addEventListener("click", handleEchoCharClick);

    // document.addEventListener("click", echoDebugger);
}

resetEchoState();
setEchoElements();
setEchoEventListeners();
handleEchoCharClick();
