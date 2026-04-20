import unittest


from htmlnode import HTMLNode
from htmlnode import LeafNode 
from htmlnode import ParentNode 

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        assert node.props_to_html() == ""

        
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        assert node.props_to_html() == ""


    def test_props_to_html_multiple(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        assert result == ' href="https://www.google.com" target="_blank"'
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        assert node.to_html() == "<p>Hello, world!</p>"

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        assert node.to_html() == "<b>Hello, world!</b>"
        
    def test_leaf_to_html_link_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
           node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
           )