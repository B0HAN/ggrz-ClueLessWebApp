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
    fetchPlayersInGame();
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
        alert(error);
    });
}

// I don't know how to get the players from that same ID so I copied fetchPlayersInLobby
function fetchPlayersInGame() {
    fetch('/get_players')
    .then(response => response.json())
    .then(data => {
        getPlayerInGame(data.players);
    })
    .catch((error) => {
        console.error('Error fetching players in lobby:', error);
    });
}

// I don't know how to get the players from that same ID so I copied renderLobby and renamed the IDs
function getPlayerInGame(playersData) {
    const playerListGameDiv = document.getElementById('playersInGameList');
    playerListGameDiv.innerHTML = ""; // Clearing previous content
    
    if (playersData.length === 0) {
        playerListGameDiv.innerHTML = "Lobby is currently empty!";
    } else {
        const playersInGameList = document.createElement('ul');
        playersData.forEach(player => {
            const listItem = document.createElement('li');
            listItem.innerHTML = player;
            playersInGameList.appendChild(listItem);
        });
        playerListGameDiv.appendChild(playersInGameList);
    }
}

const characterData = {
    scarlet: { room: [0, 0], color: 'red' },
    peacock: { room: [0, 2], color: 'blue' },
    green: { room: [2, 2], color: 'green' },
    mustard: { room: [4, 4], color: 'yellow' },
    plum: { room: [4, 4], color: 'purple' },
    white: { room: [4, 4], color: 'white' }
}

// Get all cells on the game board
const cells = document.querySelectorAll('.cell').forEach(cell => {
    const coordinates = cell.getAttribute('data-coordinates').split(',');
    const row = parseInt(coordinates[0]);
    const col = parseInt(coordinates[1]);

    // Check if the current cell matches any character's position
    Object.keys(characterData).forEach(character => {
        const characterPosition = characterData[character];
        const [cRow, cCol] = characterPosition.room;
        // Find the cell with matching coordinates
        const cell = document.querySelector(`.cell[data-coordinates="${cRow},${cCol}"]`);

        if (cell && !cell.querySelector(`.character-dot.${character}`)) {
            // Create a character dot element
            const characterDot = document.createElement('div');
            characterDot.classList.add('character-dot', character);
            characterDot.style.backgroundColor = characterPosition.color;
        
            // Append the character dot to the cell
            cell.appendChild(characterDot);
          }
    });

    cell.addEventListener('click', function() {
        // Eventually add ability to check for available moves
        if (!cell.classList.contains('restricted')) {
            var location;
            if (isRoom(row, col)) {
                location = getRoomName(row, col);
            }
            else {
                location = getHallwayName(row, col);
            }
            socket.emit('move_player', { username: currentUsername, destination: location });
        }
  });
});

function getRoomName(row, col) {
    const roomNames = [
      'Study', 'Hall', 'Lounge',
      'Library', 'Billiard Room', 'Dining Room',
      'Conservatory', 'Ballroom', 'Kitchen'
    ];
    const index = (row / 2) * 3 + col / 2;
    return roomNames[index];
}

function getHallwayName(row, col) {
    const hallwayNames = [
      'Hallway Study-Hall', 'Hallway Hall-Lounge', 'Hallway Study-Library', 'Hallway Hall-Billiard Room', 'Hallway Lounge-Dining Room',
      'Hallway Library-Billiard Room', 'Hallway Billiard Room-Dining Room', 'Hallway Library-Conservatory', 'Hallway Billiard Room-Ballroom', 'Hallway Dining Room-Kitchen',
      'Hallway Conservatory-Ballroom', 'Hallway Ballroom-Kitchen'
    ];
    const index = (row * 5 + col - 1) / 2;
    return hallwayNames[index];
  }

function isRoom(row, col) {
    const roomPositions = [
      [0, 0], [0, 2], [0, 4],
      [2, 0], [2, 2], [2, 4],
      [4, 0], [4, 2], [4, 4]
    ];
    return roomPositions.some(coords => coords[0] === row && coords[1] === col);
}

const suggestionButton = document.getElementById('suggestionButton');
const suggestionMenu = document.getElementById('suggestionMenu');

suggestionButton.addEventListener('click', function() {
    suggestionMenu.classList.toggle('hidden');
});

submitSuggestionButton.addEventListener('click', function() {
    suggestionMessage();
    suggestionMenu.classList.toggle('hidden');
});

const accusationButton = document.getElementById('accusationButton');
const accusationMenu = document.getElementById('accusationMenu');

accusationButton.addEventListener('click', function() {
    accusationMenu.classList.toggle('hidden');
});

submitAccusationButton.addEventListener('click', function() {
    accusationMessage();
    accusationMenu.classList.toggle('hidden');
});

function suggestionMessage() {
    var player = document.getElementById('suggestSuspect').value;
    var weapon = document.getElementById('suggestWeapon').value;
    socket.emit('make_suggestion', { username: currentUsername, suspect: player, weapon: weapon });
}

function accusationMessage() {
    var player = document.getElementById('accuseSuspect').value;
    var place = document.getElementById('accuseLocation').value;
    var weapon = document.getElementById('accuseWeapon').value;
    socket.emit('make_accusation', { username: currentUsername, suspect: player, location: place, weapon: weapon });
}

function endTurnMessage() {
    socket.emit('end_turn', { username: currentUsername});
}

// Sample list data
const listCards = ['Card 1', 'Card 2', 'Card 3'];

// Get the container element
const listCardsContainer = document.getElementById('listCardsContainer');

// Generate the list and populate it in the container
listCards.forEach(card => {
  const li = document.createElement('li');
  li.textContent = card;

  // Add click event listener to each list item
  li.addEventListener('click', () => {
    // Handle the click event
    // console.log(`Clicked: ${card}`);
    var message = 'Clicked on ' + card;
    socket.emit('send_message', { username: currentUsername, message: message });
  });

  listCardsContainer.appendChild(li);
});