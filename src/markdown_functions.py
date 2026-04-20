from text_node_to_html_node import text_node_to_html_node
from split_nodes_delimiter import text_to_textnodes

from textnode import TextNode, TextType
from htmlnode import LeafNode
from htmlnode import HTMLNode
from htmlnode import ParentNode
from blocktype import BlockType
from blocktype import block_to_block_type



def markdown_to_blocks(markdown):
    blocks = []
    for chunk in markdown.split("\n\n"):
        stripped = chunk.strip()
        if stripped:
            blocks.append(stripped)
    return blocks

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:   
        
            i = 0
            while i < len(block) and block[i] == "#":
                i += 1
            level = i  # 1-6
            text = block[level:].lstrip()  # removes the space after the #'s
            children = text_to_children(text)     
            finished_node = ParentNode(f"h{level}", children)
            block_nodes.append(finished_node)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"   # keep trailing newline like the test expects
            code_leaf = LeafNode(None, code_text)
            code_node = ParentNode("code", [code_leaf])
            finished_node = ParentNode("pre", [code_node])
            block_nodes.append(finished_node)

        elif block_type == BlockType.QUOTE:
            cleaned_lines = []
            lines = block.split("\n")
            for line in lines:
                cleaned_line = line.lstrip().lstrip("> ").lstrip() # removes leading whitespace (spaces/tabs),  remove any leading '>' and spaces after it, remove any leftover leading whitespace
                cleaned_lines.append(cleaned_line)
            quote_text = " ".join(cleaned_lines)
            children = text_to_children(quote_text)
            finished_node = ParentNode("blockquote", children)
            block_nodes.append(finished_node)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                if line.strip() == "": 
                    continue
                elif line.startswith(('- ', '* ')):
                    item_text = line[2:]
                else:
                    raise ValueError ("This ain't right")
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                li_nodes.append(li_node)
            finished_node = ParentNode("ul", li_nodes)
            block_nodes.append(finished_node)

        elif block_type == BlockType.ORDERED_LIST: # fix this, find the digit
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                if line.strip() == "": 
                    continue                
                i = line.find(".")
                if i == -1:
                    raise ValueError ("This ain't right")
                if line[:i].isdigit():
                    if line[i:i+2] == ". ":
                        item_text = line[i+2:]  
                    else:
                        raise ValueError ("This ain't right")                        
                else:
                    raise ValueError ("This ain't right")
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                li_nodes.append(li_node)
            finished_node = ParentNode("ol", li_nodes)
            block_nodes.append(finished_node)

        elif block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            merged_lines = " ".join(lines)
            children = text_to_children(merged_lines)
            finished_node = ParentNode("p", children)
            block_nodes.append(finished_node)
    return ParentNode("div", block_nodes)# dont trust this line
    
                                

                            
def text_to_children(text):
    text_nodes = text_to_textnodes(text)              
    return [text_node_to_html_node(tn) for tn in text_nodes]