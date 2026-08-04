async function click_register(){
    console.log("try to register")
    const login = document.getElementById("login").value
    const password = document.getElementById("password").value
    const name = document.getElementById("name").value
    const stack = document.getElementById("stack").value


    const response = await fetch("/reg", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            login,
            password,
            name,
            stack
        })
    });
    console.log(login, password, name, stack)
    const data = await response.json()
    console.log(data.OK)
    if (data.OK === true){
        location.href = "/main_page"
    }else{
        console.log("loh")
        if (data.error === 1){
            alert(`Incorrect login, ${data.description}`)
        } else if (data.error === 2){
            alert(`Incorrect password, ${data.description}`)

        } else if (data.error === 3){
            alert(`Incorrect name, ${data.description}`)

        } else if (data.error === 4){
            alert(`Incorrect stack, ${data.description}`)
        }
    }
}

async function click_login(){
    console.log("try to login")
    const login = document.getElementById("login").textContent
    const password = document.getElementById("password").textContent


    const response = await fetch(`/reg?login=${login}&password=${password}`, {method: "POST"});
    const data = await response.json()
    if (data.OK){
        location.href = "/main_page"
    }else{
        console.log("loh")
        if (data.error === 1){
            alert("Incorrect password")
        } else if (data.error === 2){
            alert("Incorrect login")
        }
    }
}

async function click_timetable(){
    location.href = "/timetable"
}
async function click_staff(){
    location.href = "/staff"
}
async function click_profile(){
    location.href = "/profile"
}
async function click_chat(){
    location.href = "/chat"
}

