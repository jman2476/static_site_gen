import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def setUp(self):
        self.bold = LeafNode('b', 'BOLD', {'style': 'size:20;'})
        self.p_leaf = LeafNode('p', 'Im trying to be ')
        self.div = ParentNode('div', [self.p_leaf, self.bold])
        self.text = LeafNode(None, 'What are you doing?')
        self.grand_div = ParentNode('div', [self.text,self.div])
        self.li = LeafNode('li', 'list item')
        self.ul = ParentNode('ul', [self.li, self.li, self.li])
        self.body = ParentNode('body', [self.div, self.ul])
        self.no_tag = ParentNode(None, [self.ul])
        self.no_child = ParentNode('head', [])

    def test_to_html_err(self):
        print('\nParentNode  to_html errors')
        with self.assertRaises(
                ValueError, msg='No tag given for parent'
                ):
            self.no_tag.to_html()
        with self.assertRaises(
                ValueError, msg='\nParentNode  has no children. Womp womp'
                ):
            self.no_child.to_html()

    def test_to_html_children(self):
        print('\nParentNode  to_html children')
        self.assertEqual(
                self.div.to_html(),
                '<div><p>Im trying to be </p><b style="size:20;">BOLD</b></div>'
                )
        self.assertEqual(
                self.ul.to_html(),
                '<ul><li>list item</li><li>list item</li><li>list item</li></ul>'
                )

    def test_to_html_grandchildren(self):
        print('\nParentNode  to_html grandchildren')
        self.assertEqual(
                self.body.to_html(),
                '<body><div><p>Im trying to be </p><b style="size:20;">BOLD</b></div><ul><li>list item</li><li>list item</li><li>list item</li></ul></body>'
                )
