from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from gencontent import generate_page
from gencontent import generate_pages_recursive

import shutil
import os


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)
    if os.path.exists('public'):
        shutil.rmtree('public')
    os.mkdir('public')
    copy_site_recursive('static', 'public')
    generate_page("content/index.md", "template.html", "public/index.html")
    if not os.path.exists("public"):
        os.mkdir("public")
    generate_pages_recursive("content", "template.html", "public")



def copy_site_recursive(sauce, dest):
    # this checks is a directoty exists, if so it deletes it, and makes a fresh directoty for the new website.
         
    for item in os.listdir(sauce):
        src_path = os.path.join(sauce, item)
        dst_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_site_recursive(src_path, dst_path)
    


main()
    
    

