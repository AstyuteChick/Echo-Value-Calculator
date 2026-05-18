
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

function renderFullVals(){

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
        nameSlct.value=statName;
    });
}

function handleFullSubstatChange(event){
    const statSlct=event.currentTarget;
    const echoInd=Number(statSlct.id[5])-1;
    const statName=statSlct.value;
    const prevStatName=statSlct.dataset.prevVal;
    statSlct.dataset.prevVal=statName;
    if (statName!=="noVal") {state["pickedStats"][echoInd].push(statName);}
    if (prevStatName!=="noVal") {state["pickedStats"][echoInd].splice(state["pickedStats"][echoInd].indexOf(prevStatName), 1);}
    updateFullSubstats();
}

function handleFullValChange(){

}

function calcFullResults(){}

function setFullEventListeners(){
    elms["charOptsLst"].addEventListener("click", renderFullSubstatNames);
    elms["allEchoesNameSlct"].forEach(function (nameSlct) {
        nameSlct.dataset.prevVal=nameSlct.value;
        nameSlct.addEventListener("change", handleFullSubstatChange);
    });
    elms["allEchoesValSlct"].forEach(function (valSlct) {valSlct.addEventListener("change", handleFullValChange)})
    elms["form"].addEventListener("submit", calcFullResults);
}

setFullEventListeners();
renderFullSubstatNames();
