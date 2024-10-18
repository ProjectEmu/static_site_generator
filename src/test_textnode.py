import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode(
            "This is a text node with URL", TextType.ITALIC, "https://www.google.com"
        )

        # Positive test for equality
        self.assertEqual(node, node2)

        # Negative test for equality
        self.assertNotEqual(node3, node2)

    def test_inequality_different_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node_diff_text = TextNode("Different text", TextType.TEXT)

        # Test inequality when text is different
        self.assertNotEqual(node, node_diff_text)

    def test_different_text_types(self):
        node_bold = TextNode("This is a text node", TextType.BOLD)
        node_italic = TextNode("This is a text node", TextType.ITALIC)

        # Test inequality for different text types
        self.assertNotEqual(node_bold, node_italic)

    def test_url_none(self):
        node_with_none_url = TextNode("This is a text node", TextType.TEXT)
        node_with_url = TextNode(
            "This is a text node", TextType.TEXT, "https://example.com"
        )

        # Test inequality when one URL is None
        self.assertNotEqual(node_with_none_url, node_with_url)

    def test_comparison_with_different_object(self):
        node = TextNode("This is a text node", TextType.BOLD)

        # Test inequality with completely different types
        self.assertNotEqual(node, "This is a string")
        self.assertNotEqual(node, 42)
        self.assertNotEqual(node, None)


if __name__ == "__main__":
    unittest.main()
