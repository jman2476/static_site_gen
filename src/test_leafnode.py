import unittest
from htmlnode import LeafNode, HTMLNode

class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.p_leaf = LeafNode('p', 'Hello, world!')
        self.p_html = HTMLNode('p', 'Hello, world!')
        self.br = LeafNode('br', None)
        self.h1 = LeafNode('h1', 'Im a header', props={'style':'color:red;flex:true'})
        self.empty = LeafNode('p', None)
        
    def test_init(self):
        print('\nTesting LeafNode initialization')
        self.assertEqual(self.h1.tag, 'h1')
        self.assertEqual(self.h1.value, 'Im a header')
        self.assertEqual(self.h1.props, {'style':'color:red;flex:true'})

    def test_to_html(self):
        print('\nTesting to_html')
        with self.assertRaises(
                ValueError,
                msg='Tag empty. Must have value or be valid empty tag'
                ):
            self.empty.to_html()
        self.assertEqual(
                self.p_leaf.to_html(),
                '<p>Hello, world!</p>'
                )
        self.assertEqual(
                self.br.to_html(), '<br>'
                )
        self.assertEqual(
                self.h1.to_html(),
                '<h1 style="color:red;flex:true">Im a header</h1>'
                )


    def test_repr(self):
        print('\nTesting LeafNode repr')
        self.assertEqual(
                repr(self.h1),
                "LeafNode(h1, Im a header, {'style': 'color:red;flex:true'})"
                )
        self.assertNotEqual(
                repr(self.p_leaf),
                repr(self.p_html)
                )

if __name__ == '__main__':
    unittest.main()
