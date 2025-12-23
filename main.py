import sys
from characters import characters
from board import valid_moves, rooms, display_board
from weapons import weapons, weapon_positions
from game_logic import roll_dice, make_suggestion, murder_solution, reveal_solution
from ai_player import AIPlayer
from knowledge_base import KnowledgeBase

# ---------------------------
# GAME INITIALIZATION
# ---------------------------

# List of all players in the Clue Game
player_names = ["Miss Scarlett", "Colonel Mustard", "Mrs. White",
                "Reverend Green", "Mrs. Peacock", "Professor Plum"]

# Humans are all players except the AI
human_players = player_names[:-1]
ai_name = "Professor Plum"

# Initialize AI Player and give it a Knowledge Base
ai = AIPlayer(ai_name)
ai.init_kb(
    all_characters=player_names,
    all_weapons=weapons,
    all_rooms=rooms,
    my_cards=characters[ai_name]["cards"]   # Cards assigned to the AI
)

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def get_choice(prompt, options):
    print(f"{prompt} (options: {', '.join(options)})")
    while True:
        choice = input("> ").strip()
        if choice in options:
            return choice
        print("Invalid choice! Please choose from the given options only.")

def move_player(player):
    player_info = characters[player]
    print(f"\n{player} is at {player_info['position']}")

    # Roll dice (1–6)
    dice = roll_dice()
    print(f"You rolled a {dice}")
    steps = dice

    # Move until steps run out or player stops
    while steps > 0:
        current = characters[player]["position"]
        moves = valid_moves(current)

        print(f"From {current}, you can move to: {moves}")
        print("Type 'pass' to stop moving early.")

        m = input(f"Enter your move ({steps} steps left): ").strip()

        if m.lower() == "pass":
            break

        if m in moves:
            characters[player]["position"] = m
            steps -= 1
            print(f"Moved to {m}")
        else:
            print("Invalid move! Please choose from the given options only.")

def referrer_display(refuter, suggester):
    if refuter == suggester:
        return ""
    return f"{refuter} refuted the suggestion (private card shown to suggester)."

# ---------------------------
# MAIN GAME LOOP
# ---------------------------

def main_loop():
    print("Welcome to Clue Game with AI Player")

    while True:

        # Find all players still in the game
        active = [p for p in player_names if not characters[p]["eliminated"]]

        # If no players left → game ends
        if len(active) == 0:
            print("No players active. Game over! 🎉")
            return

        # If only one player remains → they win automatically
        if len(active) == 1:
            print(f"{active[0]} wins 🎉 by default.")
            return

        # Loop through each player’s turn
        for player in player_names:

            if characters[player]["eliminated"]:
                continue  # Skip eliminated players

            print(f"\n--- {player}'s turn ---")
            display_board(characters, weapon_positions)

            # ---------------------------------------
            # AI PLAYER TURN
            # ---------------------------------------
            if player == ai_name:

                # AI chooses where to move
                newpos = ai.pick_move()
                characters[player]["position"] = newpos
                print(f"{player} (AI) moved to {newpos}")

                # AI makes a suggestion if inside a room
                suggest = ai.make_suggestion()
                if suggest is None:
                    print(f"{player} (AI) is not in a room and makes no suggestion.")
                else:
                    char_s, weap_s, room_s = suggest
                    refuter, shown_card, checked_players = make_suggestion(
                        player, room_s, char_s, weap_s
                    )

                    # If someone refuted → AI learns the shown card
                    if refuter:
                        print(f"(Private) {referrer_display(refuter, player)}")
                        ai.process_seen_card(refuter, shown_card)
                    else:
                        # No refutation → AI updates its deduction logic
                        ai.process_no_refute(player, checked_players, [char_s, weap_s, room_s])

                # AI decides whether to accuse
                acc = ai.consider_accusation()
                if acc:
                    print(f"{player} (AI) makes an accusation: {acc}")

                    # Check if AI is correct
                    if acc == (murder_solution["character"],
                               murder_solution["weapon"],
                               murder_solution["room"]):
                        print(f"{player} (AI) wins! 🎉")
                        return
                    else:
                        print(f"{player} (AI) made an incorrect accusation and is eliminated.")
                        characters[player]["eliminated"] = True
                continue  # End AI turn

            # ---------------------------------------
            # HUMAN PLAYER TURN
            # ---------------------------------------

            input("Press Enter to roll dice.")
            move_player(player)

            # If player is inside a room → allow suggestion
            cur = characters[player]["position"]
            if cur in rooms:
                print(f"You are in {cur}. Make a suggestion.")

                sc = get_choice("Character?", player_names)
                sw = get_choice("Weapon?", weapons)

                # Make and process suggestion
                refuter, shown_card, checked_players = make_suggestion(player, cur, sc, sw)

                if refuter:
                    print(f"{refuter} shows you a card: {shown_card}")

                    # Inform AI if relevant
                    if ai_name in checked_players or refuter == ai_name:
                        if refuter == ai_name:
                            ai.process_seen_card(refuter, shown_card)
                        else:
                            ai.process_refuter(refuter, [sc, sw, cur])
                else:
                    print("No one could refute your suggestion.")
                    ai.process_no_refute(player, checked_players, [sc, sw, cur])

            # Ask if human wants to accuse
            accq = input("Do you want to make an accusation? (yes/no): ").strip().lower()

            if accq == "yes":
                ac = get_choice("Character?", player_names)
                aw = get_choice("Weapon?", weapons)
                ar = get_choice("Room?", rooms)

                # Check accusation result
                if (ac == murder_solution["character"] and
                    aw == murder_solution["weapon"] and
                    ar == murder_solution["room"]):
                    print(f"{player} wins! Correct accusation. 🎉")
                    return
                else:
                    print(f"{player}, Wrong accusation. You are eliminated from future turns.")
                    characters[player]["eliminated"] = True

# ---------------------------
# GAME ENTRY POINT
# ---------------------------

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
    finally:
        reveal_solution()  # Show final correct answer
        sys.exit(0)
