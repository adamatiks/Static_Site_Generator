import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_single_link(self):
        matches = extract_markdown_links("This is text with a link [to google](https://www.google.com)")
        self.assertListEqual([("to google", "https://www.google.com")], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com/example.png) and another ![second image](https://www.example2.com/example2.png)", TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.example.com/example.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://www.example2.com/example2.png"),
            ], 
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is a text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_starts_with_image(self):
        node = TextNode(
            "![starting image](https://example.com/start.jpg) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("starting image", TextType.IMAGE, "https://example.com/start.jpg"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_ends_with_image(self):
        node = TextNode(
            "This text ends with an ![ending image](https://example.com/end.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text ends with an ", TextType.TEXT),
                TextNode("ending image", TextType.IMAGE, "https://example.com/end.jpg"),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example2.com")
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is a [simple link](https://example.com) in text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("simple link", TextType.LINK, "https://example.com"),
                TextNode(" in text.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) to bootdev!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" to bootdev!", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Click [here](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://www.google.com")
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com")
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This text contains no links at all.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text contains no links at all.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_input_nodes(self):
        nodes = [
            TextNode("First node with [link](https://example1.com)", TextType.TEXT),
            TextNode("Second node with no links", TextType.TEXT),
            TextNode("Third node with [another link](https://www.example2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example1.com"),
                TextNode("Second node with no links", TextType.TEXT),
                TextNode("Third node with ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.example2.com"),
            ],
            new_nodes,
        )

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text node", TextType.TEXT),
            TextNode("Bold node", TextType.BOLD),
            TextNode("Link node", TextType.LINK, "https://example.com"),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text node", TextType.TEXT),
                TextNode("Bold node", TextType.BOLD),
                TextNode("Link node", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    def test_links_with_special_chars(self):
        node = TextNode(
            "Link with [special chars: !@#$](https://example.com/path?query=value%param=2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("special chars: !@#$", TextType.LINK, "https://example.com/path?query=value%param=2"),
            ],
            new_nodes,
        )

    def test_empty_link_text(self):
        node = TextNode(
            "This has an [](https://example.com) empty link text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty link text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_link_url(self):
        node = TextNode(
            "This is a [link]() with no url",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, ""),
                TextNode(" with no url", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_adjacent_links(self):
        node = TextNode(
            "Adjacent [first](https://example1.com)[second](https://example2.com) links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Adjacent ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://example1.com"),
                TextNode("second", TextType.LINK, "https://example2.com"),
                TextNode(" links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_link(self):
        node = TextNode(
            "This has a [malformed link](https://example.com",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a [malformed link](https://example.com", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_with_no_special_formatting(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_with_bold(self):
        text = "This has **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_with_italic(self):
        text = "This has _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_with_code(self):
        text = "This has a `code` block"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " block")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_with_image(self):
        text = "This has an ![image](https://example.com/img.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This has an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.jpg")

    def test_text_with_link(self):
        text = "This has a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This has a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_text_with_mutliple_formatting(self):
        text = "This has **bold** and _italic_ text and `code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 6)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text and ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)

    def test_text_with_everything(self):
        text = "This has **bold** and _italic_ text and a `code` block. It also has a [link](https://example.com) and an ![image](https://example.com/image.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text and a ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " block. It also has a ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "link")
        self.assertEqual(nodes[7].text_type, TextType.LINK)
        self.assertEqual(nodes[7].url, "https://example.com")
        self.assertEqual(nodes[8].text, " and an ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "image")
        self.assertEqual(nodes[9].text_type, TextType.IMAGE)
        self.assertEqual(nodes[9].url, "https://example.com/image.jpg")

if __name__ == "__main__":
    unittest.main()