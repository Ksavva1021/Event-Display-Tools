import uproot
import argparse
import numpy as np
import yaml
import pandas as pd

# ntuple->Draw("event","deepTauVsJets_loose_1>0.5 && deepTauVsJets_loose_2>0.5 && deepTauVsJets_loose_3>0.5 && deepTauVsJets_loose_4>0.5 && deepTauVsMu_vloose_1>0.5 && deepTauVsMu_vloose_2>0.5 && deepTauVsMu_vloose_3>0.5 && deepTauVsMu_vloose_4>0.5 && deepTauVsEle_vvloose_1>0.5 && deepTauVsEle_vvloose_2>0.5 && deepTauVsEle_vvloose_3>0.5 && deepTauVsEle_vvloose_4>0.5")

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
    selections = selections_config['selections']

# Open the .root file
with uproot.open(args.file) as file:
    # Access the TTree
    tree = file[args.tree]
    
    # Process selections
    selection_mask = np.ones(len(tree), dtype=bool)  # Start with a mask that selects everything
    for selection in selections:
        variable, operation, value = selection.split(',')
        value = float(value)  # Assuming numerical comparisons; adjust as needed
        array = tree[variable].array()
        
        if operation == '>':
            selection_mask &= array > value
        elif operation == '<':
            selection_mask &= array < value
        elif operation == '>=':
            selection_mask &= array >= value
        elif operation == '<=':
            selection_mask &= array <= value
        elif operation == '==':
            selection_mask &= array == value
        else:
            raise ValueError("Unsupported operation: {}".format(operation))
    
    dataset = pd.DataFrame()
    for leaf in args.variable:
        dataset[leaf] = tree[leaf].array()[selection_mask]
    
    print(dataset.head())


