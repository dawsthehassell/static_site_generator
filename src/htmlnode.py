class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)
        if value is None:
            raise ValueError

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self):
        if not self.tag:
            raise ValueError ("missing tag argument")
        if not self.children:
            raise ValueError("missing children argument")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result = child.to_html()
            html += result
        html += f"</{self.tag}>"
        return html