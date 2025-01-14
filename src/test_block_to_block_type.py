import unittest

from block_to_block_type import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_cases(self):
        test_blocks = [
    # Code block
    '''```
some code here
more code
```''',
    
    # Heading (valid)
    '### This is a heading',
    
    # Heading (invalid - 7 #'s)
    '####### Too many hashes',
    
    # Quote
    '''>This is a quote
>This is still the quote
>And this too''',
    
    # Unordered list
    '''* First item
* Second item
* Third item''',
    
    # Ordered list
    '''1. First
2. Second
3. Third''',
    
    # Invalid ordered list (wrong numbers)
    '''1. First
3. Second
4. Third''',
    
    # Regular paragraph
    '''This is just
a regular paragraph
of text'''
]

        # Test each block
        for block in test_blocks:
            print(f"Type: {block_to_block_type(block)}")
            print(f"Text: {block}")
            print("-" * 40)
    
if __name__ == "__main__":
    unittest.main()