
const echoDataEle = document.querySelector("#echo-data");
const echoData = JSON.parse(echoDataEle.textContent);
const substatRollsEle = document.querySelector("#substat-rolls-data");
const substatRollsData = JSON.parse(substatRollsEle.textContent);

state["echoData"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
state["usefulStats"] = [];
state["pickedStats"] = [];

elms["allEchoNameSlct"] = document.querySelectorAll(".statNameSlct");
elms["allEchoValSlct"] = document.querySelectorAll(".statValueSlct");
elms["scoreVal"] = document.querySelector(".scoreVal");
elms["tierVal"] = document.querySelector(".tierVal");

function renderSubstatNames(){
    state["usefulStats"]=[];
    elms["allEchoNameSlct"].forEach(function (nameSlct){nameSlct.innerHTML = "<option value = 'noVal'>Select Echo Substat</option>"});
    charData[state["selectedChar"]][0].forEach(function (relVal, ind){
        if (!relVal) return;
        const curStat = echoData[ind];
        elms["allEchoNameSlct"].forEach(function (nameSlct){
            const opt = document.createElement("option");
            opt.value = curStat;
            opt.textContent = curStat;
            nameSlct.appendChild(opt);
        });
        state["usefulStats"].push(curStat);
    });
}

function updateSubstatOpts(){
    elms["allEchoNameSlct"].forEach(function (nameSlct){
        const curVal = nameSlct.value;
        nameSlct.innerHTML = "<option value = 'noVal'>Select Echo Substat</option>";
        state["usefulStats"].forEach(function (stat){
            if (stat === curVal || !state["pickedStats"].includes(stat)) {
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
        if (prevVal !== "noVal") {
            state["pickedStats"].splice(state["pickedStats"].indexOf(prevVal), 1);
            state["echoData"][echoData.indexOf(prevVal)] = 0.0;
        }
        state["pickedStats"].push(curSlct.value);
    } else {
        state["pickedStats"].splice(state["pickedStats"].indexOf(prevVal), 1);
        state["echoData"][echoData.indexOf(prevVal)] = 0.0;
    }
    updateSubstatOpts();
}

function renderValOpts(event){
    const nameSlct = event.currentTarget;
    const echoNo = Number(nameSlct.id[nameSlct.id.length - 1]);
    elms["allEchoValSlct"].forEach(function (valSlct){
        if (Number(valSlct.id[valSlct.id.length - 1]) !== echoNo) return;
        valSlct.innerHTML = `<option value="noVal">Select Value</option>`;
        if (nameSlct.value === "noVal") return;
        substatRollsData[nameSlct.value].forEach(function (val){
            const opt = document.createElement("option");
            opt.value = val;
            opt.textContent = val;
            valSlct.appendChild(opt);
        });
    });
}

function handleValOptsChange(event){
    const valSlct = event.currentTarget;
    const echoNo = Number(valSlct.id[valSlct.id.length - 1]);
    const statName = elms["allEchoNameSlct"][echoNo - 1].value;
    state["echoData"][echoData.indexOf(statName)] = valSlct.value === "noVal" ? 0.0 : Number(valSlct.value);
}

function updateResults(result){
    elms["scoreVal"].innerHTML = result.score;
    elms["tierVal"].innerHTML = result.tier;
}

async function calcResults(){
    try {
        const response = await fetch("/calcEcho", {
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
        updateResults(result);
    } catch (error) {
        console.error("Submit Failed: ", error)
    }
}

function setEchoEventListeners(){
    elms["charOptsLst"].addEventListener("click", renderSubstatNames);
    elms["allEchoNameSlct"].forEach(function (slct){
        slct.dataset.prevVal = slct.value;
        slct.addEventListener("change", handleSubstatChange);
    });
    elms["allEchoNameSlct"].forEach(function (slct){slct.addEventListener("change", renderValOpts);});
    elms["allEchoValSlct"].forEach(function (slct){slct.addEventListener("change", handleValOptsChange);});
    elms["form"].addEventListener("submit", calcResults);
}

setEchoEventListeners();
renderSubstatNames();
