import unittest
from functions import split_node_delimiter
from textnode import TextType, TextNode

class TestSplitNodeDelimit(unittest.TestCase):
    def setUp(self):
        self.bold = 'This text has **inline bold** in it'
        self.italic = 'Here is some _malto bene_ italic text'
        self.code = 'Cricket, what\'s wrong with `x=357` in my C code?'
        self.multi_bold = 'Some things are **so bold** that you need **extra** emphasis'
        self.multi_mix = 'When words are **bold**, it seems like screaming. That\'s why I need _italic text_ for my emphasis'
        self.bad_syntax = 'You know when you go to write **bold text but you forgot to close it?'
        self.italic_end = 'For greatest effect, end your sentences with _emphasis_'

    def test_split_italic(self):
        print('\nSplit delimit italic')
        node1 = TextNode(self.italic, TextType.TEXT)
        node2 = TextNode(self.italic_end, TextType.TEXT)
        new_italic = split_node_delimiter([node1], '_', TextType.ITALIC)
        long_italic = split_node_delimiter([node1,node2], '_', TextType.ITALIC)
        self.assertEqual(
            new_italic,
            [
                TextNode('Here is some ', TextType.TEXT),
                TextNode('malto bene', TextType.ITALIC),
                TextNode(' italic text', TextType.TEXT),
            ]
        )
        self.assertEqual(
            long_italic,
            [
                TextNode('Here is some ', TextType.TEXT),
                TextNode('malto bene', TextType.ITALIC),
                TextNode(' italic text', TextType.TEXT),
                TextNode('For greatest effect, end your sentences with ', TextType.TEXT),
                TextNode('emphasis', TextType.ITALIC),
                TextNode('', TextType.TEXT),
                
            ]
        )

    def test_split_bold(self):
        print('\nSplit delimit bold')
        node = TextNode(self.bold, TextType.TEXT)
        bold = split_node_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(
            bold,
            [
                TextNode('This text has ', TextType.TEXT),
                TextNode('inline bold', TextType.BOLD),
                TextNode(' in it', TextType.TEXT),
            ]
        )

    def test_split_code(self):        
        print('\nSplit delimit code')
        node = TextNode(self.code, TextType.TEXT)
        code = split_node_delimiter([node], '`', TextType.CODE)
        self.assertEqual(
            code,
            [
                TextNode('Cricket, what\'s wrong with ', TextType.TEXT),
                TextNode('x=357', TextType.CODE),
                TextNode(' in my C code?', TextType.TEXT),
            ]
        )

    def test_split_multi(self):
        print('\nSplit delimit multi')
        node1 = TextNode(self.multi_bold, TextType.TEXT)
        node2 = TextNode(self.multi_mix, TextType.TEXT)
        bold = split_node_delimiter([node1], '**', TextType.BOLD)
        self.assertEqual(
            bold,
            [
                TextNode('Some things are ', TextType.TEXT),
                TextNode('so bold', TextType.BOLD),
                TextNode(' that you need ', TextType.TEXT),
                TextNode('extra', TextType.BOLD),
                TextNode(' emphasis', TextType.TEXT),
            ]
        )
        mix = split_node_delimiter([node2], '**', TextType.BOLD)
        self.assertEqual(
            mix,
            [
                TextNode('When words are ', TextType.TEXT),
                TextNode('bold', TextType.BOLD),
                TextNode(', it seems like screaming. That\'s why I need _italic text_ for my emphasis', TextType.TEXT),
            ]
        )
        
    def test_split_err(self):
        print('\nSplit delimit error')
        node = TextNode(self.bad_syntax, TextType.TEXT)
        with self.assertRaises(
            ValueError, msg='Invalid Markdown syntax'):
            split_node_delimiter([node], '**', TextType.BOLD)

if __name__ == '__main__':
    unittest.main()