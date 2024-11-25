import os
import re
import csv
import time
import shutil
import argparse
import sys
import json
from pathlib import Path
import pandas as pd # type: ignore

# Global variables
Dataset = list()  # Dataset list
Successful_files = [] # Track the status of each file
Failed_files = [] # Track the status of each file
Failed_images = [] # Track which images don't start with a 4C/ID component
Successful_test_files = [] # Track which files where successful in testing
Failed_test_files = [] # Track which files failed in testing
Verbose = False # Verbose output flag
Testing = False # Testing output flag
Taxonomie_pattern = r'^[a-z]{2}-\d{1,3}\.[123]\.[^\s\.]+(\.[^\s\.]+)*\.(?:OI|DT|PI|LT)$' # Taxonomie pattern
ValidDynamicLinkPrefixes = ['https://', 'http://', 'tags/'] # List of valid dynamic links

Rapport_1 = {} # Rapport 1 data
Rapport_2 = {} # Rapport 2 data

# Dataset columns
TC1_COL = 1
TC2_COL = 2
TC3_COL = 5
PROCES_COL = 3
PROCESSTAP_COL = 4
LT_COL = 7
OI_COL = 8
PI_COL = 9
DT_COL = 10

# 4CID
LT = "Leertaken"
OI = "Ondersteunende-informatie" 
PI = "Procedurele-informatie"
DT = "Deeltaken"

#Error message for not including any taxonomy code
ERROR_MISSING_TAXCO = "No taxonomie found in file."

# Icons
SUCCESS = "✅"
FAIL_CIRCLE = "⛔️"
FAIL_CROSS = "❌"
NOT_NECESSARY = "🏳️"
WRONG_TAXONOMY_CODE = "⚠️"
NOT_NEEDED = "🟠"

## Structure of Rapport_1
#
# Rapport_1 = {
#     'rv-8' : {
#         'Proces' : "Requirementanalyseproces"
#         'Processtap' : "Verzamelen requirements",
#         'TC2' : ['x', '~', 'x']
#     },
#     'pu-13' : {
#         'Proces' : "Pakketselectieproces"
#         'Processtap' : "Uitvoeren analyse",
#         'TC2' : ['x', 'x', 'x']
#     }
# }

## Structure of Rapport_2
#
# Rapport_2 = {
#     'functioneel-ontwerp' : {
#         'oo-15' : {
#             'TC2' : ['x', 'x', 'x'],
#             LT : ['x', 'x', 'x'],
#             OI : ['x', 'x', 'x'], 
#             PI : ['x', 'x', 'x'], 
#             DT : ['x', 'x', 'x']
#         },
#         'rs-10' : {
#             'TC2' : ['x', 'x', 'x'],
#             LT : ['x', 'x', 'x'],
#             OI : ['x', 'x', 'x'], 
#             PI : ['x', 'x', 'x'], 
#             DT : ['x', 'x', 'x']
#         },
#         'ra-9' : {
#             'TC2' : ['x', 'x', 'x'],
#             LT : ['x', 'x', 'x'],
#             OI : ['x', 'x', 'x'], 
#             PI : ['x', 'x', 'x'], 
#             DT : ['x', 'x', 'x']
#         }
#     },
#     "Technisch ontwerp": {
#         'oo-15' : {
#           'TC2' : ['x', 'x', 'x'],
#           LT : ['x', 'x', 'x'],
#           OI : ['x', 'x', 'x'], 
#           PI : ['x', 'x', 'x'], 
#           DT : ['x', 'x', 'x']
#       }
#    }
# }

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
        Dataset = list(reader)
    except FileNotFoundError:
        print(f"File {dataset_file} not found.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading the dataset file: {e}")
        exit()

"""
Fills the rapport 1 data with the data from the dataset
Every TC1 code is the unique identifier
"""
def populate_rapport1():
    global Rapport_1
    for row in Dataset[1:]:
        tc_1 = row[TC1_COL]
        tc_2 = row[TC2_COL]
        proces = row[PROCES_COL]
        processtap = row[PROCESSTAP_COL]

        if tc_1 not in Rapport_1: 
            splitted_tc2 = tc_2.split(',')

            Rapport_1[tc_1] = {
                "Proces" : proces,
                "Processtap" : processtap,
                'TC2': [NOT_NECESSARY if splitted_tc2[0] == 'X' else 'x', NOT_NECESSARY if splitted_tc2[1] == 'X' else 'x', NOT_NECESSARY if splitted_tc2[2] == 'X' else 'x']        
            }

