from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from enum import Enum, auto
import copy
import re


MD_IMAGE_SEC_RGX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
MD_HTML_SEC_RGX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
MD_IMAGE_RGX = r"!\[.*?\]\(.*?\)"
MD_HTML_RGX = r"(?<!!)\[.*?\]\(.*?\)"


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    ORDERED_LIST = auto()
    UNORDERED_LIST = auto()


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT.value:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD.value:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC.value:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE.value:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK.value:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE.value:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unsupported TextType provided")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not TextType.is_valid(text_type):
        raise ValueError("Not a valid TextType")
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown, formatted section not closed\n-------------\n{sections}\n---------------\n"
            )
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(MD_IMAGE_SEC_RGX, text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(MD_HTML_SEC_RGX, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    last_end = 0
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        # Use re.finditer to find all matches of the pattern
        i = 0
        matches = extract_markdown_images(old_node.text)
        split_nodes = []
        for match in re.finditer(MD_IMAGE_RGX, old_node.text):
            start, end = match.span()

            # Add the text before the match as a normal text node
            if start > last_end:
                split_nodes.append(
                    TextNode(old_node.text[last_end:start], TextType.TEXT)
                )

            # Add the matched delimiter as a specific type node
            split_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))

            # Update the last_end to the end of the current match
            last_end = end
            i += 1

        # Add any remaining text after the last match
        if last_end < len(old_node.text):
            split_nodes.append(TextNode(old_node.text[last_end:], TextType.TEXT))

        new_nodes.extend(split_nodes)
        # print("\nNEW NODES: {new_nodes}")
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    last_end = 0
    # print(f"\n||old_nodes = {old_nodes}")
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        # print(f"\n||old_node.text = {old_node.text}")
        # Use re.finditer to find all matches of the pattern
        i = 0
        matches = extract_markdown_links(old_node.text)
        # print(f"\n||matches = {matches}")
        split_nodes = []
        for match in re.finditer(MD_HTML_RGX, old_node.text):
            start, end = match.span()
            # print(f"\n||match = {match}")
            # Add the text before the match as a normal text node
            if start > last_end:
                split_nodes.append(
                    TextNode(old_node.text[last_end:start], TextType.TEXT)
                )
                # print(
                #    f"\n||append text = {old_node.text[last_end:start], TextType.TEXT}"
                # )

            # Add the matched delimiter as a specific type node
            # print(
            #    f"\n||append html = {TextNode(matches[i][0], TextType.LINK, matches[i][1])}"
            # )

            split_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))

            # Update the last_end to the end of the current match
            last_end = end
            i += 1

        # Add any remaining text after the last match
        if last_end < len(old_node.text):
            split_nodes.append(TextNode(old_node.text[last_end:], TextType.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text: str):
    nodes = []
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str):
    blocks = []
    blocks = re.split(r"\n{2,}", markdown)
    return [block.strip() for block in blocks]


def block_to_block_type(md_block: str):
    md_block = md_block.strip()

    if re.match(r"^#{1,6}\s", md_block):
        md_type = BlockType.HEADING
    elif re.match(r"^```", md_block) and md_block.endswith("```"):
        md_type = BlockType.CODE
    elif all(line.startswith("> ") for line in md_block.splitlines()):
        md_type = BlockType.QUOTE
    elif all(re.match(r"^[-*+]\s", line) for line in md_block.splitlines()):
        md_type = BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\.\s", line) for line in md_block.splitlines()):
        md_type = BlockType.ORDERED_LIST
    else:
        md_type = BlockType.PARAGRAPH

    return md_type


def strip_md_block(md_block: str):
    # Determine the block type
    md_type = block_to_block_type(md_block)

    # Strip the Markdown-specific characters and leading/trailing whitespace
    stripped_text = md_block.strip()

    if md_type == BlockType.HEADING:
        # Remove the leading # and any spaces
        stripped_text = re.sub(r"^#{1,6}\s+", "", stripped_text)
    elif md_type == BlockType.CODE:
        # Remove the leading and trailing ```
        stripped_text = re.sub(r"^```|```$", "", stripped_text).strip()
    elif md_type == BlockType.QUOTE:
        # Remove the leading > and spaces for each line
        stripped_text = "\n".join(
            line[2:] for line in stripped_text.splitlines() if line.startswith("> ")
        )
    elif md_type == BlockType.UNORDERED_LIST:
        # Remove the leading -, *, or + and spaces for each line
        stripped_text = "\n".join(
            re.sub(r"^[-*+]\s+", "", line) for line in stripped_text.splitlines()
        )
    elif md_type == BlockType.ORDERED_LIST:
        # Remove the leading number and dot for each line
        stripped_text = "\n".join(
            re.sub(r"^\d+\.\s+", "", line) for line in stripped_text.splitlines()
        )
    # For paragraphs, no special stripping needed beyond whitespace

    return stripped_text, md_type


