# COMP150 Fall 2024 Project One Template

This is a template for the first project in the COMP150 Fall 2024 course. The goal of this project is to create a simplified Dungeons & Dragons text-based game in Python.

## How to Run the Project

To run the example project, follow the steps below:

### Prerequisites
- Python 3.12.6 installed on your machine.

### Steps to Run

1. Clone or download the project to your local machine.

2. Navigate to the project root directory (assumed to be named `comp150fall2024projectonetemplate`):

   ```bash
   cd comp150fall2024projectonetemplate
   ```

3. Run the game using Python:

   ```bash
   python project_code/src/main.py
   ```

### Game Idea
- Sci-fi World with multiple portals that either connect to futuristic cities, ancient civilizations or medieval fantasy. 
- GOAL: Fix broken time stream & defeat the Temporal Warden blocking the final portal
- To complete goal, players must collect 15 points (one for each portal).

### Location
- There will be a multitude of portals from different eras such as futuristic cities, ancient civilizations or medieval fantasy. 

### Events
- NPC Interaction: Can gain items or increase stats
- Portal Monsters: One big monster to defeat in each portal that will give the players one point
- Random events: Found treasure, items and ambushes
- Temporal Warden: Final Boss 

### Game Flow
- Game Statistics: Each player will roll to determine their whether they have high, medium, low stats on each statistic (e.g strength, vitality, dexterity, etc) 
- Character Classes: Players will roll for their class either mage, warrior, rogue, and time keeper
- In-Game Options: The game will prompt you to run, fight, flee, or negotiate each in-game event. 
- Turn-based Combat: Each player will get a chance to roll to determine the success of their attacks.
- Follow the instructions displayed in the terminal to play through the game.

### Example

After running the game, you will see a series of prompts like:

```
A mysterious door blocks your path, with a riddle inscribed. What will you do?

Choose a party member:
1. Character_0
2. Character_1
3. Character_2

Enter the number of the chosen party member: 
```

Simply follow the prompts to make your choices and see the outcomes.

### Running Unit Tests

To run the provided unit tests, we recommend using `pytest`, a testing framework for Python.

#### Steps to Run Tests:

1. First, make sure `pytest` is installed on your machine:

   ```bash
   pip install pytest
   ```

2. Run the tests by navigating to the project root and executing the following command:

   ```bash
   pytest
   ```

This will discover and run all the tests in the `test/` directory.

### Example Test Output:

After running the tests, you should see output like this:

```
============================= test session starts ==============================
collected 3 items

test/test_game.py ...                                                     [100%]

============================== 3 passed in 0.05s ===============================
```

### Project Structure

Here is the project directory structure:

```
.
├── PROJECT_INSTRUCTIONS.md
├── README.md
├── __init__.py
└── project_code
    ├── __init__.py
    ├── location_events
    │   └── location_1.json
    ├── src
    │   ├── __init__.py
    │   └── main.py
    └── test
        ├── __init__.py
        └── test_game.py
```

- `project_code/` - The main directory containing all the code for the project.
    - `location_events/` - Directory containing the JSON files with events for the game.
    - `src/` - Source code for the project.
    - `test/` - Directory for tests to ensure the game functions correctly.
- `README.md` - This file, with instructions on how to run the project.
- `PROJECT_INSTRUCTIONS.md` - Additional instructions or guidelines for the project.

---

Enjoy your adventure!

