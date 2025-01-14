import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Test 1: Basic blocks with single newline separation
        test_md1 = "# Heading\n\nParagraph"
        assert markdown_to_blocks(test_md1) == ["# Heading", "Paragraph"]

    def test_multi_newlines(self):
        # Test 2: Multiple newlines between blocks
        test_md2 = "# Heading\n\n\n\nParagraph"
        assert markdown_to_blocks(test_md2) == ["# Heading", "Paragraph"]

    def test_list_items_with_internal_newlines(self):
        # Test 3: List items with internal newlines
        test_md3 = "# Heading\n\n* Item 1\n* Item 2"
        assert markdown_to_blocks(test_md3) == ["# Heading", "* Item 1\n* Item 2"]

    def test_complex_list(self):
        test_md4 = "* Item 1\n* Item 2\n  * Subitem A\n* Item 3"
        print(markdown_to_blocks(test_md4))
        assert markdown_to_blocks(test_md4) == ["* Item 1\n* Item 2\n  * Subitem A\n* Item 3"]

    def test_trailing_leading_blank_lines(self):
        test_md5 = "\n\n# Header\nContent\n\n"
        assert markdown_to_blocks(test_md5) == ["# Header\nContent"]

    def test_empty_doc(self):
        test_md6 = ""
        assert markdown_to_blocks(test_md6) == []

if __name__ == "__main__":
    unittest.main()
