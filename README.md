<h1 align="center">Code Snippet Generator</h1>

<div align="center">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/ogty/diff/main?style=for-the-badge">
    <img src="https://img.shields.io/github/pipenv/locked/python-version/ogty/diff/main?style=for-the-badge">
    <img src="https://img.shields.io/github/actions/workflow/status/ogty/code-snippet-generator/unit-test.yml?style=for-the-badge">
    <img src="https://img.shields.io/codecov/c/github/ogty/code-snippet-generator?style=for-the-badge&token=99AYWQ5VVM">
</div>

<br>

## Setup

<div align="center">

```
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│ ● ◍ ○                                   zsh                                              │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ $ git clone https://github.com/ogty/code-snippet-generator                               │
│ $ cd code-snippet-generator                                                              │
│ $ make # or `chmod +x ./snippet`                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

</div>

## Usage

<div align="center">

````
╭─ Markdown ─ docs/usage.md ───────────────────────────────────────────────────────────────╮
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ ```zsh                                                                                   │
│ $ ./snippet <subcommand> --path <file-path> [options]                                    │
│ ```                                                                                      │
│                                                                                          │
│ ### Subcommands                                                                          │
│                                                                                          │
│ - `diff`                                                                                 │
│ - `simple`                                                                               │
│ - `shell`                                                                                │
│                                                                                          │
│ ### Options                                                                              │
│                                                                                          │
│ | Long               | Short | Explanation                               | Required |    │
│ | ------------------ | ----- | ----------------------------------------- | -------- |    │
│ | `--path`           | `-p`  | File path                                 | True     |    │
│ | `--file`           | `-f`  | File name                                 | False    |    │
│ | `--width`          | `-w`  | Frame width                               | False    |    │
│ | `--output`         | `-o`  | Output file path                          | False    |    │
│ | `--language`       | `-l`  | Language                                  | False    |    │
│ | `--prefix`         | `-x`  | Prefix of each line                       | False    |    │
│ | `--line-number`    | `-n`  | Display of line numbers                   | False    |    │
│ | `--start-line`     | `-s`  | Start of line number                      | False    |    │
│ | `--current-file`   | `-c`  | Name the file you are reading as `--file` | False    |    │
│ | `--command-prompt` | `-m`  | Apply command prompt header               | False    |    │
│ | `--from-log`       | `-g`  | Generated from the most recent difference | False    |    │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
````

</div>

## Examples

<div align="center">

```
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│ ● ◍ ○                                   zsh                                              │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ $ ./snippet diff -p samples/diff.txt -f main.py -w 100 | pbcopy                          │
│ $ ./snippet simple -p snippet -f snippet.py -l Python -o ./samples/example1.txt -w 100   │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

```
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│▕  ▭ Desktop ×  ▏ +                                                            -   □   ×  │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ C:\Users\ogty\Desktop>git clone https://github.com/ogty/code-snippet-generator           │
│ C:\Users\ogty\Desktop>cd code-snippet-generator                                          │
│ C:\Users\ogty\Desktop\code-snippet-generator>make # or `chmod +x ./snippet`              │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

```
╭─ snippet ────────────────────────────────────────────────────────────────────────────────╮
├──────────────────────────────────────────────────────────────────────────────────────────┤
│  6 ▓▓▓▓░ 6 Changes: 5 additions & 1 deletion                                             │
├─────────────┬────────────────────────────────────────────────────────────────────────────┤
│  ...    ... │   @@ -61,6 +61,7 @@ if __name__ == "__main__":                             │
├─────────────┼────────────────────────────────────────────────────────────────────────────┤
│   61     61 │               Arguments.output,                                            │
│   62     62 │               Arguments.prefix,                                            │
│   63     63 │               Arguments.language,                                          │
│          64 │ +             Arguments.command_prompt,                                    │
│   64     65 │           ],                                                               │
│   65     66 │       )                                                                    │
│   66     67 │                                                                            │
├─────────────┼────────────────────────────────────────────────────────────────────────────┤
│     ...     │   @@ -119,6 +120,7 @@ if __name__ == "__main__":                           │
├─────────────┼────────────────────────────────────────────────────────────────────────────┤
│  119    120 │           elif sub_command_name == "shell":                                │
│  120    121 │               shell_name = arguments.language                              │
│  121    122 │               prefix = arguments.prefix                                    │
│         123 │ +             is_command_prompt = arguments.command_prompt                 │
│  122    124 │                                                                            │
│  123    125 │               config = ShellSnippetConfig(                                 │
│  124    126 │                   language=shell_name,                                     │
├─────────────┼────────────────────────────────────────────────────────────────────────────┤
│     ...     │   @@ -127,7 +129,9 @@ if __name__ == "__main__":                           │
├─────────────┼────────────────────────────────────────────────────────────────────────────┤
│  127    129 │                   max_frame_width=max_frame_width,                         │
│  128    130 │               )                                                            │
│  129    131 │               shell_snippet = ShellSnippet(config=config)                  │
│  130        │ -             output = shell_snippet.generate(prefix=prefix)               │
│         132 │ +             output = shell_snippet.generate(                             │
│         133 │ +                 prefix=prefix, is_command_prompt=is_command_prompt       │
│         134 │ +             )                                                            │
│  131    135 │               if output_path:                                              │
│  132    136 │                     shell_snippet.write_output(output=output, file_path=o  │
│             │   utput_path)                                                              │
│  133    137 │                   exit(0)                                                  │
╰─────────────┴────────────────────────────────────────────────────────────────────────────╯
```

</div>
