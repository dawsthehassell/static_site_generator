import unittest
from markdown_to_html_node import text_to_children, markdown_to_html_node
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from htmlnode import HTMLNode
from textnode import TextNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_headers(self):
        # Input markdown for each header level
        markdown = """# Header 1
## Header 2
### Header 3"""
        # Call the function to test
        root_html_node = markdown_to_html_node(markdown)
        # Check the parent node is <div>
        assert root_html_node.tag == "div", f"Expected parent node to be <div>, got <{root_html_node.tag}>"
        # Each child:
        children = root_html_node.children
        # Test Header 1
        print(children)
        assert children[0].tag == "h1", "Header 1 not converted correctly"
        assert children[0].children[0].text == "Header 1", "Header 1 content not correct"
        # Test Header 2
        assert children[1].tag == "h2", "Header 2 not converted correctly"
        assert children[1].children[0].text == "Header 2", "Header 2 content not correct"
        # Test Header 3
        assert children[2].tag == "h3", "Header 3 not converted correctly"
        assert children[2].children[0].text == "Header 3", "Header 3 content not correct"



if __name__ == "__main__":
    unittest.main()