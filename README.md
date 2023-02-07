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

```
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
│ | Long             | Short | Explanation                               | Required |      │
│ | ---------------- | ----- | ----------------------------------------- | -------- |      │
│ | `--path`         | `-p`  | File path                                 | True     |      │
│ | `--file`         | `-f`  | File name                                 | False    |      │
│ | `--width`        | `-w`  | Frame width                               | False    |      │
│ | `--output`       | `-o`  | Output file path                          | False    |      │
│ | `--language`     | `-l`  | Language                                  | False    |      │
│ | `--prefix`       | `-x`  | Prefix of each line                       | False    |      │
│ | `--line-number`  | `-n`  | Display of line numbers                   | False    |      │
│ | `--start-line`   | `-s`  | Start of line number                      | False    |      │
│ | `--current-file` | `-c`  | Name the file you are reading as `--file` | False    |      │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

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

</div>
