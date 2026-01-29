# static_site_gen
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
