import os
from markdown_blocks import markdown_to_html_node

def extract_title(block):
    
    lines = block.split("\n")
    for line in lines:
        if line.startswith(('# ')):
            return line[2:]
    raise Exception("No Headers Found")


def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    from_contents = from_file.read()
    from_file.close()
    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()
    html = (markdown_to_html_node(from_contents)).to_html()
    page_title = extract_title(from_contents)
    template_contents = template_contents.replace("{{ Title }}", page_title)
    template_contents = template_contents.replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    
    finished_file = open(dest_path, "w")
    finished_file.write(template_contents)
    finished_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path): #This checks whether that source path is a file.
            if entry.endswith(".md"):
                final_path = os.path.join(dest_dir_path, entry[:-2] + "html")
                generate_page(full_path, template_path, final_path)
            

        else:
            new_dest_dir = os.path.join(dest_dir_path, entry)
            if not os.path.exists(new_dest_dir):
                os.mkdir(new_dest_dir)
            generate_pages_recursive(full_path, template_path, new_dest_dir,)

