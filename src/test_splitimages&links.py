import unittest
from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images ,extract_markdown_links
from splitimglink import split_nodes_image, split_nodes_link

class TestSplitFunctions(unittest.TestCase):
    
    # TESTS WITH SPLIT IMAGE FUNCTION
    
    def test_no_images_in_text(self):
        test = split_nodes_image([TextNode("This is a simple piece of text.", TextType.TEXT)])
        expected = [TextNode("This is a simple piece of text.", TextType.TEXT)]
        self.assertEqual(test, expected)
    
    def test_single_image(self):
        test = split_nodes_image([TextNode("Here is an image: ![alt text](http://image.url)", TextType.TEXT)])
        expected = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "http://image.url"),
        ]
        self.assertEqual(test, expected)

    def test_multiple_images(self):
        test = split_nodes_image([TextNode("![image1](http://url1) and ![image2](http://url2)", TextType.TEXT)])
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "http://url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "http://url2"),
        ]
        self.assertEqual(test, expected)

    def test_text_between_images(self):
        test = split_nodes_image([TextNode("Start ![img1](url1) middle ![img2](url2) end", TextType.TEXT)])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(test, expected)
    
    def test_no_text_between_images(self):
        test = split_nodes_image([TextNode("Start ![img1](url1)![img2](url2) end", TextType.TEXT)])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(test, expected)

    # TESTS WITH SPLIT LINK FUNCTION

    def test_single_link(self):
        # Test a simple case with one link
        test = split_nodes_link([TextNode("This is a [link](https://boot.dev) test", TextType.TEXT)])
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" test", TextType.TEXT)
        ]
        self.assertEqual(test, expected)

    def test_multiple_links(self):
        # Test multiple links with text between them
        test = split_nodes_link([TextNode("Click [here](url1) and [there](url2)", TextType.TEXT)])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("there", TextType.LINK, "url2")
        ]
        self.assertEqual(test, expected)

    def test_no_links(self):
        # Test text with no links
        node = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_adjacent_links(self):
        # Test links with no text between them
        test = split_nodes_link([TextNode("[link1](url1)[link2](url2)", TextType.TEXT)])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2")
        ]
        self.assertEqual(test, expected)

    def test_special_characters_in_link(self):
        # Test links containing special characters
        test = split_nodes_link([
            TextNode("[!@#$%^&*()](/url) and [../path](../test/url)", TextType.TEXT)
        ])
        expected = [
            TextNode("!@#$%^&*()", TextType.LINK, "/url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("../path", TextType.LINK, "../test/url")
        ]
        self.assertEqual(test, expected)

    def test_complex_urls(self):
        # Test various URL formats
        test = split_nodes_link([
            TextNode("[link](https://test.com?param=1&other=2#fragment)", TextType.TEXT)
        ])
        expected = [
            TextNode("link", TextType.LINK, "https://test.com?param=1&other=2#fragment")
        ]
        self.assertEqual(test, expected)

    def test_multiple_adjacent_positions(self):
        # Test adjacent links at start, middle, and end
        test = split_nodes_link([
            TextNode("[one](1)[two](2) text [three](3)[four](4)", TextType.TEXT)
        ])
        expected = [
            TextNode("one", TextType.LINK, "1"),
            TextNode("two", TextType.LINK, "2"),
            TextNode(" text ", TextType.TEXT),
            TextNode("three", TextType.LINK, "3"),
            TextNode("four", TextType.LINK, "4")
        ]
        self.assertEqual(test, expected)

if __name__ == "__main__":
    unittest.main()