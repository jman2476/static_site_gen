from htmlnode import LeafNode
from textnode import TextType, TextNode

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter, 2)
        if len(parts) == 1:
            unsplit = TextNode(parts[0], TextType.TEXT)
            new_nodes.append(unsplit)
            continue
        if len(parts) < 3:
            raise ValueError('Invalid Markdown syntax')
        start_text = TextNode(parts[0], TextType.TEXT)
        split_text = TextNode(parts[1], text_type) 
        last_text = TextNode(parts[2], TextType.TEXT)
        end_nodes = split_node_delimiter([last_text], delimiter, text_type)
        new_nodes.extend([start_text, split_text, *end_nodes])

    return new_nodes