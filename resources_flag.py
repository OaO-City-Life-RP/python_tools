import os
import json

def read_cfg_file(cfg_path):
    print(f"Reading .cfg file from: {cfg_path}")
    with open(cfg_path, 'r') as file:
        lines = file.readlines()
    
    scripts = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        if line.startswith('ensure '):
            script_name = line.split(' ')[1]
            scripts.append(script_name)
    print(f"Scripts found in .cfg file: {scripts}")
    return scripts

def get_scripts_from_directory(path):
    print(f"Scanning directory: {path}")
    scripts = {}
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(full_path, path)
            if '[' in dir_name and ']' in dir_name:
                # If it's a directory with brackets, dive deeper
                scripts.update(get_scripts_from_directory(full_path))
            else:
                # If it's a directory without brackets, consider it a script
                scripts[dir_name] = full_path
        break  # Prevents walking into subdirectories in the top-level
    print(f"Scripts found in resources directory: {scripts}")
    return scripts

def generate_report(missing_scripts, report_path):
    with open(report_path, 'w') as file:
        if missing_scripts:
            file.write("Missing Scripts:\n")
            for script in missing_scripts:
                file.write(f"- {script}\n")
    print(f"Report generated at: {report_path}")

def main():
    cfg_path = "C:\\Users\\jekab\\Documents\\OaO_Server\\resources.cfg"
    resources_path = "C:\\Users\\jekab\\Documents\\OaO_Server\\resources"
    report_path = 'report.txt'
    script_map_path = 'script_map.json'

    # Step 1: Identify all scripts in the resources directory and create a map
    resource_scripts_map = get_scripts_from_directory(resources_path)

    # Write the script map to a JSON file
    with open(script_map_path, 'w') as json_file:
        json.dump(resource_scripts_map, json_file, indent=4)
    print(f"Script map generated at: {script_map_path}")

    # Step 2: Read the .cfg file
    cfg_scripts = read_cfg_file(cfg_path)

    # Step 3: Compare scripts in .cfg with the map created from the resources directory
    missing_scripts = [script for script in cfg_scripts if script not in resource_scripts_map]

    # Step 4: Generate report
    generate_report(missing_scripts, report_path)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
