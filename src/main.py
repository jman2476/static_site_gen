from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from copy_static import delete_public_dir, create_empty_public_dir, copy_directory_contents
from page_gen import generate_page_recursive


def main():
    # create_empty_public_dir()
    copy_directory_contents('./static', './public')
    generate_page_recursive('content', 'template.html', 'public')



main()