"""
Fills the Rapport 2 data with the data from the dataset.
Every unique TC3 and TC1 combination will be added to the Rapport 2 data.
"""
def populate_rapport2():
    global Rapport_2

    for row in Dataset[1:]:
        tc_1 = row[TC1_COL]
        tc_2 = row[TC2_COL]
        tc_3 = row[TC3_COL]
        lt = row[LT_COL]
        oi = row[OI_COL]
        pi = row[PI_COL]
        dt = row[DT_COL]

        if tc_3 not in Rapport_2:
            Rapport_2[tc_3] = {}

        if tc_1 not in Rapport_2[tc_3]:
            splitted_tc2 = tc_2.split(',')
            splitted_lt = lt.split(',')
            splitted_oi = oi.split(',')
            splitted_pi = pi.split(',')
            splitted_dt = dt.split(',')
            
            Rapport_2[tc_3][tc_1] = {
                'TC2': [NOT_NECESSARY if splitted_tc2[0] == 'X' else 'x', NOT_NECESSARY if splitted_tc2[1] == 'X' else 'x', NOT_NECESSARY if splitted_tc2[2] == 'X' else 'x'],
                LT: [NOT_NECESSARY if splitted_lt[0] == 'X' else 'x', NOT_NECESSARY if splitted_lt[1] == 'X' else 'x', NOT_NECESSARY if splitted_lt[2] == 'X' else 'x'],
                OI: [NOT_NECESSARY if splitted_oi[0] == 'X' else 'x', NOT_NECESSARY if splitted_oi[1] == 'X' else 'x', NOT_NECESSARY if splitted_oi[2] == 'X' else 'x'],
                PI: [NOT_NECESSARY if splitted_pi[0] == 'X' else 'x', NOT_NECESSARY if splitted_pi[1] == 'X' else 'x', NOT_NECESSARY if splitted_pi[2] == 'X' else 'x'],
                DT: [NOT_NECESSARY if splitted_dt[0] == 'X' else 'x', NOT_NECESSARY if splitted_dt[1] == 'X' else 'x', NOT_NECESSARY if splitted_dt[2] == 'X' else 'x'],
            }

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
Generate a markdown table string from a list of rows and headers.
Args:
    headers (list): List of header values.
    rows (list): List of lists containing row values.
Returns:
    table (str): Markdown table string.
"""
def generate_markdown_table(headers, rows):
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in rows:
        table += "| " + " | ".join(row) + " |\n"
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
    global Rapport_2

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

    return combined_tags, errors

"""
Update the Rapport 1 data with the new values.
Args:
    tc_1 (str): TC1 code.
    tc_2 (str): TC2 code.
"""
def update_rapport1_data(tc_1, tc_2):
    Rapport_1[tc_1]['TC2'] = ['v' if tc_2 == '1' and Rapport_1[tc_1]['TC2'][0] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][0], 'v' if tc_2 == '2' and Rapport_1[tc_1]['TC2'][1] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][1], 'v' if tc_2 == '3' and Rapport_1[tc_1]['TC2'][2] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][2]]

"""
Update the Rapport 2 data with the new values.
Args:
    file_type (str): File type.
    tc_1 (str): TC1 code.
    tc_2 (str): TC2 code.
    tc_3 (str): TC3 code.
