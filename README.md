# LLMCodeContextualizer

## Overview
LLMCodeContextualizer is a Python script designed to let AI models interact with your project directories efficiently. It offers two main functionalities:

1. **Zipping the project directory** while respecting the rules specified in the `.gitignore` file.
2. **Converting code files** within the project directory to `.txt` format, with two output options:
   - Individual text files stored in a separate output folder with a structure file
   - A single combined text file that includes all code with proper file headers and the original project structure

These methods provide a convenient way to give Large Language Models (LLMs) context on your codebase, either by converting your project directory into a zip file or into text files, both adhering to `.gitignore` rules.

## Features

- **Zip Project**: Creates a zip file of the project directory, excluding files and directories specified in the `.gitignore` file.
- **Convert to TXT**: Converts code files (with specific extensions) to `.txt` format with two options:
  - **Separate Files**: Each code file becomes its own .txt file in an output folder, with a separate structure file
  - **Combined File**: All code files are combined into a single .txt file placed directly in the parent directory, with clear headers and the project structure at the beginning

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/LLMCodeContextualizer.git
    cd LLMCodeContextualizer
    ```

2. Run the script:
    ```bash
    python script.py
    ```

3. Follow the on-screen prompts:
   - Choose between zipping the project or converting code files to `.txt`
   - If converting to txt, choose whether to keep files separate or combine them into one file
   - Enter the project directory path

## Output Handling

- For all output options, any existing output files or folders will be automatically replaced
- The combined file option creates a single `[project_name]_combined.txt` file in the parent directory
- The separate files option creates a `[project_name]_txt` folder containing individual text files and a structure file

## Functions

### `get_user_choice()`
Prompts the user to choose between zipping the project or converting code files to `.txt`.

### `get_output_format_choice()`
If the user chooses to convert to txt, this prompts them to choose between keeping files separate or combining them into one file.

### `parse_gitignore(project_path)`
Parses the `.gitignore` file to extract ignore patterns.

### `should_ignore(path, patterns)`
Checks if a given path should be ignored based on the provided `.gitignore` patterns.

### `create_zip(project_path)`
Creates a zip file of the project directory, respecting the rules specified in `.gitignore`.

### `convert_to_txt(project_path, combine_files=False)`
Converts code files within the project directory to `.txt` format, either as separate files in a folder or as a single combined file with headers.

## Supported Extensions

The script supports converting the following code file extensions to `.txt`:
- `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cpp`, `.c`, `.cs`, `.html`, `.css`, `.json`, `.xml`, `.sh`, `.php`, `.rb`, `.swift`, `.go`, `.rs`, `.kt`, `.lua`, `.perl`, `.r`, `.scala`, `.sql`, `.bat`, `.cmd`