function showError(stringa, posizione){
	// Posizione 1: sopra
	// Posizione 2: vicino password
    // console.log("Sto eseguendo ShowError - "+stringa+" - Posizione: "+posizione);
	let posto = document.getElementById('separator');
    if(posizione == 2){
		posto = document.getElementById('username');
	}
    let err_popup = document.createElement('div');
    err_popup.className = 'err-popup';
    posto.insertAdjacentElement('afterend', err_popup);

    let icon = document.createElement('i');
    icon.className = 'fa-solid fa-circle-exclamation';
    err_popup.appendChild(icon);

    let paragraph = document.createElement('p');
    paragraph.innerHTML = stringa;
    err_popup.appendChild(paragraph);
}
function clearErrors(){
    let popupArray = Array.from(document.getElementsByClassName('err-popup'));
	popupArray.forEach((element) => element.remove());
}

function check_is_admin(){
	if (document.getElementById('username').value.toLowerCase() != 'admin'){
		return false;	
	}
	showError('Impossibile accedere come admin.');
	return true;
}


function validateForm(){
	// definire caratteri da NON trovare nelle stringhe
	clearErrors();
	
	if (check_is_admin())
		return false;

	let email = document.getElementById('email').value;
	let username = document.getElementById('username').value;
	let password1 = document.getElementById('password1').value;
	let password2 = document.getElementById('password2').value;
	
	// Controlla se ci sono caratteri speciali non consentiti nel nome utente
	let usernameRegex = /^[a-zA-Z0-9_.\-!:]+$/;
	if (!usernameRegex.test(username)) {
		showError('Username non valido.', 1);
	  	return false;
	}
	
	// Controlla la validità dell'indirizzo email
	if (email != undefined){
		let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(email)) {
			showError('Email non valida.', 1);
		  	return false;
		}
	}
	
	// Controlla se la password contiene caratteri speciali non consentiti
	let passwordRegex = /^[a-zA-Z0-9_.\-!:]+$/;
	if (!passwordRegex.test(password1)) {
		showError('Password non valida.', 2);
		return false;
	}

	if (password2 != undefined){
		let passwordRegex = /^[a-zA-Z0-9_.\-!:]+$/;
		if (!passwordRegex.test(password2)) {
			showError('Password non valida.', 2);
			return false;
		}
		if (password1 != password2){
			showError('Le due password non corrispondono.',2);
			return false;
		}
	}

	return true;	
}

function changeImgCaption(){
	let pElement = document.getElementById('img-caption');
	pElement.innerHTML = 'Immagine selezionata.';
}