import uproot
import argparse
import numpy as np
import yaml
import pandas as pd

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process a ROOT file based on given selections and variables.')
parser.add_argument('--file', '-f', type=str, required=True, help='The path to the ROOT file.')
parser.add_argument('--tree', '-t', type=str, required=True, help='The name of the TTree in the ROOT file.')
parser.add_argument('--selections_file', '-sf', type=str, required=True, help='The YAML file containing the selection criteria.')
parser.add_argument('--variable', '-v', type=str, nargs='+',required=True, help='The variable/s (leaf) to print for events passing the selections.')

args = parser.parse_args()

# Load selections from the YAML file
with open(args.selections_file, 'r') as file:
    selections_config = yaml.safe_load(file)
    selections = selections_config.get('selections', [])

# Open the .root file
with uproot.open(args.file) as file:
    # Access the TTree
    tree = file[args.tree]

    # Process selections
    selection_mask = np.ones(len(tree), dtype=bool)  # Start with a mask that selects everything
    for selection in selections:
        and_conditions = selection.split('&')
        and_mask = np.ones(len(tree), dtype=bool)
        for condition in and_conditions:
            or_conditions = condition.split('|')
            or_mask = np.zeros(len(tree), dtype=bool)
            for or_condition in or_conditions:
                variable, operation, value = or_condition.split(',')
                value = float(value)  # Assuming numerical comparisons; adjust as needed
                array = tree[variable].array()

                if operation == '>':
                    or_mask |= array > value
                elif operation == '<':
                    or_mask |= array < value
                elif operation == '>=':
                    or_mask |= array >= value
                elif operation == '<=':
                    or_mask |= array <= value
                elif operation == '==':
                    or_mask |= array == value
                else:
                    raise ValueError("Unsupported operation: {}".format(operation))
            
            and_mask &= or_mask
        
        selection_mask &= and_mask

    dataset = pd.DataFrame()
    for leaf in args.variable:
        dataset[leaf] = tree[leaf].array()[selection_mask]

    print(dataset.head())


