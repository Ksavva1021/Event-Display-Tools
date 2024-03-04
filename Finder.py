import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process dataset files to find in which file the event of interest lies.')
parser.add_argument('--dataset', '-d', type=str, required=True, help='Dataset to query')
parser.add_argument('--run', '-r', type=str, required=True, help='Run number to filter')
parser.add_argument('--event', '-ev', type=str, required=True, help='Event number to find')

args = parser.parse_args()

os.system('dasgoclient --query="file dataset={} run={}" &> files.txt'.format(args.dataset, args.run))

with open('files.txt', 'r') as file:
    for line in file:
        root_file = line.strip()
        os.system('edmFileUtil -d root://cmsxrootd.fnal.gov/{} -e &> file_info.txt'.format(root_file))
        with open('file_info.txt', 'r') as file_info:
            content = file_info.read()
        search_string = args.event
        if search_string in content:
            print('Event {} found in file: {}'.format(search_string,root_file))
            sys.exit()
        else:
            print('Event {} not found in file: {}'.format(search_string,root_file))
            continue