class Space:
    def __init__(self, name, space_type):
        self.name = name
        self.space_type = space_type
        self.neighbors = []
        self.current_players = []

    def addNeighbor(self, neighbor_space):
        self.neighbors.append(neighbor_space)

    def add_player(self, player):
        """add player to a space"""
        self.current_players.append(player)

    def remove_player(self, player):
        self.current_players.remove(player)

    def can_accommodate(self):
        # If it's a room, it can always accommodate more players.
        if self.space_type == "Room":
            return True
        # If it's a hallway, it can only accommodate one player at a time.
        elif self.space_type == "Hallway":
            return len(self.current_players) == 0

    def __str__(self):
        return self.name


class Gameboard:
    def __init__(self):
        # Initialize all spaces
        self.spaces = {
            "Study": Space("Study", "Room"),
            "Kitchen": Space("Kitchen", "Room"),
            "Hall": Space("Hall", "Room"),
            "Lounge": Space("Lounge", "Room"),
            "Library": Space("Library", "Room"),
            "Billiard Room": Space("Billiard Room", "Room"),
            "Dining Room": Space("Dining Room", "Room"),
            "Conservatory": Space("Conservatory", "Room"),
            "Ballroom": Space("Ballroom", "Room"),
            "Hallway Study-Hall": Space("Hallway Study-Hall", "Hallway"),
            "Hallway Study-Library": Space("Hallway Study-Library", "Hallway"),
            "Hallway Hall-Lounge": Space("Hallway Hall-Lounge", "Hallway"),
            "Hallway Hall-Billiard Room": Space("Hallway Hall-Billiard Room", "Hallway"),
            "Hallway Lounge-Dining Room": Space("Hallway Lounge-Dining Room", "Hallway"),
            "Hallway Library-Billiard Room": Space("Hallway Library-Billiard Room", "Hallway"),
            "Hallway Billiard Room-Dining Room": Space("Hallway Billiard Room-Dining Room", "Hallway"),
            "Hallway Library-Conservatory": Space("Hallway Library-Conservatory", "Hallway"),
            "Hallway Billiard Room-Ballroom": Space("Hallway Billiard Room-Ballroom", "Hallway"),
            "Hallway Dining Room-Kitchen": Space("Hallway Dining Room-Kitchen", "Hallway"),
            "Hallway Conservatory-Ballroom": Space("Hallway Conservatory-Ballroom", "Hallway"),
            "Hallway Ballroom-Kitchen": Space("Hallway Ballroom-Kitchen", "Hallway"),
        }
        
        # Assign neighbors to each space
        self._define_neighbors()

    def _define_neighbors(self):
        # Define neighbors for each space
        self.spaces["Study"].addNeighbor(self.spaces["Hallway Study-Hall"])
        self.spaces["Study"].addNeighbor(self.spaces["Hallway Study-Library"])
        self.spaces["Study"].addNeighbor(self.spaces["Kitchen"])  # Assuming there's a secret passage

        self.spaces["Hall"].addNeighbor(self.spaces["Hallway Study-Hall"])
        self.spaces["Hall"].addNeighbor(self.spaces["Hallway Hall-Lounge"])
        self.spaces["Hall"].addNeighbor(self.spaces["Hallway Hall-Billiard Room"])

        self.spaces["Lounge"].addNeighbor(self.spaces["Hallway Hall-Lounge"])
        self.spaces["Lounge"].addNeighbor(self.spaces["Hallway Lounge-Dining Room"])
        self.spaces["Lounge"].addNeighbor(self.spaces["Conservatory"])  # Assuming there's a secret passage

                # Continue defining neighbors
        self.spaces["Library"].addNeighbor(self.spaces["Hallway Study-Library"])
        self.spaces["Library"].addNeighbor(self.spaces["Hallway Library-Billiard Room"])
        self.spaces["Library"].addNeighbor(self.spaces["Hallway Library-Conservatory"])

        self.spaces["Billiard Room"].addNeighbor(self.spaces["Hallway Library-Billiard Room"])
        self.spaces["Billiard Room"].addNeighbor(self.spaces["Hallway Hall-Billiard Room"])
        self.spaces["Billiard Room"].addNeighbor(self.spaces["Hallway Billiard Room-Dining Room"])
        self.spaces["Billiard Room"].addNeighbor(self.spaces["Hallway Billiard Room-Ballroom"])

        self.spaces["Dining Room"].addNeighbor(self.spaces["Hallway Lounge-Dining Room"])
        self.spaces["Dining Room"].addNeighbor(self.spaces["Hallway Billiard Room-Dining Room"])
        self.spaces["Dining Room"].addNeighbor(self.spaces["Hallway Dining Room-Kitchen"])

        self.spaces["Conservatory"].addNeighbor(self.spaces["Hallway Library-Conservatory"])
        self.spaces["Conservatory"].addNeighbor(self.spaces["Hallway Conservatory-Ballroom"])
        self.spaces["Conservatory"].addNeighbor(self.spaces["Lounge"])  # Secret passage

        self.spaces["Ballroom"].addNeighbor(self.spaces["Hallway Conservatory-Ballroom"])
        self.spaces["Ballroom"].addNeighbor(self.spaces["Hallway Billiard Room-Ballroom"])
        self.spaces["Ballroom"].addNeighbor(self.spaces["Hallway Ballroom-Kitchen"])

        self.spaces["Kitchen"].addNeighbor(self.spaces["Hallway Ballroom-Kitchen"])
        self.spaces["Kitchen"].addNeighbor(self.spaces["Hallway Dining Room-Kitchen"])
        self.spaces["Kitchen"].addNeighbor(self.spaces["Study"])  # Secret passage

        # Define the neighbor relationships for hallways
        self.spaces["Hallway Study-Hall"].addNeighbor(self.spaces["Study"])
        self.spaces["Hallway Study-Hall"].addNeighbor(self.spaces["Hall"])

        self.spaces["Hallway Study-Library"].addNeighbor(self.spaces["Study"])
        self.spaces["Hallway Study-Library"].addNeighbor(self.spaces["Library"])

        self.spaces["Hallway Hall-Lounge"].addNeighbor(self.spaces["Hall"])
        self.spaces["Hallway Hall-Lounge"].addNeighbor(self.spaces["Lounge"])

        self.spaces["Hallway Ballroom-Kitchen"].addNeighbor(self.spaces["Ballroom"])
        self.spaces["Hallway Ballroom-Kitchen"].addNeighbor(self.spaces["Kitchen"])

        self.spaces["Hallway Library-Billiard Room"].addNeighbor(self.spaces["Library"])
        self.spaces["Hallway Library-Billiard Room"].addNeighbor(self.spaces["Billiard Room"])

        self.spaces["Hallway Hall-Billiard Room"].addNeighbor(self.spaces["Hall"])
        self.spaces["Hallway Hall-Billiard Room"].addNeighbor(self.spaces["Billiard Room"])

        self.spaces["Hallway Lounge-Dining Room"].addNeighbor(self.spaces["Lounge"])
        self.spaces["Hallway Lounge-Dining Room"].addNeighbor(self.spaces["Dining Room"])

        self.spaces["Hallway Billiard Room-Dining Room"].addNeighbor(self.spaces["Billiard Room"])
        self.spaces["Hallway Billiard Room-Dining Room"].addNeighbor(self.spaces["Dining Room"])

        self.spaces["Hallway Library-Conservatory"].addNeighbor(self.spaces["Library"])
        self.spaces["Hallway Library-Conservatory"].addNeighbor(self.spaces["Conservatory"])

        self.spaces["Hallway Billiard Room-Ballroom"].addNeighbor(self.spaces["Billiard Room"])
        self.spaces["Hallway Billiard Room-Ballroom"].addNeighbor(self.spaces["Ballroom"])

        self.spaces["Hallway Dining Room-Kitchen"].addNeighbor(self.spaces["Dining Room"])
        self.spaces["Hallway Dining Room-Kitchen"].addNeighbor(self.spaces["Kitchen"])

        self.spaces["Hallway Conservatory-Ballroom"].addNeighbor(self.spaces["Conservatory"])
        self.spaces["Hallway Conservatory-Ballroom"].addNeighbor(self.spaces["Ballroom"])



    def displayGraph(self):
        # Display the graph for testing purposes
        for space_name, space in self.spaces.items():
            neighbors_names = [neighbor.name for neighbor in space.neighbors]
            print(f"{space_name} -> {neighbors_names}")





