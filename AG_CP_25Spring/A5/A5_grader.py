import sys
import os
import subprocess

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utility_functions as uf