"""
def update_rapport2_data(file_type, tc_1, tc_2, tc_3):
    # Update the record with the new values
    def update_rapport2_row(tc_3, tc_1, tc_2, file_type, searchType):
        Rapport_2[tc_3][tc_1][searchType] = [
            'v' if file_type == searchType and tc_2 == '1' and Rapport_2[tc_3][tc_1][searchType][0] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][0], 
            'v' if file_type == searchType and tc_2 == '2' and Rapport_2[tc_3][tc_1][searchType][1] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][1], 
            'v' if file_type == searchType and tc_2 == '3' and Rapport_2[tc_3][tc_1][searchType][2] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][2]
        ]

    Rapport_2[tc_3][tc_1]['TC2'] = ['v' if tc_2 == '1' and Rapport_2[tc_3][tc_1]['TC2'][0] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][0], 'v' if tc_2 == '2' and Rapport_2[tc_3][tc_1]['TC2'][1] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][1], 'v' if tc_2 == '3' and Rapport_2[tc_3][tc_1]['TC2'][2] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][2]]
    update_rapport2_row(tc_3, tc_1, tc_2, file_type, LT)
    update_rapport2_row(tc_3, tc_1, tc_2, file_type, OI)
    update_rapport2_row(tc_3, tc_1, tc_2, file_type, PI)
    update_rapport2_row(tc_3, tc_1, tc_2, file_type, DT)

"""
Format the report table for table 1
Returns:
    table (str): Markdown table string.
"""
def generate_rapport_1():
    if Verbose: print("Generating Rapport 1 table...")

    headers = ["TC1", "Proces", "Processtap", "Niveau 1", "Niveau 2", "Niveau 3"]
    rows = []
    for tc, details in Rapport_1.items():
        proces = details.get('Proces', '')
        processtap = details.get('Processtap', '')
        tc2_levels = details.get('TC2', {})
        niveau_1 = FAIL_CIRCLE if tc2_levels[0] == 'x' else SUCCESS if tc2_levels[0] == 'v' or tc2_levels[0] == 'g' else NOT_NECESSARY
        niveau_2 = FAIL_CIRCLE if tc2_levels[1] == 'x' else SUCCESS if tc2_levels[1] == 'v' or tc2_levels[1] == 'g' else NOT_NECESSARY        
        niveau_3 = FAIL_CIRCLE if tc2_levels[2] == 'x' else SUCCESS if tc2_levels[2] == 'v' or tc2_levels[2] == 'g' else NOT_NECESSARY

        rows.append([tc, proces, processtap, niveau_1, niveau_2, niveau_3])

    table = generate_markdown_table(headers, rows)

    if Verbose: print("Rapport 1 table generated.")

    return table

"""
Format the report for table 2
Returns:
    table (str): Markdown table string.
