# Annealed Penguins
Authors: Ilian Herzi, Rohan Sinha
## CS 170 project api definition
### Problem Representation
problem_instance = {"G":graph, "homes":list_of_homes, "s":starting_node, "location_names":list_of_location_names}
where: 
 - graph = networkx graph
 - homes = list of ints
 - starting node = int

### Solution Representation
solution_instance = {"path":path_of_taxi, "dropoffs":list_of_dropoff}
where:
- path_of_taxi = list of ints
- list_of_dropoff = list of ints

### Notes:
TA i has home at vertex list_of_homes[i], and is dropped off at list_of_dropoff[i]
