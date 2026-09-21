# Digital Clue Game with AI Player

## Objective 
This project is a Python-based version of Clue Game where players try to deduce **who committed the murder, with which weapon, and in which room**. The game supports:

- Human players (via terminal input)  
- AI player with deductive reasoning 
- Dice-based movement  
- Suggestions, refutations, and accusations  
- ASCII board visualization  

## Features
- **Multiple players:** Up to six players, one AI player by default  
- **AI deduction:** Tracks card seen, refutations, and possible solutions  
- **Randomized setup:** Murder solution and card distribution are random each game  
- **Interactive gameplay:** Human players roll dice, move, suggest, and accuse via terminal  
- **Visual board:** ASCII representation of rooms, hallways, characters, and weapons 

## How to Run the code
1. Make sure you have Python 3 installed.
2. Open a terminal in the `SandhyaRani_Project2_SourceCode` folder.
3. Run the game: python main.py

## Files
- `main.py` : Main game loop handling player turns, movement, suggestions, and accusations.
- `board.py` : Defines board layout, room adjacency, hallways, and ASCII board display.
- `characters.py` : Defines characters and their starting positions.
- `weapons.py` : Defines weapons and their initial positions.
- `game_logic.py` : Handles dice rolling, card dealing, suggestions/refutations, and murder solution generation.
- `ai_player.py` : AI player logic, including movement, suggestions, and decision-making.
- `knowledge_base.py` : AI reasoning engine for tracking possible solutions and deducing the murder combination.
- `README.md` : Clue Game documentation and instructions.

## Setup
1. Place each character at their initial starting position.
2. Weapon positions are randomly initialized; their starting location does not affect gameplay.
3. A random murder solution is generated with: 
        - One Suspect
        - One Room
        - One Weapon
4. Players try to guess this hidden combination during gameplay.

## Gameplay
1. **Turn order:** Miss Scarlett always takes the first turn. Play then continues clockwise.
2. **Dice roll:** At the beginning of a turn, the player rolls a die to determine how many movement points are available.
3. **Movement:** The player may move up to the number of spaces rolled.
- Players may stop moving early by typing pass.
- Players cannot move diagonally.
- Players cannot move through a space occupied by another player.
4. **Suggestions:** A player who enters or begins a turn inside a room may make a suggestion containing:
- One suspect
- One weapon
- The room the player currently occupies
5. **Refutations:** Beginning with the next player in clockwise order, each player checks whether they can disprove the suggestion.
- The first player who holds one or more matching cards secretly reveals one matching card to the suggesting player.
- Only the suggesting player sees the revealed card.
- If no player can disprove the suggestion, no card is revealed.
6. **Recording Information:** Players can use revealed cards and refutation results to eliminate possibilities and determine the hidden murder solution.
7. **Next turn:** After movement and any optional suggestion or accusation are complete, play continues clockwise.
8. **Special Rules:** Secret Passages
Secret passages connect the following rooms:
- Lounge ↔ Conservatory
- Kitchen ↔ Study
9. **Movement Restrictions:**
- Players cannot move diagonally.
- Players cannot move through spaces occupied by other players.
- Suggestions may only be made while inside a room.
- Accusations may be made from any location.

## Correct Accusation
If all three cards match the hidden murder solution, the accusing player wins the game.
Incorrect Accusation
If any part of the accusation is incorrect:
- The player is eliminated from future turns.
- The player may still reveal cards when refuting other players' suggestions.
If every active player is eliminated, the game ends without a winner.

## Winning Conditions 
A player may make an accusation when they believe they know the complete murder solution.
An accusation must identify:
- The suspect
- The weapon
- The room

## AI Player
The AI player uses a knowledge base to track:
- Cards in its own hand
- Cards revealed by other players
- Suggestions and their outcomes
- Players who could or could not refute suggestions
- Remaining possible suspects, weapons, and rooms

## The AI:
- Prefers moving toward unexplored rooms
- Makes strategic suggestions to collect new information
- Updates its knowledge after every relevant action
- Eliminates impossible cards from the potential solution
- Makes an accusation when it has enough information to identify all three hidden cards

## Reveal Solution
The hidden murder solution is revealed to all players when the game ends because of:
- A correct accusation
- The elimination of all active players
- A game interruption or early exit
