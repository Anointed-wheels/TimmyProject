const chatButton = document.getElementById("ai-chat-button");
const chatBox = document.getElementById("ai-chat-box");
const closeChat = document.getElementById("close-ai-chat");

const chatForm = document.getElementById("ai-chat-form");
const chatInput = document.getElementById("ai-message-input");
const chatMessages = document.getElementById("ai-chat-messages");


chatButton.onclick = () => {
    chatBox.style.display = "flex";
}

closeChat.onclick = () => {
    chatBox.style.display = "none";
}


chatForm.addEventListener("submit", function(e){

    e.preventDefault();

    let message = chatInput.value;

    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerText = message;

    chatMessages.appendChild(userMessage);

    fetch("/ai/chat/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCookie("csrftoken")
        },
        body:JSON.stringify({message:message})
    })
    .then(response=>response.json())
    .then(data=>{

        let aiMessage = document.createElement("div");
        aiMessage.className = "ai-message";
        aiMessage.innerText = data.response;

        chatMessages.appendChild(aiMessage);

        chatMessages.scrollTop = chatMessages.scrollHeight;

    });

    chatInput.value="";
});

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;

            }
        }
    }

    return cookieValue;
}