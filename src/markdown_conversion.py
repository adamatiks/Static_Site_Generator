from textnode import TextType, TextNode

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