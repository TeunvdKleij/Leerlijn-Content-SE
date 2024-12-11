import os
import time
import shutil
import argparse
from pathlib import Path


from config import DEST_DIR, SRC_DIR, REPORT_PATH, DATASET

from files.parse import parse_dataset_file, parse_markdown_files
from files.images import fill_failed_images
from report.populate import populate_rapport1, populate_rapport2
from report.generate import generate_report

"""
Main entry point of the script.
"""
def main():
    if not os.path.exists(DATASET):
        print(f"Dataset file {DATASET} not found.")
        exit(404) 

    parse_dataset_file(DATASET)

    populate_rapport1() 
    populate_rapport2() 

    if not os.path.exists(SRC_DIR):
        print(f"Source directory {SRC_DIR} not found.")
        exit(404)

    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
        os.mkdir(DEST_DIR)

    parse_markdown_files(SRC_DIR, DEST_DIR) 
    fill_failed_images(SRC_DIR, DEST_DIR) 
    generate_report(REPORT_PATH) 

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
