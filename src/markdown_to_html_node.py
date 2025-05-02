from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            pass

def heading_block_to_html_node(block):
    heading_size = block.split()[0].count("#")
    heading_content = block.split(" ", 1)[1].strip()
    textnodes = text_to_textnodes(heading_content)
    htmlnodes = [text_node_to_html_node(node) for node in textnodes]
    return ParentNode(f"h{heading_size}", htmlnodes)