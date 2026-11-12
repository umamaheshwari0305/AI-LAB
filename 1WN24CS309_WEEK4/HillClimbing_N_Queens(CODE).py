import random

def calculate_heuristic(state):
    #calculating the number of conflicting pairs of queens 
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:  # Checking if queens are in the same row
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j): # Checking if queens are attacking each other in the diagonal
                conflicts += 1
    return conflicts

def get_neighbors(state):
    # generating all possible neighbor of the current state by changing the row position of the queen
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = list(state)
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def hill_climbing_n_queens(n):
    # Initialing the current state with a random state 
    current_state = [random.randint(0, n - 1) for _ in range(n)]
    current_h = calculate_heuristic(current_state)
    
    steps = 0
    print(f"--- START ---")
    print(f"Initial State : {current_state} | h = {current_h}\n")
    
    while True:
        steps += 1
        neighbors = get_neighbors(current_state)
        
        # Calculating heuristics of each queens
        neighbor_evaluations = [(nb, calculate_heuristic(nb)) for nb in neighbors]
        
        # Finding the minimum conflict vallue out of all
        min_neighbor_h = min(score for _, score in neighbor_evaluations)
        
        # Filtering the neighbors that has the least conflicts
        best_neighbors = [nb for nb, score in neighbor_evaluations if score == min_neighbor_h]
        
        if min_neighbor_h < current_h:
            chosen_state = random.choice(best_neighbors)
            print(f"[Step {steps}:")
            print(f"  Current State: {current_state} | h = {current_h}")
            print(f"  Chosen State : {chosen_state} | h = {min_neighbor_h}\n")
            
            current_state = chosen_state
            current_h = min_neighbor_h
            
        elif min_neighbor_h == current_h:
            chosen_state = random.choice(neighbors)
            chosen_h = calculate_heuristic(chosen_state)
            
            print(f"[Step {steps}:")
            print(f"  Current State: {current_state} | h = {current_h}")
            print(f"  Chosen State : {chosen_state} | h = {chosen_h}\n")
            
            current_state = chosen_state
            current_h = chosen_h
            
        else:
            if current_h == 0:
                print(f"Success! Global optimum reached in {steps} steps.")
                return current_state
            else:
                print(f"[Trap Encountered at Step {steps}] Stuck in Local Optimum: {current_state} (h = {current_h})")
                current_state = [random.randint(0, n - 1) for _ in range(n)]
                current_h = calculate_heuristic(current_state)
                print(f"RESTART!!! New State: {current_state} | h = {current_h}\n")

def print_board(state):
    #printing the matrix of the state at each step
    n = len(state)
    for row in range(n):
        row_str = ""
        for col in range(n):
            if state[col] == row:
                row_str += " Q "
            else:
                row_str += " . "
        print(row_str)


if __name__ == "__main__":
    try:
        num_queens = int(input("Enter the number of Queens (N): "))
        if num_queens < 4 and num_queens != 1:
            print("No solution for less than 4 queens")
        else:
            final_solution = hill_climbing_n_queens(num_queens)
            print(f"\nFinal Solution State: {final_solution}")
            # print("\nVisualized Matrix Layout:")
            # print_board(final_solution)
    except ValueError:
        print("Please enter a valid integer.")
