import numpy as np
import itertools
import matplotlib.pyplot as plt
from docplex.mp.model import Model

# Generate randomized node set
rnd = np.random
rnd.seed(33)
n = 10
N = [i for i in range(0, n)]
loc_x = rnd.rand(len(N))*200
loc_y = rnd.rand(len(N))*100

# Plot node set
plt.scatter(loc_x[1:], loc_y[1:], c='b')
for i in N:
    plt.annotate(i, (loc_x[i]+2, loc_y[i]))
plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
plt.axis('equal')

# Generating set A containing all arcs (edges) Aij between each node i and j in the graph
#      and set C containing the cost Cij between each node i and j in the graph
A = [(i, j) for i in N for j in N if i != j]
c = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i, j in A}

#Solve with DOcPlex
mdl = Model('TSP')
x = mdl.binary_var_dict(A, name='x')
mdl.minimize(mdl.sum(c[i, j]*x[i, j] for i, j in A))
mdl.add_constraints(mdl.sum(x[i, j] for j in N if j != i) == 1 for i in N)
mdl.add_constraints(mdl.sum(x[i, j] for i in N if i != j) == 1 for j in N)
subtours = []
for i in range(2,n):
    subtours += itertools.combinations(range(1,n), i)
mdl.add_constraints(mdl.sum(x[i,j] if i!=j else 0 for i,j in itertools.permutations(s,2) ) <= len(s) - 1 for s in subtours)
mdl.parameters.timelimit = 15
solution = mdl.solve(log_output=True)
mdl.parameters.timelimit = 15
solution = mdl.solve(log_output=True)

# Print active arcs (Aij = 1)
print(solution)

#Solution Visualization 
active_arcs = [a for a in A if x[a].solution_value > 0.9]
plt.scatter(loc_x[1:], loc_y[1:], c='b')
for i in N:
    plt.annotate(i, (loc_x[i]+2, loc_y[i]))
for i, j in active_arcs:
    plt.plot([loc_x[i], loc_x[j]], [loc_y[i], loc_y[j]], c='g', alpha=0.3)
plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
plt.axis('equal')
