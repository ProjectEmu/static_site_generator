import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="div", value="Hello World", props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.props, {"class": "container"})
        self.assertEqual(node.children, [])

    def test_add_child(self):
        parent = HTMLNode(tag="div")
        child = HTMLNode(tag="p", value="This is a paragraph.")
        parent.children.append(child)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)

    def test_repr(self):
        node = HTMLNode(
            tag="a", value="Link to Google", props={"href": "https://www.google.com"}
        )
        expected_repr = "HTMLNode(tag='a', value='Link to Google', children=0 children, props={'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a", props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected_props = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props)


class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        leaf = LeafNode(
            tag="span", value="Leaf node text", props={"class": "highlight"}
        )
        self.assertEqual(leaf.tag, "span")
        self.assertEqual(leaf.value, "Leaf node text")
        self.assertEqual(leaf.props, {"class": "highlight"})

    def test_initialization_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="span")

    def test_to_html(self):
        leaf = LeafNode(tag="b", value="Bold text", props={"class": "bold"})
        expected_html = '<b class="bold">Bold text</b>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_html_without_tag(self):
        leaf = LeafNode(value="Just some text")
        self.assertEqual(leaf.to_html(), "Just some text")

    def test_to_html_value_error(self):
        leaf = LeafNode(tag="b", value="Valid text")
        leaf.value = ""
        with self.assertRaises(ValueError):
            leaf.to_html()


if __name__ == "__main__":
    unittest.main()
