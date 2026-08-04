async function update(){
    const response = await fetch("/user_staff");
    const messages = await response.json();

    const chat = document.getElementById("table");
    chat.innerHTML = "";

    for (const message of messages.staff) {
        console.log(message.login)
        chat.innerHTML += `
            <tr>
                <td class="employee-name">${message.name}</td>
                <td>${message.stack}</td>
                <td>
                    <div class="rating-container">
                        <input type="number" class="rating-input" value=${message.mark} min="0" max="5">
                        <span>/5</span>
                    </div>
                </td>
                <td><button class="delete-btn" onclick="delete_s('${message.login}')">Удалить</button></td>
            </tr>
        `;
    }
}

async function delete_s(login){
    const response = await fetch("/remove_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            login
        })
    });
    const data = await response.json()
    update()
}
update()