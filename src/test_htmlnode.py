import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello", None, None)
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_one_prop(self):
        node = HTMLNode("a", "click me", None,{"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    def test_props_to_html_multi_props(self):
        node = HTMLNode("a", "click me", None, {
        "href": "https://www.google.com",
        "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
if __name__ == "__main__":
    unittest.main()