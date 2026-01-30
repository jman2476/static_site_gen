from copy_static import copy_directory_contents
from page_gen import generate_page_recursive
import sys

def main():
    basepath = sys.argv[1]
    print('basepath', basepath)
    if basepath is None:
        basepath = '/'
    # create_empty_public_dir()
    copy_directory_contents('./static', './docs')
    generate_page_recursive('content', 'template.html', 'docs', basepath)



main()
