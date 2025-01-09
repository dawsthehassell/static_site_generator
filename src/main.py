from textnode import TextNode, TextType

def main():
    node = TextNode("hello world", TextType.BOLD_TEXT, "www.youtube.com")
    print(node)

if __name__ == "__main__":
    main()