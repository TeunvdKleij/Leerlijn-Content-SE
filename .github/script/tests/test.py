# Imports
import re
from pathlib import Path
import shutil
import os
import sys

# Variables
from config import VERBOSE

# Functions
from files.images import fill_failed_images
from report.generate import generate_report
from files.parse import parse_markdown_files
from tests.evaluate import evaluate_tests

def validate_test_report():
    expected_test_report_path =  Path(__file__).resolve().parents[1] / 'report/expected_test_report.md'
    actual_test_report_path = Path(__file__).resolve().parents[1] / 'report/actual_test_report.md'
    with open(expected_test_report_path, 'r') as f1, open(actual_test_report_path, 'r') as f2:
        expected_test_report_content = f1.read()
        actual_test_report_content = f2.read()

    if expected_test_report_content == actual_test_report_content:
        return True
    else:
        return False

"""
Runs the tests for the pipeline
"""
def test():
    src_dir = Path(__file__).resolve().parents[0] / 'test_cases'
    dest_dir = Path(__file__).resolve().parents[0] / 'test_cases_build'
    report_file = ".github/report/actual_test_report.md"

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        os.mkdir(dest_dir)

    parse_markdown_files(src_dir, dest_dir) 
    
    fill_failed_images(src_dir, dest_dir) 
    generate_report(report_file) 

    
    if validate_test_report():
        if VERBOSE: print("Test report validation successful")
        if evaluate_tests():
            if VERBOSE: print("Test evaluation successful")
            sys.exit(0)
        else : 
            if VERBOSE: print("Test evaluation failed")
            sys.exit(1)  
    else : 
        if VERBOSE: print("Test report validation failed")
        sys.exit(1)  
    
