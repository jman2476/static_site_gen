import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def setUp(self):
        # set all the test nodes
        self.node = TextNode('This is a text node', TextType.BOLD)
        self.node2 = TextNode('This is a text node', TextType.BOLD)
        self.node3 = TextNode('This is another text node', TextType.BOLD)
        self.node4 = TextNode('What a wonderful Italian day', TextType.ITALIC, url='rail.it')
        self.node5 = TextNode('What a wonderful Italian day', TextType.ITALIC, url='rails.it')
        self.node6 = TextNode('Just plain', TextType.PLAIN, url='')
        self.node7 = TextNode('Just plain', TextType.PLAIN, '')

    def test_init(self):
        print('\nTextNode initialization')
        self.assertEqual(self.node4.text, 'What a wonderful Italian day')
        self.assertEqual(self.node4.text_type.value, 'italic')
        self.assertEqual(self.node4.url, 'rail.it')

    def test_eq(self):
        print('\nTextNode equality method')
        self.assertEqual(self.node, self.node2)
        self.assertNotEqual(self.node, self.node3)
        self.assertNotEqual(self.node4, self.node5)
        self.assertEqual(self.node6, self.node7)

    def test_repr(self):
        print('\nTextNode representation')
        self.assertEqual(repr(self.node), f'TextNode(This is a text node, bold, {None})')
        self.assertEqual(repr(self.node4), 'TextNode(What a wonderful Italian day, italic, rail.it)')

if __name__ == '__main__':
    unittest.main()
