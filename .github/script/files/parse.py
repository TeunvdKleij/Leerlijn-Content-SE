# Imports
import csv
from pathlib import Path
import pandas as pd

# Variables
from config import failedFiles, parsedFiles, WIPFiles, dataset

# Constants
from config import ERROR_MISSING_TAXCO, FAIL_CROSS, NOT_NEEDED, WARNING, SUCCESS, TODO_ITEMS, IGNORE_FOLDERS, VERBOSE, ERROR_TAXCO_NOT_NEEDED, ERROR_WIP_FOUND

# Functions
from files.images import copyImages
from files.links import updateDynamicLinks
from files.markdown_utils import extractHeaderValues, generateTags, createFileReportRow, findWIPItems


# Parse the dataset file from a XLSX file to a list.
def parseDatasetFile(dataset_file):
    global dataset
    try:
        df = pd.read_excel(dataset_file)
        # if df.isnull().values.any():
        #     raise ValueError("Dataset contains empty rows or cells.")
        csv_data = df.to_csv(index=False, sep=';')
        reader = csv.reader(csv_data.splitlines(), delimiter=';', quotechar='|')
        dataset.extend(list(reader))
    except FileNotFoundError:
        print(f"File {dataset_file} not found.")
        exit(404)
    # except ValueError as ve:
    #     print(f"Error: {ve}")
    #     exit(2)
    except Exception as e:
        print(f"An error occurred while reading the dataset file: {e}")
        exit(404)

# Update markdown files in the source directory with taxonomie tags and generate reports.
def parseMarkdownFiles(SRC_DIR, DEST_DIR):
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
            print(f"Parsing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content, link_errors = updateDynamicLinks(file_path, content)
        image_errors = copyImages(content, srcDir, destDir)
        existing_tags = extractHeaderValues(content, 'tags')
        taxonomie = extractHeaderValues(content, 'taxonomie')
        new_tags, tags_errors = generateTags(taxonomie, file_path, existing_tags)
        difficulty = extractHeaderValues(content, 'difficulty')
        toDoItems = findWIPItems(content)

        if(toDoItems):
            errors.append(ERROR_WIP_FOUND + "<br>" + '<br>'.join([f"{item}" for item in toDoItems]))

        # Combine all errors
        errors = link_errors + image_errors + tags_errors + errors

        # If there are any errors, the file is considered a draft
        if(errors):
            isDraft = True

        # Don't include deprecated files in the report
        if("deprecated" not in str(file_path)):
            appendFileToSpecificList(errors, toDoItems, file_path, srcDir, taxonomie, new_tags)
        
        saveParsedFile(file_path, taxonomie, new_tags, difficulty, isDraft, content, dest_path)

# Fill the lists used for the report
def appendFileToSpecificList(errors, toDoItems, file_path, srcDir, taxonomie, tags):
    if errors:
        if(toDoItems):
            WIPFiles.append(createFileReportRow(TODO_ITEMS, file_path, srcDir, taxonomie, tags, errors))
        elif(ERROR_MISSING_TAXCO in errors): 
            failedFiles.append(createFileReportRow(FAIL_CROSS, file_path, srcDir, taxonomie, tags, errors))
        elif any(ERROR_TAXCO_NOT_NEEDED in error for error in errors):
            failedFiles.append(createFileReportRow(NOT_NEEDED, file_path, srcDir, taxonomie, tags, errors))
        else: 
            failedFiles.append(createFileReportRow(WARNING, file_path, srcDir, taxonomie, tags, errors))

        if VERBOSE: print(f"Failed to parse file: {file_path}")
    else:
        parsedFiles.append(createFileReportRow(SUCCESS, file_path, srcDir, taxonomie, tags, errors))

# Combines everything into a new file
def saveParsedFile(file_path, taxonomie, tags, difficulty, isDraft, content, dest_path):
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
