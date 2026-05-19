
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

elms["allEchoesNameSlct"]=document.querySelectorAll(".fsEchoStatSlct");
elms["allEchoesValSlct"]=document.querySelectorAll(".fsEchoValSlct");

function renderFullSubstatNames(){
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

function updateFullSubstats(){
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        const statName=nameSlct.value;
        const echoInd=Number(nameSlct.id[5])-1;
        nameSlct.innerHTML=`<option value="noVal">Substat</option>`;
        state["usefulStats"].forEach(function (stat) {
            if (state["pickedStats"][echoInd].indexOf(stat)!==-1) {
                if (stat!==statName) return;
            }
            const opt=document.createElement("option");
            opt.value=stat;
            opt.textContent=stat;
            nameSlct.appendChild(opt);
        });
        if (statName==="ER(%)" && !state["usefulStats"].includes("ER(%)")) {nameSlct.value="noVal";}
        else {nameSlct.value=statName;}
    });
}

function handleFullSubstatChange(event){
    const statSlct=event.currentTarget;
    const echoInd=Number(statSlct.id[5])-1;
    const statName=statSlct.value;
    const prevStatName=statSlct.dataset.prevVal;
    statSlct.dataset.prevVal=statName;
    console.log(statName, prevStatName);
    if (statName!=="noVal") {state["pickedStats"][echoInd].push(statName);}
    if (prevStatName!=="noVal") {state["pickedStats"][echoInd].splice(state["pickedStats"][echoInd].indexOf(prevStatName), 1);}
    updateFullSubstats();
}

function handleFullTeamChange(event){
    const teamSlct=event.currentTarget;
    state["fullData"].forEach(function (echo, ind) {state["fullData"][ind][12]=0;});
    let erReq=0;
    if (teamSlct.value!=="noVal") {erReq=charData[state["selectedChar"]][1][0][teamSlct.value];}
    console.log(erReq);
    if (erReq>100) {
        if (!state["usefulStats"].includes("ER(%)")) {state["usefulStats"].push("ER(%)");}
    } else {
        if (state["usefulStats"].includes("ER(%)")) {state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1)}
    }
    updateFullSubstats();
}

function renderFullVals(event){
    const uid="val-"+event.currentTarget.id.slice(-2);
    const statName=event.currentTarget.value;
    elms["allEchoesValSlct"].forEach(function (valSlct) {
        if (uid!==valSlct.id) return;
        valSlct.innerHTML=`<option value="noVal">Value</option>`;
        if (statName==="noVal") return;
        substatRollsData[statName].forEach(function (roll) {
            const opt=document.createElement("option");
            opt.value=roll;
            opt.textContent=roll;
            valSlct.appendChild(opt);
        });
    });
}

function handleFullValChange(event){
    const valSlct=event.currentTarget;
    if (valSlct.value==="noVal") return;
    const uid=valSlct.id.slice(-2);
    const statName=document.getElementById("stat-"+uid).value;
    const statInd=echoData.indexOf(statName);
    const statRoll=valSlct.value;
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
    elms["charOptsLst"].addEventListener("click", renderFullSubstatNames);
    elms["teamSlct"].addEventListener("change", renderFullSubstatNames);
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        nameSlct.dataset.prevVal=nameSlct.value;
        nameSlct.addEventListener("change", handleFullSubstatChange);
        nameSlct.addEventListener("change", renderFullVals)
    });
    elms["allEchoesValSlct"].forEach(function (valSlct) {valSlct.addEventListener("change", handleFullValChange)})
    elms["form"].addEventListener("submit", calcFullResults);
}

setFullEventListeners();
renderFullSubstatNames();
