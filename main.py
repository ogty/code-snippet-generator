import os

from models.diff_snippet import DiffSnippet
from models.simple_snippet import SimpleSnippet
from schemas.snippet import DiffSnippetConfig, SnippetConfig
from settings import READ


if __name__ == "__main__":
    terminal_width = int(os.popen("tput cols", READ).read().strip())

    config = DiffSnippetConfig(
        file_name="abstract/code_snippet.py",
        file_path="./samples/diff.txt",
        language='',
        max_frame_width=100,
        # max_frame_width=terminal_width,
    )
    diff_snippet = DiffSnippet(config=config)
    output = diff_snippet.generate()
    print(output)

    config = SnippetConfig(
        file_name="command.sh",
        file_path="./samples/command.sh",
        language='',
        max_frame_width=100,
        # max_frame_width=terminal_width,
    )
    simple_snippet = SimpleSnippet(config=config)
    output = simple_snippet.generate()
    print(output)