def parse_markdown(markdown: str):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        stripped_text, block_type = strip_md_block(block)
        result.append((stripped_text, block_type))
    return result


"""
def markdown_to_html(markdown: str) -> HTMLNode:
    html = "<div>"
    nodes = []
    blocks = parse_markdown(markdown)

    for block in blocks:
        print(f"PARSED_BLOCK\n----------\n{block}\n-----------\n")
        

    html += "</div>"
    return html


    block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"



def markdown_to_html(markdown: str) -> HTMLNode:
    nodes = []
    blocks = parse_markdown(markdown)

    for stripped_text, block_type in blocks:
        text_nodes = text_to_textnodes(stripped_text)
        html_children = [text_node_to_html_node(node) for node in text_nodes]

        match block_type:
            case "heading":
                html_node = ParentNode(
                    "h1", html_children
                )  # Assuming all headings as <h1> for now
            case "code":
                html_node = ParentNode("pre", [ParentNode("code", html_children)])
            case "quote":
                html_node = ParentNode("blockquote", html_children)
            case "unordered_list":
                items = [
                    ParentNode(
                        "li",
                        [text_node_to_html_node(TextNode(item.strip(), TextType.TEXT))],
                    )
                    for item in stripped_text.splitlines()
                ]
                html_node = ParentNode("ul", items)
            case "ordered_list":
                items = [
                    ParentNode(
                        "li",
                        [text_node_to_html_node(TextNode(item.strip(), TextType.TEXT))],
                    )
                    for item in stripped_text.splitlines()
                ]
                html_node = ParentNode("ol", items)
            case "paragraph":
                html_node = ParentNode("p", html_children)
            case _:
                raise ValueError("Unsupported block type provided")

        nodes.append(html_node)

    html_parent = ParentNode("div", nodes)
    return html_parent.to_html()
"""


def parse_block(md_block: str) -> HTMLNode:
    stripped_text, block_type = strip_md_block(md_block)

    # Check if the stripped text contains nested Markdown blocks
    if re.search(r"\n{2,}", stripped_text):
        nested_node = parse_markdown(stripped_text)
        match block_type:
            case BlockType.QUOTE:
                return ParentNode("blockquote", [nested_node])
            case BlockType.UNORDERED_LIST:
                items = [
                    ParentNode("li", [parse_block(item.strip())])
                    for item in stripped_text.splitlines()
                ]
                return ParentNode("ul", items)
            case BlockType.ORDERED_LIST:
                items = [
                    ParentNode("li", [parse_block(item.strip())])
                    for item in stripped_text.splitlines()
                ]
                return ParentNode("ol", items)
            case _:
                return nested_node

    # Otherwise, create text nodes for inline elements
    text_nodes = text_to_textnodes(stripped_text)
    html_children = [text_node_to_html_node(node) for node in text_nodes]

    match block_type:
        case BlockType.HEADING:
            return ParentNode(
                "h1", html_children
            )  # Assuming all headings as <h1> for now
        case BlockType.CODE:
            return ParentNode("pre", [ParentNode("code", html_children)])
        case BlockType.QUOTE:
            return ParentNode("blockquote", html_children)
        case BlockType.UNORDERED_LIST:
            items = [
                ParentNode(
                    "li",
                    [text_node_to_html_node(TextNode(item.strip(), TextType.TEXT))],
                )
                for item in stripped_text.splitlines()
            ]
            return ParentNode("ul", items)
        case BlockType.ORDERED_LIST:
            items = [
                ParentNode(
                    "li",
                    [text_node_to_html_node(TextNode(item.strip(), TextType.TEXT))],
                )
                for item in stripped_text.splitlines()
            ]
            return ParentNode("ol", items)
        case BlockType.PARAGRAPH:
            return ParentNode("p", html_children)
        case _:
            raise ValueError("Unsupported block type provided")


def markdown_to_html(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = [parse_block(block) for block in blocks]
    return ParentNode("div", nodes)


def extract_title(markdown_string):
    match = re.search(r"^# (.+)", markdown_string, re.MULTILINE)
    if match:
        return match.group(1)
    else:
        raise ValueError("No H1 title found in the markdown string.")
