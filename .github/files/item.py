# Imports
import re
from pathlib import Path

# Variables
from utils import Failed_files, Verbose, Dataset, Rapport_2

# Constants
from utils import PROCES_COL, PROCESSTAP_COL, TC3_COL, TC2_COL, NOT_NECESSARY, ERROR_MISSING_TAXCO

# Functions
from report.table import generate_markdown_table
from report.update import update_rapport1_data, update_rapport2_data


# Variables used only in this file
Taxonomie_pattern = r'^[a-z]{2}-\d{1,3}\.[123]\.[^\s\.]+(\.[^\s\.]+)*\.(?:OI|DT|PI|LT)$' # Taxonomie pattern


"""
Create a file report based on the status, file path, taxonomie, and tags.
Args:
    status (str): Status of the file processing.
    file_path (str): Path to the file.
    taxonomie (list): List of taxonomie values.
    tags (list): List of tags.
Returns:
    file_report (dict): File report dictionary.
"""
def create_file_report(status, file_path, src_dir, taxonomie, tags, errors):
    return {
        "status": status,
        "file": file_path.stem,
        "path": str(file_path.relative_to(src_dir)),
        "taxonomie": '<br>'.join(taxonomie) if taxonomie else "N/A",
        "tags": '<br>'.join(tags) if tags else "N/A",
        "errors": '<br>'.join(errors) if errors else "N/A"
    }

"""
Format the success or failed report table.
Args:
    file_report (list): List of file reports.
Returns:
    table (str): Markdown table string.
"""
def format_file_report_table(file_report):
    headers = ["Status", "File", "Path", "Taxonomie", "Tags"]

    if file_report == Failed_files: headers.append("Errors")
    rows = [[
        file['status'], 
        file['file'], 
        file['path'], 
        file['taxonomie'], 
        file['tags'],
        file['errors']
    ] for file in file_report]

    table = generate_markdown_table(headers, rows)
    return table

"""
Generate tags based on the taxonomie values
Args:
    taxonomies (list): List of taxonomie values.
    file_path (str): Path to the file.
Returns:
    tags (list): List of tags generated from the taxonomie values.
"""
def generate_tags(taxonomies, file_path, existing_tags):
    tags = []
    errors = []
    combined_tags = []
    taxonomie_tags = []
    if taxonomies is not None and taxonomies != ['None']:
        for taxonomie in taxonomies:
            if Verbose : print(f"Generating tags for taxonomie: {taxonomie}")
            # Check if the taxonomie is in the correct format
            if not re.match(Taxonomie_pattern, taxonomie):
                errors.append(f"Invalid taxonomie: {taxonomie}")
                if Verbose: print(f"Invalid taxonomie: {taxonomie}")
                continue

            # split the taxonomie in it's different parts
            tc_1, tc_2, tc_3, tc_4 = split_taxonomie(taxonomie)
            # if the parts are all valid
            if tc_1 and tc_2 and tc_3 and tc_4:
                # Loop trough every row in the dataset
                for row in Dataset[1:]:
                    # Check if the first part of the taxonomie is equal to the second column (TC1) in the dataset
                    if row[1] == tc_1:
                        # Check if the second part of the taxonomie is equal to the third column (TC2) in the dataset
                        if row[5] in Rapport_2 and row[5] == tc_3:
                            # Adds the taxonomie
                            new_tag = "HBO-i/niveau-" + tc_2
                            if new_tag not in tags:
                                tags.append(new_tag)
    
                            # Adds the proces
                            if row[PROCES_COL] not in tags:
                                tags.append(row[PROCES_COL])

                            # Adds the processtap
                            if row[PROCESSTAP_COL] not in tags:
                                tags.append(row[PROCESSTAP_COL])

                            # Check if the third part of the taxonomie is in the lookup table
                            if row[TC3_COL] not in tags:
                                tags.append(row[TC3_COL])

                            # Check if the taxonomie is not needed
                            splitted_row2 =  row[TC2_COL].split(',')
                            if splitted_row2[int(tc_2)-1] == "X": 
                               tags.append(NOT_NECESSARY)    

                            # Sort the tags so that the HBO-i tags are first
                            tags.sort(key=lambda x: x.startswith('HBO-i'), reverse=True)
                            
                            update_rapport1_data(tc_1, tc_2)
                            update_rapport2_data(get_file_type(file_path), tc_1, tc_2, tc_3)   
                            taxonomie_tags = sorted(list(set(taxonomies)))

        # If no tags were found, add an error
            if NOT_NECESSARY in tags: 
                tags.remove(NOT_NECESSARY)
                errors.append(f"Taxonomie used where it is not needed: {taxonomie}")
            if tags == [] and not errors:
                    errors.append(f"Taxonomie not found in dataset: {taxonomie}")
                    if Verbose: print(f"Taxonomie not found in dataset: {taxonomie}")

    else:
        errors.append(ERROR_MISSING_TAXCO)
        if Verbose: print(ERROR_MISSING_TAXCO)

    if existing_tags: combined_tags += existing_tags 
    if tags : combined_tags += tags 
    if taxonomie_tags : combined_tags += taxonomie_tags

    return list(dict.fromkeys(combined_tags)), errors

"""
Returns the folder name after the 'content' directory in the path.
Args:
    file_path (str): Path to the file.
Returns:
    folder_name (str): Folder name after the 'content' directory.
"""
def get_file_type(file_path):
    # Convert to Path object if not already
    file_path = Path(file_path)
    
    # Find the 'content' directory in the path
    parts = file_path.parts
    if 'content' in parts:
        content_index = parts.index('content')
        # Return the first folder after 'content' without leading number and space
        if content_index + 1 < len(parts):
            folder_name = parts[content_index + 1]
            # Remove leading number and space
            cleaned_folder_name = re.sub(r'^\d+\.\s*', '', folder_name)
            return cleaned_folder_name
    
    return None

"""
Split the taxonomie value into a list of individual taxonomie parts.
Args:
    taxonomie (str): Taxonomie value to split.
Returns:
    parts (list): List of taxonomie parts.
"""
def split_taxonomie(taxonomie):
    return taxonomie.split('.')


"""
Helper function to extract values from the content of a markdown file.
Args:
    content (str): Content of the markdown file.
    field_name (str): Field name to extract values for.
Returns:
    values (list): List of values extracted from the content.
"""
def extract_values(content, field_name):
    lines = content.splitlines()
    values = []

    for i, line in enumerate(lines):
        if line.startswith(f'{field_name}:'):
            # Handle case where the field has a single value
            if ':' in line and len(line.split(':', 1)[1].strip()) > 0:
                values.append(line.split(':', 1)[1].strip())
            else:
                # Handle case where the field is a list
                for j in range(i + 1, len(lines)):
                    sub_line = lines[j].strip()
                    if sub_line.startswith('- '):
                        values.append(sub_line.lstrip('- ').strip())
                    else:
                        break
            break

    return values if values else None