"""
def generate_rapport_2():
    if Verbose: print("Generating Rapport 2 table...")

    headers = ["TC3", "TC1", "TC2", LT, OI, PI, DT]
    rows = []

    def get_status(value):
        if value == 'v' or value == 'g':
            return SUCCESS
        elif value != NOT_NECESSARY:
            return FAIL_CIRCLE
        else:
            return NOT_NECESSARY

    for tc3, details in Rapport_2.items():
        for tc1, other in details.items():
            tc2_levels = other.get('TC2', [''] * 3)
            tc2 = ' '.join([get_status(level) for level in tc2_levels])

            leertaak_levels = other.get(LT, [''] * 3)
            leertaak = ' '.join([get_status(level) for level in leertaak_levels])
            
            ondersteunende_informatie_levels = other.get(OI, [''] * 3)
            ondersteunende_informatie = ' '.join([get_status(level) for level in ondersteunende_informatie_levels])
            
            procedurele_informatie_levels = other.get(PI, [''] * 3)
            procedurele_informatie = ' '.join([get_status(level) for level in procedurele_informatie_levels])
            
            deeltaak_levels = other.get(DT, [''] * 3)
            deeltaak = ' '.join([get_status(level) for level in deeltaak_levels])

            rows.append([tc3, tc1, tc2, leertaak, ondersteunende_informatie, procedurele_informatie, deeltaak])

    table = generate_markdown_table(headers, rows)

    if Verbose: print("Rapport 2 table generated.")

    return table

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
Format the image report table.
Args:
    file_report (list): List of image reports.
Returns:
    table (str): Markdown table string.
"""
def format_image_report_table(image_report):
    headers = ["Image", "Path", "Error"]
    rows = [[
        file['image'], 
        file['path'],
        file['error']
    ] for file in image_report]

    table = generate_markdown_table(headers, rows)
    return table

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
Create a list of a file for test cases
"""
def create_test_file_result(file_path, taxonomie, tags, errors):
    return {
        "file": file_path.stem,
        "taxonomie": '<br>'.join(taxonomie) if taxonomie else "N/A",
        "tags": '<br>'.join(tags) if tags else "N/A",
        "errors": '<br>'.join(errors) if errors else "N/A"
    }

"""
Create a list of a image
"""
def create_image_result(file_path, src_dir, error):
    return {
        "image": file_path.stem,
        "path": str(file_path.relative_to(src_dir)),
        "error": error,
    }

"""
Generate the report based on the taxonomie report, success, and failed reports.
"""
def generate_report():
    if Verbose: print("Generating report...")

    report_path = "report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write('---\ndraft: true\n---\n')
        
        # Rapport 1 Section
        f.write('## Rapport 1 - Processtappen\n')
        f.write('*Doel: achterhalen welke processtappen nog helemaal niet zijn geïmplementeerd*\n\n')
        f.write('- ✅ Er bestaat een bestand met deze taxonomiecode op dit niveau \n\n')
        f.write('- ⛔️ Er is geen enkel bestand met deze taxonomiecode op dit niveau \n\n')
        f.write('- 🏳️ De taxonomiecode wordt niet aangeboden op dit niveau (X in de Dataset) \n\n')
        f.write('\n')
        f.write(generate_rapport_1())

        f.write('\n\n')

        # Rapport 2 Section
        f.write('## Rapport 2 - Onderwerpen Catalogus\n')
        f.write('*Doel: Lijst met onderwerpen + gekoppelde taxonomie code voor inzicht in aangeboden onderwerpen.*\n')
        f.write('Bij kolom *TC2*, *Leertaken*, *Ondersteunende informatie*, *Procedurele informatie* en *Deeltaken* zijn drie tekens aanwezig om de drie HBO-i niveaus weer te geven\n\n')
        f.write('- ✅ Het onderwerp met taxonomie code wordt aangeboden op het aangegeven niveau \n\n')
        f.write('- ⛔️ Het onderwerp met taxonomie code wordt **niet** aangeboden op het aangegeven niveau \n\n')
        f.write('- 🏳️ Het onderwerp hoeft met deze taxonomie code niet aangeboden te worden op het aangegeven niveau \n\n')
        f.write('\n')
        f.write(generate_rapport_2())

        f.write('\n\n')

        # Passed Files Section
        f.write("## Geslaagde bestanden\n")
        f.write("De onderstaande bestanden zijn succesvol verwerkt.\n")
        f.write('\n')
        f.write(format_file_report_table(Successful_files))

        f.write('\n\n')

        # Failed Files Section
        f.write("## Gefaalde bestanden\n")
        f.write("*Doel: De onderstaande bestanden zijn niet succesvol verwerkt.*\n\n")
        f.write('❌ Dit bestand bevat nog geen taxonomie code\n\n')
        f.write('⚠️ Dit bestand bevat een foute taxonomie code. Zie de *Errors* kolom om te weten wat er mis is\n\n')
        f.write('🟠 Dit bestand bevat een taxonomie code die niet toegevoegd hoeft te zijn\n\n')
        f.write('\n')
        f.write(format_file_report_table(Failed_files))

        f.write('\n\n')

        f.write("## Gefaalde images\n")
        f.write("*Doel: De onderstaande images missen een 4C/ID component.*\n\n")
        f.write(format_image_report_table(Failed_images))

    # Print reports for quick feedback
    if Verbose:
        print("Rapport 1:")
        print(generate_rapport_1())
        print("Rapport 2:")
        print(generate_rapport_2())
        print("Geslaagde bestanden:")
        print(format_file_report_table(Successful_files))
        print("Gefaalde bestanden:")
        print(format_file_report_table(Failed_files))
        print("Gefaalde images:")
        print(format_image_report_table(Failed_images))

        print("Report generated.")

"""
Search for image links in the markdown content, and copy the images from the source/
folder to the build/ folder, preserving the folder structure.

Args:
    content (str): Content of the markdown file.
