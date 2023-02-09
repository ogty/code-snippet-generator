```zsh
$ ./snippet <subcommand> --path <file-path> [options]
```

### Subcommands

- `diff`
- `simple`
- `shell`

### Options

| Long               | Short | Explanation                               | Required |
| ------------------ | ----- | ----------------------------------------- | -------- |
| `--path`           | `-p`  | File path                                 | True     |
| `--file`           | `-f`  | File name                                 | False    |
| `--width`          | `-w`  | Frame width                               | False    |
| `--output`         | `-o`  | Output file path                          | False    |
| `--language`       | `-l`  | Language                                  | False    |
| `--prefix`         | `-x`  | Prefix of each line                       | False    |
| `--line-number`    | `-n`  | Display of line numbers                   | False    |
| `--start-line`     | `-s`  | Start of line number                      | False    |
| `--current-file`   | `-c`  | Name the file you are reading as `--file` | False    |
| `--command-prompt` | `-m`  | Apply command prompt header               | False    |
| `--from-log`       | `-g`  | Generated from the most recent difference | False    |
