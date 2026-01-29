from htmlnode import(
    LeafNode,ParentNode
)
from textnode import(
    TextNode, TextType,
    text_node_to_html_node
)
from inline_md import text_to_textnodes
from block_md import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType, block_to_lines
)

def markdown_to_block_tuples(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks == []:
        raise ValueError('Markdown file is empty.')
    block_tuples = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_tuples.append((block,block_type))
    return block_tuples

def markdown_to_html_node(markdown):
    # 1. md to blocks
    # 2. block to textnode
    # 3. textnode to htmlnode(already exists)
    # 4. put children into parents
    # 5. Profit
    parent_div = ParentNode('div', [])
    children = []
    blocks = markdown_to_block_tuples(markdown)

    for block, b_type in blocks:
        if b_type != BlockType.CODE:
            new_parent = text_to_children(block,b_type)
            children.append(new_parent)

        else:
            trim_code = block.strip('`\n')
            code_node = TextNode(trim_code+'\n', TextType.CODE)
            code_html = text_node_to_html_node(code_node)
            code_parent = ParentNode('pre', [code_html])
            children.append(code_parent)    
        
    if len(children) == 0:
        raise RuntimeError(
            'Child nodes not appended to Parent <div>')
    parent_div.children = children
    return parent_div

def text_to_children(text, block_type):
    new_parent = None

    match block_type:
        case BlockType.PARAGRAPH:
            new_parent = handle_paragraph(text)
        case BlockType.HEADING:
            new_parent = handle_heading(text)
        case BlockType.QUOTE:
            new_parent = handle_quote(text)
        case BlockType.OLIST:
            new_parent = handle_list(True)(text)
        case BlockType.ULIST:
            new_parent = handle_list()(text)
    if new_parent is None:
        raise ValueError('Issue converting text to children')
    return new_parent

def _trim_to_htmlnode(trim_text):
    text_nodes = text_to_textnodes(trim_text)
    html_nodes = []
    for text in text_nodes:
        html = text_node_to_html_node(text)
        html_nodes.append(html)
    return html_nodes

def _trim_newline(text):
    return ' '.join(text.split('\n'))

def handle_paragraph(text):
    parent = ParentNode('p', [])
    trimmed = _trim_newline(text)
    children = _trim_to_htmlnode(trimmed)
    parent.children.extend(children)
    return parent

def handle_heading(text):
    split_head = text.split(' ',1)
    level = split_head[0].count('#')
    parent = ParentNode(f'h{level}', [])
    children = _trim_to_htmlnode(split_head[1])
    parent.children.extend(children)
    print('heading parent', parent)
    return parent

def handle_quote(text):
    parent = ParentNode('blockquote', [])
    quote_text = []
    lines = block_to_lines(text)
    for line in lines:
        trim = line.strip('> ')
        quote_text.append(trim)
    quote = ' '.join(quote_text)
    parent.children.extend(_trim_to_htmlnode(quote))
    return parent

def handle_list(ordered=False):

    def handle_ordered(block):
        parent = ParentNode('ol', [])
        items = block_to_lines(block)
        for item in items:
            trimmed = item[2:].strip()
            html_nodes = _trim_to_htmlnode(trimmed)
            li_item = ParentNode('li', html_nodes)
            parent.children.append(li_item)
        return parent
    
    def handle_unordered(block):
        parent = ParentNode('ul', [])
        items = block_to_lines(block)
        for item in items:
            trimmed = item.strip('- ')
            html_nodes = _trim_to_htmlnode(trimmed)
            li_item = ParentNode('li', html_nodes)
            parent.children.append(li_item)
        return parent
    
    if ordered:
        return handle_ordered
    return handle_unordered