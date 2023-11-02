// WebSocket Initialization
var socket = io.connect('http://' + document.domain + ':' + location.port);
var currentUsername = "";

socket.on('broadcast_message', function(data) {
    document.getElementById('messagesBox').innerHTML += '<br>' + data;
});

// Socket event listener for player list updates
socket.on('players_update', function(updatedPlayers) {
    console.log("Received players_update event", updatedPlayers);
    renderLobby(updatedPlayers);
});

socket.on('game_started', function() {
    document.getElementById('lobbySection').style.display = 'none';
    document.getElementById('gameSection').style.display = 'block';
});

// Message Sending Function
function sendMessage() {
    var message = document.getElementById('messageInput').value;
    if (message.trim() !== '') {
        socket.emit('send_message', { username: currentUsername, message: message });
        document.getElementById('messageInput').value = ''; // Clear input after sending
    }
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
            fetchPlayersInLobby();
        }
        return response.text();
    })
    .then(data => alert(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}
// join Function
function join() {
    fetch('/join', { method: 'POST' })
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


function fetchPlayersInLobby() {
    fetch('/get_players')
    .then(response => response.json())
    .then(data => {
        renderLobby(data.players);
    })
    .catch((error) => {
        console.error('Error fetching players in lobby:', error);
    });
}



function renderLobby(playersData) {
    const playerListDiv = document.getElementById('playersList');
    playerListDiv.innerHTML = ""; // Clearing previous content
    
    if (playersData.length === 0) {
        playerListDiv.innerHTML = "Lobby is currently empty!";
    } else {
        const playersList = document.createElement('ul');
        playersData.forEach(player => {
            const listItem = document.createElement('li');
            listItem.innerHTML = player;
            playersList.appendChild(listItem);
        });
        playerListDiv.appendChild(playersList);
    }
}



function startGame() {
    fetch('/start_game', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert("Game started!");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("An error occurred while trying to start the game.");
    });
}



