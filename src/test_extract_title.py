import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Simple Title"
        self.assertEqual(extract_title(markdown), "Simple Title")

    def test_title_with_spaces(self):
        markdown = "#      example title    "
        self.assertEqual(extract_title(markdown), "example title")

    def test_missing_title(self):
        markdown = "No title here\nStill no title\n## Not an h1"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_wrong_header_format(self):
        markdown = "#Header but wrong format"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_not_h1_headers(self):
        markdown = "## header 2\n### header 3"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == '__main__':
    unittest.main()