async function click_create(){
    console.log("try to create")
    const name = document.getElementById("name").value
    const owner = document.getElementById("owner").value
    const response = await fetch("/create_organization", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({

            name,
            owner
        })
    });
    const data = await response.json()
    if (data.OK){
        location.href = "/main_page"
    }else{
        alert("You have already joined organization")
    }
}