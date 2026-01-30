import unittest
from page_gen import extract_title

class TestPageGeneration(unittest.TestCase):
    def test_extract_title(self):
        md = '# Hello, how are you?'
        md2 = """
# This is a title

## This is a subheading
"""
        md3 = """# Title

#Not Title"""

        title1 = extract_title(md)
        title2 = extract_title(md2)
        title3 = extract_title(md3)

        self.assertEqual(title1, 'Hello, how are you?')
        self.assertEqual(title2, 'This is a title')
        self.assertEqual(title3, 'Title')

    def test_extract_title_err(self):
        md = "Hello, how's it going?"
        
        with self.assertRaises(ValueError, msg="No title found in markdown"):
            extract_title(md)


