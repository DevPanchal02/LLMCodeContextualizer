# LLMCodeContextualizer

## Overview
LLMCodeContextualizer is a Python script designed to let AI models interact with your project directories efficiently. It offers two main functionalities:

1. **Zipping the project directory** while respecting the rules specified in the `.gitignore` file.
2. **Converting code files** within the project directory to `.txt` format and storing them in a separate output folder with an extra file labeling the original project directory structure (Useful for Gemini).

These methods provide a convenient way to give Large Language Models (LLMs) context on your codebase, either by converting your project directory into a zip file or into text files, both adhering to `.gitignore` rules.

## Features

- **Zip Project**: Creates a zip file of the project directory, excluding files and directories specified in the `.gitignore` file.
- **Convert to TXT**: Converts code files (with specific extensions) to `.txt` format and stores them in a separate output folder, while preserving the original folder structure. Includes a seperate txt file labeled as original project structure.

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

3. Follow the on-screen prompts to choose between zipping the project or converting code files to `.txt`.

## Functions

### `get_user_choice()`
Prompts the user to choose between zipping the project or converting code files to `.txt`.

### `parse_gitignore(project_path)`
Parses the `.gitignore` file to extract ignore patterns.

### `should_ignore(path, patterns)`
Checks if a given path should be ignored based on the provided `.gitignore` patterns.

### `create_zip(project_path)`
Creates a zip file of the project directory, respecting the rules specified in `.gitignore`.

### `convert_to_txt(project_path)`
Converts code files within the project directory to `.txt` format and stores them in a separate output folder.

## Supported Extensions

The script supports converting the following code file extensions to `.txt`:
- `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cpp`, `.c`, `.cs`, `.html`, `.css`, `.json`, `.xml`, `.sh`, `.php`, `.rb`, `.swift`, `.go`, `.rs`, `.kt`, `.lua`, `.perl`, `.r`, `.scala`, `.sql`, `.bat`, `.cmd`