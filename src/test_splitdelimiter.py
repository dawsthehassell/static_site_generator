import unittest
from markdown_textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("Hello **world** today", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " today")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_no_spaces(self):
        node = TextNode("Hello**world**today", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, "today")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_invalid_markdown_exception(self):
        node = TextNode("Hello **world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_delimited_sections(self):
        node = TextNode("Text with **bold** and more **bold** words", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Text with ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[2].text, " and more ")
        self.assertEqual(nodes[3].text, "bold")
        self.assertEqual(nodes[4].text, " words")

    def test_code_blocks(self):
        node = TextNode("Here is `code` and more `code` blocks", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Here is ")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " and more ")
        self.assertEqual(nodes[3].text_type, TextType.CODE)
        self.assertEqual(nodes[4].text, " blocks")

    def test_empty_delimited_content(self):
        node = TextNode("Text with **** empty bold", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Text with ")
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[2].text, " empty bold")

if __name__ == "__main__":
    unittest.main()
