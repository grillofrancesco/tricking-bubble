window.onload = () =>{
    let circularProgress = document.querySelectorAll(".circular-progress");
    
    circularProgress.forEach(element => {

        
        let progressValue = element.querySelector(".progress-value"),       // Prende elemento per mostrare percent
            endValue = element.dataset.progress;                            // Prende valore finale percent

        let progressStartValue = 0,
            progressEndValue = endValue,
            speed = 50;

        let progress = setInterval(()=>{
            //console.log(progressStartValue);
            
            progressValue.textContent = `${progressStartValue}%`;           // Aggiorna percent
            if (endValue == 0)
                element.style.background = 'transparent';
                else
                element.style.background = `conic-gradient(var(--rich-blue) ${progressStartValue * 3.6}deg, transparent 0deg)`; // Aggiorna radial
                
                if (progressStartValue >= progressEndValue){
                    clearInterval(progress);
            }
            progressStartValue ++;
        }, speed); 
    });
}