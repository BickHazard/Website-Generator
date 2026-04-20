from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        
        temp_texts = [] #this will be a list of strings
        temp_texts = node.text.split(delimiter)
        if len(temp_texts)%2 == 0:
            raise Exception ("Error: Invalid Markdown Syntax.")

        for i in range(len(temp_texts)):
            if i%2 != 0:
                temp_node =  TextNode(temp_texts[i], text_type)             
            else:
                temp_node = TextNode(temp_texts[i],TextType.TEXT)
            new_nodes.append(temp_node)
    return new_nodes

def extract_markdown_links(text): #links
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_images(text): #images
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:    
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        else:
            to_be_split = old_node.text
            images = extract_markdown_images(to_be_split)

            if len(images) == 0:
                # no images in this text, keep it as-is
                new_nodes.append(old_node)
                continue

            for image in images:
                alt = image[0]
                url = image[1]

                sections = to_be_split.split(f"![{alt}]({url})", 1)
                before = sections[0]
                after = sections[1]

                to_be_split = after
                image_node = TextNode(alt, TextType.IMAGE, url)

                

                if before != "":
                    new_node = TextNode(before,TextType.TEXT)
                    new_nodes.append(new_node)
                new_nodes.append(image_node)

        if to_be_split != "":
            new_nodes.append(TextNode(to_be_split, TextType.TEXT))
    return new_nodes

    
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:    
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        else:
            to_be_split = old_node.text
            links = extract_markdown_links(to_be_split)

            if len(links) == 0:
                # no links in this text, keep it as-is
                new_nodes.append(old_node)
                continue

            for url in links:
                alt = url[0]
                href = url[1]

                sections = to_be_split.split(f"[{alt}]({href})", 1)
                before = sections[0]
                after = sections[1]

                to_be_split = after
                link_node = TextNode(alt, TextType.LINK, href)

                

                if before != "":
                    new_node = TextNode(before,TextType.TEXT)
                    new_nodes.append(new_node)
                new_nodes.append(link_node)

        if to_be_split != "":
            new_nodes.append(TextNode(to_be_split, TextType.TEXT))
    return new_nodes
    


def text_to_textnodes(text):
    
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**" , TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
