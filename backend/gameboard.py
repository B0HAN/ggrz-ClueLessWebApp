class Space:
    def __init__(self, name, space_type):
        self.name = name
        self.neighbors = []
        self.type = space_type # Either Room or Hallway
        self.occupants = []
        self.max_occupants = float('inf') if self.type == "Room" else 1
        

    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.addNeighbor(self)  # Ensure the relationship is bidirectional
    
    def can_accommodate(self):
        """Check if the space can accommodate another player."""
        return len(self.occupants) < self.max_occupants
    
    def add_player(self, player):
        """Add a player to the space if possible."""
        if self.can_accommodate():
            self.occupants.append(player)
        else:
            raise ValueError(f"{self.name} cannot accommodate more players.")
    
    def remove_player(self, player):
        """Remove a player from the space."""
        if player in self.occupants:
            self.occupants.remove(player)

    def __str__(self):
        return f"Space({self.name})"


class Gameboard:
    def __init__(self):
        # Initialize all spaces
        self.study = Space("Study", "Room")
        self.kitchen = Space("Kitchen", "Room")
        self.hall = Space("Hall", "Room")
        self.lounge = Space("Lounge", "Room")
        self.library = Space("Library", "Room")
        self.billiardRoom = Space("BilliardRoom", "Room")
        self.diningRoom = Space("DiningRoom", "Room")
        self.conservatory = Space("Conservatory", "Room")
        self.ballRoom = Space("BallRoom", "Room")
        self.hallway_study_hall = Space("Hallway_Study_Hall", "Hallway")
        self.hallway_study_library = Space("Hallway_Study_Library", "Hallway")
        self.hallway_hall_lounge = Space("Hallway_Hall_Lounge", "Hallway")
        self.hallway_hall_billiardRoom = Space("Hallway_Hall_BilliardRoom", "Hallway")
        self.hallway_lounge_diningRoom = Space("Hallway_Lounge_DiningRoom", "Hallway")
        self.hallway_library_billiardRoom = Space("Hallway_Library_BilliardRoom", "Hallway")
        self.hallway_billiardRoom_diningRoom = Space("Hallway_BilliardRoom_DiningRoom", "Hallway")
        self.hallway_library_conservatory = Space("Hallway_Library_Conservatory", "Hallway")
        self.hallway_billiardRoom_ballRoom = Space("Hallway_BilliardRoom_BallRoom", "Hallway")
        self.hallway_diningRoom_kitchen = Space("Hallway_DiningRoom_Kitchen", "Hallway")
        self.hallway_conservatory_ballRoom = Space("Hallway_Conservatory_BallRoom", "Hallway")
        self.hallway_ballRoom_kitchen = Space("Hallway_BallRoom_Kitchen", "Hallway")

        # Define neighbors based on the requirements
        self.study.addNeighbor(self.kitchen)
        self.study.addNeighbor(self.hallway_study_hall)
        self.study.addNeighbor(self.hallway_study_library)

        self.hallway_study_hall.addNeighbor(self.hall)

        self.hall.addNeighbor(self.hallway_study_hall)
        self.hall.addNeighbor(self.hallway_hall_lounge)
        self.hall.addNeighbor(self.hallway_hall_billiardRoom)

        self.hallway_hall_lounge.addNeighbor(self.lounge)

        self.lounge.addNeighbor(self.hallway_hall_lounge)
        self.lounge.addNeighbor(self.hallway_lounge_diningRoom)
        self.lounge.addNeighbor(self.conservatory)


        self.hallway_study_library.addNeighbor(self.library)

        self.hallway_hall_billiardRoom.addNeighbor(self.billiardRoom)

        self.hallway_lounge_diningRoom.addNeighbor(self.diningRoom)

        self.library.addNeighbor(self.hallway_study_library)
        self.library.addNeighbor(self.hallway_library_billiardRoom)
        self.library.addNeighbor(self.hallway_library_conservatory)

        self.hallway_library_billiardRoom.addNeighbor(self.billiardRoom)

        self.billiardRoom.addNeighbor(self.hallway_library_billiardRoom)
        self.billiardRoom.addNeighbor(self.hallway_hall_billiardRoom)
        self.billiardRoom.addNeighbor(self.hallway_billiardRoom_diningRoom)
        self.billiardRoom.addNeighbor(self.hallway_billiardRoom_ballRoom)

        self.hallway_billiardRoom_diningRoom.addNeighbor(self.diningRoom)

        self.diningRoom.addNeighbor(self.hallway_lounge_diningRoom)
        self.diningRoom.addNeighbor(self.hallway_billiardRoom_diningRoom)
        self.diningRoom.addNeighbor(self.hallway_diningRoom_kitchen)

        self.hallway_library_conservatory.addNeighbor(self.conservatory)

        self.hallway_billiardRoom_ballRoom.addNeighbor(self.ballRoom)

        self.hallway_diningRoom_kitchen.addNeighbor(self.kitchen)

        self.conservatory.addNeighbor(self.hallway_library_conservatory)
        self.conservatory.addNeighbor(self.hallway_conservatory_ballRoom)
        self.conservatory.addNeighbor(self.lounge)

        self.hallway_conservatory_ballRoom.addNeighbor(self.ballRoom)

        self.ballRoom.addNeighbor(self.hallway_conservatory_ballRoom)
        self.ballRoom.addNeighbor(self.hallway_billiardRoom_ballRoom)
        self.ballRoom.addNeighbor(self.hallway_ballRoom_kitchen)

        self.kitchen.addNeighbor(self.hallway_ballRoom_kitchen)
        self.kitchen.addNeighbor(self.hallway_diningRoom_kitchen)
        self.kitchen.addNeighbor(self.study)

    # for testing if the graph is correct
    def displayGraph(self):
        spaces = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for space_name in spaces:
            space = getattr(self, space_name)
            print(f"{space} -> {[str(neighbor) for neighbor in space.neighbors]}")

