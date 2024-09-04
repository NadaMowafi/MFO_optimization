import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import funcs  # Import the funcs module that contains benchmark functions
import time

def mfo_main():
    # Number of moths and iterations
    n_moths = 50  # Number of moths (agents)
    max_iterations = 1000  # Maximum number of iterations for optimization
    num_runs = 10  # Number of optimization runs (set to 1 for animation purposes)

    # Define problem dimensions and boundaries
    dim = 2  # Dimension of the problem (e.g., 2D)
    lb = -40  # Lower boundary for the search space
    ub = 40  # Upper boundary for the search space

    # Get the benchmark functions from the funcs module
    benchmark_functions = get_benchmark_functions()

    # Choose the benchmark function to optimize
    print('Choose a benchmark function:')
    for i, func in enumerate(benchmark_functions, 1):
        print(f'{i}: {func.__name__}')  # Display available benchmark functions
    choice = int(input('Enter the function number: ')) - 1  # User selects a functionhjhjkh

    # Select the corresponding benchmark function
    benchmark_func = benchmark_functions[choice]

    # Known global minimum (set based on the selected benchmark function)
    global_minimum = np.zeros(dim)  # Assuming global minimum at [0, 0] for simplicity

    # Store results and solutions for all runs
    results = []  # Store the best result of each run
    best_solutions = []  # Store the best position of each run

    # Initialize moths' positions randomly within the boundaries
    moths = lb + (ub - lb) * np.random.rand(n_moths, dim)
    initial_moths = moths.copy()  # Store initial positions for comparison later

    # Perform multiple optimization runs to check for consistency and local minima
    for run in range(num_runs):
        all_moth_positions = []  # Track positions of all moths at each iteration

        # Variables to store the best solution and position found during this run
        best_solution = np.inf  # Initialize to infinity (worst case)
        best_position = np.zeros(dim)  # Initialize to zero vector

        # Start the timer to measure time taken for this run
        start_time = time.time()

        # Main optimization loop
        for iteration in range(max_iterations):
            # Evaluate the fitness (objective function value) of each moth
            for i in range(n_moths):
                fitness = benchmark_func(moths[i])
                # If this moth has a better fitness, update the best solution and position
                if fitness < best_solution:
                    best_solution = fitness
                    best_position = moths[i].copy()

            # Store the positions of moths at this iteration for animation purposes
            all_moth_positions.append(moths.copy())

            # Calculate the number of flames (which decreases over time)
            n_flames = round(n_moths - iteration * (n_moths - 1) / max_iterations)

            # Update the moths' positions using the MFO update rule
            moths = update_moths(moths, best_position, lb, ub, n_flames, iteration, max_iterations)

            # Ensure moths remain within the boundaries of the search space
            moths = np.clip(moths, lb, ub)

        # Stop the timer and calculate the time taken for this run
        end_time = time.time()
        time_taken = end_time - start_time

        # Save the best solution and position found during this run
        results.append(best_solution)
        best_solutions.append(best_position)

        # Display the best solution found and the time taken for this run
        print(f'Run {run+1}: Best Solution: {best_solution:.4f}')
        print('Best position:')
        print(best_position)
        print(f'Time taken for this run: {time_taken:.2f} seconds')
        print("_____________________________________________________")

# Check if the best solution is close to the global minimum (local minima check)
        check_local_minimum(best_position, global_minimum)

        # Animate the optimization process to visualize moth movement
        animate_optimization_paths(all_moth_positions, lb, ub)

    # Compute the mean and standard deviation of the best solutions across all runs
    mean_result = np.mean(results)
    std_result = np.std(results)

    # Display the mean and standard deviation of the best solutions
    print(f'Mean of best solutions: {mean_result:.4f}')
    print(f'Standard deviation of best solutions: {std_result:.4f}')

    # 3D Plot of the benchmark function and best positions found
    plot_3d_function(benchmark_func, lb, ub, best_solutions)

    # Plot the moth positions before and after optimization for comparison
    plot_before_after_optimization(initial_moths, moths, best_solutions)

def update_moths(moths, best_position, lb, ub, n_flames, iteration, max_iterations):
    # Calculate the flame decay coefficient (linearly changes over iterations)
    b = 1  # Constant value defining the shape of the logarithmic spiral
    t = -1 + (iteration / max_iterations) * 2  # Linearly decreases from -1 to 1

    # Loop over all moths and update their positions
    for i in range(moths.shape[0]):
        for j in range(moths.shape[1]):
            # Calculate the distance to the flame (best position)
            distance_to_flame = np.abs(moths[i, j] - best_position[j])
            # Update position according to the MFO update rule (logarithmic spiral)
            moths[i, j] = distance_to_flame * np.exp(b * t) * np.cos(t * 2 * np.pi) + best_position[j]

    # Ensure moths remain within the boundaries of the search space
    moths = np.clip(moths, lb, ub)

    return moths

def get_benchmark_functions():

    return [getattr(funcs, f) for f in dir(funcs) if callable(getattr(funcs, f)) and not f.startswith("_")]

def plot_3d_function(func, lb, ub, best_positions):

    # Generate a grid for plotting the objective function
    x = np.linspace(lb, ub, 100)
    y = np.linspace(lb, ub, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    # Calculate the function values for the entire grid
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = func(np.array([X[i, j], Y[i, j]]))
    
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)  # Surface plot of the function
    
    # Plot the best positions found by the optimization algorithm
    best_positions = np.array(best_positions)
    ax.scatter(best_positions[:, 0], best_positions[:, 1], func(best_positions.T), color='b', marker='o', s=100, label='Best Solutions')

    # Set labels and title for the plot
    ax.set_title(f'3D Plot of {func.__name__}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Objective Function')
    plt.legend()
    plt.show()

def plot_before_after_optimization(initial_moths, final_moths, best_solutions):

    # Create a plot to compare moths' positions before and after optimization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Plot initial moth positions before optimization
    ax1.scatter(initial_moths[:, 0], initial_moths[:, 1], c='red')
    ax1.set_title('Moths Before Optimization')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Plot final moth positions after optimization
    ax2.scatter(final_moths[:, 0], final_moths[:, 1], c='green')
    ax2.scatter(np.array(best_solutions)[:, 0], np.array(best_solutions)[:, 1], c='blue', marker='x', s=100, label='Best Solutions')
    ax2.set_title('Moths After Optimization')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.legend()
    plt.show()

def animate_optimization_paths(all_moth_positions, lb, ub):

    fig, ax = plt.subplots()
    
    # Create a scatter plot for moth positions (initially empty)
    scat = ax.scatter([], [], c='blue')
    
    # Set the limits of the plot based on the boundaries
    ax.set_xlim(lb, ub)
    ax.set_ylim(lb, ub)
    ax.set_title("Moth Optimization Animation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    
    def update(frame):
        # Update the scatter plot with moth positions for the current frame (iteration)
        scat.set_offsets(all_moth_positions[frame])
        return scat,
    
    # Create the animation object
    ani = animation.FuncAnimation(fig, update, frames=len(all_moth_positions), blit=True, repeat=False)
    plt.show()

def check_local_minimum(best_position, global_minimum, tolerance=1e-3):

    if np.allclose(best_position, global_minimum, atol=tolerance):
        print(f"Solution is close to the global minimum (within tolerance of {tolerance})")
    else:
        print(f"Solution is NOT close to the global minimum (possible local minimum)")
        

# Run the MFO algorithm
if __name__== "__main__":
    mfo_main()