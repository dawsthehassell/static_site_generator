import unittest
from text_to_textnodes import text_to_textnodes
from markdown_textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images ,extract_markdown_links
from splitimglink import split_nodes_image, split_nodes_link

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "Hello world"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Hello world"
        assert nodes[0].text_type == TextType.TEXT

    def test_bold_markdown(self):
        text = "Hello **there** world"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "Hello "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "there"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " world"
        assert nodes[2].text_type == TextType.TEXT

    def test_bold_and_italic(self):
        text = "**Hello** *world*"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "Hello"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == " "
        assert nodes[1].text_type == TextType.TEXT
        assert nodes[2].text == "world"
        assert nodes[2].text_type == TextType.ITALIC

    def test_multiple_bold(self):
        text = "**Hello** normal **world**"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3  # Two bold nodes, two text nodes
        assert nodes[0].text == "Hello"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == " normal "
        assert nodes[1].text_type == TextType.TEXT
        assert nodes[2].text == "world"
        assert nodes[2].text_type == TextType.BOLD

    def test_mixed_text_types(self):
        text = "**Bold** *italic* `code` normal **more bold**"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 7
        assert nodes[0].text == "Bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == " "
        assert nodes[1].text_type == TextType.TEXT
        assert nodes[2].text == "italic"
        assert nodes[2].text_type == TextType.ITALIC
        assert nodes[3].text == " "
        assert nodes[3].text_type == TextType.TEXT
        assert nodes[4].text == "code"
        assert nodes[4].text_type == TextType.CODE
        assert nodes[5].text == " normal "
        assert nodes[5].text_type == TextType.TEXT
        assert nodes[6].text == "more bold"
        assert nodes[6].text_type == TextType.BOLD

    def test_complex_nested_formats(self):
        text = "**Bold** with ![image](http://url.com) and *italic* and [link](http://boot.dev) and `code`"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 9
        assert nodes[0].text == "Bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == " with "
        assert nodes[1].text_type == TextType.TEXT
        assert nodes[2].text == "image"
        assert nodes[2].text_type == TextType.IMAGE
        assert nodes[2].url == "http://url.com"
        assert nodes[3].text == " and "
        assert nodes[3].text_type == TextType.TEXT
        assert nodes[4].text == "italic"
        assert nodes[4].text_type == TextType.ITALIC
        assert nodes[5].text == " and "
        assert nodes[5].text_type == TextType.TEXT
        assert nodes[6].text == "link"
        assert nodes[6].text_type == TextType.LINK
        assert nodes[6].url == "http://boot.dev"
        assert nodes[7].text == " and "
        assert nodes[7].text_type == TextType.TEXT
        assert nodes[8].text == "code"
        assert nodes[8].text_type == TextType.CODE

    def test_edge_cases(self):
        # Test code blocks with delimiters inside
        text = "`code with **bold** inside`"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "code with **bold** inside"
        assert nodes[0].text_type == TextType.CODE
        
        # Test simple nested case
        text = "**bold with *italic* text**"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "bold with *italic* text"
        assert nodes[0].text_type == TextType.BOLD

    def test_adjacent_elements(self):
        text = "**bold**`code`*italic*![image](http://test.com)[link](http://test.com)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 5
        assert nodes[0].text == "bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == "code"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[2].text == "italic"
        assert nodes[2].text_type == TextType.ITALIC
        assert nodes[3].text == "image"
        assert nodes[3].text_type == TextType.IMAGE
        assert nodes[3].url == "http://test.com"
        assert nodes[4].text == "link"
        assert nodes[4].text_type == TextType.LINK
        assert nodes[4].url == "http://test.com"

    def test_empty_and_whitespace(self):
        text = "** ** *  * ` ` ![  ](test.com) [   ](test.com)"
        nodes = text_to_textnodes(text)
        # Let's check the nodes we do get are formatted correctly
        for node in nodes:
            if node.text_type == TextType.BOLD:
                assert node.text.strip() == ""
            elif node.text_type == TextType.ITALIC:
                assert node.text.strip() == ""
            elif node.text_type == TextType.CODE:
                assert node.text.strip() == ""
            elif node.text_type == TextType.IMAGE:
                assert node.url == "test.com"
            elif node.text_type == TextType.LINK:
                assert node.url == "test.com"
            
        # Verify we at least get the nodes with URLs
        assert any(node.text_type == TextType.IMAGE for node in nodes)
        assert any(node.text_type == TextType.LINK for node in nodes)

    def test_real_world_markdown(self):
        text = """This is a **complex** test with *multiple* `code blocks` and ![images](img.png).
        It even has [links](https://boot.dev) and **bold text with *italic* inside**."""
        nodes = text_to_textnodes(text)
        expected_types = [
            TextType.TEXT,   # "This is a "
            TextType.BOLD,   # "complex"
            TextType.TEXT,   # " test with "
            TextType.ITALIC, # "multiple"
            TextType.TEXT,   # " "
            TextType.CODE,   # "code blocks"
            TextType.TEXT,   # " and "
            TextType.IMAGE,  # "images" with URL
            TextType.TEXT,   # ". It even has "
            TextType.LINK,   # "links" with URL
            TextType.TEXT,   # " and "
            TextType.BOLD,   # "bold text with italic inside"
            TextType.TEXT,   # '.'
        ]
        
        for i, node in enumerate(nodes):
            print(f"{i}. Text: '{node.text}', Type: {node.text_type}")
        
        for i, t in enumerate(expected_types):
            print(f"{i}. {t}")
        
        assert len(nodes) == len(expected_types)
        for node, expected_type in zip(nodes, expected_types):
            assert node.text_type == expected_type

    def test_text_node_separation(self):
        text = "Hello**bold**.*italic*,`code`."
        nodes = text_to_textnodes(text)
        
        expected_types = [
            TextType.TEXT,   # "Hello"
            TextType.BOLD,   # "bold"
            TextType.TEXT,   # "."
            TextType.ITALIC, # "italic"
            TextType.TEXT,   # ","
            TextType.CODE,   # "code"
            TextType.TEXT,   # "."
        ]
        assert len(nodes) == len(expected_types)
        for node, expected_type in zip(nodes, expected_types):
            assert node.text_type == expected_type

if __name__ == "__main__":
    unittest.main()