class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        properties = ''
        if self.props:
            for key, value in self.props.items():
                properties += f' {key}="{value}"'

        return properties

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            if self.__check_empty():
                return f'<{self.tag}>'
            else:
                raise ValueError('Tag empty. Must have value or be valid empty tag')
        if self.tag is None:
            return f'{self.value}'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    def __check_empty(self):
        empty_tags = [
                'area',
                'base',
                'br',
                'col',
                'embed',
                'hr',
                'img',
                'input',
                'link',
                'meta',
                'param',
                'source',
                'track',
                'wbr'
                ]
        return self.tag in empty_tags


    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('No tag given for parent')
        if self.children is None or len(self.children) == 0:
            raise ValueError('\nParentNode  has no children. Womp womp')
        html = [f'<{self.tag}>',f'</{self.tag}>']
        for child in self.children:
            child_html = child.to_html()
            html.insert(-1, child_html)
        return ''.join(html)
