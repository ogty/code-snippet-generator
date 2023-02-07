import os
from subprocess import run


def get_path() -> str:
    return os.getcwd()


def get_file_name(path: str) -> str:
    path = os.path.abspath(path)
    return os.path.basename(path).split("/")[-1]


def get_branch() -> str:
    git_branches = run(["git", "branch"], capture_output=True).stdout.decode()
    current_branch = [
        branch.strip() for branch in git_branches.splitlines() if branch.startswith("*")
    ][0]
    return current_branch[2:]
