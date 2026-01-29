import unittest

from block_md import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestMarkdown2Block(unittest.TestCase):
    def setUp(self):
        self.md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.md_lists = """
1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.

⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses

1. Make my changes
    1. Fix bug
    2. Improve formatting
        - Make the headings bigger
2. Push my commits to GitHub
3. Open a pull request
    * Describe my changes
    * Mention all the members of my team
        * Ask for feedback

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!"""
        self.empty = """






"""
        self.extra_spaces = """
        
        
        This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items


"""
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(self.md)
        self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ]
            )

    def test_markdown_to_blocks_long(self):
        blocks = markdown_to_blocks(self.md_lists)
        self.assertListEqual(
            blocks,
            [
                """1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.""",
                "⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).",
                """⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)""",
                """* Unordered list can use asterisks
- Or minuses
+ Or pluses""",
                """1. Make my changes
    1. Fix bug
    2. Improve formatting
        - Make the headings bigger
2. Push my commits to GitHub
3. Open a pull request
    * Describe my changes
    * Mention all the members of my team
        * Ask for feedback""",
                """+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!"""
            ]
        )

    def test_empty_markdown(self):
        blocks = markdown_to_blocks(self.empty)
        self.assertEqual(blocks, [])

    def test_extra_spaces_markdown(self):
        blocks = markdown_to_blocks(self.extra_spaces)
        self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ]
            )
        
class TestBlock2BlockType(unittest.TestCase):
    def setUp(self):
        self.plain = """
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32."""
        self.code = """
```
def test_to_html_children(self):
        #print('\nParentNode  to_html children')
        self.assertEqual(
                self.div.to_html(),
                '<div><p>Im trying to be </p><b style="size:20;">BOLD</b></div>'
                )
        self.assertEqual(
                self.ul.to_html(),
                '<ul><li>list item</li><li>list item</li><li>list item</li></ul>'
                )
```

and an invalid code block:

```const x = 69```
"""
        self.quote="""
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
>   -- John Donne"""
        self.lists="""-This
-is
-a
-valid
-list

+this
+too

-but
+not
-this

1.this
2.is
3.valid
4.for
5.ordered
6.lists

1.this
2isn't
3.valid
4.for
5.ordered
6.lists

1.neither
1.is
3.this"""
        self.head="""
# Valid

#Invalid

## Still good

### good

#### good

##### good

###### good

####### bad

#"""
        self.file="""# static_site_gen
Serves a static site, following boot.dev

## Here is a test of block to blocktype

Here is a paragraph that is double spaced under its heading. 
Hooray!
We ams special!

### Here is a test of codeblock

```
def test_to_html_children(self):
        #print('\nParentNode  to_html children')
        self.assertEqual(
                self.div.to_html(),
                '<div><p>Im trying to be </p><b style="size:20;">BOLD</b></div>'
                )
        self.assertEqual(
                self.ul.to_html(),
                '<ul><li>list item</li><li>list item</li><li>list item</li></ul>'
                )
```

and an invalid code block:

```const x = 69```

### And quotes:

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
>   -- John Donne

>Dis
is
>not
>valid
>quote

### and lists

-This
-is
-a
-valid
-list

+this
+too

-but
+not
-this

1.this
2.is
3.valid
4.for
5.ordered
6.lists

1.this
2isn't
3.valid
4.for
5.ordered
6.lists

1.neither
1.is
3.this
"""

    def test_paragraph_block(self):
        blocks = markdown_to_blocks(self.plain)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [BlockType.PARAGRAPH],
            block_types
        )

    def test_code_block(self):
        blocks = markdown_to_blocks(self.code)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH
            ],
            block_types
        )

    def test_quote_block(self):
        blocks = markdown_to_blocks(self.quote)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [BlockType.QUOTE],
            block_types
        )

    def test_list_block(self):
        blocks = markdown_to_blocks(self.lists)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.ULIST,
                BlockType.ULIST,
                BlockType.PARAGRAPH,
                BlockType.OLIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            block_types
        )

    def test_header_block(self):
        blocks = markdown_to_blocks(self.head)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            block_types
        )

    def test_all_block_types(self):
        blocks = markdown_to_blocks(self.file)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.ULIST,
                BlockType.ULIST,
                BlockType.PARAGRAPH,
                BlockType.OLIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
            block_types
        )