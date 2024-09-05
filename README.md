Moth-Flame Optimization Algorithm (MFO)
Moth Flame Optimization (MFO) is particularly interesting as it is a bio-inspired algorithm based on the way moths navigate. This algorithm was proposed by Seyed Ali Mirjalili as an article named Moth-flame optimization algorithm: A novel nature-inspired heuristic paradigm in Knowledge-Based Systems journal back in 2015. 
MFO makes use of the special phototactic movement of moths, which allows them to navigate by maintaining a constant angle in relation to moonlight. This movement can be used to optimize difficult tasks.

Explanation of MFO algorithm:
 The position of the moths in the space is thought to be one of the problem's variables, and moths represent the possible solutions. As a result, by altering their position vectors, the moths can fly in 1-D, 2-D, 3-D, or hyper-dimensional space.
 The set of moths is represented in a matrix M_nd
where, n: no. of moths 
           d: no. of dimension
 there is also another array for each moth, where n is the number of moths, that stores the relevant fitness values
 Flames and moths are also solutions but techniques of approaching and updating each cycle are different where flames are the moth's best-calculated position, but moths are the real search agents that travel through the search space and flames are the flags or pins that moths drop while they search the search field. 
 At each iteration, the positions of the flames are updated by comparing the fitness values of the current moths. If a moth finds a better solution than its corresponding flame, the flame is updated to the new position. Therefore, the flames represent the most promising areas of the search space found by the moths up to that point.
 The movement of each moth towards a flame is modeled using a spiral equation, inspired by the real-world behavior of moths flying in a logarithmic spiral around light sources. This spiral movement allows the moths to balance exploration.
 he mathematical formulation of the moth’s movement towards the flame
                    x_(ij )= d_ij.e^(b.t).cos(t.2?) +y_j
Where:
     x_(ij ): the new position of the moth
  d_ij: the distance between the moth and the flame
  b: constant defining the shape of the logarithmic spiral.
  t: random number between [-1,1], which controls the   movement direction.
  y_j: the position of the flame.
This formula ensures that moths do not move directly toward the flames but instead follow a spiral path around them.
  As the algorithm progresses, the number of flames reduces linearly. This forces the moths to converge towards the best solutions as the search narrows down.
The reduction in the number of flames is governed by the equation
                N_f=round (N_f-l*N_f/max?iterations )
Where,
       N_f: the current number of flames.
        l : the total number of iterations. 
 Early stopping conditions:
The MFO algorithm continues the iterative process of evaluating fitness, updating flames, and moving moths until a stopping criterion is met including reaching a maximum number of iterations or when there is no significant improvement in the best solution. A small threshold value is set to define the minimum improvement needed for the algorithm to continue. If the improvement is smaller than this threshold for a specified number of iterations (in our code = 20), the algorithm stops early to save computational resources. This mechanism helps in speeding up the optimization process by avoiding unnecessary iterations when further improvements are unlikely.
Results and visualization of our code:
 Results:
 Best solution, best position and time taken for each run.
 Mean and standard deviation for all runs.
 Visualization:
 3D Plot of Benchmark Function and Best Positions.
 Moths Before and After Optimization.
 Animation of Moth Optimization Paths.
Application of MFO:
 Neural Network Training
 Antenna Design Optimization
 Economic Load Dispatch in Power Systems
 Robot Path Planning  








