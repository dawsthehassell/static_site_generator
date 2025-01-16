from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown_content = file.read()
    print("Raw markdown:", markdown_content)
    with open(template_path) as file:
        template = file.read()
    html_node = markdown_to_html_node(markdown_content)
    print("HTML node structure:", html_node)
    html_string = html_node.to_html()
    print("Generated HTML:", html_string) 
    print("Final HTML nodes before writing:", html_string)
    title = extract_title(markdown_content)
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_string)
    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(final_html)
    
    # Add this debug print
    with open(dest_path, 'r') as f:
        print("FINAL FILE CONTENTS:", f.read())
    
    
