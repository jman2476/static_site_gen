import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def setUp(self):
        # set all the test nodes
        self.node = TextNode('This is a text node', TextType.BOLD)
        self.node2 = TextNode('This is a text node', TextType.BOLD)
        self.node3 = TextNode('This is another text node', TextType.BOLD)
        self.node4 = TextNode('What a wonderful Italian day', TextType.ITALIC, url='rail.it')
        self.node5 = TextNode('What a wonderful Italian day', TextType.ITALIC, url='rails.it')
        self.node6 = TextNode('Just plain', TextType.TEXT, url='')
        self.node7 = TextNode('Just plain', TextType.TEXT, '')


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


class TestTextToHTMLNode(unittest.TestCase):
    def setUp(self):
        # test nodes for text_to_html:
        self.plain = TextNode('Plain text', TextType.TEXT)
        self.bold = TextNode('Bold text', TextType.BOLD)
        self.italic = TextNode('Italic text', TextType.ITALIC)
        self.code = TextNode('Code block', TextType.CODE)
        self.link = TextNode(
            'Link text', 
            TextType.LINK, 
            'https://google.com')
        self.image = TextNode(
            'Alt image text',
            TextType.IMAGE,
            'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patates.jpg/2560px-Patates.jpg'
        )
        self.none = TextNode('None type', None)

    def test_plain_to_html(self):
        print('\nTextToHTML plain')
        plain_node = text_node_to_html_node(self.plain)
        self.assertEqual(plain_node.tag, None)
        self.assertEqual(plain_node.value, 'Plain text')

    def test_bold_to_html(self):
        print('\nTextToHTML bold')
        bold_node = text_node_to_html_node(self.bold)
        self.assertEqual(bold_node.tag, 'b')
        self.assertEqual(bold_node.value, 'Bold text')

    def test_italic_to_html(self):
        print('\nTextToHTML italic')
        italic_node = text_node_to_html_node(self.italic)
        self.assertEqual(italic_node.tag, 'i')
        self.assertEqual(italic_node.value, 'Italic text')

    def test_code_to_html(self):
        print('\nTextToHTML code')
        code_node = text_node_to_html_node(self.code)
        self.assertEqual(code_node.tag, 'code')
        self.assertEqual(code_node.value, 'Code block')

    def test_link_to_html(self):
        print('\nTextToHTML link')
        link_node = text_node_to_html_node(self.link)
        self.assertEqual(link_node.tag, 'a')
        self.assertEqual(
            link_node.value, 
            'Link text',
            {'href': 'https://google.com'}
            )
        
    def test_img_to_html(self):
        print('\nTextToHTML image')
        image_node = text_node_to_html_node(self.image)
        self.assertEqual(image_node.tag, 'img')
        self.assertEqual(image_node.value, None)
        self.assertEqual(
            image_node.props, 
            {
                'alt': 'Alt image text',
                'src': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patates.jpg/2560px-Patates.jpg'
            })
        
    def test_none_to_html(self):
        print('\nTextToHTML none')
        with self.assertRaises(
            ValueError, msg='Text type not in TextType enum'):
            text_node_to_html_node(self.none)
    
      
if __name__ == '__main__':
    unittest.main()
