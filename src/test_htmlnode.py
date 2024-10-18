import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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
        leaf.value = None
        with self.assertRaises(ValueError):
            leaf.to_html()


class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        child1 = LeafNode(tag="p", value="First paragraph")
        child2 = LeafNode(tag="p", value="Second paragraph")
        parent = ParentNode(
            tag="div", children=[child1, child2], props={"class": "container"}
        )

        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.props, {"class": "container"})
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)

    def test_to_html_simple(self):
        child1 = LeafNode(tag="p", value="First paragraph")
        child2 = LeafNode(tag="p", value="Second paragraph")
        parent = ParentNode(
            tag="div", children=[child1, child2], props={"class": "container"}
        )
        expected_html = (
            '<div class="container"><p>First paragraph</p><p>Second paragraph</p></div>'
        )
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_nested(self):
        grandchild1 = LeafNode(tag="span", value="Nested span 1")
        grandchild2 = LeafNode(tag="span", value="Nested span 2")
        child1 = ParentNode(tag="div", children=[grandchild1, grandchild2])
        child2 = LeafNode(tag="p", value="A paragraph with nested div")
        parent = ParentNode(
            tag="section", children=[child1, child2], props={"id": "main-section"}
        )
        expected_html = '<section id="main-section"><div><span>Nested span 1</span><span>Nested span 2</span></div><p>A paragraph with nested div</p></section>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_deeply_nested(self):
        great_grandchild = LeafNode(tag="b", value="Bold text")
        grandchild1 = ParentNode(
            tag="span",
            children=[great_grandchild],
            props={"style": "font-weight: bold"},
        )
        grandchild2 = LeafNode(tag="i", value="Italic text")
        child1 = ParentNode(tag="div", children=[grandchild1, grandchild2])
        child2 = LeafNode(tag="p", value="Another paragraph")
        parent = ParentNode(
            tag="article", children=[child1, child2], props={"class": "article-class"}
        )
        expected_html = '<article class="article-class"><div><span style="font-weight: bold"><b>Bold text</b></span><i>Italic text</i></div><p>Another paragraph</p></article>'
        self.assertMultiLineEqual(parent.to_html(), expected_html)

    def test_initialization_value_error(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div")  # No children provided

    def test_to_html_missing_tag_error(self):
        child1 = LeafNode(tag="p", value="A paragraph")
        with self.assertRaises(ValueError):
            ParentNode(children=[child1]).to_html()  # Tag is required for ParentNode

    def test_to_html_missing_children_error(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div").to_html()  # Children are required for ParentNode


if __name__ == "__main__":
    unittest.main()
