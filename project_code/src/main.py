import json
import random
from typing import List
from enum import Enum
import os

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

class CharacterClass(Enum):
    MAGE = "Mage"
    WARRIOR = "Warrior"
    ROGUE = "Rogue"
    TIME_KEEPER = "Time Keeper"

class Character:
    def __init__(self, name: str, character_class: CharacterClass):
        self.name = name
        self.character_class = character_class
        self.strength = Statistic("Strength", description="Physical power")
        self.intelligence = Statistic("Intelligence", description="Cognitive ability")
        self.dexterity = Statistic("Dexterity", description="Agility and skill")
        self.vitality = Statistic("Vitality", description="Resilience and health")
        self.time_energy = Statistic("Time Energy", description="Ability to manipulate time", min_value=0, max_value=50)
        self.health = 100
        self.set_class_attributes()

    def set_class_attributes(self):
        if self.character_class == CharacterClass.MAGE:
            self.intelligence.modify(20)
            self.time_energy.modify(10)
        elif self.character_class == CharacterClass.WARRIOR:
            self.strength.modify(25)
            self.vitality.modify(15)
        elif self.character_class == CharacterClass.ROGUE:
            self.dexterity.modify(20)
            self.strength.modify(10)
        elif self.character_class == CharacterClass.TIME_KEEPER:
            self.intelligence.modify(15)
            self.time_energy.modify(25)

    def get_stats(self):
        """Return a list of character statistics."""
        return [self.strength, self.intelligence, self.dexterity, self.vitality, self.time_energy]

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            print(f"{self.name} has fallen!")

class Event:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        action = parser.select_action()
        if action == "Run":
            print("You decided to run. Event avoided!")
            self.status = EventStatus.UNKNOWN
        elif action == "Fight":
            character = parser.select_party_member(party)
            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)
        elif action == "Flee":
            self.handle_flee(party, parser)
        elif action == "Negotiate":
            self.handle_negotiate(party, parser)

    def handle_flee(self, party, parser):
        print("You attempted to flee!")
        if random.random() > 0.5:
            print("You successfully escaped!")
            self.status = EventStatus.UNKNOWN
        else:
            print("You failed to escape and must face the challenge.")
            character = parser.select_party_member(party)
            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)

    def handle_negotiate(self, party, parser):
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
            character.take_damage(10)

class Boss(Event):
    def __init__(self, data: dict):
        super().__init__(data)
        self.reward = data['reward']

class Location:
    def __init__(self, boss_event: Boss):
        self.boss_event = boss_event
        self.boss_defeated = False
        self.name = boss_event.name

    def defeat_boss(self):
        self.boss_defeated = True

class UserInputParser:
    def parse(self, prompt: str) -> str:
        """Prompt the user for input."""
        return input(prompt)

    def select_option(self, options: List[str], prompt: str) -> int:
        """Generic method to select an option from a list with validation."""
        while True:
            for idx, option in enumerate(options):
                print(f"{idx + 1}. {option}")
            try:
                choice = int(self.parse(prompt)) - 1
                if 0 <= choice < len(options):
                    return choice
                print("Invalid choice. Please select a valid option number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def select_party_member(self, party: List[Character]) -> Character:
        """Select a party member with validation."""
        alive_party = [member for member in party if member.is_alive()]
        options = [member.name for member in alive_party]
        choice_index = self.select_option(options, "Enter the number of the chosen party member: ")
        return alive_party[choice_index]

    def select_stat(self, character: Character) -> Statistic:
        """Select a stat for a character with validation."""
        stats = character.get_stats()
        options = [f"{stat.name} ({stat.value})" for stat in stats]
        choice_index = self.select_option(options, f"Choose a stat for {character.name}: ")
        return stats[choice_index]

    def select_action(self) -> str:
        """Select an action with validation."""
        actions = ["Run", "Fight", "Flee", "Negotiate"]
        choice_index = self.select_option(actions, "Enter the number of your action: ")
        return actions[choice_index]

class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.time_machine_pieces = []
        self.continue_playing = True

    def start(self):
        while self.continue_playing and self.party:
            self.party = [character for character in self.party if character.is_alive()]
            location = random.choice(self.locations)
            event = location.boss_event

            if event.execute(self.party, self.parser):
                location.defeat_boss()
                self.time_machine_pieces.append(event.reward)

            if not self.party:
                print("All characters have fallen. Game Over.")
                self.continue_playing = False

def load_boss_from_json(file_name: str) -> Boss | None:
    """Load boss data from a JSON file."""
    try:
        # Adjust the base directory to point to 'project_code/location_events'
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'location_events')
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'r') as file:
            return Boss(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading boss file '{file_name}': {e}")
        return None

def start_game():
    parser = UserInputParser()
    characters = [Character(f"{cls.value}", cls) for cls in CharacterClass]

    # Load bosses from JSON files, filtering out any that failed to load
    boss_files = ['future.json', 'ancient.json', 'medieval.json', 'boss.json']
    bosses = [load_boss_from_json(file) for file in boss_files]
    bosses = [boss for boss in bosses if boss is not None]

    locations = [Location(boss) for boss in bosses]
    Game(parser, characters, locations).start()

if __name__ == '__main__':
    start_game()
