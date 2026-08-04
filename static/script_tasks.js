async function updatee(){
    const response = await fetch("../user_tasks");
    const messages = await response.json();

    const chat = document.getElementById("tasksList");
    chat.innerHTML = "";

    for (const message of messages.tasks) {
        chat.innerHTML += `
            <li class="task-item">
                <div class="task-header">
                    <input type="checkbox" class="task-checkbox">
                    <div class="task-avatar">Р</div>
                    <div class="task-main-info">
                        <h3>${message.title}</h3>
                        <p class="task-status">${message.deadline}</p>
                    </div>
                    <div class="task-rating">
                        <span class="star">★</span>
                        <span class="star">★</span>
                        <span class="star">★</span>
                        <span class="star">★</span>
                        <span class="star">★</span>
                    </div>
                </div>
                <button class="task-delete-btn" onclick="delete_task('${message.title}')">✕</button>
            </li>
        `;
    }
}

async function create_task(){
    console.log("try to create")
    const login = document.getElementById("login").value
    const title = document.getElementById("title").value
    const deadline = document.getElementById("deadline").value
    const response = await fetch("../add_task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            login,
            title,
            deadline
        })
    });
    console.log(login, title, deadline)
    const data = await response.json()
    console.log(data.OK)
}

async function delete_task(name){
    const response = await fetch("../remove_task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name
        })
    });
    const data = await response.json()
    updatee()
}
updatee()