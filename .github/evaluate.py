import time
import os
import shutil
import sys
from pathlib import Path
import argparse
from wikiversie_parser import parse_markdown_files, populate_image_report, generate_report, Verbose

Markdown_Count_Check = False  

def check_markdown_files_count(folder_path):
    return len(list(folder_path.glob("*.md")))

def evaulate_tests(src_dir, dest_dir):
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

