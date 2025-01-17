import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for content in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, content)) and os.path.join(dir_path_content, content).endswith(".md"):
            print(f"Processing file: {content}")
            print(f"Source path: {os.path.join(dir_path_content, content)}")
            html_name = content.replace('.md', '.html')
            dest_path = os.path.join(dest_dir_path, html_name)
            print(f"Dest path: {dest_path}")
            generate_page(os.path.join(dir_path_content, content), template_path, dest_path)
        if os.path.isdir(os.path.join(dir_path_content, content)):
            print(f"Found directory: {content}")
            source_subdir = os.path.join(dir_path_content, content)
            dest_subdir = os.path.join(dest_dir_path, content)
            os.makedirs(dest_subdir, exist_ok=True)
            print(f"Created directory: {dest_subdir}")
            generate_pages_recursive(source_subdir, template_path, dest_subdir)