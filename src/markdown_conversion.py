from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        
        if text.count(delimiter) < 2:
            if text.count(delimiter) == 1:
                raise ValueError(f"No matching closing delimiter for '{delimiter}'")
            new_nodes.append(old_node)
            continue
        
        parts = text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing delimiter '{delimiter}'")
        
        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
        for i in range(1, len(parts), 2):
            new_nodes.append(TextNode(parts[i], text_type))
            
            if i+1 < len(parts) and parts[i+1]:
                new_nodes.append(TextNode(parts[i+1], TextType.TEXT))
                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    # Skipping non-text nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extracting all images from the node's text
        images = extract_markdown_images(node.text)

        # If no images found, keeping the original node intact
        if len(images) == 0:
            new_nodes.append(node)
            continue

        # Processing images
        remaining_text = node.text

        for image_alt, image_url in images:
            # Image markdown pattern to split on
            image_markdown = f"![{image_alt}]({image_url})"

            # Splitting the text into sections (before and after the image)
            sections = remaining_text.split(image_markdown, 1)

            # Add the text before the image (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Adding the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            # Updating remaining text to be what comes after the image
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""

        # Adding remaining text after ALL images
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

# Same thing as above but for links instead of images
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for link_alt, link_url in links:
            link_markdown = f"[{link_alt}]({link_url})"

            sections = remaining_text.split(link_markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    # Creating a list with one TextNode containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]

    # Processing for bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Processing for italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Processing for code blocks
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Processing images
    nodes = split_nodes_image(nodes)

    # Processing links
    nodes = split_nodes_link(nodes)

    return nodes