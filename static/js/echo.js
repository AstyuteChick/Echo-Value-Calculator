
const echoDataEle = document.querySelector("#echo-data");
const echoData = JSON.parse(echoDataEle.textContent);
const substatRollsEle = document.querySelector("#substat-rolls-data");
const substatRollsData = JSON.parse(substatRollsEle.textContent);

state["echoData"] = [null, null, null, null, null, null, null, null, null, null, null, null, null];
state["usefulStats"] = [];
state["pickedStats"] = [];

elms["allEchoNameSlct"] = document.querySelectorAll(".statNameSlct");
elms["allEchoValSlct"] = document.querySelectorAll(".statValueSlct");

function setEchoEventListeners(){
    elms["allEchoNameSlct"].forEach(function (slct){
        slct.dataset.prevVal = slct.value;
        slct.addEventListener("change", handleSubstatChange);
    });
    elms["allEchoValSlct"].forEach(function (slct){slct.addEventListener("change", handleSubstatChange);});
    elms["charOptsLst"].addEventListener("click", renderSubstatNames);
}

function renderSubstatNames(){
    elms["allEchoNameSlct"].forEach(function (nameSlct){nameSlct.innerHTML = "<option value = 'noVal'>Select Echo Substat</option>"});
    charData[state.selectedChar][0].forEach(function (relVal, ind){
        if (!relVal) return;
        const curStat = echoData[ind];
        state.usefulStats.push(curStat);
        elms["allEchoNameSlct"].forEach(function (nameSlct){
            const opt = document.createElement("option");
            opt.value = curStat;
            opt.textContent = curStat;
            nameSlct.appendChild(opt);
        });
    });
}

function updateSubstatOpts(){
    elms["allEchoNameSlct"].forEach(function (nameSlct){
        const curVal = nameSlct.value;
        // const prevVal = nameSlct.dataset.prevVal;
        nameSlct.innerHTML = "<option value = 'noVal'>Select Echo Substat</option>";
        state.usefulStats.forEach(function (stat){
            if (stat === curVal) {
                const opt = document.createElement("option");
                opt.value = stat;
                opt.textContent = stat;
                nameSlct.appendChild(opt);
            } else if (!state.pickedStats.includes(stat)) {
                const opt = document.createElement("option");
                opt.value = stat;
                opt.textContent = stat;
                nameSlct.appendChild(opt);
            }
        });
        nameSlct.value = curVal;
    });
}

function handleSubstatChange(event){
    const curSlct = event.currentTarget;
    const prevVal = curSlct.dataset.prevVal;
    curSlct.dataset.prevVal = curSlct.value;
    if (curSlct.value !== "noVal") {
        if (prevVal !== "noVal") {state.pickedStats.splice(state.pickedStats.indexOf(prevVal), 1);}
        state.pickedStats.push(curSlct.value);
    } else {
        state.pickedStats.splice(state.pickedStats.indexOf(prevVal), 1);
    }
    updateSubstatOpts();
}

setEchoEventListeners();
renderSubstatNames();
