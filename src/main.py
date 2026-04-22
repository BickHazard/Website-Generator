from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from gencontent import generate_page
from gencontent import generate_pages_recursive

import shutil
import os
import sys

def main():
    if  len(sys.argv) <= 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    
    #node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(node)
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.mkdir('docs')
    copy_site_recursive('static', 'docs')
    
    if not os.path.exists("docs"):
        os.mkdir("docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)



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
    
    

