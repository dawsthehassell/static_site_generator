from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_textnode import TextNode, TextType
from markdown_textnode import text_node_to_html_node
import re


import re

def text_to_children(text):
    children = []
    pattern = r"(\*\*([^\*]+)\*\*)|(\*([^\*]+)\*)|(\[([^\]]+)\]\(([^\)]+)\))|(`([^`]+)`)|([^\*\[\]`]+)"
    matches = list(re.finditer(pattern, text))
    
    for match in matches:
        if match.group(1):  # **bold**
            bold_text = match.group(2)
            bold_node = ParentNode("b", [LeafNode(None, bold_text)])
            children.append(bold_node)
        elif match.group(3):  # *italic*
            italic_text = match.group(4)
            italic_node = ParentNode("i", [LeafNode(None, italic_text)])
            children.append(italic_node)
        elif match.group(5):  # [text](url)
            link_text = match.group(6)
            link_url = match.group(7)
            link_node = ParentNode("a", [LeafNode(None, link_text)], {"href": link_url})
            children.append(link_node)
        elif match.group(8):  # `code`
            code_text = match.group(9)
            code_node = ParentNode("code", [LeafNode(None, code_text)])
            children.append(code_node)
        elif match.group(10):  # Plain text
            plain_text = match.group(10)
            if plain_text:
                text_node = text_node_to_html_node(TextNode(plain_text, TextType.TEXT))
                children.append(text_node)
    
    return children

def markdown_to_blocks(markdown):
    markdown = str(markdown).strip('"\'')
    blocks = []
    current_block = []
    in_list = False
    
    for line in markdown.split("\n"):
        stripped_line = line.strip()
        
        # Empty line handling
        if stripped_line == "":
            if current_block:
                if in_list:
                    blocks.append("\n".join(current_block))
                else:
                    blocks.append(" ".join(current_block))
                current_block = []
                in_list = False
            continue
            
        # List item detection
        if stripped_line.startswith("* ") or stripped_line.startswith("- "):
            if not in_list:
                # If we were building a non-list block, finish it
                if current_block:
                    blocks.append(" ".join(current_block))
                    current_block = []
                in_list = True
            current_block.append(line)
            continue
            
        # If we're not in a list anymore but were before
        if in_list and not (stripped_line.startswith("* ") or stripped_line.startswith("- ")):
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            in_list = False
            
        # Header handling
        if stripped_line.startswith("#"):
            if current_block:
                if in_list:
                    blocks.append("\n".join(current_block))
                else:
                    blocks.append(" ".join(current_block))
                current_block = []
            blocks.append(stripped_line)
            continue
            
        # Add line to current block
        current_block.append(line)
    
    # Handle last block
    if current_block:
        if in_list:
            blocks.append("\n".join(current_block))
        else:
            blocks.append(" ".join(current_block))
    
    return blocks

def markdown_to_html_node(markdown):
    markdown = markdown.strip('"\'')  # Remove surrounding quotes
    markdown = markdown.replace('\\n', '\n')
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # heading type
        if block_type.startswith("heading_"):
            level = int(block_type.split("_")[1])
            cleaned_block = block[level + 1:].strip()
            children = text_to_children(cleaned_block)
            html_node = ParentNode(tag=f"h{level}", children=children)
            html_nodes.append(html_node)
        
        # paragraph type
        elif block_type == "paragraph":
            text_children = text_to_children(block)
            paragraph_node = ParentNode("p", children=text_children)
            html_nodes.append(paragraph_node)
        
        # code type
        elif block_type == "code":
            code_content = block.strip().strip('```')
            code_node = LeafNode(
                tag="code",
                value=code_content
            )
            pre_node = ParentNode(
                tag="pre",
                children=[code_node]
            )
            html_nodes.append(pre_node)
        
        # unordered list type
        elif block_type == "unordered_list":
            li_nodes = []
            lines = block.split('\n')
            for line in lines:
                # Only remove the first * and one following space
                if line.startswith('*'):
                    line = line[1:]  # Remove the *
                    line = line.lstrip(' ')  # Remove leading spaces after *
                if line:  # Skip empty lines
                    children = text_to_children(line)
                    li_node = ParentNode(
                        tag="li",
                        children=children
                    )
                    li_nodes.append(li_node)
            ul_node = ParentNode(
                tag="ul",
                children=li_nodes
            )
            html_nodes.append(ul_node)
        
        # ordered list type
        elif block_type == "ordered_list":
            list_items = []
            # Use regex to split the block on each numbered item (e.g., "1.", "2.", etc.)
            lines = re.split(r'\s*\d+\.\s+', block.strip())
            for content in lines:
                content = content.strip()
                if content:  # Skip any empty results from the split
                    list_items.append(ParentNode("li", text_to_children(content)))
            html_node = ParentNode("ol", list_items)
            html_nodes.append(html_node)
                
        # blockquote type
        elif block_type == "blockquote":
            quote_content = "\n".join(
                line.lstrip('>').strip() 
                for line in block.split('\n')
            )
            blockquote_node = ParentNode(
                tag="blockquote",
                children=text_to_children(quote_content)
            )
            html_nodes.append(blockquote_node)
        
        else:
            raise ValueError(f"Unhandled block type: {block_type}")
    
    parent = ParentNode(tag="div", children=html_nodes)
    return parent