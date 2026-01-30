import os
import shutil
def copy_directory_contents(source, destination, tree_root=True):
    absolute_source = os.path.abspath(source)
    absolute_destination = os.path.abspath(destination)
    destination_check = os.path.abspath(os.path.join(absolute_destination, '..'))
    if not os.path.exists(absolute_source):
        raise ValueError('Invalid source path')
    if not os.path.exists(destination_check):
        raise ValueError('Invalid destination path: destination parent directory not found')
    
    src_print_name = absolute_source.split(os.path.abspath('.'))[1]
    if tree_root:
        create_empty_public_dir()
    print(f'Reading [{src_print_name}] directory contents')
    source_dir = os.listdir(absolute_source)
    for entry in source_dir:
        entry_path = os.path.join(absolute_source, entry)
        dest_path = os.path.join(absolute_destination, entry)
        print(f'Copy path:\n     {entry_path}')
        print(f'Target path:\n     {dest_path}')
        if os.path.isfile(entry_path):
            # print('Its a file!', entry)
            shutil.copy(entry_path, dest_path)
        else:
            # print('Looks like a directory:', entry)
            # print(f'Making {entry} dir at\n     {dest_path}')
            os.mkdir(dest_path)
            copy_directory_contents(entry_path, dest_path, tree_root=False)
    if src_print_name == '/static':
        print('Static directory successfully copied')

def delete_public_dir():
    path = os.path.abspath('./public')
    if os.path.exists(path):
        print('Removing public dir @', path)
        print('Public dir successfully deleted')
        shutil.rmtree(path)
    else:
        print('No public dir to delete')
    
def create_empty_public_dir():
    path = os.path.abspath('./public')
    if os.path.exists(path):
        delete_public_dir()
    # print(os.listdir(path))
    os.mkdir(path)
    print('Empty public dir successfully created')