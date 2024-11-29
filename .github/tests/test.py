# Imports
import re
from pathlib import Path

# Variables
from config import Verbose

# Constants
from config import ERROR_MISSING_TAXCO

# Functions
from files.markdown_utils import extract_values, generate_tags
from files.links import update_dynamic_links

# Variables only in this file
Successful_test_files = [] # Track which files where successful in testing
Failed_test_files = [] # Track which files failed in testing

"""
Runs the functions to test the pipeline
Args:
    test_dir (str): Test directory with the test case files.
"""
def run_test_cases(test_dir):
    for file_path in Path(test_dir).rglob('*.md'):
        if Verbose: print(f"Testing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract existing tags and taxonomie
        existing_tags = extract_values(content, 'tags')
        taxonomie = extract_values(content, 'taxonomie')
        tags, errors = generate_tags(taxonomie, file_path, existing_tags)

        fill_test_lists(errors, file_path, taxonomie, tags)
    return validate_test();  


"""
Fills the files of Failed_test_files and Successful_test_files after getting all the information from the files
"""
def fill_test_lists(errors, file_path, taxonomie, tags):
    if errors:
        if(ERROR_MISSING_TAXCO in errors): 
            Failed_test_files.append(create_test_file_result(file_path, taxonomie, tags, errors))
        elif any("Taxonomie use where it is not need" in error for error in errors):
            Failed_test_files.append(create_test_file_result(file_path, taxonomie, tags, errors))
        else: 
            Failed_test_files.append(create_test_file_result(file_path, taxonomie, tags, errors))
        if Verbose: print(f"Failed to parse file: {file_path}")
    else:
        Successful_test_files.append(create_test_file_result(file_path, taxonomie, tags, errors))


"""
Validates the test cases against the expected outcome
"""
def validate_test():
    from tests.expected_result_taxco_tests import Expected_failed_test_files, Expected_successful_test_files
    if Verbose: 
        print(f"Succesful test files: {check_files_set_equal(Successful_test_files, Expected_successful_test_files)}")
        print(f"Failed test files: {check_files_set_equal(Failed_test_files, Expected_failed_test_files)}")
    return check_files_set_equal(Successful_test_files, Expected_successful_test_files) and check_files_set_equal(Failed_test_files, Expected_failed_test_files)


"""
Tests the file with incorrect links. This check makes sure inccorrect links get noticed and "content/" gets filtered out.
"""
def test_link_file(test_dir):
    yaml_pattern = re.compile(r"^---\s*([\s\S]*?)\s*---", re.MULTILINE)
    for file_path in Path(test_dir).rglob("*.md"): 
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = yaml_pattern.match(content)
            if match:
                front_matter = match.group(1) 
                if "linktest" in front_matter:
                    content, errors = update_dynamic_links(file_path, content)
                    error_first_link = "Invalid dynamic link: `[[foutieveLinkEen]]`"
                    error_second_link = "Invalid dynamic link: `[[foutieveLinkTwee]]`"
                    if error_first_link in errors and error_second_link in errors:
                        return True
    return False     
    
"""
Checks if the expected output is the same as the result from the pipeline
Args:
    actual_unsorted (str): Unsorted list of the output of the pipeline
    expected_unsorted (str): Unsorted list of the expected output
"""
def check_files_set_equal(actual_unsorted, expected_unsorted):
    normalized_expected = normalize_list(expected_unsorted)
    normalized_actual = normalize_list(actual_unsorted)

    # Compare
    if normalized_expected == normalized_actual:
        if Verbose: print("The lists contain the same information.")
        return True
    else:
        if Verbose: print("The lists are different.")
        return False

"""
Normalizes a list to be able to match it against another list
Args:
    data (list) : list of either successful or failed files (expected or actual)
"""
def normalize_list(data):
    normalized_data = []
    for obj in data:
        normalized_obj = obj.copy()
        for key in ['tags', 'taxonomie', 'tags']:
            if key in obj:
                normalized_obj[key] = '<br>'.join(sorted(obj[key].split('<br>')))
        normalized_data.append(normalized_obj)
    return sorted(normalized_data, key=lambda x: x.get('file', ''))


"""
Create a list of a file for test cases
"""
def create_test_file_result(file_path, taxonomie, tags, errors):
    return {
        "file": file_path.stem,
        "taxonomie": '<br>'.join(taxonomie) if taxonomie else "N/A",
        "tags": '<br>'.join(tags) if tags else "N/A",
        "errors": '<br>'.join(errors) if errors else "N/A"
    }

