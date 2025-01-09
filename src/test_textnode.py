import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("hello", TextType.ITALIC_TEXT)
        node2 = TextNode("hello", TextType.ITALIC_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Hello World", TextType.BOLD_TEXT)
        node2 = TextNode("hello world", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("hello", TextType.BOLD_TEXT, url="https://url1.com")
        node2 = TextNode("hello", TextType.BOLD_TEXT, url="https://url2.com")
        self.assertNotEqual(node, node2)

    def test_string_edge(self):
        node = TextNode("", TextType.BOLD_TEXT, url="https://url2.com")
        node2 = TextNode(None, TextType.BOLD_TEXT, url="https://url2.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()