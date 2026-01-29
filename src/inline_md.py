import re
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
            print('Error causing parts', delimiter, parts)
            raise ValueError('Invalid Markdown syntax')
        start_text = TextNode(parts[0], TextType.TEXT)
        split_text = TextNode(parts[1], text_type) 
        last_text = TextNode(parts[2], TextType.TEXT)
        end_nodes = split_node_delimiter([last_text], delimiter, text_type)
        new_nodes.extend([start_text, split_text, *end_nodes])

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        to_add = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        alt_text, url = images[0]
        split = node.text.split(
            f'![{alt_text}]({url})', 1
        )
        start_node = TextNode(split[0], TextType.TEXT)
        img_node = TextNode(alt_text, TextType.IMAGE, url)
        end_text = TextNode(split[1], TextType.TEXT)
        end_nodes = split_nodes_image([end_text])
        if start_node.text != '' and start_node.text != None:
            to_add.append(start_node)
        to_add.append(img_node)
        to_add.extend(clean_empty_text_nodes(end_nodes))
        new_nodes.extend(to_add)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        to_add = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        anchor_txt, url = links[0]
        split = node.text.split(
            f'[{anchor_txt}]({url})', 1
        )
        start_node = TextNode(split[0], TextType.TEXT)
        link_node = TextNode(anchor_txt, TextType.LINK, url)
        end_text = TextNode(split[1], TextType.TEXT)
        end_nodes = split_nodes_link([end_text])
        if start_node.text != '' and start_node.text != None:
            to_add.append(start_node)
        to_add.append(link_node)
        to_add.extend(clean_empty_text_nodes(end_nodes))
        new_nodes.extend(to_add)

    return new_nodes

def clean_empty_text_nodes(node_list):
    clean_nodes = []
    for node in node_list:
        if node.text_type == TextType.TEXT: 
            if node.text == '' or node.text == None:
                continue
        clean_nodes.append(node)
    return clean_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [
        ('_', TextType.ITALIC),
        ('**', TextType.BOLD),
        ('`', TextType.CODE),
    ]
    with_imgs = split_nodes_image(text_nodes)    
    all_nodes = split_nodes_link(with_imgs)
    
    for char, type in delimiters:
        all_nodes = split_node_delimiter(all_nodes, char, type)
        

    return all_nodes