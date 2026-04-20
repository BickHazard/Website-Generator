import unittest
import re

from textnode import TextType, TextNode


from htmlnode import HTMLNode
from htmlnode import LeafNode 
from htmlnode import ParentNode 
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_delimiter import extract_markdown_images
from split_nodes_delimiter import extract_markdown_links

from split_nodes_delimiter import split_nodes_image
from split_nodes_delimiter import split_nodes_link
from split_nodes_delimiter import text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_pair_delimiter(self):
        node = TextNode("help, I'm a *fat* loser!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    
        expected = [
            TextNode("help, I'm a ", TextType.TEXT),
            TextNode("fat", TextType.ITALIC),
            TextNode(" loser!", TextType.TEXT),
        ]
    
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "![one](https://a.com/1.png) and ![two](https://b.com/2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("one", "https://a.com/1.png"),
                ("two", "https://b.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_matches(self):
        text = "This has no images, only text and [a link](https://boot.dev)."
        matches = extract_markdown_images(text)
        self.assertEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "![](https://example.com/no-alt.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("", "https://example.com/no-alt.png")],
            matches,
        )

    def test_extract_markdown_links_multiple(self):
        text = "Link [one](https://a.com) and [two](https://b.com/page)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("one", "https://a.com"),
                ("two", "https://b.com/page"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_matches(self):
        text = "This has no [links] or images ![img](https://a.com)."
        matches = extract_markdown_links(text)
        self.assertEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        text = "![img](https://a.com/img.png) and [link](https://a.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "https://a.com")],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [Best website to learn coding](https://www.boot.dev) and [worst website to learn anything](https://www.learingcenter.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("Best website to learn coding", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "worst website to learn anything", TextType.LINK, "https://www.learingcenter.org"
                ),
            ],
            new_nodes,
        )

  

    def test_text_to_textnodes_all_features(text):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        assert nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        