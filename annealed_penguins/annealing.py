import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pdb



def inital_candidate(G, homes, starting_node):
  init_path = [starting_node] + homes + [starting_node]
  return [homes, init_path]

def cost(homes, dropoff, D):
  taxi_cost = sum([2/3 * D[u,v] for u,v in list(zip(dropoff[:-1], dropoff[1:]))])
  return taxi_cost

def simulated_annealing(G, homes, start, inital_candidate, D, T=100000, epochs=10):
  t = T
  best_solution = inital_candidate
  best_solution_cost = cost(*inital_candidate, D)
  initial_cost = best_solution_cost
  while (t > 0):
    for epoch in range(epochs):
      candidate = propose_candidate(G, homes, best_solution)
      candidate_cost = cost(*candidate, D)
      cost_change = best_solution_cost - candidate_cost # we want to accept lower cost
      if (cost_change > 0):
        # move to candidate state
        best_solution = candidate
        best_solution_cost = candidate_cost
      elif (np.e ** (cost_change / t) > np.random.uniform()):
        # move to candidate state
        best_solution = candidate
        best_solution_cost = candidate_cost
    t -= 1
  return best_solution, best_solution_cost, initial_cost



def propose_candidate(G, homes, best_solution):
  homes, dropoff = best_solution
  i = np.random.randint(1, len(dropoff)-1)  # index along the path
  length = np.random.randint(1, len(dropoff)- i) # some random chuck starting from i

  reversed_section = list(reversed(dropoff[i:i+length]))


  dropoff = (dropoff[:i] +  
          reversed_section + 
          dropoff[i + length:]
          )

  new_path = []
  for i in range(0, len(dropoff)-1): 
    if dropoff[i] != dropoff[i + 1]:
      new_path += [dropoff[i]]
  new_path += [dropoff[-1]]

  return [homes, new_path]

def solution_to_trajectory(solution, G):
	shortest_paths_dict = dict(nx.all_pairs_shortest_path(G, cutoff=None))
	homes = solution[0]
	path = solution[1]
	#pdb.set_trace()
	trajectory_path = [] 
	for i in range(len(path) - 1):
		trajectory_path += shortest_paths_dict[path[i]][path[i + 1]][:-1]
	trajectory_path += [path[-1]]
	return {"path": trajectory_path, "dropoffs": homes}
