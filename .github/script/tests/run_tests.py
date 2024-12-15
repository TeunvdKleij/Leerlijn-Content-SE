# Imports
import re
from pathlib import Path
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#variables
from config import failedFiles

# Functions
from files.images import fillFailedImages
from report.generate import generateReport
from files.parse import parseMarkdownFiles, parseDatasetFile
from tests.evaluate import evaluate_tests
from report.populate import populateRapport1, populateRapport2

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
    
def validate_draft():
    expectedAmountOfDraftFiles = len(failedFiles)
    actualAmountOfDraftFiles = 0
    for file in failedFiles:
        fullPath = "./.github/script/tests/test_cases_build/" + file['path']
        try:
            with open(fullPath, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip().startswith('draft:'):
                        draft_value = line.strip().split(':', 1)[1].strip().lower()
                        if draft_value == 'true':
                            actualAmountOfDraftFiles += 1
        except FileNotFoundError:
            print(f"Error: The file at '{fullPath}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    return expectedAmountOfDraftFiles == actualAmountOfDraftFiles

"""
Runs the tests for the pipeline
"""
def test():
    global SRC_DIR, DEST_DIR, REPORT_PATH, DATASET

    SRC_DIR = Path(__file__).resolve().parents[0] / 'test_cases'
    DEST_DIR = Path(__file__).resolve().parents[0] / 'test_cases_build'
    DATASET = Path(__file__).resolve().parents[2] / 'datasets/test_dataset.xlsx'
    REPORT_PATH = "./.github/script/report/actual_test_report.md"

    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
        os.mkdir(DEST_DIR)

    parseDatasetFile(DATASET)
    populateRapport1()
    populateRapport2()

    parseMarkdownFiles(SRC_DIR, DEST_DIR) 
    
    fillFailedImages(SRC_DIR, DEST_DIR) 
    generateReport(REPORT_PATH) 

    if validate_test_report():
        print("Test report validation successful")
        if evaluate_tests():
            print("Test evaluation successful")
            if(validate_draft()):
                print("Draft test successful")
                sys.exit(0)
            else:
                print("Draft test failed")
                sys.exit(1)
        else : 
            print("Test evaluation failed")
            sys.exit(1)  
    else : 
        print("Test report validation failed")
        sys.exit(1)

if __name__ == "__main__":
    test()
    
