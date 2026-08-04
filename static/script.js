async function click_register(){
    console.log("try to register")
    const login = document.getElementById("login").textContent
    const password = document.getElementById("password").textContent
    const name = document.getElementById("name").textContent
    const stack = document.getElementById("stack").textContent


    const response = await fetch(`/reg?login=${login}&password=${password}&name=${name}&stack=${stack}`, {method: "POST"});
    const data = await response.json()
    if (data.OK){

    }else{
        console.log("loh")
    }
}