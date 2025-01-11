from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            splitted = node.text.split(delimiter)
            if len(splitted) % 2 == 0:
                raise Exception(
                    f"Unmatched delimiter '{delimiter}' found in content: {node.text}")
            is_text = True
            for split in splitted:
                new_type = TextType.TEXT if is_text else text_type
                result_nodes.append(TextNode(split, new_type))
                is_text = not is_text
                
        else:
            result_nodes.append(node)
    
    return result_nodes
    
    