import random
from characters import characters
from weapons import weapons, weapon_positions
from board import rooms, hallways

# Murder solution
murder_solution = {
    "character": random.choice(list(characters.keys())),
    "weapon": random.choice(weapons),
    "room": random.choice(rooms)
}

# Prepare deck (exclude solution cards)
character_cards = [c for c in characters if c != murder_solution["character"]]
weapon_cards = [w for w in weapons if w != murder_solution["weapon"]]
room_cards = [r for r in rooms if r != murder_solution["room"]]
cards = character_cards + weapon_cards + room_cards
random.shuffle(cards)

# Deal cards
player_names = list(characters.keys())
for player in characters.values():
    player["cards"] = []

for i, card in enumerate(cards):
    receiver = player_names[i % len(player_names)]
    characters[receiver]["cards"].append(card)

# Initialize weapon positions
valid_locations = rooms + hallways
for weapon in weapons:
    weapon_positions[weapon] = random.choice(valid_locations)

# Dice
def roll_dice():
    return random.randint(1, 6)

# Suggestion
def make_suggestion(suggester, room, suggested_character, suggested_weapon):
    characters[suggested_character]["position"] = room
    weapon_positions[suggested_weapon] = room

    print(f"\n🔎 Suggestion by {suggester}: {suggested_character} with {suggested_weapon} in {room}")

    names = player_names
    start_index = names.index(suggester)
    checked_players = []

    for offset in range(1, len(names)):
        p = names[(start_index + offset) % len(names)]
        checked_players.append(p)
        hand = characters[p]["cards"]
        possible_cards = [card for card in hand if card in (suggested_character, suggested_weapon, room)]
        if possible_cards:
            shown_card = random.choice(possible_cards)
            return (p, shown_card, checked_players)

    return (None, None, checked_players)

def reveal_solution():
    print("\n============= 🔐 MURDER SOLUTION 🔐 =============")
    print(f"👤 Suspect : {murder_solution['character']}")
    print(f"🔪 Weapon  : {murder_solution['weapon']}")
    print(f"🏠 Room    : {murder_solution['room']}")
    print("=================================================\n")
