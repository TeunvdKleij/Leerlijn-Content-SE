# Imports
import time
import os
import shutil
import sys
from pathlib import Path
import argparse

# Variables
from config import Verbose

# Functions
from files.parse import parse_markdown_files

Markdown_Count_Check = False  


"""
returns the amount of markdown files in a folder
"""
def check_markdown_files_count(folder_path):
    return len(list(folder_path.glob("*.md")))

"""
Evaluate the tests by using check_markdown_files_count and removing the build folder afterwards
"""
def evaluate_tests(src_dir, dest_dir):
    dest_dir = Path(dest_dir).resolve().parents[0] / 'temp_build'
    print(dest_dir)
    start_time = time.time()
    if os.path.exists(dest_dir):
        #
        shutil.rmtree(dest_dir)
        os.mkdir(dest_dir)
    # Parse the markdown files in the source directory
    parse_markdown_files(src_dir, dest_dir)

    Markdown_Count_Check = check_markdown_files_count(src_dir) == check_markdown_files_count(dest_dir)

    shutil.rmtree(dest_dir) 
    end_time = time.time()
    if Verbose: 
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        print("-----------")

    return Markdown_Count_Check   

