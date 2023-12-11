// WebSocket Initialization
var socket = io.connect('http://' + document.domain + ':' + location.port);
var currentUsername = "";
var newGame = false;
var spaces = {
    "Study": [0,0],
    "Kitchen": [4,4],
    "Hall": [0,2],
    "Lounge": [0,4],
    "Library": [2,0],
    "Billiard Room": [2,2],
    "Dining Room": [2,4],
    "Conservatory": [4,0],
    "Ballroom": [4,2],
    "Hallway Study-Hall": [0,1],
    "Hallway Study-Library": [1,0],
    "Hallway Hall-Lounge": [0,3],
    "Hallway Hall-Billiard Room": [1,2],
    "Hallway Lounge-Dining Room": [1,4],
    "Hallway Library-Billiard Room": [2,1],
    "Hallway Billiard Room-Dining Room": [2,3],
    "Hallway Library-Conservatory": [3,0],
    "Hallway Billiard Room-Ballroom": [3,2],
    "Hallway Dining Room-Kitchen": [3,4],
    "Hallway Conservatory-Ballroom":[4,1],
    "Hallway Ballroom-Kitchen": [4,3],
};
var char_pos = {
    "Miss Scarlet": [0,3],
    "Colonel Mustard": [1,4],
    "Mrs. White": [4,3],
    "Mr. Green": [4,1],
    "Mrs. Peacock": [3,0],
    "Professor Plum": [1,0]
};

var char_name = {
    "Miss Scarlet": "scarlet",
    "Colonel Mustard": "mustard",
    "Mrs. White": "white",
    "Mr. Green": "green",
    "Mrs. Peacock": "peacock",
    "Professor Plum": "plum"
};

var char_color = {
    "Miss Scarlet": "Red",
    "Colonel Mustard": "Yellow",
    "Mrs. White": "White",
    "Mr. Green": "Green",
    "Mrs. Peacock": "Blue",
    "Professor Plum": "Purple"
};

//starting positions for all characters
let scarlet_pos = [0,3];
let peacock_pos = [3,0];
let green_pos = [4,1];
let mustard_pos = [1,4];
let plum_pos = [1,0];
let white_pos = [4,3];


socket.on('broadcast_message', function(data) {
    document.getElementById('messagesBox').innerHTML += '<br>' + data;
});

socket.on('notify_player', function(data){
    var username = data[0];
    var message = data[1];
    if(username == currentUsername){
        alert(message);
    }
});

socket.on('notify_all', function(message){
    alert(message);
});


socket.on('turn_data', function(data){
    const currentPlayersTurnElement = document.getElementById("currentPlayersTurn");
    currentPlayersTurnElement.textContent = "Current Players Turn: " + data;
});

socket.on('private_to_user', function(data) {
    let username = data[0];
    let message = data[1];
    if (currentUsername === username) {
        document.getElementById('messagesBox').innerHTML += '<br>' + message;
    }
});



socket.on('return_to_lobby', function(){
    console.log("Returning to Lobby");
    newGame = true;
    
    const playerListDiv = document.getElementById('playersList');
    
    // Check if the 'playersList' element exists
    if (playerListDiv) {
        // Remove all <li> elements
        const liElements = playerListDiv.querySelectorAll('li');
        liElements.forEach(function(liElement) {
            liElement.parentNode.removeChild(liElement);
            console.log("removed a child");
        });

        // Render the lobby with an empty array
        renderLobby([]);
    } else {
        console.error("Element with ID 'playersList' not found.");
    }
});

socket.on('update_locations', function(data) {
    var n = data[0]
    var character_name = char_name[n];
    var location_coordinate = spaces[data[1]];
    var position = characterData[character_name];
    removeDot(character_name);
    position.room = location_coordinate;
    moveCharacterDot(character_name, location_coordinate);
});

function removeDot(name) {
    const characterPosition = characterData[name];
    const [cRow, cCol] = characterPosition.room;
    // Get the parent element
    const cell = document.querySelector(`.cell[data-coordinates="${cRow},${cCol}"]`);
    const dotElement = cell.querySelector(`.${name}`);
    dotElement.parentNode.removeChild(dotElement);       
};

