function togglePopup(){
    let popup = document.getElementById('popup');
    popup.classList.toggle('active');
}
function scrollToTop(){
    scrollTo(0,0, 'instant');
}
function resetColor(list_of_svg){
    list_of_svg.forEach(element => {
        element.style.fill = 'var(--rich-blue)';
    });
}
function setValutazioni(media, nValori){
    let i_space = document.querySelector('.i-space');
    i_space.innerHTML = "";

    const num_fulls = String(media).charAt(0),        // prende valore media
        second_digit = parseInt(String(media).charAt(2));     // prende seconda cifra per capire se serve piena o mezza icona
    const num_remaining = () => {
        if (num_fulls == 5)
            return 0;
        else
            return 5 - num_fulls - 1;
    }
    
    //console.log("fulls: "+num_fulls, "second digit: "+ second_digit+" remaining: "+num_remaining());

    const full_circle = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/></svg>`;
    const half_circle = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M448 256c0-106-86-192-192-192V448c106 0 192-86 192-192zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256z"/></svg>`
    const empty_circle = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M464 256A208 208 0 1 0 48 256a208 208 0 1 0 416 0zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256z"/></svg>`
    
    const full_or_half = () => {
        if (isNaN(second_digit))
            return empty_circle
        if (second_digit < 3)           // controlla se deve aggiungere cerchio pieno, vuoto o metà
            return empty_circle;
        if (second_digit > 8)
            return full_circle;
        return half_circle;
    };

    let icon_sequence_html = full_circle.repeat(num_fulls);     // inserisce pieni

    if (num_fulls < 5)
        icon_sequence_html += full_or_half()                    // inserisce metà se necessario
    if (num_remaining() > 0)
        icon_sequence_html += empty_circle.repeat(num_remaining()); // inserisce rimanenti se necessario

    i_space.insertAdjacentHTML('beforeend', icon_sequence_html);
    let svgs = i_space.querySelectorAll('svg');
    
    for (let i = 0; i< svgs.length; i++){
        svgs[i].addEventListener('click', ()=>{
            //console.log("Valore: ", i+1);
            canVote = false;
            let new_value = i+1;
            resetColor(svgs);
            svgs[i].style.fill = "var(--rich-dark)";

            $.ajax({                                // impostazione chiamata al server per l'invio del valore della valutazione
                type: 'POST',
                url: '/trick_tree/',
                data: {
                    form_use: '1',
                    trick_selezionato: $('#checkIfCompletato').val(),
                    valore_selezionato: new_value,

                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                }
            });
            nValori = parseInt(nValori);
            new_media = (media * nValori + new_value)/(nValori+1);
            console.log("media, new_media, nValori, nValori+1");
            console.log(media, new_media, nValori, nValori+1);
            

            new_media = new_media.toFixed(1);
            shownMediaValue = document.querySelector('.shown-media');
            shownMediaValue.remove();
            setValutazioni(new_media, nValori+1);
        });
    }
    let shownMediaValue = `<p class='shown-media'>Media: ${parseFloat(media).toFixed(1)} / 5</p>`
    
    i_space.insertAdjacentHTML('afterend', shownMediaValue);
}
function creaCommento(nomeUtente, testo){
    var comments_space = document.querySelector('.comments-space');

    /* console.log(comments_space.querySelector('#no-comment')); */
    let p_no_comment = comments_space.querySelector('#no-comment')
    if ( p_no_comment != null){
        p_no_comment.remove();
    }

    c_div = document.createElement('div');
    c_div.className = 'comment';
    comments_space.insertAdjacentElement("afterbegin", c_div);
    
    c_span = document.createElement('span');
    c_span.className = 'nome-utente';
    c_div.appendChild(c_span);
    c_span.innerHTML = '@ '+nomeUtente + ":";
    
    c_content = document.createElement('p');
    c_content.className = 'comment-content';
    c_div.appendChild(c_content);
    

    c_content.innerHTML += testo
}
function visualizzaCommenti(json_commenti){
    json_commenti = JSON.parse(json_commenti);

    // Crea tanti commenti quanti richiesti    
    json_commenti.forEach((commento)=>{
        //console.log("Creando commento")
        creaCommento(commento.user_id, commento.testo)
    });
}
function setCommenti(json_commenti){
    //console.log(json_commenti);
    var comments_space = document.querySelector('.comments-space');

    json_commenti = json_commenti.replace(/'/g, '"');
    if (json_commenti == '[]'){
        comments_space.insertAdjacentHTML('afterbegin', '<p id="no-comment">Non ci sono commenti.</p>');
    }else{
        visualizzaCommenti(json_commenti);
    }
}
function completeTrick(){
    let button = document.querySelector('.pressable-trick');

    if (button.classList.contains('completed')){
        button.classList.toggle('completed');

        // console.log('Non più completato');
    }else{
        if(!button.classList.contains('moving')){
            button.classList.toggle('moving');
    
            // console.log('Ora si muove');
            
            setTimeout(()=>{
                button.classList.toggle('moving');
                button.classList.toggle('completed');
            }, 1000)
        }
    }

    // Sends info to server:
    $.ajax({
        type: 'POST',
        url: "/trick_tree/",
        data: {
            form_use: '0',
            trick_selezionato: $('#checkIfCompletato').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
    });
}
function registraCommento(){
    // console.log("Premuto send");
    let commentValue = document.querySelector('#comment-content').value;
    document.querySelector('#comment-content').value = "";
    if (commentValue == "")
        return

    $.ajax({                                // impostazione chiamata al server per l'invio del valore della valutazione
        type: 'POST',
        url: '/trick_tree/',
        data: {
            form_use: '2',
            trick_selezionato: $('#checkIfCompletato').val(),
            commento: commentValue,

            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
    });
    
    creaCommento(utente, commentValue)
}

function openPopup(titolo=null, descrizione=null, link_1=null, link_2=null, link_3=null, media=null, foto_trick, id_trick, completed="false", json_commenti){
    scrollToTop();
    let popup = document.getElementById('popup');
    
    popup.querySelector('.inside-trick').src = foto_trick;        // icona visualizzata
    let button = popup.querySelector('.pressable-trick');
    button.value = id_trick;     // id trick
    if (Boolean(completed))
        button.classList.add('completed');

    let popupWindow = popup.querySelector('.window');
    popupWindow.querySelector('h1').innerHTML = titolo;   // h1

    let content = popupWindow.querySelector('.content');
    content.querySelector('p').innerHTML = descrizione;  // p

    let ul = content.querySelector('ul');

    ul.innerHTML = `<li><iframe src=${link_1} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen async></iframe></li>`;
    
    if (link_2 != 'None')
        ul.innerHTML += `<li><iframe src=${link_2} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen async></iframe></li>`;
    if (link_3 != 'None')
        ul.innerHTML += `<li><iframe src=${link_3} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen async></iframe></li>`;


    //  Valutazioni
        
    var nValori = media.split('|')[0];
    media = media.split('|')[1];
    canVote = true;
    setValutazioni(media, nValori);
    
    // Commenti
    setCommenti(json_commenti);
       
    togglePopup();
}

var new_media = null;