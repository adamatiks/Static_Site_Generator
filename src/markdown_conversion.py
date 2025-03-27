from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If it's not a TEXT node, just add it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # For TEXT nodes, we need to split by the delimiter
        text = old_node.text
        
        # If the delimiter doesn't appear or appears only once, no splitting needed
        if text.count(delimiter) < 2:
            # If there's one delimiter, that's an error (unmatched)
            if text.count(delimiter) == 1:
                raise ValueError(f"No matching closing delimiter for '{delimiter}'")
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = text.split(delimiter)
        
        # We should have an odd number of parts for valid delimiter pairs
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing delimiter '{delimiter}'")
        
        # First part is always regular text (could be empty)
        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
        # Process remaining parts in pairs
        for i in range(1, len(parts), 2):
            # The part at index i should have the special text_type
            new_nodes.append(TextNode(parts[i], text_type))
            
            # The part at index i+1 (if it exists and isn't empty) should be regular text
            if i+1 < len(parts) and parts[i+1]:
                new_nodes.append(TextNode(parts[i+1], TextType.TEXT))
                
    return new_nodes