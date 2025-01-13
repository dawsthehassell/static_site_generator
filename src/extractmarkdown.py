import re

def extract_markdown_images(text):
    if len(text) == 0:
        return []
    extraction = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extraction

def extract_markdown_links(text):
    if len(text) == 0:
        return []
    extraction = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extraction