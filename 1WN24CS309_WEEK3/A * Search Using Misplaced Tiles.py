def misplaced_tiles_heuristic(state, goal_state):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal_state[i]:
            count += 1
    return count


def manhattan_distance_heuristic(state, goal_state):
    distance = 0
    for i in range(9):
        tile = state[i]
        if tile != 0:
            curr_row, curr_col = i // 3, i % 3
            goal_idx = goal_state.index(tile)
            goal_row, goal_col = goal_idx // 3, goal_idx % 3
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance


def generate_possible_moves(state):
    zero_idx = state.index(0)
    row, col = zero_idx // 3, zero_idx % 3
    moves = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_zero_idx] = new_state[new_zero_idx], new_state[zero_idx]
            moves.append(tuple(new_state))

    return moves


def A_Star(Start, Goal, heuristic_type="misplaced"):
    if heuristic_type == "misplaced":
        initial_h = misplaced_tiles_heuristic(Start, Goal)
    else:
        initial_h = manhattan_distance_heuristic(Start, Goal)

    start_node = {
        "state": Start,
        "g": 0,
        "h": initial_h,
        "f": 0 + initial_h,
        "parent": None
    }

    OPEN = [start_node]
    CLOSED = set()

    while OPEN:
        current_node = min(OPEN, key=lambda node: node["f"])
        OPEN.remove(current_node)
        CLOSED.add(current_node["state"])

        if current_node["state"] == Goal:
            path = []
            curr = current_node
            while curr:
                path.append(curr["state"])
                curr = curr["parent"]
            return "SUCCESS", path[::-1]

        next_states = generate_possible_moves(current_node["state"])

        for new_state in next_states:
            if new_state in CLOSED:
                continue

            g = current_node["g"] + 1

            if heuristic_type == "misplaced":
                h = misplaced_tiles_heuristic(new_state, Goal)
            else:
                h = manhattan_distance_heuristic(new_state, Goal)

            new_node = {
                "state": new_state,
                "g": g,
                "h": h,
                "f": g + h,
                "parent": current_node
            }

            OPEN.append(new_node)

    return "FAILURE", []


def get_grid_input(prompt):
    print(prompt)
    print("Enter 9 space-separated integers (0 for blank tile):")
    while True:
        try:
            values = list(map(int, input().split()))
            if len(values) == 9 and set(values) == set(range(9)):
                return tuple(values)
            else:
                print("Invalid input! Please enter exactly 9 unique numbers from 0 to 8.")
        except ValueError:
            print("Invalid input! Please enter integers only.")


def print_board(state):
    for i in range(0, 9, 3):
        print(f"{state[i]} {state[i+1]} {state[i+2]}")
    print()


if __name__ == "__main__":
    Start = get_grid_input("--- Enter Initial State ---")
    Goal = get_grid_input("--- Enter Goal State ---")

    print("\nSelect Heuristic Function:")
    print("1. Misplaced Tiles")
    print("2. Manhattan Distance")
    choice = input("Enter choice (1 or 2): ").strip()

    heuristic_choice = "misplaced" if choice == "1" else "manhattan"

    print(f"\nRunning A* Search using {'Misplaced Tiles' if choice == '1' else 'Manhattan Distance'}...\n")
    result, path = A_Star(Start, Goal, heuristic_type=heuristic_choice)

    if result == "SUCCESS":
        print(f"Goal Reached in {len(path) - 1} steps!\n")
        for step, state in enumerate(path):
            print(f"Step {step}:")
            print_board(state)
    else:
        print("No solution found.")
