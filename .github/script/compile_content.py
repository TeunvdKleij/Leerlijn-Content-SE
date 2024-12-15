import os
import time
import shutil

from config import DEST_DIR, SRC_DIR, TAXCO_REPORT_PATH, CONTENT_REPORT_PATH, DATASET

from files.parse import parseDatasetFile, parseMarkdownFiles
from files.images import fill_failed_images
from report.populate import populateRapport1, populateRapport2
from report.generateTaxcoReport import generateTaxcoReport
from report.generateContentReport import generateContentReport

"""
Main entry point of the script.
"""
def main():
    if not os.path.exists(DATASET):
        print(f"Dataset file {DATASET} not found.")
        exit(404) 

    parseDatasetFile(DATASET)

    populateRapport1() 
    populateRapport2() 

    if not os.path.exists(SRC_DIR):
        print(f"Source directory {SRC_DIR} not found.")
        exit(404)

    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
        os.mkdir(DEST_DIR)

    parseMarkdownFiles(SRC_DIR, DEST_DIR) 
    fill_failed_images(SRC_DIR, DEST_DIR) 
    generateTaxcoReport(TAXCO_REPORT_PATH)
    generateContentReport(CONTENT_REPORT_PATH)

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
