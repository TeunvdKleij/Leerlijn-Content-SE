# Imports
import csv
from pathlib import Path
import pandas as pd

# Variables
from config import failedFiles, parsedFiles, WIPFiles, dataset

# Constants
from config import ERROR_MISSING_TAXCO, FAIL_CROSS, NOT_NEEDED, WARNING, SUCCESS, TODO_ITEMS, DEST_DIR, SRC_DIR, IGNORE_FOLDERS, VERBOSE

# Functions
from files.images import copy_images
from files.links import update_dynamic_links
from files.markdown_utils import extract_values, generate_tags, create_file_report, find_ToDo_items


# Parse the dataset file from a XLSX file to a list.
def parse_dataset_file(dataset_file):
    global dataset
    try:
        df = pd.read_excel(dataset_file)
        csv_data = df.to_csv(index=False, sep=';')
        reader = csv.reader(csv_data.splitlines(), delimiter=';', quotechar='|')
        dataset.extend(list(reader))
    except FileNotFoundError:
        print(f"File {dataset_file} not found.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading the dataset file: {e}")
        exit()

# Update markdown files in the source directory with taxonomie tags and generate reports.
def parse_markdown_files(testing):
    if VERBOSE: print("Parsing markdown files...")

    destDir = Path(DEST_DIR).resolve()
    destDir.mkdir(parents=True, exist_ok=True)

    srcDir = Path(SRC_DIR).resolve()

    # Loop through all markdown files in the source directory
    for file_path in Path(srcDir).rglob('*.md'):
        relative_path = file_path.relative_to(srcDir)
        dest_path = destDir / relative_path
        errors = []
        isDraft = False

        # Skip curtain folders
        if any(folder in str(file_path) for folder in IGNORE_FOLDERS):
            continue

        if VERBOSE: 
            print("*" * 50) 
            if testing: print(f"Testing parsing file: {file_path}")
            else : print(f"Parsing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content, link_errors = update_dynamic_links(file_path, content)
        image_errors = copy_images(content, srcDir, destDir)

        existing_tags = extract_values(content, 'tags')
        taxonomie = extract_values(content, 'taxonomie')
        new_tags, tags_errors = generate_tags(taxonomie, file_path, existing_tags)
        difficulty = extract_values(content, 'difficulty')
        toDoItems = find_ToDo_items(content)

        if(toDoItems):
            errors.append("To-Do item(s) found in the file:<br>" + '<br>'.join([f"{item}" for item in toDoItems]))

        # Combine all errors
        errors = link_errors + image_errors + tags_errors + errors

        # If there are any errors, the file is considered a draft
        if(errors):
            isDraft = True

        # Don't include deprecated files in the report
        if("deprecated" not in str(file_path)):
            fill_lists(errors, toDoItems, file_path, srcDir, taxonomie, new_tags)
        
        create_new_file(file_path, taxonomie, new_tags, difficulty, isDraft, content, dest_path)

# Fill the lists used for the report
def fill_lists(errors, toDoItems, file_path, srcDir, taxonomie, tags):
    if errors:
        if(toDoItems):
            WIPFiles.append(create_file_report(TODO_ITEMS, file_path, srcDir, taxonomie, tags, errors))
        elif(ERROR_MISSING_TAXCO in errors): 
            failedFiles.append(create_file_report(FAIL_CROSS, file_path, srcDir, taxonomie, tags, errors))
        elif any("Taxonomie used where it is not needed:" in error for error in errors):
            failedFiles.append(create_file_report(NOT_NEEDED, file_path, srcDir, taxonomie, tags, errors))
        else: 
            failedFiles.append(create_file_report(WARNING, file_path, srcDir, taxonomie, tags, errors))

        if VERBOSE: print(f"Failed to parse file: {file_path}")
    else:
        parsedFiles.append(create_file_report(SUCCESS, file_path, srcDir, taxonomie, tags, errors))

# Combines everything into a new file
def create_new_file(file_path, taxonomie, tags, difficulty, isDraft, content, dest_path):
    new_content = (
        f"---\ntitle: {file_path.stem}\ntaxonomie: {taxonomie}\ntags:\n" +
        '\n'.join([f"- {tag}" for tag in tags]) +
        "\n"
    )

    if difficulty:
        new_content += "difficulty: " + ''.join([f"{level}" for level in difficulty]) + "\n"
        
    if isDraft:
        new_content += "draft: true \n"

    new_content += "---" + content.split('---', 2)[-1]

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    if VERBOSE:
        print(f"File completed: {file_path}")
        print("-" * 50)                