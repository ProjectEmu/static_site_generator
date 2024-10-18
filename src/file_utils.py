import os
import shutil
from converters import *


def copy_files(src_dir, dest_dir, log_to_console=False, clean_dest=False):
    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory '{src_dir}' does not exist.")
    if not os.path.isdir(src_dir):
        raise ValueError(f"Source path '{src_dir}' is not a directory.")

    # Clean the destination directory if required
    if clean_dest and os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    for root, dirs, files in os.walk(src_dir):
        # Create corresponding directories in the destination
        for dir_name in dirs:
            src_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(src_path, src_dir)
            dest_path = os.path.join(dest_dir, rel_path)
            os.makedirs(dest_path, exist_ok=True)
            if log_to_console:
                print(f"Directory copied: {dest_path}")

        # Copy files
        for file_name in files:
            src_file = os.path.join(root, file_name)
            rel_path = os.path.relpath(src_file, src_dir)
            dest_file = os.path.join(dest_dir, rel_path)
            shutil.copy2(src_file, dest_file)
            if log_to_console:
                print(f"File copied: {dest_file}")


# Example usage
# copy_files("/path/to/source", "/path/to/destination", log_to_console=True, clean_dest=True)


def generate_page(from_path, template_path, dest_path, root_dir):
    # Read the markdown file into a string
    with open(from_path, "r") as file:
        content = file.read()

    # Placeholder for parsing logic (could be converting markdown to HTML)
    title = extract_title(content)
    parsed_content = markdown_to_html(content).to_html()

    # Read the HTML template into a string
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    # Combine template and parsed content (placeholder)

    full_content = template_content.replace("{{ Title }}", title)
    full_content = full_content.replace("{{ Content }}", parsed_content)

    # Determine the new file path in the destination directory (excluding the root folder)
    relative_path = os.path.relpath(from_path, root_dir)
    dest_file_path = os.path.join(
        dest_path, os.path.splitext(relative_path)[0] + ".html"
    )

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

    # Write the generated HTML to the destination
    with open(dest_file_path, "w") as dest_file:
        dest_file.write(full_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Look for markdown files
                from_path = os.path.join(root, file)
                generate_page(from_path, template_path, dest_dir_path, dir_path_content)


# Example usage
# generate_pages_recursive("/path/to/content", "/path/to/template.html", "/path/to/destination")
