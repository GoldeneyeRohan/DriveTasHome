import sys, os
import networkx as nx
import numpy as np
import annealed_penguins.utils as utils

def input_to_graph(input_file):
	data = utils.read_file(input_file)
	n_locations = int(data[0][0])
	n_homes = int(data[1][0])
	location_names = data[2]
	home_names = data[3]
	starting_location = data[4][0]

	adjacency = np.array(data[5:])
	adjacency[adjacency == "x"] = "0"
	adjacency = adjacency.astype(float)

	graph = nx.from_numpy_matrix(adjacency)
	location_names_array = np.array(location_names, dtype=str)
	s = np.argwhere(location_names_array == starting_location)[0][0]
	homes = [np.argwhere(location_names_array == home)[0][0] for home in home_names]

	problem = {"G":graph, "homes":homes, "s":s, "location_names": location_names}
	return problem

'''
- space separated list of route (start and end with starting node)
- number of dropoff locations
- list of drop off location homes of tas dropped off there
'''
def graph_to_output(problem, solution, output_file):
	"""
	problem is defined in spec
	solution is defined in spec
	output file is string name of output
	"""
	# homes = np.array(problem["homes"])
	dropoffs = solution["dropoffs"]
	# dropoff_locations = set(dropoffs)
	# dropoff_mapping = {loc : homes[dropoffs == loc] for loc in dropoff_locations}
	convertToFile(solution["path"], dropoffs, output_file, problem["location_names"])



"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)
