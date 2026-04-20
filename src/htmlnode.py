
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTML Not Implemented")
    
    def props_to_html(self):
        answer = ""
        if self.props is None or self.props == {}:
            return ""
        for key, value in self.props.items():
            answer = answer + f' {key}="{value}"'  

        return answer

    def __repr__(self):
        return (f" tag={self.tag}, value={self.value}, children={self.children},  props ={self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)
        

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        # No tag: raw text
        if self.tag is None:
            return self.value

        # Build attributes string
        attrs = ""
        if self.props:
            for key, val in self.props.items():
                attrs += f' {key}="{val}"'

        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (f"LeafNode(tag={self.tag}, value={self.value}, props ={self.props})")



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children = children, props = props)
        #self.tag = tag
        #self.children = children
        #self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        attrs = ""
        attrs = f"<{self.tag}{self.props_to_html()}>"
        if self.children:
            for child in self.children:
                attrs += child.to_html()
            
        attrs += f'</{self.tag}>'
            

        return attrs