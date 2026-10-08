8puzzle

import time
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def get_board_input(prompt_name):
    """Prompts the user to enter a 3x3 board as 9 space-separated numbers."""
    print(f"\n--- Enter {prompt_name} ---")
    print("Enter 9 numbers (0 to 8) separated by spaces (0 represents the blank space):")
    while True:
        try:
            raw_input = input(">> ").strip().split()
            if len(raw_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            board_flat = [int(x) for x in raw_input]
            if sorted(board_flat) != list(range(9)):
                print("Error: Board must contain all digits from 0 to 8 with no duplicates.")
                continue
            return tuple(tuple(board_flat[i:i + 3]) for i in range(0, 9, 3))
        except ValueError:
            print("Error: Invalid input! Please enter space-separated integers only.")

def find_blank(state):
    """Find row and column of the blank tile (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_neighbors(state):
    """Generate valid next states by sliding adjacent tiles into the blank space."""
    r, c = find_blank(state)
    neighbors = []
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_board = [list(row) for row in state]
            new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
            neighbors.append(tuple(tuple(row) for row in new_board))
    return neighbors

def print_board(state):
    """Print state in a clean 3x3 layout."""
    for row in state:
        print(" ".join(str(val) if val != 0 else "_" for val in row))
    print()

def print_path(path):
    """Display the full sequence of moves from start to goal."""
    print(f"\nSolution Found in {len(path) - 1} moves:\n")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_board(state)


def dfs(start_state, goal_state, max_depth=30):
    """Solve 8-puzzle using Depth First Search (DFS)."""
    stack = [(start_state, [start_state])]
    visited = set([start_state])
    while stack:
        current_state, path = stack.pop()
        if current_state == goal_state:
            return path
        if len(path) - 1 < max_depth:
            for neighbor in get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
    return None


def depth_limited_search(state, goal_state, limit, path, visited):
    """Recursive Depth-Limited Search helper function for IDS."""
    if state == goal_state:
        return path
    if limit <= 0:
        return None
    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            visited.add(neighbor)
            result = depth_limited_search(neighbor, goal_state, limit - 1, path + [neighbor], visited)
            if result is not None:
                return result
            visited.remove(neighbor)  # Backtrack
    return None


def ids(start_state, goal_state, max_limit=30):
    """Solve 8-puzzle using Iterative Deepening Search (IDS)."""
    for limit in range(max_limit + 1):
        visited = set([start_state])
        result = depth_limited_search(start_state, goal_state, limit, [start_state], visited)
        if result is not None:
            print(f"Goal reached at Depth Limit: {limit}")
            return result
    return None


def main():
    print("=" * 45)
    print("         8-PUZZLE PROBLEM SOLVER")
    print("=" * 45)
    initial_state = get_board_input("INITIAL STATE")
    goal_state = get_board_input("GOAL STATE")
    while True:
        print("\n" + "=" * 45)
        print("                MENU")
        print("=" * 45)
        print("1. Solve using Depth First Search (DFS)")
        print("2. Solve using Iterative Deepening Search (IDS)")
        print("3. Enter New Initial & Goal States")
        print("4. Exit")
        print("-" * 45)
        choice = input("Enter choice (1-4): ").strip()
        match choice:
            case '1':
                print("\nRunning Depth First Search (DFS)...")
                start_time = time.time()
                path = dfs(initial_state, goal_state, max_depth=30)
                end_time = time.time()
                if path:
                    print_path(path)
                    print(f"Time Taken: {end_time - start_time:.4f} seconds")
                else:
                    print("No solution found within the specified depth limit.")
            case '2':
                print("\nRunning Iterative Deepening Search (IDS)...")
                start_time = time.time()
                path = ids(initial_state, goal_state, max_limit=30)
                end_time = time.time()
                if path:
                    print_path(path)
                    print(f"Time Taken: {end_time - start_time:.4f} seconds")
                else:
                    print("No solution found within the maximum depth limit.")
            case '3':
                initial_state = get_board_input("INITIAL STATE")
                goal_state = get_board_input("GOAL STATE")
            case '4':
                print("Exiting program. Goodbye!")
                break
            case _:
                print("Invalid choice! Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
