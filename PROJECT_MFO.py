import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def mfo_main():
    # Number of moths and iterations
    n_moths = 50
    max_iterations = 100
    
    # Define problem dimensions and boundaries
    dim = 2  # Dimension of the problem
    lb = 2.5  # Lower boundary
    ub = 5  # Upper boundary
    
    # Choose the benchmark function
    print('Choose a benchmark function:')
    for i, func in enumerate(benchmark_functions, 1):
        print(f'{i}: {func.__name__}')
    choice = int(input('Enter the function number: ')) - 1
    
    # Select the corresponding function
    benchmark_func = benchmark_functions[choice]
    
    # Initialize moths' positions
    moths = lb + (ub - lb) * np.random.rand(n_moths, dim)
    initial_moths = moths.copy()  # Store initial positions for comparison later
    
    # Store best solution found
    best_solution = np.inf
    best_position = np.zeros(dim)
    
    fig, ax = plt.subplots()
    ax.set_xlim(lb, ub)
    ax.set_ylim(lb, ub)
    
    scat = ax.scatter(moths[:, 0], moths[:, 1], c='red')
    best_scat = ax.scatter(best_position[0], best_position[1], c='blue', marker='x')
    
    def update(iteration):
        nonlocal moths, best_solution, best_position
        
        # Evaluate the fitness of each moth
        for i in range(n_moths):
            fitness = benchmark_func(moths[i])
            if fitness < best_solution:
                best_solution = fitness
                best_position = moths[i].copy()
        
        # Calculate the number of flames
        n_flames = round(n_moths - iteration * (n_moths - 1) / max_iterations)
        
        # Update moths' positions using the MFO update rule
        moths = update_moths(moths, best_position, lb, ub, n_flames, iteration, max_iterations)
        
        # Update the scatter plot data
        scat.set_offsets(moths)
        best_scat.set_offsets(best_position)
        ax.set_title(f"Iteration {iteration + 1}/{max_iterations}")
        return scat, best_scat
    
    ani = animation.FuncAnimation(fig, update, frames=max_iterations, interval=100, repeat=False)
    plt.show()
    
    # Display the best solution found
    print(f'Best solution found: {best_solution:.4f}')
    print('Best position:')
    print(best_position)
    
    # Plot before and after optimization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.scatter(initial_moths[:, 0], initial_moths[:, 1], c='red')
    ax1.set_title('Moths Before Optimization')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.grid(True)
    
    ax2.scatter(moths[:, 0], moths[:, 1], c='blue')
    ax2.set_title('Moths After Optimization')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.grid(True)
    
    plt.show()

def update_moths(moths, best_position, lb, ub, n_flames, iteration, max_iterations):
    # Calculate the flame decay coefficient
    b = 1  # Constant value defining the shape of the logarithmic spiral
    t = -1 + (iteration / max_iterations) * 2  # Linearly decreases from -1 to 1
    
    # Loop over all moths and update their positions
    for i in range(moths.shape[0]):
        for j in range(moths.shape[1]):
            distance_to_flame = np.abs(moths[i, j] - best_position[j])
            moths[i, j] = distance_to_flame * np.exp(b * t) * np.cos(t * 2 * np.pi) + best_position[j]
    
    # Clamp the positions within the boundaries
    moths = np.clip(moths, lb, ub)
    
    return moths

# Example benchmark functions
def ackley(x):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x[0]**2 + x[1]**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))) + np.exp(1) + 20

def beale(x):
    return (1.5 - x[0] + x[0] * x[1])**2 + (2.25 - x[0] + x[0] * x[1]**2)**2 + (2.625 - x[0] + x[0] * x[1]**3)**2

# Add more benchmark functions here...

# List of benchmark functions
benchmark_functions = [ackley, beale]

if __name__ == "__main__":
    mfo_main()