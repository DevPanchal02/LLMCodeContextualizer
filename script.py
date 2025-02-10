
import os
import sys
import zipfile
import fnmatch
from pathlib import Path
import re

def find_requirements(project_path):
    """Find all Python requirements in the project."""
    requirements = set()
    
    # Check for requirements.txt
    req_file = os.path.join(project_path, 'requirements.txt')
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove version specifiers
                    package = re.split(r'[=<>]', line)[0].strip()
                    requirements.add(package)
    
    # Scan Python files for imports
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        # Find import statements
                        imports = re.findall(r'^import\s+(\w+)|^from\s+(\w+)', content, re.MULTILINE)
                        for imp in imports:
                            package = imp[0] or imp[1]
                            # Filter out standard library modules
                            if package and not is_stdlib_module(package):
                                requirements.add(package)
                except Exception as e:
                    print(f"Warning: Could not process {file}: {e}")
    
    return sorted(list(requirements))

def is_stdlib_module(module_name):
    """Check if a module is part of the Python standard library."""
    try:
        # Try to find the module's spec
        import importlib.util
        spec = importlib.util.find_spec(module_name)
        
        # If spec is None, the module doesn't exist
        if spec is None:
            return False
            
        # Check if the module's location is within Python's installation directory
        return spec.origin is not None and "site-packages" not in spec.origin
    except (ImportError, AttributeError):
        # If we can't determine it, assume it's not stdlib
        return False

def parse_gitignore(project_path):
    """Parse .gitignore file and return list of patterns to ignore."""
    gitignore_path = os.path.join(project_path, '.gitignore')
    patterns = []
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    
    return patterns

def should_ignore(path, patterns):
    """Check if a path should be ignored based on gitignore patterns."""
    path_str = str(path)
    for pattern in patterns:
        if pattern.startswith('/'):
            pattern = pattern[1:]
        if fnmatch.fnmatch(path_str, f'*{pattern}*'):
            return True
    return False

def create_zip(project_path):
    """Create a zip file from the project directory, respecting .gitignore rules."""
    project_path = Path(project_path).resolve()
    
    if not project_path.exists():
        print(f"Error: Path '{project_path}' does not exist.")
        return
    
    if not project_path.is_dir():
        print(f"Error: Path '{project_path}' is not a directory.")
        return
    
    # Get project name for zip file
    project_name = project_path.name
    output_path = project_path.parent / f"{project_name}.zip"
    
    # Parse .gitignore patterns
    ignore_patterns = parse_gitignore(project_path)
    
    try:
        # Find requirements first
        print("Scanning for Python dependencies...")
        requirements = find_requirements(project_path)
        
        print("\nCreating zip file...")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for root, dirs, files in os.walk(project_path):
                root_path = Path(root)
                
                # Skip .git directory
                if '.git' in root_path.parts:
                    continue
                
                # Process each file
                for file in files:
                    file_path = root_path / file
                    rel_path = file_path.relative_to(project_path)
                    
                    # Skip .gitignore file itself
                    if file == '.gitignore':
                        continue
                    
                    # Check if file should be ignored
                    if not should_ignore(rel_path, ignore_patterns):
                        zipf.write(file_path, rel_path)
                        file_count += 1
        
        # Print summary
        print(f"\nZip file created successfully!")
        print(f"Location: {output_path}")
        print(f"Size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        print(f"Files included: {file_count}")
        
        # Print requirements
        if requirements:
            print("\nRequired Python packages:")
            print("To install all requirements, run:")
            for req in requirements:
                print(f"pip install {req}")
        else:
            print("\nNo Python package requirements detected.")
        
    except Exception as e:
        print(f"Error creating zip file: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <project_directory>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    create_zip(project_dir)

if __name__ == "__main__":
    main()
