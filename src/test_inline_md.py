import unittest
from inline_md import (
    split_node_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
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
        #print('\nSplit delimit italic')
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
        #print('\nSplit delimit bold')
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
        #print('\nSplit delimit code')
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
        #print('\nSplit delimit multi')
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
        #print('\nSplit delimit error')
        node = TextNode(self.bad_syntax, TextType.TEXT)
        with self.assertRaises(
            ValueError, msg='Invalid Markdown syntax'):
            split_node_delimiter([node], '**', TextType.BOLD)

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.image = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.links =  "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.nill = "Plaalsdkfjas;dlfjasdl;kfjasl sdjfsdkfj23ruewoiuncmvncvcvcmvn,vijfsdjfa"
        
    def test_extract_markdown_images(self):
        #print('\nExtract md images')
        matches = extract_markdown_images(self.images)
        self.assertListEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ], matches
        )
        match = extract_markdown_images(self.image)
        self.assertListEqual(
            [('image', 'https://i.imgur.com/zjjcJKZ.png')],
            match
        )
    
    def test_extract_markdown_links(self):
        #print('\nExtract md links')
        matches = extract_markdown_links(self.links)
        self.assertListEqual(
            [
                ('to boot dev', 'https://www.boot.dev'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev')
            ], matches
        )

class TestSplitImgLink(unittest.TestCase):
    def setUp(self):
        self.node_imgs = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.node_links = TextNode(
            "This is text with links, so [here's an image](https://i.imgur.com/zjjcJKZ.png) and another [freeking second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.link_start = TextNode(
            '[What happens if we start](https://www.youtube.com/watch?v=dQw4w9WgXcQ) our text node with a link?',
            TextType.TEXT
        )
        self.img_only = TextNode(
            '![This isnt the best image in the world](https://upload.wikimedia.org/wikipedia/en/3/34/RickAstleyNeverGonnaGiveYouUp7InchSingleCover.jpg)',
            TextType.TEXT
        )
        self.img_link_mix = TextNode(
            'Here is a little picture of a kitty cat: ![kitty kitty cat](https://scz.org/wp-content/uploads/2021/09/snow-leopard-sedgwick-county-zoo-1024x727.jpg) and here is link to a video of the kitty cat: [click me to see kitty cat!](https://www.youtube.com/shorts/HwnnkJWbbG8) Is he not the cutest?',
            TextType.TEXT
        )

    def test_split_images(self):
        new_nodes = split_nodes_image([self.node_imgs])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        new_nodes = split_nodes_link([self.node_links])
        self.assertListEqual(
            [
                TextNode("This is text with links, so ", TextType.TEXT),
                TextNode("here's an image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "freeking second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_start(self):
        new_nodes = split_nodes_link([self.link_start])
        self.assertListEqual(
            [
                TextNode('What happens if we start', TextType.LINK, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                TextNode(' our text node with a link?', TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_img_only(self):
        new_nodes = split_nodes_image([self.img_only])
        self.assertListEqual(
            [
                TextNode('This isnt the best image in the world', TextType.IMAGE, 'https://upload.wikimedia.org/wikipedia/en/3/34/RickAstleyNeverGonnaGiveYouUp7InchSingleCover.jpg')
            ],
            new_nodes
        )
    
    def test_split_link_then_image(self):
        new_nodes = split_nodes_link([self.img_link_mix])
        newer_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode('Here is a little picture of a kitty cat: ', TextType.TEXT),
                TextNode('kitty kitty cat', TextType.IMAGE, 'https://scz.org/wp-content/uploads/2021/09/snow-leopard-sedgwick-county-zoo-1024x727.jpg'),
                TextNode(' and here is link to a video of the kitty cat: ', TextType.TEXT),
                TextNode('click me to see kitty cat!', TextType.LINK, 'https://www.youtube.com/shorts/HwnnkJWbbG8'),
                TextNode(' Is he not the cutest?', TextType.TEXT)
            ],
            newer_nodes
        )

    def test_split_image_then_link(self):
        new_nodes = split_nodes_image([self.img_link_mix])
        newer_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode('Here is a little picture of a kitty cat: ', TextType.TEXT),
                TextNode('kitty kitty cat', TextType.IMAGE, 'https://scz.org/wp-content/uploads/2021/09/snow-leopard-sedgwick-county-zoo-1024x727.jpg'),
                TextNode(' and here is link to a video of the kitty cat: ', TextType.TEXT),
                TextNode('click me to see kitty cat!', TextType.LINK, 'https://www.youtube.com/shorts/HwnnkJWbbG8'),
                TextNode(' Is he not the cutest?', TextType.TEXT)
            ],
            newer_nodes
        )

class TestTxtToNodes(unittest.TestCase):
    def setUp(self):
        self.text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.no_link = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link'


    def test_txt_to_node_one_each(self):
        node_list = text_to_textnodes(self.text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list
        )
    
    def test_txt_to_nodes_no_link(self):
        node_list = text_to_textnodes(self.no_link)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a link", TextType.TEXT),
            ],
            node_list
        )
    

if __name__ == '__main__':
    unittest.main()