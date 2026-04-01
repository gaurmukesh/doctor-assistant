const session_id = Math.random().toString(36).substring(2);
//let history = []; //removed for langchain
function sendMessage() {
    const input = document.getElementById("userInput").value;
    const name = document.getElementById("patientName").value;
    const phone = document.getElementById("patientPhone").value;
    const email = document.getElementById("patientEmail").value;
    //history.push({"role": "user", "content": input}); //removed for langchain
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            session_id: session_id,
            //history: history,
            message: input,
            patient_name: name,
            phone: phone,
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += "<p><b>You:</b> " + input + "</p>";

        // Display bot response cleanly
        if (data.reply) {
            chatbox.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";
            //history.push({"role": "assistant", "content": data.reply});
        } else {
            chatbox.innerHTML += "<p><b>Bot:</b> " + JSON.stringify(data) + "</p>";
        }
        
        document.getElementById("userInput").value = "";
    });
}
