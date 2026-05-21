
function resetFullState(){
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

function setFullElements(){
    elms["allEchoesNameSlct"]=document.querySelectorAll(".fsEchoStatSlct");
    elms["allEchoesValSlct"]=document.querySelectorAll(".fsEchoValSlct");
}

function renderFullSubstats(){
    //also updates state
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {nameSlct.innerHTML=`<option value="noVal">Substat</option>`;});
    charData[state["selectedChar"]][0].forEach(function (relVal, ind) {
        if (!relVal) return;
        const statName=echoData[ind];
        elms["allEchoesNameSlct"].forEach(function (nameSlct) {
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            nameSlct.appendChild(opt);
        });
        state["usefulStats"].push(statName);
    });
}

function resetFullVals() {
    elms["allEchoesValSlct"].forEach(function (valSlct) {valSlct.innerHTML=`<option value="noVal">Value</option>`;});
}

function handleFullCharClick(){
    resetFullState();
    renderFullSubstats();
    resetFullVals();
}

function updateFullState(){
    state["usefulStats"].push()
}

function handleFullTeamChange(event){
    updateFullState();
    updateFullSubstats();
}

function renderFullVals(){
    elms["allEchoesValSlct"].forEach(function (valSlct) {
        const statSlct=document.getElementById("stat-"+valSlct.id.slice(-2));
        const statName=statSlct.value;
        const curVal=valSlct.value;
        valSlct.innerHTML=`<option value="noVal">Value</option>`;
        if (statName==="noVal") return;
        substatRollsData[statName].forEach(function (roll) {
            const opt=document.createElement("option");
            opt.value=roll;
            opt.textContent=roll;
            valSlct.appendChild(opt);
        });
        valSlct.value=curVal;
    });
}



function renderFullER(event){

    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    state["fullData"].forEach(function (echo, ind) {state["fullData"][ind][12]=0;});
    let erReq=0;
    if (teamName!=="noVal") {erReq=charData[state["selectedChar"]][1][0][teamName];}
    console.log(erReq);
    if (erReq>100) {
        if (!state["usefulStats"].includes("ER(%)")) {state["usefulStats"].push("ER(%)");}
    } else {
        if (state["usefulStats"].includes("ER(%)")) {state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1)}
    }
    updateFullSubstats();
}

function updateFullSubstats(){
    // Updates available substats based on the state of useful and picked stats, and calls for val updates
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        const statName=nameSlct.value;
        const echoInd=Number(nameSlct.id[5])-1;
        nameSlct.innerHTML=`<option value="noVal">Substat</option>`;
        state["usefulStats"].forEach(function (stat) {
            if (state["pickedStats"][echoInd].includes(stat) && stat!==statName) return;
            const opt=document.createElement("option");
            opt.value=stat;
            opt.textContent=stat;
            nameSlct.appendChild(opt);
        });
        if (statName==="ER(%)" && !state["usefulStats"].includes("ER(%)")) {nameSlct.value="noVal";}
        else {nameSlct.value=statName;}
    });
    renderFullVals();
}

function handleFullSubstatChange(event){
    // Updates state of picked stats and calls for update
    const statSlct=event.currentTarget;
    const echoInd=Number(statSlct.id[5])-1;
    const statName=statSlct.value;
    const prevStatName=statSlct.dataset.prevVal;
    statSlct.dataset.prevVal=statName;
    console.log(statName, prevStatName); 
    if (prevStatName!=="noVal") {state["pickedStats"][echoInd].splice(state["pickedStats"][echoInd].indexOf(prevStatName), 1);}
    if (statName!=="noVal") {state["pickedStats"][echoInd].push(statName);}
    updateFullSubstats();
}

function handleFullTeamChange(event){
    // Updates state of useful stats based on team and calls for update
    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    state["fullData"].forEach(function (echo, ind) {state["fullData"][ind][12]=0;});
    let erReq=0;
    if (teamName!=="noVal") {erReq=charData[state["selectedChar"]][1][0][teamName];}
    console.log(erReq);
    if (erReq>100) {
        if (!state["usefulStats"].includes("ER(%)")) {state["usefulStats"].push("ER(%)");}
    } else {
        if (state["usefulStats"].includes("ER(%)")) {state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1)}
    }
    updateFullSubstats();
}



function handleFullValChange(event){
    // Updates state based on echo index, stat and value
    const valSlct=event.currentTarget;
    const statRoll=valSlct.value;
    if (statRoll==="noVal") return;
    const uid=valSlct.id.slice(-2);
    const statName=document.getElementById("stat-"+uid).value;
    const statInd=echoData.indexOf(statName);
    state["fullData"][Number(uid[0])-1][statInd]=statRoll;
}

async function calcFullResults(){
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

function setFullEventListeners(){
    elms["charOptsLst"].addEventListener("click", handleFullCharClick);
    elms["teamSlct"].addEventListener("change", handleFullTeamChange);
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        nameSlct.dataset.prevVal=nameSlct.value;
        nameSlct.addEventListener("change", handleFullSubstatChange);
    });
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {nameSlct.addEventListener("change", renderFullVals)});
    elms["allEchoesValSlct"].forEach(function (valSlct) {valSlct.addEventListener("change", handleFullValChange)});
    elms["form"].addEventListener("submit", calcFullResults);
}

resetFullState();
setFullElements();
setFullEventListeners();
