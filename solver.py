import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse

import annealed_penguins.utils as utils
import annealed_penguins.problem_parser as prob_parser
import annealed_penguins.annealing as annealing
from annealed_penguins.student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(problem, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    G = problem["G"]
    homes = problem["homes"]
    start = problem["s"]
    T_map = {50:100,100:500,200:1500}
    L = len(problem["location_names"])
    ts = np.array(list(T_map.keys()))
    key = ts[np.where(ts >= L)[0][0]]


    init_path = annealing.inital_candidate(G, homes, start)
    D = nx.floyd_warshall_numpy(G)
    for i in range(3):
        solution, intermediate_cost, init_cost = annealing.simulated_annealing(G, homes, start, init_path, D, T=T_map[key], epochs=10, propose_candidate=annealing.propose_candidate_order);
        solution, final_cost, intermediate_cost_dummy = annealing.simulated_annealing(G, homes, start, solution, D, T=T_map[key], epochs=10, propose_candidate=annealing.propose_candidate_neighbor)
    for i in range(3):
        solution, intermediate_cost, init_cost = annealing.simulated_annealing(G, homes, start, init_path, D, T=i * 100, epochs=10, propose_candidate=annealing.propose_candidate_order);
        solution, final_cost, intermediate_cost_dummy = annealing.simulated_annealing(G, homes, start, solution, D, T=i * 100, epochs=10, propose_candidate=annealing.propose_candidate_neighbor)
    print("init cost:", init_cost, "intermediate_cost:", intermediate_cost, "final_cost", final_cost)
    trajectory = annealing.solution_to_trajectory(solution, G)
    return trajectory



def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    problem = prob_parser.input_to_graph(input_file)
    solution = solve(problem, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)
    prob_parser.graph_to_output(problem, solution, output_file)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
