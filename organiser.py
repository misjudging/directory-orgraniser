from __future__ import annotations

import argparse
import shutil
from pathlib import Path


TYPE_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md", ".odt"},
    "spreadsheets": {".xls", ".xlsx", ".csv"},
    "presentations": {".ppt", ".pptx"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "video": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".html",
        ".css",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".sh",
        ".ps1",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organise files into folders.")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Target directory")
    parser.add_argument(
        "--mode",
        choices=("type", "extension"),
        default="type",
        help="Grouping mode",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files",
    )
    return parser.parse_args()


def type_folder(extension: str) -> str:
    ext = extension.lower()
    for folder, extensions in TYPE_MAP.items():
        if ext in extensions:
            return folder
    return "other"


def extension_folder(extension: str) -> str:
    if not extension:
        return "no_extension"
    return extension.lower().lstrip(".") + "_files"


def pick_destination(file_path: Path, mode: str) -> str:
    if mode == "extension":
        return extension_folder(file_path.suffix)
    return type_folder(file_path.suffix)


def is_hidden(path: Path) -> bool:
    return path.name.startswith(".")


def unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        candidate = dest.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organise_directory(target: Path, mode: str, dry_run: bool, include_hidden: bool) -> int:
    moved = 0
    script_name = Path(__file__).name
    for item in target.iterdir():
        if item.is_dir():
            continue
        if item.name == script_name:
            continue
        if not include_hidden and is_hidden(item):
            continue

        folder = pick_destination(item, mode)
        destination_dir = target / folder
        destination_file = unique_destination(destination_dir / item.name)

        if dry_run:
            print(f"[DRY-RUN] {item.name} -> {destination_file.relative_to(target)}")
            moved += 1
            continue

        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(item), str(destination_file))
        print(f"Moved {item.name} -> {destination_file.relative_to(target)}")
        moved += 1
    return moved


def main() -> None:
    args = parse_args()
    target = args.path.resolve()

    if not target.exists() or not target.is_dir():
        raise SystemExit(f"Invalid directory: {target}")

    moved = organise_directory(target, args.mode, args.dry_run, args.include_hidden)
    print(f"Done. Processed {moved} file(s).")


if __name__ == "__main__":
    main()
