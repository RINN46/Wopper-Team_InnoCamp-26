async function click_register(){
    console.log("try to register")
    const login = document.getElementById("login").textContent
    const password = document.getElementById("password").textContent
    const name = document.getElementById("name").textContent
    const stack = document.getElementById("stack").textContent


    const response = await fetch(`/reg?login=${login}&password=${password}&name=${name}&stack=${stack}`, {method: "POST"});
    const data = await response.json()
    if (data.OK){
        location.href = "/main_page"
    }else{
        console.log("loh")
        if (response.error === 1){
            alert("Incorrect login")
        } else if (response.error === 2){
            alert("Incorrect password")

        } else if (response.error === 3){
            alert("Incorrect name")

        } else if (response.error === 4){
            alert("Incorrect stack")
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
        if (response.error === 1){
            alert("Incorrect password")
        } else if (response.error === 2){
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
