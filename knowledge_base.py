class KnowledgeBase:
    def __init__(self, all_characters, all_weapons, all_rooms, my_cards):
        # Convert my cards to a set for fast lookup
        self.my_cards = set(my_cards)

        # Possible solution candidates (remove cards that the AI already holds)
        self.possible = {
            "character": set(all_characters) - self.my_cards,
            "weapon": set(all_weapons) - self.my_cards,
            "room": set(all_rooms) - self.my_cards
        }

        # All players in the game
        self.players = list(all_characters)

        # Cards players definitely showed at some point
        self.known_by_player = {p: set() for p in self.players}

        # Cards players might have (inferred from refutations)
        self.maybe_by_player = {p: set() for p in self.players}

    # ----------------------------------------------------------------------
    def mark_seen(self, player, card):
        for category in self.possible:
            self.possible[category].discard(card)

        self.known_by_player[player].add(card)

        # Once a card is known, no other player can "maybe" have it
        for p in self.maybe_by_player:
            self.maybe_by_player[p].discard(card)

    # ----------------------------------------------------------------------
    def note_refutation(self, refuter, suggestion_triplet):
        for card in suggestion_triplet:
            # Skip cards we already own
            if card in self.my_cards:
                continue

            # If refuter doesn't already definitely have it, they might have it
            if card not in self.known_by_player[refuter]:
                self.maybe_by_player[refuter].add(card)

    # ----------------------------------------------------------------------
    def note_no_refutation(self, suggester, players_checked, suggestion_triplet):
        # Remove the suggested cards from players who could not refute
        for p in players_checked:
            for card in suggestion_triplet:
                self.maybe_by_player[p].discard(card)

        # Check if each card has no possible owner → must be in solution
        for card in suggestion_triplet:
            if card in self.my_cards:
                continue

            # Check if ANY player could still have the card
            somebody_could_have_it = any(
                card in self.known_by_player[p] or card in self.maybe_by_player[p]
                for p in self.players
            )

            # If nobody can have it → it's a solution card
            if not somebody_could_have_it:
                self.eliminate_all_except(card)

    # ----------------------------------------------------------------------
    def eliminate_all_except(self, card):
        for category, items in self.possible.items():
            if card in items:
                self.possible[category] = {card}

    # ----------------------------------------------------------------------
    def single_solution_candidate(self):
        if all(len(self.possible[cat]) == 1 for cat in ["character", "weapon", "room"]):
            return (
                next(iter(self.possible["character"])),
                next(iter(self.possible["weapon"])),
                next(iter(self.possible["room"]))
            )
        return None
