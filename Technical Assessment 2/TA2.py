import agentpy as ap


# Ask the user for the starting condition of a room.
# The function keeps asking until the user enters "dirty" or "clean".
def get_initial_state(room_name):
    while True:
        state = input(f"Is room {room_name} Dirty or Clean? ").strip().lower()

        if state == "dirty":
            return "Dirty"
        elif state == "clean":
            return "Clean"
        else:
            print("Please enter only Dirty or Clean.")


# Check if the selected room is dirty.
def is_room_dirty(rooms, room):
    return rooms[room] == "Dirty"


# Change the selected room's state to clean.
def clean_room(rooms, room):
    rooms[room] = "Clean"


# This class represents the vacuum cleaner agent.
class VacuumAgent(ap.Agent):

    # Set the agent's starting location to room A.
    def setup(self, **kwargs):
        self.location = "A"

    # Decide what the agent does during each step.
    def act(self, step_number):
        rooms = self.model.rooms

        print(f"Step {step_number}: Agent is in room {self.location}")

        # If the current room is dirty, clean it.
        if is_room_dirty(rooms, self.location):
            clean_room(rooms, self.location)
            print(f"Room {self.location} has been cleaned.")

        # If the current room is already clean, move to the other room.
        else:
            if self.location == "A":
                self.location = "B"
                print("Moving to room B")
            else:
                if self.location == "B":
                    self.location = "C"
                    print("Moving to room C")
                else:
                    self.location = "A"
                    print("Moving to room A")

        # Display the current condition of both rooms.
        print(f"Environment state: {rooms}\n")


# This class represents the whole simulation model.
class VacuumModel(ap.Model):

    # Create the room dictionary and create one vacuum agent.
    def setup(self, **kwargs):
        self.rooms = {
            "A": self.p.room_a,
            "B": self.p.room_b,
            "C": self.p.room_c
        }

        self.agent = ap.AgentList(self, 1, VacuumAgent)
        self.step_count = 0

    # Run one action for every model step.
    def step(self):
        self.step_count += 1
        self.agent[0].act(self.step_count)


# Get the initial state of each room from the user.
room_a = get_initial_state("A")
room_b = get_initial_state("B")
room_c = get_initial_state("C")

# Ask how many steps the simulation should run.
steps = int(input("\nHow many steps should the agent run? "))

# Store user input as model parameters.
parameters = {
    "room_a": room_a,
    "room_b": room_b,
    "room_c": room_c
}

# Create and run the model.
model = VacuumModel(parameters)
model.run(steps=steps, display=False)