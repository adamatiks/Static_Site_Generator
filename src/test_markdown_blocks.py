from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
import unittest, textwrap

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        """Test provided by the course."""
        md = textwrap.dedent("""\
        This is a **bolded** paragraph
    
        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line
    
        - This is a list
        - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        """Test that an empty imput will return an empty list."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_whitespace_only(self):
        """Test that whitespace only will return an empty list."""
        md = "    \n \n\t\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        """Test that a single block will simply return a list with a single element."""
        md = "This is a single block of markdown"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block of markdown"])

    expected_list = ["Block 1", "Block 2", "Block 3"]

    def test_multiple_blank_lines(self):
        """Test that multiple blank lines will give us the expected result."""
        md = "Block 1\n\n\n\nBlock 2\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, self.expected_list)


    def test_non_standard_line_endings(self):
        """Test that non-standard line endings (\r, \r\n) split blocks correctly."""
        md_old_mac = "Block 1\rBlock 2\rBlock 3"
        md_windows = "Block 1\r\n\r\nBlock 2\r\n\r\nBlock 3"
        blocks_old_mac = markdown_to_blocks(md_old_mac)
        blocks_windows = markdown_to_blocks(md_windows)

        self.assertEqual(blocks_old_mac, self.expected_list)
        self.assertEqual(blocks_windows, self.expected_list)

    def test_mixed_content_blocks(self):
        """Test blocks with different markdown constructs."""
        md = textwrap.dedent("""\
            # Heading
            
            Paragraph with **bold** and _italic_.
                             
            ```
            code block
            with multiple lines
            ```
                             
            > Blockquote
            > continues here
            
            - List item 1
            - List item 2
        """)

        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 5)
        self.assertTrue(blocks[0].startswith("# Heading"))
        self.assertTrue(blocks[2].startswith("```"))
        self.assertTrue(blocks[3].startswith(">"))

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        # Tests for various heading sizes
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Tests for invalid headings
        self.assertEqual(block_to_block_type("#Heading without space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\ndef function():\n  pass\n```"), BlockType.CODE)

        # Test for invalid code block
        self.assertEqual(block_to_block_type("``\nNot enough backticks\n``"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2"), BlockType.QUOTE)

        # Test for invalid quote block
        self.assertEqual(block_to_block_type(">Line 1\nLine 2 without >"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- This is an unordered list with just a single yet lengthy item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)

        # Tests for invalid unordered list
        self.assertEqual(block_to_block_type("-Oops forgot whitespace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item 1\nItem 2 without dash"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)

        # Tests for invalid ordered lists
        self.assertEqual(block_to_block_type("1. Item 1\nItem 2 without being numbered"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2 but numbered wrong"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n4. Item 3 but numbered wrong"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("0. Item starting with 0"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Line 1\nLine 2"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()