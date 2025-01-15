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
        assert children[0].tag == "h1", "Header 1 not converted correctly"
        assert children[0].children[0].text == "Header 1", "Header 1 content not correct"
        # Test Header 2
        assert children[1].tag == "h2", "Header 2 not converted correctly"
        assert children[1].children[0].text == "Header 2", "Header 2 content not correct"
        # Test Header 3
        assert children[2].tag == "h3", "Header 3 not converted correctly"
        assert children[2].children[0].text == "Header 3", "Header 3 content not correct"

    def test_paragraph_edge_cases(self):
        paragraph_markdown = """Normal paragraph here.

Paragraph with
multiple lines
   and some indentation

Paragraph with *italic*
and **bold** text

Paragraph with
        lots of spaces
    and indents

Paragraph with special chars: #, *, >, 1.
"""
        root_node = markdown_to_html_node(paragraph_markdown)
        children = root_node.children

        # Test first basic paragraph
        assert children[0].tag == "p", "First node should be paragraph"
        
        # Test multi-line paragraph
        assert children[1].tag == "p", "Multi-line should be single paragraph"
        assert len(children[1].children) > 0, "Paragraph should have content"
        
        # Test paragraph with formatting
        assert children[2].tag == "p", "Formatted paragraph should be paragraph"
        
        # Test paragraph with indentation
        assert children[3].tag == "p", "Indented paragraph should be paragraph"

    def test_more_paragraph_edge_cases(self):
        paragraph_markdown = """Normal paragraph here.

Paragraph with
multiple lines
   and some indentation

Paragraph with special chars: # not a header
* not a list
> not a quote
1. not ordered list

    Paragraph with lots of spaces at start
"""
        root_node = markdown_to_html_node(paragraph_markdown)
        children = root_node.children
        # Test basic paragraph
        assert children[0].tag == "p", "First node should be paragraph"
        assert children[0].children[0].text == "Normal paragraph here.", "First paragraph content mismatch"

        # Test multi-line paragraph
        assert children[1].tag == "p", "Multi-line should be single paragraph"
        assert "Paragraph with" in children[1].children[0].text, "Multi-line content start mismatch"
        assert "indentation" in children[1].children[0].text, "Multi-line content end mismatch"

        # Test paragraph with special characters
        assert children[2].tag == "p", "Special chars paragraph should be paragraph"
        assert "# not a header" in children[2].children[0].text, "Special chars content mismatch"

    def test_code_blocks(self):
        markdown = """```
def hello_world():
    print('Hello, World!')
```"""
        root_node = markdown_to_html_node(markdown)
        assert root_node.tag == "div"
        # Code blocks should be wrapped in both <pre> and <code> tags
        assert root_node.children[0].tag == "pre"
        assert root_node.children[0].children[0].tag == "code"
        # Check the content
        code_content = root_node.children[0].children[0].children[0].text
        assert "def hello_world():" in code_content

    def test_blockquotes(self):
        markdown = """> This is a blockquote
> It can span multiple lines
> Like this"""
        root_node = markdown_to_html_node(markdown)
        assert root_node.tag == "div"
        assert root_node.children[0].tag == "blockquote"
        # Check the content
        quote_content = root_node.children[0].children[0].text
        assert "This is a blockquote" in quote_content

    def test_lenient_blockquotes(self):
        markdown = """> This is a blockquote
This line is still part of it even without >
And this one too"""
        root_node = markdown_to_html_node(markdown)
        assert root_node.tag == "div"
        assert root_node.children[0].tag == "blockquote"
        quote_content = root_node.children[0].children[0].text
        assert "This line is still part of it" in quote_content

    # this might need more unittests for the other types!

if __name__ == "__main__":
    unittest.main()