// WebSocket Initialization
var socket = io.connect('http://' + document.domain + ':' + location.port);
var currentUsername = "";

socket.on('broadcast_message', function(data) {
    document.getElementById('messages').innerHTML += '<br>' + data;
});

socket.on('lobby_update', function(updatedLobbies) {
    console.log("Received lobby_update event", updatedLobbies);
    renderLobbies(updatedLobbies);
});

// Message Sending Function
function sendMessage() {
    var message = document.getElementById('messageInput').value;
    socket.emit('send_message', {username: currentUsername, message: message});
}

// User Registration Function
function registerUser() {
    var username = document.getElementById('usernameInput').value;
    var password = document.getElementById('passwordInput').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}

// User Login Function
function loginUser() {
    var username = document.getElementById('usernameInput').value;
    var password = document.getElementById('passwordInput').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => {
        if (response.status === 200) {
            currentUsername = username;  // <-- Using the variable directly instead of querying the DOM again
            document.getElementById('chatSection').style.display = 'block';
            document.getElementById('userSection').style.display = 'none';
            document.getElementById('lobbySection').style.display = 'block';
            fetchLobbies();
        }
        return response.text();
    })
    .then(data => alert(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Lobby Creation Function
function createLobby() {
    fetch('/create_lobby', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        fetchLobbies();
    });
}

// Join Lobby Function
function joinLobby(lobbyId) {
    fetch(`/join_lobby/${lobbyId}`, { method: 'POST' })
    .then(response => {
        if (response.status === 403) {
            alert("Lobby is full!");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            console.log(data);
        }
    });
}

// Fetch Lobbies Function
function fetchLobbies() {
    fetch('/lobbies')
    .then(response => response.json())
    .then(data => {
        renderLobbies(data);
    });
}

// Render Lobbies Function
function renderLobbies(lobbiesData) {
    const lobbiesList = document.getElementById('lobbies-list');
    lobbiesList.innerHTML = "";
    for (let lobbyId in lobbiesData) {
        const listItem = document.createElement('li');
        listItem.innerHTML = `Lobby ${lobbyId}: ${lobbiesData[lobbyId].join(", ")} <button onclick="joinLobby(${lobbyId})">Join</button>`;
        lobbiesList.appendChild(listItem);
    }
}
