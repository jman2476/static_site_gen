from textnode import TextNode, TextType

def main():
    nodeA = TextNode('hello', TextType.ITALIC)
    nodeB = TextNode('hello', TextType.ITALIC)
    nodeC = TextNode('hello', TextType.ITALIC, url='https:')
    nodeD = TextNode('Hello', TextType.BOLD, url='reddit.com')
    nodeE = TextNode('Oooga booga', TextType.PLAIN, url='google.com')

    nodes = [nodeA, nodeB, nodeC, nodeD, nodeE]

    for i in range(0, len(nodes)):
        print(nodes[i])
        print('Comp', nodes[i]==nodes[(i+1)%len(nodes)])


main()
