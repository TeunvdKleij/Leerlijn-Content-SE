import os
import time
import shutil
import argparse
from pathlib import Path


from config import DEST_DIR, SRC_DIR, REPORT_PATH

from files.parse import parse_dataset_file, parse_markdown_files
from files.images import fill_failed_images
from report.populate import populate_rapport1, populate_rapport2
from report.generate import generate_report

"""
Main entry point of the script.
"""
def main():
    parser = argparse.ArgumentParser(description="Update markdown files with taxonomie tags and generate reports.")
    parser.add_argument("--dataset", required=True, help="Path to the dataset file (XLSX file).")
    parser.add_argument("--testing", action="store_true", help="Determines if it should only check testcases")
    args = parser.parse_args()

    if not os.path.exists(args.dataset):
        print(f"Dataset file {args.dataset} not found.")
        exit(404) 

    parse_dataset_file(args.dataset)

    populate_rapport1() 
    populate_rapport2() 

    if args.testing:
        from tests.test import test
        test()

    else: 
        if not os.path.exists(SRC_DIR):
            print(f"Source directory {SRC_DIR} not found.")
            exit(404)

        if os.path.exists(DEST_DIR):
            shutil.rmtree(DEST_DIR)
            os.mkdir(DEST_DIR)

        parse_markdown_files(SRC_DIR, DEST_DIR, args.testing) 
        fill_failed_images(SRC_DIR, DEST_DIR) 
        generate_report(REPORT_PATH) 

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
