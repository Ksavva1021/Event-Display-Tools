# Running instructions:

## Process.py:
Intended to process a ROOT file (flat tree), apply a series of selections, and return some variables of interest for the corresponding surviving events.
- --file: Path to the ROOT file
- --tree: Name of the TTree
- --selections_file: Path to the YAML file containing the selections (Look at example)
- --variable: Variables of interest

## Finder.py:
Intended to figure out in which file within a dataset for a given run number, an event number resides in. Utilises dasgoclient to retrieve the list of files that hold events with a given run number. Then edmFileUtil is used to dump the contents and a lookup for the event number begins.
- --dataset: Dataset to query on DAS
- --run: Run number to filter
- --event: Event number to find
