from textnode import TextNode, TextType

def main():
    new_textnode = TextNode("A link to the git repo for this project!", TextType.LINK, "https://github.com/adamatiks/Static_Site_Generator")
    print(new_textnode)

main()