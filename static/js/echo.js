
state["echoData"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
state["usefulStats"] = [];
state["pickedStats"] = [];

elms["allEchoNameSlct"] = document.querySelectorAll(".statNameSlct");
elms["allEchoValSlct"] = document.querySelectorAll(".statValueSlct");

function renderEchoSubstatNames(){
    state["echoData"]=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    state["usefulStats"]=[];
    state["pickedStats"]=[];
    elms["allEchoNameSlct"].forEach(function (nameSlct){nameSlct.innerHTML = `<option value="noVal">Select Echo Substat</option>`});
    elms["allEchoValSlct"].forEach(function (valSlct){valSlct.innerHTML=`<option value="noVal">Select Value</option>`});
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
    const erArray=[charData[state["selectedChar"]][1][0][state["selectedTeam"]], charData[state["selectedChar"]][1][1], charData[state["selectedChar"]][1][2]];
    console.log(erArray, echoData[12], );
    if (erArray[0]<=100 || erArray[1]===0 || erArray[0]===undefined) return;
    elms["allEchoNameSlct"].forEach(function (nameSlct){
        const opt=document.createElement("option");
        opt.value=echoData[12];
        opt.textContent=echoData[12];
        nameSlct.appendChild(opt);
    });
    state["usefulStats"].push(echoData[12]);
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
        console.log(curVal, state["usefulStats"].indexOf("ER(%)"));
        if (curVal==="ER(%)" && state["usefulStats"].indexOf("ER(%)")===-1) {
            nameSlct.value="noVal";
            
        }
        else {nameSlct.value=curVal;}
    });
}

function handleEchoSubstatChange(event){
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

function renderEchoValOpts(event){
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

function handleEchoTeamChange() {
    const erArr=[];
    const teamReqEr=charData[state["selectedChar"]][1][0][state["selectedTeam"]];
    const erImp=charData[state["selectedChar"]][1][1];
    const rc=charData[state["selectedChar"]][1][2];
    console.log(teamReqEr, erImp, rc);
    state["echoData"][12]=0.0;
    if (Number(teamReqEr)<=100 || erImp===0){
        if (state["usefulStats"].indexOf("ER(%)")!==-1) {
            state["usefulStats"].splice(state["usefulStats"].indexOf("ER(%)"), 1);
        }
        if (state["pickedStats"].indexOf("ER(%)")!==-1) {
            state["pickedStats"].splice(state["pickedStats"].indexOf("ER(%)"), 1);
        }
    }
    else {
        if (state["usefulStats"].indexOf("ER(%)")===-1) {state["usefulStats"].push("ER(%)");}
    }
    updateSubstatOpts();
}

function updateEchoResults(result){
    elms["scoreVal"].innerHTML = result.score;
    elms["tierVal"].innerHTML = result.tier;
}

async function calcEchoResults(){
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
        updateEchoResults(result);
    } catch (error) {
        console.error("Submit Failed: ", error)
    }
}

function setEchoEventListeners(){
    elms["charOptsLst"].addEventListener("click", renderEchoSubstatNames);
    elms["teamSlct"].addEventListener("change", handleEchoTeamChange);
    elms["allEchoNameSlct"].forEach(function (slct){
        slct.dataset.prevVal = slct.value;
        slct.addEventListener("change", handleEchoSubstatChange);
        slct.addEventListener("change", renderEchoValOpts);
    });
    elms["allEchoValSlct"].forEach(function (slct){slct.addEventListener("change", handleValOptsChange);});
    elms["form"].addEventListener("submit", calcEchoResults);
}

setEchoEventListeners();
renderEchoSubstatNames();
