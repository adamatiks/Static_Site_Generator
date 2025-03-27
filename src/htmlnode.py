from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        key_value_list = []
        for key in self.props:
            current_result = (f'{key}="{self.props[key]}"')
            key_value_list.append(current_result)
        result = " " + " ".join(key_value_list) if key_value_list else ""
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props)
        self.children = []

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return (f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        if self.children == []:
            raise ValueError("Parent node Children lists must not be empty")
        else:
            result = ""
            for child in self.children:
                result += child.to_html()
            return (f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>")
        
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        node = LeafNode("a", text_node.text)
        node.props["href"] = text_node.url
        return node
    elif text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", "")
        node.props["src"] = text_node.url
        node.props["alt"] = text_node.text
        return node
    else:
        raise Exception("TextType not supported")