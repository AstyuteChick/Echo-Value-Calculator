
const mainStatDataEle=document.querySelector("#main-stat-data");
const mainStatData=JSON.parse(mainStatDataEle.textContent);

state["buildData"]=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
state["costSetup"]=[0, 0, 0, 0, 0];
state["mainStats"]=["noVal", "noVal", "noVal", "noVal", "noVal"];

elms["costSetup"]=document.querySelector("#cost-slct");
elms["mainStatSlct"]=document.querySelectorAll(".mainStatSlct");
elms["statInp"]=document.querySelectorAll(".statInp");

function renderBuildStatNames(){
    state["buildData"]=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    state["costSetup"]=[0, 0, 0, 0, 0];
    state["mainStats"]=["noVal", "noVal", "noVal", "noVal", "noVal"];
    elms["costSetup"].value="noVal";
    elms["mainStatSlct"].forEach(function (slct){
        slct.innerHTML="<option value='noVal'>Select your Echo's Main-Stat</option>";
        slct.labels[0].textContent="? - Cost Echo: ";
    });
    elms["statInp"].forEach(function (inp){
        inp.value=0.0;
        inp.hidden=true;
        inp.labels[0].hidden=true;
    });
    charData[state["selectedChar"]][0].forEach(function (relVal, ind){
        if (!relVal) return;
        elms["statInp"].forEach(function (inp){
            if (echoData[ind]!==inp.id) return;
            inp.hidden=false;
            inp.labels[0].hidden=false;
        });
    });
}

function handleBuildCostChange(event){
    const prevCostSetupState=state["costSetup"];
    const curCostSetup=event.currentTarget.value;
    state["costSetup"]=[];
    for (let char of curCostSetup) {state["costSetup"].push(Number(char));}
    elms["mainStatSlct"].forEach(function (slct){
        slct.innerHTML="<option value='noVal'>Select your Echo's Main-Stat</option>";
        slct.labels[0].textContent="? - Cost Echo: ";
    });
    if (curCostSetup==="noVal") return;
    elms["mainStatSlct"].forEach(function (slct, ind){
        const echoCost=state["costSetup"][ind];
        slct.labels[0].textContent=String(echoCost) + " - Cost Echo: ";
        Object.keys(mainStatData[echoCost]).forEach(function (statName){
            const opt=document.createElement("option");
            opt.value=statName;
            opt.textContent=statName;
            slct.appendChild(opt);
        });
    });
}

function handleBuildMainStatChange(event){
    const curSlct=event.currentTarget;
    const echoNo=Number(curSlct.id[curSlct.id.length-1]);
    state["mainStats"][echoNo-1]=curSlct.value;
}

function handleBuildStatFocus(event){
    if (event.currentTarget.value){event.currentTarget.value="";}
}

function handleBuildStatInp(event){
    const curInp=event.currentTarget;
    state["buildData"][echoData.indexOf(curInp.id)]=curInp.value;
}

function updateBuildResults(result){
    elms["scoreVal"].innerHTML = result.score;
    elms["tierVal"].innerHTML = result.tier;
}

async function calcBuildResults(){
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

function setBuildEventListeners(){
    elms["charOptsLst"].addEventListener("click", renderBuildStatNames);
    elms["costSetup"].addEventListener("change", handleBuildCostChange);
    elms["mainStatSlct"].forEach(function (slct){slct.addEventListener("change", handleBuildMainStatChange);});
    elms["statInp"].forEach(function (inp){inp.addEventListener("focus", handleBuildStatFocus)});
    elms["statInp"].forEach(function (inp){inp.addEventListener("input", handleBuildStatInp)});
    elms["form"].addEventListener("submit", calcBuildResults);
}

setBuildEventListeners();
renderBuildStatNames();