"""
def copy_images(content):
    # Define the root content directory and the build directory
    content_path = Path(__file__).resolve().parents[1] / 'content'
    build_path = Path(__file__).resolve().parents[1] / 'build'
    errors = []

    if content is None:
        return errors

    # Regex to find all image paths in markdown content (both markdown and obsidian style)
    image_links = re.findall(r'!\[\[([^\]]+)\]\]|\!\[([^\]]*)\]\(([^)]+)\)', content)

    # Iterate over each image link found
    for image_link in image_links:
        # If the image link matches the Obsidian-style (first capture group), use that
        if image_link[0]:
            image_path = image_link[0].strip()
        # If the image link matches the Markdown-style (second and third capture groups), use the path from group 2
        elif image_link[2]:
            image_path = image_link[2].strip()

        # If the image path is empty or invalid, skip this one
        if not image_path:
            continue

        # Skip external links
        if image_path.startswith('http://') or image_path.startswith('https://'):
            continue

        # Find the image file by walking through the content directory
        found_image_path = None
        for root, dirs, files in os.walk(content_path):
            if image_path in files:
                found_image_path = Path(root) / image_path
                break

        # If the image file is found, proceed with copying it
        if found_image_path and found_image_path.exists():

            # Calculate the relative path of the image within 'content' folder
            relative_path = found_image_path.relative_to(content_path)

            # Determine the new location in the 'build' directory (preserving the folder structure)
            new_image_path = build_path / relative_path

            # Create the new directory if it doesn't exist
            new_image_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the image to the new location
            shutil.copy(found_image_path, new_image_path)
        else:
            if Verbose: print(f"Image not found: {image_path}")
            errors.append(f"Image not found: {image_path}")

    return errors

"""
Checks if the dynamic link is valid and the file exists.

Args:
    source_file_path (str): Path to the source file.
    link (str): Dynamic link to validate.
"""
def validate_dynamic_link(source_file_path, link):
    # Define the root content directory (assuming it is one level up from the current script)
    content_path = Path(__file__).resolve().parents[1] / 'content'

    # Verify that content_path exists
    if not content_path.exists():
        if Verbose: print(f"Error: Content path '{content_path}' does not exist.")
        return False

    # Clean up the link by removing the surrounding [[ and ]]
    cleaned_link = link.strip('[[]]')

    # If the link contains a section (anchor), split the link at '#'
    if '#' in cleaned_link:
        cleaned_link = cleaned_link.split('#')[0]  # Use only the part before '#'

    # Parse the base name from the cleaned link
    link_parts = cleaned_link.split('|')
    file_name = link_parts[0].strip().split('/')[-1]

    # Search for the file in all subdirectories within 'content' using os.walk
    found_file = None
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file.startswith(file_name):  # Check if the file name matches
                found_file = os.path.join(root, file)
                return True

    # If no valid file is found, report error with details
    if not found_file:
        if Verbose: print(f"Error: source file: {source_file_path}, target file '{file_name}' not found in content.")

    return False

"""
Update dynamic links in the content of a markdown file.

Args:
    file_path (str): Path to the markdown file.
    content (str): Content of the markdown file.
"""
def update_dynamic_links(file_path, content):
    # Find all dynamic links in the content
    dynamic_links = re.findall(r'\[\[[^"\[][^]]*?\]\]', content)
    errors = []

    for link in dynamic_links:
        # Skip links that start with any of the valid prefixes
        cleaned_link = link.strip('[[]]')
        if any(cleaned_link.startswith(prefix) for prefix in ValidDynamicLinkPrefixes):
            return content, errors
            
        # Strip 'content/' prefix if present
        new_link = link.replace('content/', '')

        # Replace the old link with the new link in the content
        content = content.replace(link, new_link)

        # Check if the dynamic link is valid
        if not validate_dynamic_link(file_path, new_link):
            if Verbose: print(f"Error: Invalid dynamic link: {new_link}")
            errors.append(f"Invalid dynamic link: `{new_link}`")

    return content, errors

"""
Update markdown files in the source directory with taxonomie tags and generate reports.
Args:
    src_dir (str): Source directory containing markdown files.
    dest_dir (str): Destination directory to save updated markdown files and reports.
