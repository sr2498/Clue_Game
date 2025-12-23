# Main rooms on the board
rooms = ["Study", "Library", "Billiard Room", "Conservatory", "Lounge", "Kitchen"]

# Hallway spaces between rooms
hallways = ["Hallway1", "Hallway2", "Hallway3"]

# The graph structure represents which areas connect to each other.
board_graph = {
    "Study": ["Hallway1", "Kitchen"],               # Secret passage
    "Hallway1": ["Study", "Library"],               # Secret passage
    "Library": ["Hallway1", "Hallway2", "Billiard Room"],
    "Billiard Room": ["Library", "Hallway3"],
    "Hallway2": ["Library", "Conservatory"],
    "Conservatory": ["Hallway2", "Lounge"],
    "Lounge": ["Hallway3", "Conservatory"],
    "Hallway3": ["Billiard Room", "Lounge", "Kitchen"],
    "Kitchen": ["Hallway3", "Study"]                # Secret passage
}

# A visual grid version of the board used for ASCII display.
ascii_board = [
    ["Study", "Hallway1", "Library"],
    ["Billiard Room", "Hallway2", "Conservatory"],
    ["Kitchen", "Hallway3", "Lounge"]
]

# -----------------------------
# MOVEMENT LOGIC
# -----------------------------

def valid_moves(pos):
    return board_graph.get(pos, [])


# -----------------------------
# ASCII BOARD DISPLAY
# -----------------------------

def display_board(characters, weapon_positions):
    cell_width = 28     
    cell_height = 3     

    # Header
    print("\n" + "=" * (len(ascii_board[0]) * (cell_width + 3)))
    print(" " * 30 + "🏠  Mansion Layout (Game Board)  🏠")
    print("=" * (len(ascii_board[0]) * (cell_width + 3)))

    # Loop through each row of the ASCII board
    for row in ascii_board:
        row_cells = []

        for cell in row:
            # Find characters standing in this cell
            chars_here = [name for name, info in characters.items() if info["position"] == cell]

            # Find weapons placed in this cell
            weapons_here = [w for w, pos in weapon_positions.items() if pos == cell]

            # Create the 3 text lines inside the cell block
            lines = [cell.center(cell_width)]  

            # Characters line
            if chars_here:
                lines.append(("👥 " + ", ".join(chars_here))[:cell_width].center(cell_width))
            else:
                lines.append(" ".center(cell_width))

            # Weapons line
            if weapons_here:
                lines.append(("🔪 " + ", ".join(weapons_here))[:cell_width].center(cell_width))
            else:
                lines.append(" ".center(cell_width))

            # If fewer lines than cell height, pad with blank lines
            while len(lines) < cell_height:
                lines.append(" ".center(cell_width))

            row_cells.append(lines)

        # Draw separator above row
        print("-" * (len(row) * (cell_width + 3)))

        # Print each line of every cell side-by-side
        for line_index in range(cell_height):
            print("|", end="")
            for lines in row_cells:
                print(" " + lines[line_index] + " |", end="")
            print()

    # Footer
    print("-" * (len(ascii_board[0]) * (cell_width + 3)))
    print("=" * (len(ascii_board[0]) * (cell_width + 3)))
