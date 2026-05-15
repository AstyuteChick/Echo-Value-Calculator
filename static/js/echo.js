
const echoDataEle = document.querySelector("#echo-data");
const echoData = JSON.parse(echoDataEle.textContent);
const substatRollsEle = document.querySelector("#substat-rolls-data");
const substatRollsData = JSON.parse(substatRollsEle.textContent);

if (!charData[state.selectedChar]){selectChar(`Aemeath`);}
state["echoData"] = [null, null, null, null, null, null, null, null, null, null, null, null, null];

elms["allEchoNameSlct"] = document.querySelectorAll(".statNameSlct");
elms["allEchoValSlct"] = document.querySelectorAll(".statValueSlct");

function setEchoEventListeners(){
    elms["allEchoNameSlct"].forEach(function (slct){slct.addEventListener("change", handleEchoSlctChange);});
    elms["allEchoValSlct"].forEach(function (slct){slct.addEventListener("change", handleEchoSlctChange);});
    elms["charOptsLst"].addEventListener("click", setEchoSubstatNames);
}

function setEchoSubstatNames(){
    elms["allEchoNameSlct"].forEach(function (nameSlct){nameSlct.innerHTML = "<option val = 'noVal'>Select Echo Substat</option>"});
    charData[state.selectedChar][0].forEach(function (relVal, ind){
        if (relVal) {
            elms["allEchoNameSlct"].forEach(function (nameSlct){
                const opt = document.createElement("option");
                opt.value = echoData[ind];
                opt.textContent = echoData[ind];
                nameSlct.appendChild(opt);});
        }
    });
}

function handleEchoSlctChange(event){
    elms["allEchoNameSlct"].forEach(function (nameSlct){
        console.log(event.currentTarget.value);
        console.log(nameSlct.id, event.currentTarget.id);
        if (nameSlct.id !== event.currentTarget.id && event.currentTarget.value !== "noVal"){
            nameSlct.querySelector(`option[value='${event.currentTarget.value}']`).remove();
        } else if (event.currentTarget.value === "noVal") {
            // Nahh this is getting too weird. Need functions to handle adding and removing elements. 
        }
    });
}

setEchoEventListeners();
setEchoSubstatNames();