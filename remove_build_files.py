import os
import fnmatch
import shutil

def read_gitignore(filepath='.gitignore'):
    with open(filepath, 'r') as file:
        patterns = file.readlines()
    patterns = [pattern.strip() for pattern in patterns if pattern.strip() and not pattern.startswith('#')]
    return patterns

def matches_pattern(file_path, patterns, exceptions):
    for pattern in patterns:
        if any(fnmatch.fnmatch(file_path, exception) for exception in exceptions):
            return False
        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(file_path, os.path.join('**', pattern)):
            return True
    return False

def delete_files(base_path, patterns, exceptions):
    for root, dirs, files in os.walk(base_path, topdown=False):
        for name in files:
            file_path = os.path.relpath(os.path.join(root, name), base_path)
            if matches_pattern(file_path, patterns, exceptions):
                os.remove(os.path.join(root, name))
                print(f"Deleted file: {file_path}")
        for name in dirs:
            dir_path = os.path.relpath(os.path.join(root, name), base_path)
            if matches_pattern(dir_path, patterns, exceptions):
                shutil.rmtree(os.path.join(root, name))
                print(f"Deleted directory: {dir_path}")

if __name__ == '__main__':
    gitignore_path = '.gitignore'  # Path to the .gitignore file
    base_path = '.'  # Base path to start deleting files from
    exceptions = ['.vscode', '.venv']  # List of exceptions

    patterns = read_gitignore(gitignore_path)
    delete_files(base_path, patterns, exceptions)

