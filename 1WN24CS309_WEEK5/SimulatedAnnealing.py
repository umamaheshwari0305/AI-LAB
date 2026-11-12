import math
import random


def parse_function(expr):
    return lambda x: eval(expr, {"math": math, "x": x})


def simulated_annealing(objective, start_x, t_init, alpha, steps=500):
    curr_x = start_x
    curr_y = objective(curr_x)

    best_x, best_y = curr_x, curr_y
    t = t_init

    while t > 0.001:
        for _ in range(steps):
            next_x = curr_x + random.gauss(0, 0.5)

            next_y = objective(next_x)
            delta = next_y - curr_y

            if delta < 0:
                accept = True
            else:
                prob = math.exp(-delta / t)
                accept = random.random() < prob

            if accept:
                curr_x = next_x
                curr_y = next_y

                if curr_y < best_y:
                    best_x = next_x
                    best_y = next_y

        t *= alpha

    return best_x, best_y


if __name__ == "__main__":
    
    init_x = float(input("Enter initial state: "))
    init_temp = float(input("Enter initial temperature: "))
    cool_rate = float(input("Enter cooling rate: "))
    func_input = input("Enter function of x: ")

    user_objective = parse_function(func_input)

    sol_x, sol_y = simulated_annealing(
        user_objective, start_x=init_x, t_init=init_temp, alpha=cool_rate
    )

    print(f"\nResult of x: {sol_x:.5f}")
    print(f"Minimum Value f(x): {sol_y:.5f}")