"""
def parse_markdown_files(src_dir, dest_dir):
    if Verbose: print("Parsing markdown files...")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Loop through all markdown files in the source directory
    for file_path in Path(src_dir).rglob('*.md'):
        relative_path = file_path.relative_to(src_dir)
        dest_path = dest_dir / relative_path
        errors = []

        # Skip the folder schrijfwijze
        if "schrijfwijze" in str(file_path):
            continue

        if Verbose: 
            print("*" * 50) 
            print(f"Parsing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if there are any dynamic links which need to be updated
        content, link_errors = update_dynamic_links(file_path, content)

        # Copy images from source to build directory
        image_errors = copy_images(content)

        # Extract existing tags and taxonomie
        existing_tags = extract_values(content, 'tags')
        taxonomie = extract_values(content, 'taxonomie')
        new_tags, tags_errors = generate_tags(taxonomie, file_path, existing_tags)
        difficulty = extract_values(content, 'difficulty')

        # Combine all errors
        errors = link_errors + image_errors + tags_errors

        # If any errors occurred, add the file to the failed files list
        if errors:
            if(ERROR_MISSING_TAXCO in errors): 
                Failed_files.append(create_file_report(FAIL_CROSS, file_path, src_dir, taxonomie, new_tags, errors))
            elif any("Taxonomie use where it is not need" in error for error in errors):
                Failed_files.append(create_file_report(NOT_NEEDED, file_path, src_dir, taxonomie, new_tags, errors))
            else: 
                Failed_files.append(create_file_report(WRONG_TAXONOMY_CODE, file_path, src_dir, taxonomie, new_tags, errors))
            if Verbose: print(f"Failed to parse file: {file_path}")
        else:
            Successful_files.append(create_file_report(SUCCESS, file_path, src_dir, taxonomie, new_tags, errors))

        # Create the new content with updated tags
        new_content = (
            f"---\ntitle: {file_path.stem}\ntaxonomie: {taxonomie}\ntags:\n" +
            '\n'.join([f"- {tag}" for tag in new_tags]) +
            "\n"
        )

        if difficulty:
            new_content += "difficulty: " + ''.join([f"{level}" for level in difficulty]) + "\n"

        new_content += "---" + content.split('---', 2)[-1]

        # Create the destination directory if it doesn't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the new content to the destination file
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        if Verbose:
            print(f"File completed: {file_path}")
            print("-" * 50)

def populate_image_report(src_dir, dest_dir):
    src_folders = [folder for folder in Path(src_dir).rglob("src") if folder.is_dir()]
    src_images = set()
    for folder in src_folders:
        if "schrijfwijze" in str(folder):
            continue
        src_images.update(
            file_path
            for file_path in folder.rglob("*")  # Search recursively in each 'src' folder
        ) 
    dest_folders = [folder for folder in Path(dest_dir).rglob("src") if folder.is_dir()]
    dest_images = set()
    for folder in dest_folders:
        if "schrijfwijze" in str(folder):
            continue
        dest_images.update(
            file_path
            for file_path in folder.rglob("*")  # Search recursively in each 'src' folder
        ) 
    for image in dest_images :
        if not str(image.stem).startswith(("PI", "OI")):
            Failed_images.append(create_image_result(image, dest_dir, "Image does not include 4C/ID component"))
    for image in src_images : 

        if str(image.stem) not in {str(img.stem) for img in dest_images}:
            Failed_images.append(create_image_result(image, src_dir, "Image not used in any file"))
             

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
    return validate_test();  


"""
Validates the test cases against the expected outcome
"""
def validate_test():
    from expected_result_taxco_tests import Expected_failed_test_files, Expected_successful_test_files
    if Verbose: 
        print(f"Succesful test files: {check_files_set_equal(Successful_test_files, Expected_successful_test_files)}")
        print(f"Failed test files: {check_files_set_equal(Failed_test_files, Expected_failed_test_files)}")
    return check_files_set_equal(Successful_test_files, Expected_successful_test_files) and check_files_set_equal(Failed_test_files, Expected_failed_test_files)


    
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
            if test_link_file(test_dir): 
                from evaluate import evaulate_tests
                markdown_count_check = evaulate_tests(src_dir, dest_dir)
                if markdown_count_check:
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

        generate_report()

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
