import sys, os
import networkx as nx
import numpy as np
import utils

def input_to_graph(input_file):
	data = read_file(input_file)
	n_locations = int(data[0][0])
	n_homes = int(data[1][0])
	location_names = data[2]
	home_names = data[3]
	starting_location = data[4][0]

	adjacency = np.array(data[5:])
	adjacency[adjacency == "x"] = "0"
	adjacency = adjacency.astype(float)

	graph = nx.from_numpy_matrix(adjacency)
	
	# instance = {"G":graph, "locations":location_names,
	#  "home_names":home_names, "start":starting_location}

	

	return problem

def graph_to_output(problem, solution, output_file):
	"""
	problem is defined in spec
	solution is defined in spec
	output file is string name of output
	"""

	return None


