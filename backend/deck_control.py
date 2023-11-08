import random

class Card:
    def __init__(self, name, card_type):
        self.name = name
        self.card_type = card_type  # This can be "Room", "Character", or "Weapon"
    
    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} ({self.card_type})"

class Deck:
    def __init__(self):
        # Initiate the deck with all the cards
        self.cards = self._construct_deck()
        self.solution_cards = []

    def _construct_deck(self):
        """Initialize the deck with all required cards."""
        # List all room names, character names, and weapon names
        rooms = ["Study", "Hall", "Lounge", "Library", "Billiard Room", "Dining Room", "Conservatory", "Ballroom", "Kitchen"]
        characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
        weapons = ["Rope", "Lead Pipe", "Knife", "Wrench", "Candlestick", "Revolver"]

        # Create the card objects
        room_cards = [Card(room, "Room") for room in rooms]
        character_cards = [Card(character, "Character") for character in characters]
        weapon_cards = [Card(weapon, "Weapon") for weapon in weapons]

        # Return the combined list of all cards
        return room_cards + character_cards + weapon_cards
    
    def prepare_for_game(self):
        """call this function to prepare the deck for the game, it will shuffle and hide 3 solution cards."""
        self.shuffle()
        self.set_solution_cards()
        self.hide_solution_cards()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def set_solution_cards(self): 
        """Randomly select a room, character, and weapon card as the solution."""
        room_card = random.choice([card for card in self.cards if card.card_type == "Room"])
        character_card = random.choice([card for card in self.cards if card.card_type == "Character"])
        weapon_card = random.choice([card for card in self.cards if card.card_type == "Weapon"])
        self.solution_cards = [room_card, character_card, weapon_card]

    def hide_solution_cards(self):
        """Remove the solution cards from the main deck"""
        for card in self.solution_cards:
            self.cards.remove(card)

    def get_solution_cards(self):
        """Get the solution cards for display or other purposes."""
        return self.solution_cards

    def add_card(self, card):
        self.cards.append(card)


    def draw_card(self):
        return self.cards.pop()

    
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)