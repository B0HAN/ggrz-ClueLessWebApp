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
        self.solution = self.deck.solution_cards
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

    def next_turn(self):
        # Increment the player index
        self.current_player_index += 1
        # Modulo by the number of players to cycle back to the first player
        self.current_player_index %= len(self.players)

    def current_player(self):
        # Return the current player
        return self.players[self.current_player_index]


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
        return None  # If no player has the character, which shouldn't happen

    def player_makes_suggestion(self, player: Player, suggested_character, suggested_weapon):
        """Handle a player's suggestion, ensuring the player is in a room."""
        # Check if the player is in a room
        if player.current_space.space_type != "Room":
            print("You can only make a suggestion when you are in a room.")
            return None

        # Set the suggested room to the player's current location
        suggested_room = player.current_space.name

        # Find the player object for the suggested character
        suggested_character_player = self.find_player_by_character(suggested_character)

        # Move the suggested character player to the current player's room
        if suggested_character_player:
            suggested_character_player.move(player.current_space)
            print(f"{suggested_character} has been moved to {suggested_room}.")

        # Players attempt to refute the suggestion
        for other_player in self.players:
            if other_player != player:
                card_shown = other_player.show_card([suggested_character, suggested_weapon, suggested_room])
                if card_shown:
                    print(f"{other_player.character} has shown a card.")
                    return card_shown

        print("No one could refute the suggestion.")
        return None

    def player_makes_accusation(self, player: Player, character, weapon, room):
        """Handle a player's accusation."""
        correct = player.make_accusation(character, weapon, room, [card.name for card in self.solution])
        if correct:
            self.game_over = True
            print(f"{player} has won the game!")
        else:
            print(f"{player} has made an incorrect accusation and faces the consequences.")
        return correct
    
    def move_player(self, player: Player, new_space_name):
        """Handle a player's request to move to a new space."""
        # Assuming you have a dictionary of spaces and a player object with a current_space attribute.
        if new_space_name in self.gameboard.spaces:
            new_space = self.gameboard.spaces[new_space_name]
            if new_space.can_accommodate():
                # If the player is currently in a space, remove them from that space.
                if player.current_space:
                    player.current_space.remove_player(player)
                # Move player to the new space and add them to the space's list of players.
                player.move(new_space)
                new_space.add_player(player)
                print(f"{player.name} has moved to {new_space.name}.")
                return True
            else:
                print(f"{new_space.name} cannot accommodate more players.")
        else:
            print("Invalid space name.")
        return False

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