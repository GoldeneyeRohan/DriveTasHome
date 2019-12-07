import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pdb

def inital_candidate(G, homes, starting_node):
  s = starting_node
  init_path = [starting_node] + homes + [starting_node]
  init_droppoff = dict(list(zip(homes, [[h] for h in homes])))
  return [init_droppoff, init_path]

def cost(dropoff_dict, path, homes, D):
  taxi_cost = sum([2/3 * D[u,v] for u,v in list(zip(path[:-1], path[1:]))])
  ta_cost = sum([sum([D[k,v] for v in lst]) for k,lst in dropoff_dict.items()])
  return taxi_cost + ta_cost

def propose_candidate_order(G, best_solution):
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

def propose_candidate_neighbor(G, best_solution):
  dropoff_dict, path = best_solution
  i = np.random.randint(1, len(path) - 1)
  vtx = path[i]
  nbr = np.random.choice(list(G.neighbors(vtx)))
  if sum(np.array(path) == vtx) == 1:
  	if vtx in dropoff_dict and nbr not in dropoff_dict:
  		ta_homes = dropoff_dict.pop(vtx)
  		dropoff_dict[nbr] = ta_homes
  	if vtx in dropoff_dict and nbr in dropoff_dict:
  		ta_homes = dropoff_dict.pop(vtx)
  		dropoff_dict[nbr] = dropoff_dict[nbr] + ta_homes
  path[i] = nbr
  return [dropoff_dict, path]

def simulated_annealing(G, homes, start, inital_candidate, D, T=100000, epochs=10, propose_candidate=propose_candidate_order):
  t = T
  best_solution = [v.copy() for v in inital_candidate]
  best_solution_cost = cost(*inital_candidate, homes, D)
  initial_cost = best_solution_cost
  while (t > 0):
    for epoch in range(epochs):
      candidate = propose_candidate(G, best_solution)
      candidate_cost = cost(*candidate, homes, D)
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

  if initial_cost < best_solution_cost:
  	best_solution = inital_candidate
  	best_solution_cost = initial_cost

  return best_solution, best_solution_cost, initial_cost

def solution_to_trajectory(solution, G):
	shortest_paths_dict = dict(nx.all_pairs_shortest_path(G, cutoff=None))
	dropoff_dict = solution[0]
	path = solution[1]
	#pdb.set_trace()
	trajectory_path = []
	for i in range(len(path) - 1):
		trajectory_path += shortest_paths_dict[path[i]][path[i + 1]][:-1]
	trajectory_path += [path[-1]]
	return {"path": trajectory_path, "dropoffs": dropoff_dict}
