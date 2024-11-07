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
    def __init__(self, name: str = "Bob",  character_class: CharacterClass = CharacterClass.WARRIOR):
        self.name = name
        self.character_class = character_class
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        self.dexterity = Statistic("Dexterity", description="Skill in using technology and ancient tools.")
        self.vitality = Statistic("Vitality", description="Health and resilience to survive through ages.")
        self.time_energy = Statistic("Time Energy", description="Ability to manipulate time.", min_value=0, max_value=50)
        self.health = 100
        self.inventory = []

        # Set class-specific attributes
        self.set_class_attributes()

    def __str__(self):
        return (f"Character: {self.name}, Class: {self.character_class}, "
                f"Strength: {self.strength}, Intelligence: {self.intelligence}, "
                f"Dexterity: {self.dexterity}, Vitality: {self.vitality}, "
                f"Time Energy: {self.time_energy}")

    def set_class_attributes(self):
        """Adjust character stats based on class selection."""
        if self.character_class == CharacterClass.MAGE:
            self.intelligence.modify(20)  # Mages are highly intelligent
            self.time_energy.modify(10)  # Ability to use more time energy
        elif self.character_class == CharacterClass.WARRIOR:
            self.strength.modify(25)  # Warriors have high strength
            self.vitality.modify(15)  # Warriors are more resilient
        elif self.character_class == CharacterClass.ROGUE:
            self.dexterity.modify(20)  # Rogues excel in stealth and agility
            self.strength.modify(10)   # Adequate strength for combat
        elif self.character_class == CharacterClass.TIME_KEEPER:
            self.intelligence.modify(15)
            self.time_energy.modify(25)  # Time Keepers focus on manipulating time

    def is_alive(self):
        return self.health > 0
    def get_stats(self):
        return [self.strength, self.intelligence, self.dexterity, self.vitality]  # Extend this list if there are more stats

    def modify_stat(self, stat_name: str, amount: int):
        """Modify a specific stat by name."""
        stats = {stat.name: stat for stat in self.get_stats()}
        if stat_name in stats:
            stats[stat_name].modify(amount)

    def take_damage(self, amount: int):
        """Apply damage to the character."""
        self.health -= amount
        if self.health <= 0:
            print(f"{self.name} has fallen!")
            
    def attack(self):
        """Character attack method - success determined by dice roll."""
        roll = random.randint(1, 20)  # Roll a 20-sided dice
        if roll > 10:  # Success if roll > 10
            damage = random.randint(5, 20)  # Random damage
            print(f"{self.name} successfully attacks for {damage} damage!")
            return damage
        else:
            print(f"{self.name}'s attack missed!")
            return 0
            
            

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
        # print("we got here")
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
            # Apply damage to the character if they fail
            character.take_damage(10)



class Boss(Event):
    def __init__(self, data: dict):
        super().__init__(data)
        self.reward = data['reward']

    def execute(self, party: List[Character], parser):
        print(f"Boss Encounter: {self.prompt_text}")

        while True:
            character = parser.select_party_member(party)

            if not character.is_alive():
                print(f"{character.name} has already fallen. Choose another member.")
                continue  # Prompt again if the selected character is fallen

            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)

            if self.status == EventStatus.PASS:
                print(f"You defeated the boss and obtained a time machine piece: {self.reward}!")
                return self.reward  # Return the reward if the boss is defeated

            elif self.status == EventStatus.FAIL:
                print(f"The beast is too strong. {character.name} has fallen.")

            # Break if all party members are defeated
            if all(not member.is_alive() for member in party):
                print("All party members have fallen. The boss remains undefeated.")
                return False


# Time portal mechanic: selecting events from different eras
class Location:
    def __init__(self, boss_event: Boss, era: str=""):
        self.era = era
        self.boss_event = boss_event
        self.boss_defeated = False
        self.name = boss_event.name

    def get_event(self) -> Event:
        return self.boss_event

    def defeat_boss(self):
        self.boss_defeated = True


