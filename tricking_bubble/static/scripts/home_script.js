function setStartingValues(){
    // Array associativo: {'nomeId':{'element':element ,'top':0value, 'left':0value}}
    base_values = {}
    arrayId = ['rear_1','rear_2', 'rear_3','front_1','front_2']

    arrayId.forEach((idName)=>{
        element = document.getElementById(idName);
        style = window.getComputedStyle(element);
        start_top = style.getPropertyValue('top').replace('px','');
        start_left = style.getPropertyValue('left').replace('px','');

        base_values[idName] = {'element': element, 'top': parseInt(start_top), 'left':parseInt(start_left)};
    })
    //console.log( JSON.stringify(base_values, null, 2) )
    return base_values;
}
function setImageBehaviour(){
    let startingValues = setStartingValues();   // Array associativo: {'nomeId':{'top':0value, 'left':0value}}

    window.addEventListener('scroll', () => {
        let value = window.scrollY;
        // console.log(value);
        document.getElementById('rear_1').style.top = startingValues['rear_1'].top + value * 0.5+'px';
        document.getElementById('rear_1').style.left = startingValues['rear_1'].left - value * 0.4+'px';
        document.getElementById('rear_1').style.rotate = -value * 0.005 +'rad';
        document.getElementById('rear_2').style.top = startingValues['rear_2'].top - value * 0.75 +'px';
        document.getElementById('rear_2').style.left = startingValues['rear_2'].left + value * 0.5 +'px';
        document.getElementById('rear_3').style.top = startingValues['rear_3'].top - value * 0.75 +'px';
        document.getElementById('rear_3').style.left = startingValues['rear_3'].left + value * 0.5 +'px';
        if (screen.width > 490){
            document.getElementById('front_1').style.top = startingValues['front_1'].top + value * 0.3+'px';
            document.getElementById('front_1').style.left = startingValues['front_1'].left - value * 0.5+'px';
            document.getElementById('front_1').style.rotate = -value * 0.0005 +'rad';
            document.getElementById('front_2').style.top = startingValues['front_2'].top + value * 0.75 +'px';
            document.getElementById('front_2').style.left = startingValues['front_2'].left + value * 0.5 +'px';
            document.getElementById('front_2').style.rotate = value * 0.001 +'rad';
        }
    })
}
setImageBehaviour();