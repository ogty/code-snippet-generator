from typing import TypedDict


class Changes(TypedDict):

    additions: int
    deletions: int


class SnippetConfig(TypedDict):

    language: str
    file_name: str
    file_path: str
    max_frame_width: int


class DiffSnippetConfig(SnippetConfig, total=False):

    number_digits: int
