import os
import fnmatch
import shutil
from pathlib import Path

def project_root(anchor: str = ".git"):
    path = Path.cwd()
    for parent in [path] + list(path.parents):
        if (parent / anchor).exists():
            return parent
    raise FileNotFoundError(
        f"Could not find {anchor} in the parent directories of {path}")

def read_gitignore(filepath='.gitignore'):
    with open(filepath, 'r') as file:
        patterns = file.readlines()
    patterns = [pattern.strip() for pattern in patterns if pattern.strip()
                and not pattern.startswith('#')]
    return patterns


def matches_pattern(file_path: str, patterns: list[str], exceptions: list[str]):
    for pattern in patterns:
        if any(fnmatch.fnmatch(file_path, exception) for exception in exceptions):
            return False
        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(file_path, os.path.join('**', pattern)):
            return True
    return False


def delete_files(base_path: str, patterns: list[str], exceptions: list[str]):
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
    ROOT = project_root()

    gitignore_path = ROOT / '.gitignore'
    base_path = '.' 
    exceptions = ['.vscode', '.venv']

    patterns = read_gitignore(gitignore_path)
    delete_files(base_path, patterns, exceptions)
