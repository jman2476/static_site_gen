import os, shutil

def copy_directory_contents(source, destination, tree_root=True):
    destination_check = os.path.join(destination, '..')
    if not os.path.exists(source):
        raise ValueError('Invalid source path')
    if not os.path.exists(destination_check):
        raise ValueError('Invalid destination path: destination parent directory not found')
    if tree_root:
        create_empty_public_dir()
    print(f'Reading [{source}] directory contents')
    source_dir = os.listdir(source)
    for entry in source_dir:
        entry_path = os.path.join(source, entry)
        dest_path = os.path.join(destination, entry)
        print(f'Copy path:\n     {entry_path}')
        print(f'Target path:\n     {dest_path}')
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_directory_contents(entry_path, dest_path, tree_root=False)
    if tree_root:
        print('Directory successfully copied')

def delete_public_dir():
    path = './public'
    if os.path.exists(path):
        print('Removing public dir @', path)
        shutil.rmtree(path)
    else:
        print('No public dir to delete')
    
def create_empty_public_dir():
    path = './public'
    if os.path.exists(path):
        delete_public_dir()
    os.mkdir(path)
    print('Empty public dir successfully created')
