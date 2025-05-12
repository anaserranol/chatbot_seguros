document.addEventListener('DOMContentLoaded', () => {
    console.log("Cargado")
    const chat = document.getElementById('chat');
    const chatInput = document.getElementById('input');
    const chatButton = document.getElementById('sendButton');
    const questionButtonClientArea = document.getElementById('clientArea');
    const questionButtonNewUser = document.getElementById('newUser');
    const questionButtonRegisterUser = document.getElementById('registerUser');
    const questionButtonTypesInsurance = document.getElementById('typesInsurance');
    const questionButtonContactInfo = document.getElementById('contactInfo');

    function addMessage(text, sender = 'bot', state = '') {
        console.log("Estado", state)
        const msg = document.createElement('div');
        msg.className = `msg msg_${sender}`;
        text_modify = text.replace(/\n/g, '<br>');
        console.log(text_modify)
        if (state != 'thinking') {
            msg.innerHTML = `<div class=msg_${sender}_text>
                                <span class="text"> ${text_modify} </span>
                            </div>`;
                
        } else {
            msg.innerHTML = `<div class="msg_${sender}_text" id = "wave">
                                <span class="dot"></span>
                                <span class="dot"></span>
                                <span class="dot"></span>
                            </div>`
        }
        chat.appendChild(msg);
        chat.scrollTop = chat.scrollHeight;
        return msg;
    }

    async function sendMessage(freqQuestion = false) {
        let text = "";
        if (!freqQuestion) {
            const input = document.getElementById('input');
            text = input.value.trim();
            if (!text) return;
        } else {
            text = freqQuestion
        }

        addMessage(text, 'user');
        input.value = '';
        
        const thinking = addMessage("...", 'bot', "thinking")
        
        try {
            // Petición respuesta modelo
            const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: text })
            });
            
            // Quitamos el mensaje de que está pensando
            chat.removeChild(thinking)

            // Respondemos
            const data = await res.json();
            addMessage(data.reply, 'bot', "answer");

        } catch (err) {
            addMessage("Hubo un error al contactar con el chatbot :(")
        }

    }


    chatButton.addEventListener(
        "click",
        sendMessage
    );

    chatInput.addEventListener(
        "keydown",
        manageTypeMessage
    );

    questionButtonClientArea.addEventListener(
        "click",
        manageClickQuestionButton
    );

    questionButtonNewUser.addEventListener(
        "click",
        manageClickQuestionButton
    );

    questionButtonRegisterUser.addEventListener(
        "click",
        manageClickQuestionButton
    );

    questionButtonTypesInsurance.addEventListener(
        "click",
        manageClickQuestionButton
    );

    questionButtonContactInfo.addEventListener(
        "click",
        manageClickQuestionButton
    );

    /**
     * Función que recoge los dos eventos que puede hacer el usuario:
     *	--> Si pulsa enter (keycode == 13): enviar el mensaje
    *  --> Si pulsa cualquier otra tecla: escribir dicho caracter
    * @param {Event} event 	- Evento de pulsar una tecla
    */
    function manageTypeMessage (event) {
        if (event.which === 13) {
			// Anulamos el evento por defecto (\n)	
	    	event.preventDefault();
			// Enviamos el mensaje
	      	sendMessage();
	    }
    }

    function manageClickQuestionButton () {
        console.log("HOLAAA")
        sendMessage(this.innerHTML)
    }
});