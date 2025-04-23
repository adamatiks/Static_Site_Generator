import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    is_old_mac = '\r' in markdown and '\r\n' not in markdown

    normalized = markdown.replace('\r\n', '\n').replace('\r', '\n')

    if is_old_mac:
        raw_blocks = normalized.split('\n')
    else:
        import re
        raw_blocks = re.split(r'\n\s*\n', normalized)

    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:
            blocks.append(cleaned)

    return blocks

def block_to_block_type(block: str) -> BlockType:
    # Checking for heading block
    heading_match = re.match(r"^#{1,6} ", block)
    if heading_match:
        return BlockType.HEADING
    
    # Checking for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Checking for quote block
    lines = block.split("\n")
    is_quote = True
    
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote and lines:
        return BlockType.QUOTE
    
    # Checking for unordered lists
    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    
    if is_unordered_list and lines:
        return BlockType.UNORDERED_LIST
    
    # Checking for ordered lists
    is_ordered_list = True
    
    if len(lines) == 0:
        is_ordered_list = False
    else:
        for i, line in enumerate(lines):
            expected_prefix = f"{i+1}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH