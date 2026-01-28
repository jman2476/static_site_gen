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
        super(self, tag, value, props=props)

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
