import unittest
from markdown_to_html_node import text_to_children, markdown_to_html_node
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from htmlnode import HTMLNode
from markdown_textnode import TextNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_unordered_list_with_emphasis(self):
        markdown = "* Disney *didn't ruin it*\n* Another item"
        print("Original markdown:", markdown)  # removed repr()
        blocks = markdown_to_blocks(markdown)
        print("Blocks:", blocks)  # removed repr() and list comprehension
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        print("Generated HTML:", html)
        assert "<li>Disney <i>didn't ruin it</i></li>" in html
        
    ### NEED TO MAKE MORE UNIT TESTS
    
if __name__ == "__main__":
    unittest.main()
