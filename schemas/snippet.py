from typing import TypedDict


class Changes(TypedDict):
    changes: int
    additions: int
    deletions: int


class SnippetConfig(TypedDict):
    language: str
    file_name: str
    file_path: str
    output_path: str


class DiffSnippetConfig(SnippetConfig, total=False):
    number_digits: int


class ShellSnippetConfig(SnippetConfig, total=False):
    shell_name: str
