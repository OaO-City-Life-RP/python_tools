import os

def generate_structure(path, prefix=''):
    structure = ''
    items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))
    
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        if item == 'node_modules':
            if index == len(items) - 1:
                connector = '└── '
            else:
                connector = '├── '
            structure += prefix + connector + item + '\n'
            continue
        
        if index == len(items) - 1:
            connector = '└── '
        else:
            connector = '├── '
        structure += prefix + connector + item + '\n'
        
        if os.path.isdir(item_path):
            if index == len(items) - 1:
                structure += generate_structure(item_path, prefix + '    ')
            else:
                structure += generate_structure(item_path, prefix + '│   ')
    return structure

def main(path, output_file):
    structure = generate_structure(path)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(structure)
    print(f"The directory structure has been written to {output_file}")

if __name__ == '__main__':
    path = input("Enter the directory path: ")
    output_file = 'file_structure.txt'
    main(path, output_file)
