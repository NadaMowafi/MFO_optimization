
from mpl_toolkits.mplot3d import Axes3D
import funcs
import time
from global_minima import get_global_minima
from domain import get_function_domain

def mfo_main():
    # parameters:
    n_moths = 50  
    max_iterations = 1000  
    num_runs = 10  
    dim = 2  # Dimensions

    # Get the benchmark functions from the funcs module