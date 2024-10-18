from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from converters import *
from file_utils import copy_files, generate_page, generate_pages_recursive

TEMPLATE_PATH = "./template.html"


def main():

    copy_files("static", "public", clean_dest=True, log_to_console=True)
    generate_page("content/index.md", TEMPLATE_PATH, "public")
    pass


main()
