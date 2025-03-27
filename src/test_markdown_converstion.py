import unittest
from textnode import TextNode, TextType
from markdown_conversion import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_no_delimiter(self):
        # Test with no delimiter in the text
        node = TextNode("Plain text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiter")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_code_delimiter(self):
        node = TextNode("Text with a `code block` in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_bold_delimiter(self):
        node = TextNode("Text with a **bold part** in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold part")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_italic_delimiter(self):
        node = TextNode("Text with an _italic part_ in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic part")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("Text with `one code` and `another code` block", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "one code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "another code")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[4].text, " block")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "already bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_missing_closing_delimiter(self):
        node = TextNode("Text with an unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes_input(self):
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("More text", TextType.TEXT)
        node3 = TextNode("**Bold text**", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "More text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "**Bold text**")
        self.assertEqual(result[3].text_type, TextType.TEXT)