# Define the FinalBoss class
class FinalBoss:
    def __init__(self, name="Dark Overlord", health=200, attack_power=25, defense=15):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack_power
        self.defense = defense
        self.special_abilities = {
            "Time Warp": {"damage": 35, "cooldown": 3},  # Causes additional damage, has cooldown
            "Heal": {"healing": 30, "cooldown": 5}       # Heals itself, has cooldown
        }
        self.ability_cooldowns = {key: 0 for key in self.special_abilities}  # Tracks ability cooldowns

    def take_damage(self, damage):
        # Calculate the damage taken after applying defense
        actual_damage = max(damage - self.defense, 0)
        self.health -= actual_damage
        print(f"{self.name} takes {actual_damage} damage! Remaining health: {self.health}")

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.time_machine_pieces = []
        self.defeated_locations = []

    def start(self):
        while self.continue_playing:
            # Filter out fallen characters before each encounter
            self.party = [character for character in self.party if character.is_alive()]

            if not self.party:  # Check if all characters have fallen
                print("All characters have fallen. Game Over.")
                break

            location = random.choice(self.locations)
            event: Event = location.get_event()

            # Get the index of the randomly chosen location
            location_index = self.locations.index(location)

            if event.execute(self.party, self.parser):
                # Pop the location by index if the event is defeated
                self.defeated_locations.append(self.locations.pop(location_index))

            if isinstance(event, Boss) and event.status == EventStatus.PASS:
                self.time_machine_pieces.append(event.reward)
                location.defeat_boss()

            if self.check_game_over():
                self.continue_playing = False

    def check_game_over(self):
        if len(self.party) == 0 :
            print("Game Over.")
        elif len(self.time_machine_pieces) == len(self.locations):
            final_boss = FinalBoss()
            boss_battle(self.party, final_boss)


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        alive_party = [member for member in party if member.is_alive()]

        while True:
            for idx, member in enumerate(alive_party):
                print(f"{idx + 1}. {member.name}")
            try:
                choice = int(self.parse("Enter the number of the chosen party member: "))
                if 0 < choice <= len(alive_party):  # Ensure choice is positive and within range
                    return alive_party[choice - 1]
                print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        while True:
            for idx, stat in enumerate(stats):
                print(f"{idx + 1}. {stat.name} ({stat.value})")
            try:
                choice = int(self.parse("Enter the number of the stat to use: "))
                if 0 < choice <= len(stats):  # Ensure choice is valid
                    return stats[choice - 1]
                print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def select_action(self) -> str:
        print("Choose an action:")
        actions = ["Run", "Fight", "Flee", "Negotiate"]
        while True:
            for idx, action in enumerate(actions):
                print(f"{idx + 1}. {action}")
            try:
                choice = int(self.parse("Enter the number of your action: "))
                if 0 < choice <= len(actions):  # Ensure choice is valid
                    return actions[choice - 1]
                print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def load_boss_from_json(file_name: str) -> Boss:
    file_path = os.path.join(os.path.dirname(__file__), '..', 'location_events', file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return Boss(data)


def boss_battle(party: List[Character], boss):
    print(f"{boss.name} Battle! ")

    while any(player.is_alive() for player in party) and boss.is_alive():
        # Filter the party to include only alive players
        alive_party = [player for player in party if player.is_alive()]

        # Loop over each alive player in the party
        for player in alive_party:
            if not boss.is_alive():
                break  # Exit if the boss is defeated

            # Player turn
            ability = player.abilities[0]  # Assume player uses the first ability for simplicity
            print(f"{player.name}'s turn!")
            player.use_ability(ability)
            boss.take_damage(player.attack)

            # Boss turn if still alive
            if boss.is_alive():
                boss_ability = boss.abilities[0]  # Boss also uses first ability for simplicity
                print(f"{boss.name}'s turn!")
                boss.use_ability(boss_ability)
                player.take_damage(boss.attack)

            # Check if the player was defeated during the boss's turn
            if not player.is_alive():
                print(f"{player.name} has fallen!")

    # Determine the outcome
    if any(player.is_alive() for player in party):
        print(f"The party has defeated {boss.name}!")
    else:
        print(f"{boss.name} has defeated the party... Game Over!")




def start_game():
    parser = UserInputParser()
    character_classes =  [member.value for member in CharacterClass]
    characters = [Character(f"{character_class}", CharacterClass(character_class)) for character_class in character_classes]

    # Load events for different eras & bosses
    boss_event_files = ['../location_events/future.json', '../location_events/ancient.json', '../location_events/medieval.json' ]
    bosses: List[Boss] = [load_boss_from_json(file) for file in boss_event_files]

    locations = [Location(boss) for boss in bosses]

    game = Game(parser, characters, locations)
    game.start()

if __name__ == '__main__':
    start_game()

