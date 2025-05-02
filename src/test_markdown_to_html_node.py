import unittest

from markdown_to_html_node import heading_block_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHeadingBlockToHTMLNode(unittest.TestCase):

    def test_basic_heading_block(self):
        markdown = "# My Heading"
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h1>My Heading</h1>")

    def test_heading_h2_bold(self):
        markdown = "## My **Bear** Friend"
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h2>My <b>Bear</b> Friend</h2>")

    def test_multiple_inline_formats(self):
        markdown = "### The _quick_ **brown** `bear`"
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h3>The <i>quick</i> <b>brown</b> <code>bear</code></h3>")

    def test_extra_spaces_after_hashes(self):
        markdown = "## _Magic_  "
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h2><i>Magic</i></h2>")

    def test_no_content(self):
        markdown = "## "
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h2></h2>")

    def test_nested_or_mixed_inline_markdown(self):
        markdown = "#### This is **bold and _nested italic_**"
        htmlnode = heading_block_to_html_node(markdown)
        html = htmlnode.to_html()
        self.assertEqual(html, "<h4>This is <b>bold and <i>nested italic</i></b>")