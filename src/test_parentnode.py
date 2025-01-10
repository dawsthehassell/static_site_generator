import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_basic_parent_with_leaf_children(self):
        node1 = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = "<div><b>Bold text</b>Normal text</div>"
        self.assertEqual(node1.to_html(), expected)

    def test_parent_with_props(self):
        node2 = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "greeting"}
        )
        expected = '<div class="greeting"><p>Hello</p></div>'
        self.assertEqual(node2.to_html(), expected)

    def test_nested_parent_nodes(self):
        node3 = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("span", "Nested")]
                )
            ]
        )
        expected = "<div><p><span>Nested</span></p></div>"
        self.assertEqual(node3.to_html(), expected)

    def test_error_cases(self):
        # Test missing tag
        with self.assertRaises(ValueError):
            bad_node = ParentNode(None, [LeafNode("p", "test")])
            bad_node.to_html()

        # Test empty children
        with self.assertRaises(ValueError):
            bad_node2 = ParentNode("div", [])
            bad_node2.to_html()

if __name__ == "__main__":
    unittest.main()