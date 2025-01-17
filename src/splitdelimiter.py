from markdown_textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            print(f"Processing text: {node.text}")
            if delimiter == "`":
                # Look for text between backticks
                parts = node.text.split("`")
                print(f"Parts after split: {parts}")
                for i, part in enumerate(parts):
                    if i % 2 == 0:  # Regular text
                        if part:  # Only add if not empty
                            result_nodes.append(TextNode(part, TextType.TEXT))
                    else:  # Code text (between backticks)
                        if part:  # Only add if not empty
                            result_nodes.append(TextNode(part, TextType.CODE))
            else:
                # Original logic for other delimiters
                splitted = node.text.split(delimiter)
                if len(splitted) % 2 == 0:
                    raise Exception(
                        f"Unmatched delimiter '{delimiter}' found in content: {node.text}")
                is_text = True
                for i, split in enumerate(splitted):
                    if is_text:
                        # For regular text, keep trailing space if there was one
                        if i < len(splitted) - 1 and split.endswith(" "):
                            result_nodes.append(TextNode(split, TextType.TEXT))
                        else:
                            result_nodes.append(TextNode(split.rstrip(), TextType.TEXT))
                    else:
                        # For emphasized text, preserve leading/trailing spaces
                        result_nodes.append(TextNode(split, text_type))
                    is_text = not is_text
        else:
            result_nodes.append(node)
    
    return result_nodes
    
    