import os

##This script will create a text file with the names of all subdirectories in a given directory. And will create ready to use for resources.cfg file.

dir_path = input("Please enter the directory path: ")


subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]


with open('folder_names.txt', 'w') as f:
    for subdir in subdirs:
        f.write("ensure " + subdir + '\n')

print("The names of all subdirectories have been written to folder_names.txt.")