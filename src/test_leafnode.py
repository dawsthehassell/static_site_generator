import unittest


from htmlnode import HTMLNode
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tag_and_value(self):
        node = LeafNode("a", "click here!")
        self.assertEqual(node.to_html(), "<a>click here!</a>")
   
    def test_tag_value_properties(self):
        node = LeafNode("a", "click here!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">click here!</a>')

    def test_with_none_tag(self):
        node = LeafNode(None, "click here!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), 'click here!')

    def test_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)

if __name__ == "__main__":
    unittest.main()