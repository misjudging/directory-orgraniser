# Directory Orgraniser

A quick CLI tool to organise files in a directory into subfolders.

## What it does

- Scans a target directory
- Groups files by extension or broad type
- Moves files into generated folders (for example `images`, `documents`, `code`, `archives`, `other`)
- Supports dry-run mode so you can preview changes first

## Usage

```bash
python organiser.py --path "C:\path\to\target" --dry-run
python organiser.py --path "C:\path\to\target"
```

## Options

- `--path`: directory to organise (default: current directory)
- `--mode`: `type` or `extension` (default: `type`)
- `--dry-run`: print planned moves without changing files
- `--include-hidden`: include hidden files

## Notes

- The script ignores directories and only moves files.
- It never moves the script itself.
