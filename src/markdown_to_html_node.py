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
    lines = markdown.split("\n")
    blocks = [line.strip() for line in lines if line.strip()]
    return blocks

def markdown_to_html_node(blocks):
    blocks = markdown_to_blocks(blocks)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # heading type
        if block_type.startswith("heading_"):
            level = int(block_type.split("_")[1])
            cleaned_block = block[level + 1:].strip()
            children = text_to_children(cleaned_block)
            print(f"Text to Children for '{cleaned_block}': {children}")  # Debug statement
            html_node = HTMLNode(f"h{level}", children)
        # paragraph type
        elif block_type == "paragraph":
            html_node = HTMLNode("p", text_to_children(block))
        # code type
        elif block_type == "code":
            html_node = HTMLNode(
                "pre",
                [HTMLNode("code", [TextNode(block)])]
            )
        # unordered list type
        elif block_type == "unordered_list":
            list_items = []
            for line in block.split("\n"):
                list_items.append(HTMLNode("li", text_to_children(line.strip())))
            html_node = HTMLNode("ul", list_items)
        # ordered list type
        elif block_type == "ordered_list":
            list_items = []
            for line in block.split("\n"):
                list_items.append(HTMLNode("li", text_to_children(line.strip())))
            html_node = HTMLNode("ol", list_items)
        # blockquote type
        elif block_type == "blockquote":
            cleaned_block = block.lstrip("> ").strip()
            html_node = HTMLNode("blockquote", text_to_children(cleaned_block))
        else:
            raise ValueError(f"Unhandled block type: {block_type}")
        html_nodes.append(html_node)
    parent_node = HTMLNode("div", html_nodes)
    return parent_node