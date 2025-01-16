from splitimglink import split_nodes_image, split_nodes_link
from markdown_textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images ,extract_markdown_links
from splitdelimiter import split_nodes_delimiter
import re

def text_to_textnodes(text):
    text = re.sub(r'\s+', ' ', text)
    initial_nodes = [TextNode(text, TextType.TEXT)]
    split_image = split_nodes_image(initial_nodes)
    split_link = split_nodes_link(split_image)
    split_code = split_nodes_delimiter(split_link, "`", TextType.CODE)
    split_bold = split_nodes_delimiter(split_code, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
    return [node for node in split_italic if node.text != ""]

