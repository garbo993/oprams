const forelement = document.getElementById("login");

forelement.addEventListener("submit", (event)=>{

    event.preventDefault();
    let loginuser = document.getElementById("user").value;
    let loginpass = document.getElementById("password").value;
    let login = { user : loginuser , password : loginpass }
    let loginJson = JSON.stringify(login) 

    fetch('http://127.0.0.1:5000/login' , {
        method: 'Post' , 
        body : loginJson
    })  
})