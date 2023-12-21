const socket = new WebSocket('ws://127.0.0.1:8765');  // Replace with your server's address

const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');

const name = prompt("Please enter your name:");

socket.onopen = (event) => {
    const data = {
        id: 1,  // Announcement
        length: name.length,
        pseudo: name
    };
    socket.send(JSON.stringify(data));
    console.log('Announcement sent:', data);
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    console.log('Message received:', data);

    switch (data.id) {
        case 0:  // Message
            displayMessage(data);
            break;
        case 1:  // Announcement
            displayAnnouncement(data);
            break;
        case 2:  // Self message (sent by the user)
            displaySelfMessage(data);
            break;
        default:
            console.error('Unknown message type:', data);
    }
};

socket.onclose = (event) => {
    console.log('WebSocket connection closed:', event);
};

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== '') {
        const data = {
            id: 0,  // Message
            length: message.length,
            message: message
        };
        socket.send(JSON.stringify(data));
        messageInput.value = '';
        console.log('Message sent:', data);
    }
}

function displayMessage(data) {
    const messageElement = document.createElement('div');
    messageElement.style.color = `hsl(${data.color}, 100%, 50%)`;
    messageElement.textContent = `${data.hours}:${data.minutes} [${data.pseudo}]: ${data.message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function displayAnnouncement(data) {
    const announcementElement = document.createElement('div');
    announcementElement.textContent = `${data.hours}:${data.minutes} ${data.announcement}`;
    chatBox.appendChild(announcementElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function displaySelfMessage(data) {
    const selfMessageElement = document.createElement('div');
    selfMessageElement.style.color = `hsl(${data.color}, 100%, 50%)`;
    selfMessageElement.textContent = `${data.hours}:${data.minutes} [You]: ${data.message}`;
    chatBox.appendChild(selfMessageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
