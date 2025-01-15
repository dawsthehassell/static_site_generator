from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from htmlnode import HTMLNode
from textnode import TextNode, TextType

def text_to_children(text):
    children = []
    while text:
        if text.startswith("**"):  # Bold (**...**)
            end = text.find("**", 2)  # Look for closing **
            if end != -1:
                strong_text = text[2:end]  # Extract text between **
                children.append(HTMLNode("strong", [TextNode(strong_text, TextType.BOLD)]))
                text = text[end + 2:]  # Remove processed text
            else:
                break  # Malformed bold markdown; stop processing
        elif text.startswith("*"):  # Italics (*...*)
            end = text.find("*", 1)  # Look for closing *
            if end != -1:
                em_text = text[1:end]  # Extract text between *
                children.append(HTMLNode("em", [TextNode(em_text, TextType.ITALIC)]))
                text = text[end + 1:]  # Remove processed text
            else:
                break  # Malformed italic markdown; stop processing
        else:  # Plain text
            # Find the next special marker (** or *)
            next_bold = text.find("**") if "**" in text else float("inf")
            next_italic = text.find("*") if "*" in text else float("inf")
            next_special = min(next_bold, next_italic)

            if next_special != float("inf"):  # Some special marker exists
                plain_text = text[:next_special]  # Extract plain text before the marker
                if plain_text.strip():  # Avoid empty strings (from markers side-by-side)
                    children.append(TextNode(plain_text.strip(), TextType.TEXT))
                text = text[next_special:]  # Remove processed plain text
            else:  # No special markers; all remaining text is plain
                if text.strip():
                    children.append(TextNode(text.strip(), TextType.TEXT))
                break  # Exit the loop, as there's nothing left to process
    return children

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    
    for line in markdown.split("\n"):
        if line.strip() == "":
            # Empty line = end of block
            if current_block:
                blocks.append(" ".join(current_block))
                current_block = []
        # Check if it's a header
        elif line.strip().startswith("#"):
            # If we have a current block, add it
            if current_block:
                blocks.append(" ".join(current_block))
                current_block = []
            # Add header as its own block
            blocks.append(line.strip())
        else:
            current_block.append(line.strip())
    
    # Don't forget last block
    if current_block:
        blocks.append(" ".join(current_block))
    
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # heading type
        if block_type.startswith("heading_"):
            level = int(block_type.split("_")[1])
            cleaned_block = block[level + 1:].strip()
            children = text_to_children(cleaned_block)
            html_node = HTMLNode(tag=f"h{level}", children=children)
            html_nodes.append(html_node)
        
        # paragraph type
        elif block_type == "paragraph":
            text_children = text_to_children(block)
            paragraph_node = HTMLNode("p", children=text_children)
            html_nodes.append(paragraph_node)
        
        # code type
        elif block_type == "code":
            code_content = block.strip().strip('```')
            code_node = HTMLNode(
                tag="code",
                children=[TextNode(code_content, "text")]
            )
            pre_node = HTMLNode(
                tag="pre",
                children=[code_node]
            )
            html_nodes.append(pre_node)
        
        # unordered list type
        elif block_type == "unordered_list":
            li_nodes = []
            items = [item.strip() for item in block.split('*') if item.strip()]
            for item in items:
                children = text_to_children(item)
                li_node = HTMLNode(
                    tag="li",
                    children=children
                )
                li_nodes.append(li_node)
            ul_node = HTMLNode(
                tag="ul",
                children=li_nodes
            )
            html_nodes.append(ul_node)
        
        # ordered list type
        elif block_type == "ordered_list":
            list_items = []
            for line in block.split("\n"):
                list_items.append(HTMLNode("li", text_to_children(line.strip())))
            html_node = HTMLNode("ol", list_items)
            html_nodes.append(html_node)
        
        # blockquote type
        elif block_type == "blockquote":
            quote_content = "\n".join(
                line.lstrip('>').strip() 
                for line in block.split('\n')
            )
            blockquote_node = HTMLNode(
                tag="blockquote",
                children=[TextNode(quote_content, "text")]
            )
            html_nodes.append(blockquote_node)
        
        else:
            raise ValueError(f"Unhandled block type: {block_type}")
    
    html_node = HTMLNode(tag="div", children=html_nodes)
    return html_node