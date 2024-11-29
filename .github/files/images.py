# Imports
import os, re, shutil
from pathlib import Path

# Variables
from config import Verbose

# Functions
from report.table import generate_markdown_table


"""
Search for image links in the markdown content, and copy the images from the source/
folder to the build/ folder, preserving the folder structure.

Args:
    content (str): Content of the markdown file.
    src_dir_name (str): Source directory (only the name of the folder itself)
    dest_dir_name (str): Destination directory (only the name of the folder itself)
"""
def copy_images(content, src_dir_name, dest_dir_name):
    # Define the root content directory and the build directory
    content_path = Path(__file__).resolve().parents[2] / src_dir_name
    build_path = Path(__file__).resolve().parents[2] / dest_dir_name
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
Create a list of a image
"""
def create_image_result(status, file_path, src_dir, error):
    return {
        "status" : status,
        "image": file_path.stem,
        "path": str(file_path.relative_to(src_dir)),
        "error": error,
    }

"""
Format the image report table.
Args:
    file_report (list): List of image reports.
Returns:
    table (str): Markdown table string.
"""
def format_image_report_table(image_report):
    headers = ["Status", "Image", "Path", "Error"]
    rows = [[
        file['status'], 
        file['image'], 
        file['path'],
        file['error']
    ] for file in image_report]

    table = generate_markdown_table(headers, rows)
    return table
