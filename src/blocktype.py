from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(incoming_block):
    lines = incoming_block.split("\n")
    #print(lines)
    first_line = lines[0]
    last_line = lines[len(lines)-1]

    i = 0
    while i <len(first_line) and first_line[i] == '#': #this loops as long as the character is a '#'
        i+=1
    if 1<=i <=6 and i < len(first_line) and first_line[i] == " ": #check for heading
        return BlockType.HEADING
    
    if first_line == "```" and last_line.strip() == "```": #check for code
        return BlockType.CODE
    
    is_quote = True #check for quotes
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered == True:
        return BlockType.UNORDERED_LIST
    
    i = 1
    is_ordered = True
    for line in lines:
        if line.startswith(f"{i}. "):
            i+=1
        else: 
            is_ordered = False
            break
    if is_ordered == True:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

    
