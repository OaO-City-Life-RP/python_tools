import os
import zipfile

def find_json_files(base_dir):
    """
    Recursively find all .json files in the given directory, maintaining the directory structure.

    :param base_dir: The base directory to start searching from.
    :return: A list of paths to .json files relative to the base directory.
    """
    json_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                json_files.append(relative_path)
    return json_files

def create_archive(base_dir, output_filename):
    """
    Archive all .json files in the given directory, maintaining the directory structure.

    :param base_dir: The base directory to start searching from.
    :param output_filename: The name of the output zip file.
    """
    try:
        json_files = find_json_files(base_dir)
        if not json_files:
            print("No .json files found in the directory.")
            return

        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file in json_files:
                archive.write(os.path.join(base_dir, file), file)
        print(f"Archive created successfully: {output_filename}")
    except PermissionError:
        print("Permission denied: Unable to create the archive file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Starting the JSON archive process...")
    try:
        base_directory = os.getcwd()  # Start from the current directory
        output_zip = "json_files_archive.zip"

        create_archive(base_directory, output_zip)
        print("Archive process completed successfully.")
    except Exception as e:
        print(f"Error initializing the script: {e}")
    input("Press Enter to exit...")
