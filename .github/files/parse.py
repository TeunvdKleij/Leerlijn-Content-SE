# Imports
import csv
from pathlib import Path
import pandas as pd # type: ignore

#Variables
from config import Verbose, Failed_files, Successful_files, WIP_files, Dataset, Testing

# Constants
from config import ERROR_MISSING_TAXCO, FAIL_CROSS, NOT_NEEDED, WARNING, SUCCESS, TODO_ITEMS

# Functions
from files.images import copy_images
from files.links import update_dynamic_links
from files.markdown_utils import extract_values, generate_tags, create_file_report, find_ToDo_items


"""
Parse the dataset file from a XLSX file to a list.

Args:
    dataset_file (str): Path to the dataset XLSX file.
"""
def parse_dataset_file(dataset_file):
    global Dataset
    try:
        df = pd.read_excel(dataset_file)
        csv_data = df.to_csv(index=False, sep=';')
        reader = csv.reader(csv_data.splitlines(), delimiter=';', quotechar='|')
        Dataset.extend(list(reader))
    except FileNotFoundError:
        print(f"File {dataset_file} not found.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading the dataset file: {e}")
        exit()

"""
Update markdown files in the source directory with taxonomie tags and generate reports.
Args:
    src_dir (str): Source directory containing markdown files.
    dest_dir (str): Destination directory to save updated markdown files and reports.
"""
def parse_markdown_files(src_dir, dest_dir):
    if Verbose: print("Parsing markdown files...")

    dest_dir.mkdir(parents=True, exist_ok=True)

    for file_path in Path(src_dir).rglob('*.md'):
        relative_path = file_path.relative_to(src_dir)
        dest_path = dest_dir / relative_path
        errors = []
        isDraft = False

        if "schrijfwijze" in str(file_path):
            continue

        if Verbose: 
            print("*" * 50) 
            if Testing: print(f"Testing parsing file: {file_path}")
            else : print(f"Parsing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content, link_errors = update_dynamic_links(file_path, content)
        image_errors = copy_images(content, src_dir, dest_dir)

        existing_tags = extract_values(content, 'tags')
        taxonomie = extract_values(content, 'taxonomie')
        new_tags, tags_errors = generate_tags(taxonomie, file_path, existing_tags)
        difficulty = extract_values(content, 'difficulty')
        toDoItems = find_ToDo_items(content)

        if(toDoItems):
            errors.append("To-Do item(s) found in the file:<br>" + '<br>'.join([f"{item}" for item in toDoItems]))

        errors = link_errors + image_errors + tags_errors + errors

        fill_lists(errors, toDoItems, file_path, src_dir, taxonomie, new_tags)
        create_new_file(file_path, taxonomie, new_tags, difficulty, isDraft, content, dest_path)


def fill_lists(errors, toDoItems, file_path, src_dir, taxonomie, tags):
    if errors:
        if(toDoItems):
            # isDraft = True
            WIP_files.append(create_file_report(TODO_ITEMS, file_path, src_dir, taxonomie, tags, errors))
        elif(ERROR_MISSING_TAXCO in errors): 
            # isDraft = True
            Failed_files.append(create_file_report(FAIL_CROSS, file_path, src_dir, taxonomie, tags, errors))
        elif any("Taxonomie used where it is not needed:" in error for error in errors):
            # isDraft = True
            Failed_files.append(create_file_report(NOT_NEEDED, file_path, src_dir, taxonomie, tags, errors))
        else: 
            # isDraft = True
            Failed_files.append(create_file_report(WARNING, file_path, src_dir, taxonomie, tags, errors))

        if Verbose: print(f"Failed to parse file: {file_path}")
    else:
        Successful_files.append(create_file_report(SUCCESS, file_path, src_dir, taxonomie, tags, errors))

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

    if Verbose:
        print(f"File completed: {file_path}")
        print("-" * 50)                