from splitimglink import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images ,extract_markdown_links
from splitdelimiter import split_nodes_delimiter

def text_to_textnodes(text):
    # Normalize whitespace and newlines first
    text = " ".join(text.split())  # This replaces multiple spaces/newlines with single spaces
    initial_nodes = [TextNode(text, TextType.TEXT)]
    split_image = split_nodes_image(initial_nodes)
    split_link = split_nodes_link(split_image)
    split_code = split_nodes_delimiter(split_link, "`", TextType.CODE)
    split_bold = split_nodes_delimiter(split_code, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
    return [node for node in split_italic if node.text != ""]

