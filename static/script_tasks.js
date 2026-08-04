async function update(){
    const response = await fetch("/user_tasks");
    const messages = await response.json();

    const chat = document.getElementById("tasks");
    chat.innerHTML = "";

    for (const message of messages.tasks) {
        chat.innerHTML += `
            <div class="schedule-card">
                <h3>${message.title}</h3>
                <p>Дедлайн: ${message.time}</p>
            </div>
        `;
    }
}
update()