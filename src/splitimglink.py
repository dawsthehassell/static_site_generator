from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images ,extract_markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []
    for text_node in old_nodes:
        extract = extract_markdown_images(text_node.text)
        
        if not extract:
            new_nodes.append(text_node)
        else:
            remaining_text = text_node.text
            first_section = True
            for alt, url in extract:
                markdown = f"![{alt}]({url})"
                sections = remaining_text.split(markdown, 1)
                
                # Keep empty text node if it's the first section
                if first_section:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                elif len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remaining_text = sections[1] if len(sections) > 1 else ""
                first_section = False
            
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
        



def split_nodes_link(old_nodes):
    new_nodes = []
    for text_node in old_nodes:
        extract = extract_markdown_links(text_node.text)
        
        if not extract:
            new_nodes.append(text_node)
        else:
            remaining_text = text_node.text
            first_section = True
            for text, url in extract:
                markdown = f"[{text}]({url})"
                sections = remaining_text.split(markdown, 1)
                
                # Keep empty text node if it's the first section
                if first_section and len(sections[0]) > 0:  # Only add if there's content
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                elif len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
                new_nodes.append(TextNode(text, TextType.LINK, url))
                remaining_text = sections[1] if len(sections) > 1 else ""
                first_section = False
            
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes