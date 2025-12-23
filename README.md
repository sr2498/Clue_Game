# Digital Clue Game - Part 2 (with AI Player)

## Objective 
This project is a Python-based version of Clue where players try to deduce **who committed the murder, with which weapon, and in which room**. The game supports:

- Human players (via terminal input)  
- AI player with deductive reasoning 
- Dice-based movement  
- Suggestions, refutations, and accusations  
- ASCII board visualization  

## Features
- **Multiple players:** Up to six players, one AI by default  
- **AI deduction:** Tracks card seen, refutations, and possible solutions  
- **Randomized setup:** Murder solution and card distribution are random each game  
- **Interactive gameplay:** Human players roll dice, move, suggest, and accuse via terminal  
- **Visual board:** ASCII representation of rooms, hallways, characters, and weapons 

## How to Run
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
1. **Turn order:** Miss Scarlett always goes first.
2. **Dice roll:** On a player’s turn, roll a dice to determine movement points.
3. **Movement:** Move up to the number rolled. Players can stop early by typing pass.
4. **Suggestions:** When in a room, a player may suggest a suspect and weapon.
5. **Refutations:** The first player clockwise who can disprove the suggestion shows one card secretly to the suggesting player.
    - If no player can disprove, the suggestion provides no new information.
6. **Marking cards:** Players note which cards have been seen.
7. **Next turn:** Play continues clockwise. Suggestions can only be made in rooms.

**Special rules:**
- Secret passages exist between:
    - Lounge ↔ Conservatory
    - Kitchen ↔ Study
- Players cannot move diagonally or through a space occupied by another player.

## Winning Conditions
1. Players may make an accusation when they believe they know all three hidden cards.
2. Accusations can be made from any location.
3. Correct accusation: The player wins the game.
4. Incorrect accusation: The player is eliminated from future turns but may still show cards when refuting others’ suggestions.

## AI Player
- AI uses a knowledge base to track:
    - Cards it has seen
    - Possible cards other players may hold
    - Deduction of the solution
- AI movement prefers unexplored rooms.
- AI makes suggestions strategically to gain new information.
- When confident, AI makes an accusation to attempt winning.

## Reveal Solution
At the end of the game (either by correct accusation, all players eliminated, or game interruption), the actual murder solution is revealed to all players.
