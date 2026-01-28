import os
import re

def read_latex_project(project_dir, main_file):
    """
    Reads a LaTeX project, recursively expanding \input{} commands.
    Returns the full text content.
    """
    main_file_path = os.path.join(project_dir, main_file)
    if not os.path.exists(main_file_path):
        raise FileNotFoundError(f"Main file not found: {main_file_path}")

    with open(main_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find \input{filename}
    # Matches \input{filename} or \input{filename.tex}
    input_regex = re.compile(r'\\input\{([^}]+)\}')

    def replace_input(match):
        filename = match.group(1)
        if not filename.endswith('.tex'):
            filename += '.tex'

        filepath = os.path.join(project_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                sub_content = f.read()
            # Recursively process imports in the sub-file
            return input_regex.sub(replace_input, sub_content)
        else:
            print(f"Warning: file not found: {filepath}")
            return match.group(0) # Keep original text if file not found

    full_content = input_regex.sub(replace_input, content)
    return full_content
