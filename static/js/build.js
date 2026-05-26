
const mainStatDataEle=document.querySelector("#main-stat-data");
const mainStatData=JSON.parse(mainStatDataEle.textContent);

function resetBuildState() {
    state["buildData"]=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    state["costSetup"]=[];
    state["mainStats"]=["noVal", "noVal", "noVal", "noVal", "noVal"];
    elms["scoreVal"].innerHTML="[Your Build Score]";
    elms["tierVal"].innerHTML="[Your Build Tier]";
}

function setBuildElements() {
    elms["costSetup"]=document.querySelector("#cost-slct");
    elms["mainStatSlct"]=document.querySelectorAll(".mainStatSlct");
    elms["statInp"]=document.querySelectorAll(".statInp");
}

function handleBuildCharChange() {
    resetBuildState();
    elms["costSetup"].value="";
    elms["mainStatSlct"].forEach(function (slct) {
        slct.innerHTML="<option value=''>Select your Echo's Main-Stat</option>";
        slct.labels[0].textContent="? - Cost Echo: ";
        slct.classList.remove("hasVal");
        slct.labels[0].classList.remove("hasVal");
    });
    elms["statInp"].forEach(function (inp) {
        inp.value=0;
        inp.hidden=true;
        inp.classList.remove("hasVal");
        inp.labels[0].hidden=true;
    });
    charData[state["selectedChar"]][0].forEach(function (relVal, ind) {
        if (!relVal) return;
        elms["statInp"].forEach(function (inp) {
            if (echoData[ind]!==inp.id) return;
            inp.hidden=false;
            inp.labels[0].hidden=false;
        });
    });
}

function handleBuildTeamChange(event) {
    const teamSlct=event.currentTarget;
    const teamName=teamSlct.value;
    const erInp=document.getElementById("ER(%)");
    const erVal=erInp.value;
    let erReqs=0;
    if (teamName!=="") {
        erReqs=charData[state["selectedChar"]][1][0][teamName];
        teamSlct.classList.add("hasVal");
    } else {teamSlct.classList.remove("hasVal");}
    if (erReqs>100) {
        erInp.hidden=false;
        erInp.labels[0].hidden=false;
        erInp.value=erVal;
        state["buildData"][12]=erVal;
    } else {
        erInp.hidden=true;
        erInp.labels[0].hidden=true;
        erInp.value=0;
        state["buildData"][12]=0;
    }
}

function handleBuildCostChange(event) {
    const costSlct=event.currentTarget;
    const curCostSetup=costSlct.value;
    state["costSetup"]=[];
    if (curCostSetup!=="") {
        for (let char of curCostSetup) {state["costSetup"].push(Number(char));}
    }
    elms["mainStatSlct"].forEach(function (slct) {
        slct.innerHTML="<option value=''>Select your Echo's Main-Stat</option>";
        slct.labels[0].textContent="? - Cost Echo: ";
        slct.classList.remove("hasVal");
        slct.labels[0].classList.remove("hasVal");
    });
    if (curCostSetup==="") {
        costSlct.classList.remove("hasVal");
        return
    } else {costSlct.classList.add("hasVal");}
    elms["mainStatSlct"].forEach(function (slct, ind) {
        const echoCost=state["costSetup"][ind];
        slct.labels[0].textContent=String(echoCost) + " - Cost Echo: ";
        Object.keys(mainStatData[echoCost]).forEach(function (statName) {
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            slct.appendChild(opt);
        });
    });
}

function handleBuildMainStatChange(event) {
    const curSlct=event.currentTarget;
    const curMainStatVal=curSlct.value;
    const echoNo=Number(curSlct.id.slice(-1));
    if (curMainStatVal==="") {curSlct.classList.remove("hasVal");} else {curSlct.classList.add("hasVal");}
    state["mainStats"][echoNo-1]=curMainStatVal;
}

function handleBuildStatFocus(event) {event.currentTarget.value="";}

function handleBuildStatInp(event) {
    const curInp=event.currentTarget;
    if (Number(curInp.value)!==0) {curInp.classList.add("hasVal");} else {curInp.classList.remove("hasVal");}
    state["buildData"][echoData.indexOf(curInp.id)]=Number(curInp.value);
}

function updateBuildResults(result) {
    elms["scoreVal"].innerHTML=result.score;
    elms["tierVal"].innerHTML=result.tier;
}

async function calcBuildResults() {
    try {
        const response = await fetch("/calcBuild", {
            method: "POST", 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({
                char: state.selectedChar, 
                team: state.selectedTeam, 
                totEr: state.totEr, 
                ssr: state.buildData, 
                echoCost: state.costSetup, 
                echoMainStats: state.mainStats
            })
        });
        if (!response.ok) {throw new Error("Server Error");}
        const result = await response.json();
        updateBuildResults(result);
    } catch (error) {
        console.error("Submit Failed: ", error)
    }
}

function setBuildEventListeners() {
    elms["charOptsLst"].addEventListener("click", handleBuildCharChange);
    elms["teamSlct"].addEventListener("change", handleBuildTeamChange);
    elms["costSetup"].addEventListener("change", handleBuildCostChange);
    elms["mainStatSlct"].forEach(function (slct) {
        slct.addEventListener("change", handleBuildMainStatChange);
        slct.addEventListener("change", controlStyles);
    });
    elms["statInp"].forEach(function (inp) {inp.addEventListener("focus", handleBuildStatFocus)});
    elms["statInp"].forEach(function (inp) {
        inp.addEventListener("input", handleBuildStatInp);
        inp.addEventListener("input", controlStyles);
    });
    elms["form"].addEventListener("submit", calcBuildResults);
    elms["costSetup"].addEventListener("change", controlStyles);
}

resetBuildState();
setBuildElements();
setBuildEventListeners();
handleBuildCharChange();
