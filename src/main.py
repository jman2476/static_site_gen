from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from page_gen import delete_public_dir, create_empty_public_dir, copy_directory_contents


def main():
    # create_empty_public_dir()
    copy_directory_contents('./static', './public')


main()
