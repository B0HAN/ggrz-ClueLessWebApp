
from deck_control import Card
from gameboard import Space
class Player:
    def __init__(self, name, character=None):
        self.name = name
        self.hand = []
        self.character = character
        self.current_space = Space("None", "None")
        self.can_move = True

    def receive_card(self, card: Card):
        """Add a card to the player's hand."""
        self.hand.append(card)

    def show_hand(self):
        """Display all cards in the player's hand."""
        return ', '.join(str(card) for card in self.hand)

    def make_accusation(self, character, weapon, room, solution):
        """Make an accusation to attempt to solve the game."""
        accusation = [character, weapon, room]
        return accusation == solution

    def make_suggestion(self, character, weapon, room):
        """Make a suggestion to gather information."""
        return character, weapon, room

    def show_card(self, suggestion):
        """Reveal a card from the hand to disprove a suggestion."""
        for card in self.hand:
            if card.name in suggestion:
                return card
        return None
    
    def move(self, destination_space: Space):
        """Move the player to a new space."""
        destination_space.add_player(self)
        self.current_space = destination_space
    
    def set_move(self, state):
        self.can_move = state

    def __str__(self):
        return self.name
