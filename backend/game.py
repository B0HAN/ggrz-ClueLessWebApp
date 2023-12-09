import random
from player import Player
from deck_control import Deck, Card
from gameboard import Gameboard, Space
class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.gameboard = Gameboard()
        self.deck = Deck()
        self.deck.prepare_for_game()  # Shuffle, draw solution, and hide solution cards
        self.solution = self.deck.get_solution_cards()
        self.game_over = False
        self.character_birthplaces = {
            "Miss Scarlet": "Hallway Hall-Lounge",
            "Colonel Mustard": "Hallway Lounge-Dining Room",
            "Mrs. White": "Hallway Ballroom-Kitchen",
            "Mr. Green": "Hallway Conservatory-Ballroom",
            "Mrs. Peacock": "Hallway Library-Conservatory",
            "Professor Plum": "Hallway Study-Library"
        }
        self.assign_random_characters()
        self.distribute_cards()
        self.place_players_at_birthplaces()

    def assign_random_characters(self):
        characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
        random.shuffle(characters)  # Shuffle the list of characters

        # If there are fewer players than characters, this will only assign as many characters as there are players
        for player, character in zip(self.players, characters):
            player.character = character

    def place_players_at_birthplaces(self):
        """Place each player on their character's starting space."""
        for player in self.players:
            birthplace_name = self.character_birthplaces[player.character]
            birthplace_space = self.gameboard.spaces[birthplace_name]
            player.current_space = birthplace_space
            birthplace_space.add_player(player)

    def removePlayerFromSpace(self, playerObject: Player, spaceObject: Space):
        if spaceObject.space_type == "Hallway":
            spaceObject.current_players = []
            print("Player removed from " + spaceObject.name)
        else:
            #bug player not being removed from rooms properly
            spaceObject.remove_player(playerObject)
            print(playerObject.name + "removed from " + spaceObject.name)    
    
    def next_turn(self):
        # Increment the player index
        self.current_player_index += 1
        # Modulo by the number of players to cycle back to the first player
        self.current_player_index %= len(self.players)

    def current_player(self):
        # Return the current player
        return self.players[self.current_player_index]
    
    def get_player_at(self, index):
        return self.players[index]

    def distribute_cards(self):
        """Distribute cards to players."""
        self.deck.shuffle()
        player_index = 0
        while len(self.deck.cards) > 0:
            card = self.deck.draw_card()
            self.players[player_index].receive_card(card)
            player_index = (player_index + 1) % len(self.players)
    
    def find_player_by_character(self, character_name):
        """Find the player object based on the character name."""
        for player in self.players:
            if player.character == character_name:
                return player
        return None
        # If no player has the character, which shouldn't happen
    def removePlayerfromRotation(self, player_name):
        list_players = self.players
        print(" TOTAL PLAYERS:" + str(len(list_players)))
        for i in range(len(list_players)):
            curr_player = list_players[i]
            if curr_player.name == player_name:
                self.players.remove(curr_player)
                player_count = len(self.players)
                print(curr_player.name + "was removed. New number of player is: " + str(player_count))
                break

    def player_makes_suggestion(self, player: Player, suggested_character):
        result = ""
        """Handle a player's suggestion, ensuring the player is in a room."""
        # Check if the player is in a room
        if player.current_space.space_type != "Room":
            result = "You can only make a suggestion when you are in a room."
            return result
        # Set the suggested room to the player's current location
        suggested_room = player.current_space.name
        if "Hallway" in suggested_room:
            result = "You can only make a suggestion when you are in a room."
            return result

        # Find the player object for the suggested character
        # bug: NPC's are not being listed if less than 6 players
        suggested_character_player = self.find_player_by_character(suggested_character)
        # Move the suggested character player to the current player's room
        if suggested_character_player is not None:
            old_space = suggested_character_player.current_space
            suggested_character_player.move(player.current_space)
            self.removePlayerFromSpace(suggested_character_player, old_space)
        result = suggested_character + " has been moved to " + suggested_room
        return result

    def find_refute(self, player: Player, next_player,suggested_character, suggested_weapon, suggested_room):
        suggestion = [suggested_character, suggested_weapon, suggested_room]
        valid_cards = []
        if(player.name != next_player):
            for next_player_obj in self.players:
                if next_player_obj.name == next_player:
                    valid_cards = next_player_obj.get_valid_card(suggestion)
            print(" VALID CARDS FOR " + next_player + " are: ")
            print(valid_cards)
            if(len(valid_cards) > 0):
                return True
        return False


    def player_makes_accusation(self, player: Player, character, weapon, room):
        """Handle a player's accusation."""
        correct = True
        accusation = [room, character, weapon]
        for i in range(3):
            if accusation[i] != self.solution[i]:
                correct = False
        if correct:
            self.game_over = True
            result =  player.name + " has won the game!"
        else:
             result = player.name + " has made an incorrect accusation and faces the consequences."
             self.removePlayerfromRotation(player.name)

        return result
    
    def move_player(self, player: Player, new_space_name):
        return_message = ""
        """Handle a player's request to move to a new space."""
        # Assuming you have a dictionary of spaces and a player object with a current_space attribute.
        if new_space_name in self.gameboard.spaces:
            new_space = self.gameboard.spaces[new_space_name]
            if (new_space_name == player.current_space.name):
                return_message = "You are already in " + new_space_name
                return return_message
            # validates if destination is a neighbor for the current space
            isValidNeighbor = self.gameboard.isNeighbor(player.current_space.name,new_space_name)
            if new_space.can_accommodate():
                if isValidNeighbor:
                    # Move player to the new space and add them to the space's list of players.
                    self.removePlayerFromSpace(player, player.current_space)
                    player.move(new_space)
                    new_space.add_player(player)
                    return_message = player.name + " has moved to " + new_space.name + "."
                else:
                    return_message = new_space.name + " is not a valid move from " + player.current_space.name + ". Please choose a valid location to move to."                  
            else:
                return_message = new_space.name + " cannot accommodate more players."
        else:
            print("Invalid space name.")
        return return_message

    def get_game_status(self):
        """Retrieve the status of the game, including player details."""
        game_status = []
        for player in self.players:
            player_status = {
                'name': player.name,
                'character': player.character,
                'current_position': player.current_space.name if player.current_space else 'Not yet placed'
            }
            game_status.append(player_status)
        return game_status

    def is_over(self):
        # Check if the game has ended
        return self.game_over