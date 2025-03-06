import os
import sys
import zipfile
import fnmatch
from pathlib import Path
import re
import shutil

"""Get User Choice"""
def get_user_choice():
    print("Choose an option:")
    print("1 - Zip the project (respecting .gitignore)")
    print("2 - Convert code files to .txt and store in a single folder")
    choice = input("Enter 1 or 2: ")
    return choice

"""Get Output Format Choice for txt conversion"""
def get_output_format_choice():
    print("\nChoose an output format:")
    print("1 - Keep files separate (one .txt file per code file)")
    print("2 - Combine all files into a single .txt file")
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

"""Check if a path should be ignored based on gitignore patterns or is package-lock.json."""
def should_ignore(rel_path, patterns): # Changed parameter to rel_path
    path_str = str(rel_path) # Use rel_path
    
    # Always ignore package-lock.json
    if path_str == 'package-lock.json' or path_str.endswith('/package-lock.json'):
        return True
        
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

    # Remove existing zip if it exists
    if output_path.exists():
        output_path.unlink()

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
def convert_to_txt(project_path, combine_files=False):
    project_path = Path(project_path).resolve()
    project_name = project_path.name
    ignore_patterns = parse_gitignore(project_path)

    valid_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.cs', '.html', '.css', '.json', '.xml', '.sh', '.php',
        '.rb', '.swift', '.go', '.rs', '.kt', '.lua', '.perl', '.r', '.scala', '.sql', '.bat', '.cmd'
    }

    try:
        # Get the folder structure first
        folder_structure = []
        for root, _, files in os.walk(project_path):
            root_path = Path(root)
            if '.git' in root_path.parts:
                continue
            for file in files:
                file_path = root_path / file
                rel_path = file_path.relative_to(project_path)
                if not should_ignore(rel_path, ignore_patterns): # Only add if not ignored
                    folder_structure.append(rel_path.as_posix()) # Store as string for structure list

        if combine_files:
            # For combined option, create a single file in the parent directory
            combined_file_path = project_path.parent / f"{project_name}_combined.txt"

            # Remove existing file if it exists
            if combined_file_path.exists():
                combined_file_path.unlink()

            with open(combined_file_path, 'w', encoding='utf-8') as combined_f:
                # Write the project structure at the beginning
                combined_f.write("# PROJECT DIRECTORY STRUCTURE\n\n")
                for path in sorted(folder_structure):
                    combined_f.write(f"{path}\n")
                combined_f.write("\n\n")

                # Process and add each file
                for root, _, files in os.walk(project_path):
                    root_path = Path(root)
                    if '.git' in root_path.parts:
                        continue
                    for file in files:
                        file_path = root_path / file
                        rel_path = file_path.relative_to(project_path) # Get rel_path as Path object

                        if not should_ignore(rel_path, ignore_patterns) and file_path.suffix in valid_extensions: # Pass rel_path to should_ignore
                            # Create a header for this file
                            combined_f.write(f"\n{'=' * 80}\n")
                            combined_f.write(f"# FILE: {rel_path}\n")
                            combined_f.write(f"{'=' * 80}\n\n")

                            # Add the file content
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_src:
                                    content = f_src.read()
                                    combined_f.write(content)
                                    # Add a newline if the file doesn't end with one
                                    if content and not content.endswith('\n'):
                                        combined_f.write('\n')
                            except Exception as e:
                                combined_f.write(f"Error reading file: {e}\n")

            print(f"All files combined into {combined_file_path}")
        else:
            # For separate files option, create an output folder
            output_folder = project_path.parent / f"{project_name}_txt"

            # Remove existing output folder if it exists
            if output_folder.exists():
                shutil.rmtree(output_folder)

            # Create the output folder
            output_folder.mkdir(exist_ok=True)

            # Create the structure file
            structure_file = output_folder / "Original_Folder_Structure.txt"
            with open(structure_file, 'w', encoding='utf-8') as struct_f:
                struct_f.write("Original Folder Structure:\n\n")
                for path in sorted(folder_structure):
                    struct_f.write(f"{path}\n")

            # Process individual files
            for root, _, files in os.walk(project_path):
                root_path = Path(root)
                if '.git' in root_path.parts:
                    continue
                for file in files:
                    file_path = root_path / file
                    rel_path = file_path.relative_to(project_path) # Get rel_path as Path object

                    if not should_ignore(rel_path, ignore_patterns) and file_path.suffix in valid_extensions: # Pass rel_path to should_ignore
                        output_file = output_folder / f"{rel_path.as_posix().replace('/', '_')}.txt"
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
        output_format = get_output_format_choice()
        if output_format not in {'1', '2'}:
            print("Invalid choice. Using separate files by default.")
            convert_to_txt(project_dir, combine_files=False)
        else:
            combine_files = (output_format == '2')
            convert_to_txt(project_dir, combine_files=combine_files)

if __name__ == "__main__":
    main()