function moveCharacterDot(name, location) {

        const characterPosition = characterData[name];
        const [cRow, cCol] = location;
        // Find the cell with matching coordinates
        const cell = document.querySelector(`.cell[data-coordinates="${cRow},${cCol}"]`);
        // Create a character dot element
        const characterDot = document.createElement('div');
        characterDot.classList.add('character-dot', name);
        characterDot.style.backgroundColor = characterPosition.color;
        
        // Append the character dot to the cell
        cell.appendChild(characterDot);
};


// Socket event listener for player list updates
socket.on('players_update', function(updatedPlayers) {
    console.log("Received players_update event", updatedPlayers);
    renderLobby(updatedPlayers);
});

socket.on('game_started', function() {
    document.getElementById('lobbySection').style.display = 'none';
    document.getElementById('gameSection').style.display = 'block';
    fetchPlayersInGame();
    updateList(currentUsername);
});

// Message Sending Function
function sendMessage() {
    var message = document.getElementById('messageInput').value;
    if (message.trim() !== '') {
        socket.emit('send_message', { username: currentUsername, message: message });
        document.getElementById('messageInput').value = ''; // Clear input after sending
    }
};

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
};

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
};
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
};



function fetchPlayersInLobby() {
    fetch('/get_players')
    .then(response => response.json())
    .then(data => {
        renderLobby(data.players);
    })
    .catch((error) => {
        console.error('Error fetching players in lobby:', error);
    });
};



function renderLobby(playersData) {
    const playerListDiv = document.getElementById('playersList');
    playerListDiv.innerHTML = ""; // Clearing previous content
    if (playersData.length == 0) {
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
};



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
    const currentPlayersTurnElement = document.getElementById("currentPlayersTurn");
    currentPlayersTurnElement.textContent = "Current Players Turn: " + currentUsername;
    if (playersData.length === 0) {
        playerListGameDiv.innerHTML = "Lobby is currently empty!";
    } else {
        playersData.forEach(player => {
            var player_data = "";
            const listItem = document.createElement('div');
            player_data = player[0] + " --> " + player[1] + " [" + player[2] + "]"
            listItem.classList.add('player');
            listItem.innerHTML = player_data;
            playerListGameDiv.appendChild(listItem);
        });
    }
}


var characterData = {
    scarlet: { room: char_pos["Miss Scarlet"], color: 'red' },
    peacock: { room: char_pos["Mrs. Peacock"], color: 'blue' },
    green: { room: char_pos["Mr. Green"], color: 'green' },
    mustard: { room: char_pos["Colonel Mustard"], color: 'yellow' },
    plum: { room: char_pos["Professor Plum"], color: 'purple' },
    white: { room: char_pos["Mrs. White"], color: 'white' }
};

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
 var listCards = [];

function updateList(currUser) {
    fetch('/update_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: currUser
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data.data);
        
            // Update the frontend list display
            listCards = data.data;

            // Clear the existing list items
            const listCardsContainer = document.getElementById('listCardsContainer');
            listCardsContainer.innerHTML = '';

            // Generate the list and populate it in the container
            listCards.forEach(card => {
                const li = document.createElement('li');
                li.textContent = card;
  
                // Add click event listener to each list item
                li.addEventListener('click', () => {
                    socket.emit('pick_card', { username: currentUsername, cardChosen: card });
                });
  
                listCardsContainer.appendChild(li);
            });
    })
    .catch(error => console.error('Error:', error));
};


// Notes section
// Get the lists of suspects, weapons, and rooms
const suspectsList = document.getElementById('suspects-list');
const weaponsList = document.getElementById('weapons-list');
const roomsList = document.getElementById('rooms-list');

// Add event listeners to the checkboxes
suspectsList.addEventListener('change', handleCheckboxChange);
weaponsList.addEventListener('change', handleCheckboxChange);
roomsList.addEventListener('change', handleCheckboxChange);

// Function to handle checkbox change
function handleCheckboxChange(event) {
    const checkbox = event.target;
    const isChecked = checkbox.checked;
    const label = checkbox.nextElementSibling;

    if (isChecked) {
        label.style.textDecoration = 'line-through';
    } else {
        label.style.textDecoration = 'none';
    }
};

const toggleNotes = document.getElementById('toggleNotes');
const notesSection = document.getElementById('notes');

toggleNotes.addEventListener('click', function() {
    notesSection.classList.toggle('hidden');
});