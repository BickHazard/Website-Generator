import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_node_to_html_node import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_equal_when_url_missing(self):
        node1 = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_equal_when_url_differs(self):
        node1 = TextNode("hello", TextType.LINK, None)
        node2 = TextNode("hello", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_node_to_html(self):
        node = TextNode("Boot", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image_node_to_html(self):
        node = TextNode("A wizard bear", TextType.IMAGE, "https://example.com/bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/bear.png", "alt": "A wizard bear"},
    )


if __name__ == "__main__":
    unittest.main()