import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with empty props
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode("a", "Click me", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode("img", props={"src": "image.png", "alt": "An image", "width": "500"})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image" width="500"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Image", props={"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image">Image</img>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", [])
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("b", "Bold text Leaf Node")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        parent_node = ParentNode("span", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<span><a href="https://www.google.com">Click me!</a></span>'
        )
    
    def test_to_html_with_props_and_grandchildren(self):
        grandchild_node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com">Click me!</a></span></div>'
        )                

if __name__ == "__main__":
    unittest.main()