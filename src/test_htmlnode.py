import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

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

class TestTextNodeToHTML(unittest.TestCase):
    def test_test(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is some bold text")

    def test_italic(self):
        node = TextNode("This is some italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is some italic text")

    def test_code(self):
        node = TextNode("This is some code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is some code text")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Test image", TextType.IMAGE, "test.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props.get("src"), "test.jpg")
        self.assertEqual(html_node.props.get("alt"), "Test image")

if __name__ == "__main__":
    unittest.main()