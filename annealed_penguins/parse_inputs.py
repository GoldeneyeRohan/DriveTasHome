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
	
	instance = {"G":graph, "locations":location_names,
	 "home_names":home_names, "start":starting_location}
	return instance


	problem_instance = {"G":graph, "homes":list_of_homes, "s":starting_node}
	graph = networkx graph, homes= list of ints, starting node = int

	solution_instance = {"path":path_of_taxi, "dropoffs":list_of_dropoff}
