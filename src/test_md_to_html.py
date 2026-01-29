from md_to_html import markdown_to_html_node
import unittest

class TestMarkdown2HTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading level 1

## Heading level 2

### Heading level 3

#### Heading **level** 4

##### Heading _level_ 5

###### Heading level 6

### Heading with a snek ![python](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Ball_python_lucy.JPG/250px-Ball_python_lucy.JPG) """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Heading level 1</h1><h2>Heading level 2</h2><h3>Heading level 3</h3><h4>Heading <b>level</b> 4</h4><h5>Heading <i>level</i> 5</h5><h6>Heading level 6</h6><h3>Heading with a snek <img alt="python" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Ball_python_lucy.JPG/250px-Ball_python_lucy.JPG"></h3></div>'
        )
        pass

    def test_quote(self):
        md = """
>No man is an island,
>Entire of itself.
>Each is a piece of the continent,
> A part of the main.
>  If a clod be washed away by the sea,
>Europe is the less.
> As well as if a promontory were.
>As well as if a manor of thine own
>Or of thine friend's were.
>Each man's death diminishes me,
>For I am involved in mankind.
>Therefore, send not to know
>For whom the bell tolls,
>It tolls for thee.
>   -- [John Donne](https://en.wikipedia.org/wiki/John_Donne)"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>No man is an island, Entire of itself. Each is a piece of the continent, A part of the main. If a clod be washed away by the sea, Europe is the less. As well as if a promontory were. As well as if a manor of thine own Or of thine friend\'s were. Each man\'s death diminishes me, For I am involved in mankind. Therefore, send not to know For whom the bell tolls, It tolls for thee. -- <a href="https://en.wikipedia.org/wiki/John_Donne">John Donne</a></blockquote></div>'
        )

    def test_unordered_list(self):
        md = """
-item 1
-item 3
-item 2
-item 46"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>item 1</li><li>item 3</li><li>item 2</li><li>item 46</li></ul></div>'
        )

    def test_ordered_list(self):
        md = """
1. item 1
2. item 2
3. item 3
4. item 4"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li></ol></div>'
        )


