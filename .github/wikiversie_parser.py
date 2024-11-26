import os
import time
import shutil
import argparse
import sys
from pathlib import Path

from files.parse import parse_dataset_file, parse_markdown_files

from report.populate import populate_rapport1, populate_rapport2, populate_image_report
from report.generate import generate_report

from tests.test import run_test_cases, test_link_file
from tests.evaluate import evaluate_tests

"""
Main entry point of the script.
"""
def main():
    global Verbose
    global Testing

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Update markdown files with taxonomie tags and generate reports.")
    parser.add_argument("--src", required=True, help="Source directory containing markdown files.")
    parser.add_argument("--dest", required=True, help="Destination directory to save updated markdown files and reports.")
    parser.add_argument("--dataset", required=True, help="Path to the dataset file (XLSX file).")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output.")
    parser.add_argument("--testing", action="store_true", help="Determines if it should only check testcases")
    parser.add_argument("--testdir", required=False, help="The directory where the tests are located")

    args = parser.parse_args()
    src_dir = Path(args.src).resolve()
    dest_dir = Path(args.dest).resolve()
    Verbose = args.verbose
    Testing = args.testing
    if args.testdir != None:
        test_dir = Path(args.testdir).resolve() 

    
    # Fill the reports with the dataset information
    parse_dataset_file(args.dataset)

    populate_rapport1() 
    populate_rapport2() 

    if Testing :
        if run_test_cases(test_dir) :
            if Verbose : print("Test cases successful")
            if test_link_file(test_dir): 
                if Verbose : print("Test links successful")
                if evaluate_tests(src_dir, dest_dir):
                    if Verbose : print("Test evaluation successful")
                    sys.exit(0)
                else : sys.exit(1)  
            else : 
                if Verbose : print("Changing of dynamic links tests: Failed")
                sys.exit(1)
        else : 
            if Verbose : print("Markdown tests: Failed")
            sys.exit(1)    
    else :
        # Delete everything in the destination folder
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
            os.mkdir(dest_dir)

        # Parse the markdown files in the source directory
        parse_markdown_files(src_dir, dest_dir) 
        populate_image_report(src_dir, dest_dir) 

        generate_report() ##report/generate

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
