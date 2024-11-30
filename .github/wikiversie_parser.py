import os
import time
import shutil
import argparse
import sys
from pathlib import Path


from config import Testing

from files.parse import parse_dataset_file, parse_markdown_files
from files.images import fill_failed_images
from report.populate import populate_rapport1, populate_rapport2
from report.generate import generate_report

"""
Main entry point of the script.
"""
def main():
    global Verbose
    global Testing

    parser = argparse.ArgumentParser(description="Update markdown files with taxonomie tags and generate reports.")
    parser.add_argument("--src", required=True, help="Source directory containing markdown files.")
    parser.add_argument("--dest", required=True, help="Destination directory to save updated markdown files and reports.")
    parser.add_argument("--dataset", required=True, help="Path to the dataset file (XLSX file).")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output.")
    parser.add_argument("--testing", action="store_true", help="Determines if it should only check testcases")

    args = parser.parse_args()
    src_dir = Path(args.src).resolve()
    dest_dir = Path(args.dest).resolve()
    Verbose = args.verbose
    Testing = args.testing
    
    parse_dataset_file(args.dataset)

    populate_rapport1() 
    populate_rapport2() 

    if Testing :
        from tests.test import test
        test()

    else: 
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
            os.mkdir(dest_dir)

        parse_markdown_files(src_dir, dest_dir) 
        fill_failed_images(src_dir, dest_dir) 
        generate_report("report.md") 




if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
