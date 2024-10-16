import json
import sys
import random
from typing import List, Optional
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.character_class = character_class
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        self.dexterity = Statistic("Dexterity", description="Skill in using technology and ancient tools.")
        self.vitality = Statistic("Vitality", description="Health and resilience to survive through ages.")
        self.time_energy = Statistic("Time Energy", description="Ability to manipulate time.", min_value=0, max_value=50)

            # Set class-specific attributes
        self.set_class_attributes()

    def __str__(self):
        return (f"Character: {self.name}, Class: {self.character_class}, "
                f"Strength: {self.strength}, Intelligence: {self.intelligence}, "
                f"Dexterity: {self.dexterity}, Vitality: {self.vitality}, "
                f"Time Energy: {self.time_energy}")

    def get_stats(self):
        return [self.strength, self.intelligence]  # Extend this list if there are more stats


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        action = parser.select_action()  # New method to select the player's action**
        if action == "Run":
            print("You decided to run. Event avoided!")
            self.status = EventStatus.UNKNOWN  # Neutral outcome**
        elif action == "Fight":
            character = parser.select_party_member(party)
            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)
        elif action == "Flee":
            print("You attempted to flee!")
            if random.random() > 0.5:
                print("You successfully escaped!")
                self.status = EventStatus.UNKNOWN
            else:
                print("You failed to escape and must face the challenge.")
                character = parser.select_party_member(party)
                chosen_stat = parser.select_stat(character)
                self.resolve_choice(character, chosen_stat)
        elif action == "Negotiate":
            print("You attempted to negotiate.")
            if random.random() > 0.5:
                print("Negotiation successful!")
                self.status = EventStatus.PASS
            else:
                print("Negotiation failed. Prepare to face the event.")
                character = parser.select_party_member(party)
                chosen_stat = parser.select_stat(character)
                self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)

# Time portal mechanic: selecting events from different eras
class Location:
    def __init__(self, events: List[Event]):
        self.events = events
        self.era = era

    def get_event(self) -> Event:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True

    def start(self):
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False
        print("Game Over.")

    def check_game_over(self):
        return len(self.party) == 0


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]

    def select_action(self) -> str:  # New method to choose an action**
        print("Choose an action:")
        actions = ["Run", "Fight", "Flee", "Negotiate"]
        for idx, action in enumerate(actions):
            print(f"{idx + 1}. {action}")
        choice = int(self.parse("Enter the number of your action: ")) - 1
        return actions[choice]

# Modify the event loader to include the era
def load_events_from_json(file_path: str, era: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()
    characters = [Character(f"Character_{i}") for i in range(3)]

# Load events for different eras
    future_events = load_events_from_json('location_events/future.json', "Futuristic City")
    ancient_events = load_events_from_json('location_events/ancient.json', "Ancient Civilization")
    medieval_events = load_events_from_json('location_events/medieval.json', "Medieval Fantasy")
   
    # Create locations based on time periods
    locations = [Location("Futuristic City", future_events), 
                 Location("Ancient Civilization", ancient_events),
                 Location("Medieval Fantasy", medieval_events)]
    
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()
