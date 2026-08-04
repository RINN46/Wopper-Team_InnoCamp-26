async function update(){
    const response = await fetch("/user_staff");
    const messages = await response.json();

    const chat = document.getElementById("table");
    chat.innerHTML = "";

    for (const message of messages.staff) {
        chat.innerHTML += `
            <div class="schedule-card">
                <h3>${message.title}</h3>
                <p>${message.time}</p>
                <span class="event-type">${message.description}</span>
            </div>
        `;
    }
}