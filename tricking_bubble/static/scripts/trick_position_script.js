//import positionData from './trickPositions.json' assert {"type":"json"}
const positionData = {
    "0":{ "offset": "3rem"},
    "1":{ "offset": "-6rem"},
    "2":{ "offset": "8rem"},
    "3":{ "offset": "-10rem"},
    "4":{ "offset": "3rem"},
    "5":{ "offset": "-10rem"},
    "6":{ "offset": "0rem"},
    "7":{ "offset": "8rem"},
    "8":{ "offset": "-6rem"},
    "9":{ "offset": "9rem"},
    "10":{ "offset": "-10rem"},
    "11":{ "offset": "2rem"},
    "12":{ "offset": "-10rem"},
    "13":{ "offset": "10rem"},
    "14":{ "offset": "0rem"},
    "15":{ "offset": "8rem"},
    "16":{ "offset": "-6rem"},
    "17":{ "offset": "0rem"},
    "18":{ "offset": "8rem"},
    "19":{ "offset": "-6rem"}
};

function setPositions(_multiplier, _direction){
    let trick_array = document.getElementsByClassName('trick');
    for(let i=0; i < trick_array.length; i++){
        // usa alt 96 per concatenare:      '${variabile} stringa'

        trick_array[i].style.transform = `translate${_direction}(calc(${positionData[i].offset} * ${_multiplier}))`
    }
}

function spreadTricks(){
    let screenWidth = screen.width;
    let direction = "";
    let multiplier = 1;
    // Imposta direzione in cui inserire offset
    if (screenWidth <= 490){
        // Mobile -> X
        direction = "X";
        multiplier = 0.65;
    }else{
        // Desktop -> Y
        direction = "Y";
        multiplier = 1.3;
    }
    setPositions(multiplier, direction);
}
spreadTricks();
