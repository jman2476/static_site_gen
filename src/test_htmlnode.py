import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMLNode('a', 'Bananas', [], {'href':'https://www.google.com', 'height':'30'})
        self.li1 = HTMLNode('li', 'Pancakes', props={'hidden':'false'})
        self.li2 = HTMLNode('li', 'Tasty ', [self.node], {'id':'3'})
        self.li3 = HTMLNode('li', 'Waffles', props={'lang':'english'})
        self.node2 = HTMLNode('ul', 'Breakfast foods', [self.li1, self.li2, self.li3])
        self.h1 = HTMLNode('h1', 'Hello there')
        
    def test_init(self):
        print('\nHTMLNode initialization')
        self.assertEqual(self.li2.tag, 'li')
        self.assertEqual(self.li2.value, 'Tasty ')
        self.assertEqual(self.li2.children, [self.node])
        self.assertEqual(self.li2.props, {'id':'3'})

    def test_props_to_html(self):
        print('\nHTMLNode props_to_html')
        self.assertEqual(self.node.props_to_html(), ' href="https://www.google.com" height="30"')
        self.assertEqual(self.li1.props_to_html(), ' hidden="false"')
        self.assertEqual(self.li2.props_to_html(), ' id="3"')
        self.assertEqual(self.li3.props_to_html(), ' lang="english"')

    def test_repr(self):
        print('\nHTMLNode repr')
        self.assertEqual(repr(self.node), "HTMLNode(a, Bananas, [], {'href': 'https://www.google.com', 'height': '30'})")
        self.assertEqual(repr(self.h1), "HTMLNode(h1, Hello there, None, None)")

if __name__ == '__main__':
    unittest.main()
