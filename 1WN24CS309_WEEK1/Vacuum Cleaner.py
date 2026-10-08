def simple_reflex_vacuum_agent(location, status_a, status_b):
    print("\n--- Simple Reflex Vacuum Agent Step ---")
    current_status = status_a if location == 'A' else status_b
    
    print(f"Percept: Location = {location}, Current Room Status = {'Dirty' if current_status == 1 else 'Clean'}")
    
    if current_status == 1:
        action = "Suck"
    elif location == 'A':
        action = "Move Right"
    elif location == 'B':
        action = "Move Left"
        
    print(f"Action Taken: {action}")
    return action


def run_simulation(location, status_a, status_b):
    steps = 0
    
    # Loop until both rooms are clean (0)
    while status_a == 1 or status_b == 1:
        steps += 1
        action = simple_reflex_vacuum_agent(location, status_a, status_b)
        
        # Update the environment state based on the agent's action
        if action == "Suck":
            if location == 'A':
                status_a = 0
            elif location == 'B':
                status_b = 0
        elif action == "Move Right":
            location = 'B'
        elif action == "Move Left":
            location = 'A'

    print(f"\nBoth rooms are now clean! Simulation ended in {steps} step(s).")
    print(f"Final State: Room A = {'Dirty' if status_a == 1 else 'Clean'}, Room B = {'Dirty' if status_b == 1 else 'Clean'}")


if __name__ == "__main__":
    loc = input("Enter Vacuum Location (A/B): ").strip().upper()
    st_a = int(input("Enter Room A status (1 for Dirty, 0 for Clean): "))
    st_b = int(input("Enter Room B status (1 for Dirty, 0 for Clean): "))
    
    run_simulation(loc, st_a, st_b)
