import re, os
from md_to_html import markdown_to_html_node

def extract_title(markdown):
    title = re.findall(r'^([ |\n]*#{1} .+)', markdown)
    if len(title) == 0:
        raise ValueError('No title found in markdown')
    return title[0].strip('# \n')

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    with open(from_path, 'r') as file:
        markdown = file.read()
    
    with open(template_path, 'r') as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)

    add_title = template.replace('{{ Title }}', title)
    html = add_title.replace('{{ Content }}', html_node.to_html())
        
    dir_path = '/'.join(dest_path.split('/')[:-1])
    os.makedirs(dir_path, exist_ok=True)
    
    with open(dest_path, 'w') as file:
        file.write(html)

    print('Generation done')