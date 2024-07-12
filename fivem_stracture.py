import os

def generate_structure(path, prefix='', is_root=False):
    structure = ''
    items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))
    
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        ignore_list = ['.git', '.idea', 'node_modules', 'venv', '__pycache__', 'Writerside']
        if item in ignore_list:
            continue
        
        if index == len(items) - 1:
            connector = '└── '
        else:
            connector = '├── '
        
        structure += prefix + connector + item + '\n'
        
        if os.path.isdir(item_path):
            # Go deeper if item contains [] or is "resources" or we are not at root level
            if ('[' in item and ']' in item) or item == "resources":
                if index == len(items) - 1:
                    structure += generate_structure(item_path, prefix + '    ', is_root=False)
                else:
                    structure += generate_structure(item_path, prefix + '│   ', is_root=False)
    
    return structure

def main(path, output_file):
    structure = generate_structure(path, is_root=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(structure)
    print(f"The directory structure has been written to {output_file}")

if __name__ == '__main__':
    path = input("Enter the directory path: ")
    output_file = 'fivem_file_structure.txt'
    main(path, output_file)
