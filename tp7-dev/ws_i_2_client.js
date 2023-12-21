// Créer une connexion WebSocket
const socket = new WebSocket('ws://localhost:8765');

// Événement appelé lors de l'ouverture de la connexion WebSocket
socket.addEventListener('open', (event) => {
    console.log('WebSocket connection opened:', event);
});

// Événement appelé lors de la réception de données du serveur
socket.addEventListener('message', (event) => {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML += '<p>Received: ' + event.data + '</p>';
});

// Événement appelé en cas d'erreur
socket.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});

// Événement appelé lorsque la connexion WebSocket est fermée
socket.addEventListener('close', (event) => {
    console.log('WebSocket connection closed:', event);
});

// Fonction pour envoyer un message au serveur
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;

    // Envoyer le message au serveur
    socket.send(message);

    // Effacer le champ de saisie
    messageInput.value = '';
}