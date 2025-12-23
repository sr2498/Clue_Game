import random
from knowledge_base import KnowledgeBase
from board import valid_moves, rooms
from characters import characters
from weapons import weapons

# Initialize AI player
class AIPlayer:
    def __init__(self, name):
        self.name = name
        self.kb = None

    # Create a KnowledgeBase object for the AI
    def init_kb(self, all_characters, all_weapons, all_rooms, my_cards):
        self.kb = KnowledgeBase(all_characters, all_weapons, all_rooms, my_cards)

    # -----------------------------------------------------------
    # MOVEMENT DECISION
    # -----------------------------------------------------------
    def pick_move(self):
        pos = characters[self.name]["position"]
        moves = valid_moves(pos)

        # If no moves are possible (should not happen), stay put
        if not moves:
            return pos

        # Prefer rooms that are still not eliminated by the knowledge base
        preferred = [m for m in moves if m in rooms and m in self.kb.possible["room"]]

        # If AI sees a still-possible room, it will go there
        if preferred:
            return random.choice(preferred)

        # Otherwise, move randomly among valid paths
        return random.choice(moves)

    # -----------------------------------------------------------
    # MAKING A SUGGESTION
    # -----------------------------------------------------------
    def make_suggestion(self):
        pos = characters[self.name]["position"]

        # Cannot suggest outside a room
        if pos not in rooms:
            return None

        # Characters not in AI's hand OR fallback to all remaining possible
        char_choices = (
            [c for c in self.kb.possible["character"] if c not in self.kb.my_cards]
            or list(self.kb.possible["character"])
        )

        # Same selection logic for weapons
        weap_choices = (
            [w for w in self.kb.possible["weapon"] if w not in self.kb.my_cards]
            or list(self.kb.possible["weapon"])
        )

        # Randomly choose from filtered possibilities
        chosen_char = random.choice(char_choices)
        chosen_weapon = random.choice(weap_choices)

        # Room is always the one AI stands in
        return (chosen_char, chosen_weapon, pos)

    # -----------------------------------------------------------
    # KNOWLEDGE UPDATES
    # -----------------------------------------------------------
    def process_seen_card(self, from_player, card):
        self.kb.mark_seen(from_player, card)

    def process_refuter(self, refuter, suggestion_triplet):
        self.kb.note_refutation(refuter, suggestion_triplet)

    def process_no_refute(self, suggester, players_checked, suggestion_triplet):
        self.kb.note_no_refutation(suggester, players_checked, suggestion_triplet)

    # -----------------------------------------------------------
    # ACCUSATION LOGIC
    # -----------------------------------------------------------
    def consider_accusation(self):
        return self.kb.single_solution_candidate()
