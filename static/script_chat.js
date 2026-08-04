async function loadMessages() {
    const response = await fetch("/chat");
    const messages = await response.json();

    const chat = document.getElementById("chat");
    chat.innerHTML = "";

    for (const message of messages.messages) {
        chat.innerHTML += `
            <div>
                <b>${message.user}</b>: ${message.text}
            </div>
        `;
    }
}

loadMessages();
setInterval(loadMessages, 500)