import os
import sys
import zipfile
import fnmatch
from pathlib import Path
import re

"""Get User Choice"""
def get_user_choice():
    print("Choose an option:")
    print("1 - Zip the project (respecting .gitignore)")
    print("2 - Convert code files to .txt and store in a single folder")
    choice = input("Enter 1 or 2: ")
    return choice

"""Parse .gitignore file and return list of patterns to ignore."""
def parse_gitignore(project_path):
    gitignore_path = os.path.join(project_path, '.gitignore')
    patterns = []
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    
    return patterns

"""Check if a path should be ignored based on gitignore patterns."""
def should_ignore(path, patterns):
    path_str = str(path)
    for pattern in patterns:
        if pattern.startswith('/'):
            pattern = pattern[1:]
        if fnmatch.fnmatch(path_str, f'*{pattern}*'):
            return True
    return False

"""Create a zip file from the project directory, respecting .gitignore rules."""
def create_zip(project_path):
    project_path = Path(project_path).resolve()
    project_name = project_path.name
    output_path = project_path.parent / f"{project_name}.zip"
    ignore_patterns = parse_gitignore(project_path)
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_path):
                root_path = Path(root)
                if '.git' in root_path.parts:
                    continue
                for file in files:
                    file_path = root_path / file
                    rel_path = file_path.relative_to(project_path)
                    if file != '.gitignore' and not should_ignore(rel_path, ignore_patterns):
                        zipf.write(file_path, rel_path)
        print(f"Zip file created at {output_path}")
    except Exception as e:
        print(f"Error creating zip file: {e}")

"""Convert all code files to .txt and store in a single output folder."""
def convert_to_txt(project_path):
    project_path = Path(project_path).resolve()
    output_folder = project_path.parent / f"{project_path.name}_txt"
    output_folder.mkdir(exist_ok=True)
    structure_file = output_folder / "Original_Folder_Structure.txt"
    ignore_patterns = parse_gitignore(project_path)
    
    valid_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.cs', '.html', '.css', '.json', '.xml', '.sh', '.php', 
        '.rb', '.swift', '.go', '.rs', '.kt', '.lua', '.perl', '.r', '.scala', '.sql', '.bat', '.cmd'
    }
    
    try:
        with open(structure_file, 'w', encoding='utf-8') as struct_f:
            struct_f.write("Original Folder Structure:\n\n")
            for root, _, files in os.walk(project_path):
                root_path = Path(root)
                if '.git' in root_path.parts:
                    continue
                for file in files:
                    file_path = root_path / file
                    rel_path = file_path.relative_to(project_path).as_posix()
                    struct_f.write(f"{rel_path}\n")
                    if not should_ignore(file_path, ignore_patterns):
                        if file_path.suffix in valid_extensions:
                            output_file = output_folder / f"{rel_path.replace('/', '_')}.txt"
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_src, open(output_file, 'w', encoding='utf-8') as f_dst:
                                f_dst.write(f_src.read())
        print(f"Converted files stored in {output_folder}")
    except Exception as e:
        print(f"Error converting files: {e}")

def main():
    choice = get_user_choice()
    if choice not in {'1', '2'}:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    project_dir = input("Enter the project directory path: ").strip()
    if not os.path.exists(project_dir) or not os.path.isdir(project_dir):
        print("Invalid directory path. Exiting.")
        sys.exit(1)
    if choice == '1':
        create_zip(project_dir)
    elif choice == '2':
        convert_to_txt(project_dir)

if __name__ == "__main__":
    main()
