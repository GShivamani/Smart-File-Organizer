"""
Smart File Organizer
Automatically organizes files in a directory by type, date, or size.
Supports dry-run mode, undo, and logging.
"""

import os
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

LOG_FILE = "organizer_log.json"

FILE_CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos":     [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".java", ".go", ".rs", ".json", ".xml", ".yaml", ".yml"],
    "Executables": [".exe", ".msi", ".sh", ".bat", ".app"],
    "Fonts":      [".ttf", ".otf", ".woff", ".woff2"],
}


def get_category(file_path):
    ext = Path(file_path).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def get_date_folder(file_path):
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m")


def get_size_folder(file_path):
    size = os.path.getsize(file_path)
    if size < 1024 * 100:
        return "Small_under100KB"
    elif size < 1024 * 1024 * 10:
        return "Medium_100KB-10MB"
    else:
        return "Large_over10MB"


def scan_directory(directory):
    stats = defaultdict(list)
    total_size = 0
    for item in Path(directory).iterdir():
        if item.is_file() and item.name != LOG_FILE:
            cat = get_category(item)
            size = item.stat().st_size
            stats[cat].append({"name": item.name, "size": size})
            total_size += size

    print(f"\n📁 Scan Results for: {directory}")
    print("=" * 50)
    for cat, files in sorted(stats.items()):
        total = sum(f["size"] for f in files)
        print(f"  {cat:20s} | {len(files):4d} files | {total/1024:.1f} KB")
    print(f"\n  Total: {sum(len(v) for v in stats.values())} files | {total_size/1024:.1f} KB")
    return stats


def organize(directory, mode="type", dry_run=False):
    directory = Path(directory)
    log = []
    moved = 0

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Organizing by: {mode.upper()}")
    print("=" * 50)

    for item in directory.iterdir():
        if not item.is_file() or item.name == LOG_FILE:
            continue

        if mode == "type":
            folder_name = get_category(item)
        elif mode == "date":
            folder_name = get_date_folder(item)
        elif mode == "size":
            folder_name = get_size_folder(item)
        else:
            folder_name = get_category(item)

        dest_dir = directory / folder_name
        dest_path = dest_dir / item.name

        print(f"  {'[WOULD MOVE]' if dry_run else 'Moving':12s} {item.name} → {folder_name}/")

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            if dest_path.exists():
                stem = item.stem
                suffix = item.suffix
                timestamp = datetime.now().strftime("%H%M%S")
                dest_path = dest_dir / f"{stem}_{timestamp}{suffix}"

            shutil.move(str(item), str(dest_path))
            log.append({
                "original": str(item),
                "moved_to": str(dest_path),
                "timestamp": datetime.now().isoformat()
            })
            moved += 1

    if not dry_run:
        log_path = directory / LOG_FILE
        existing = []
        if log_path.exists():
            with open(log_path) as f:
                existing = json.load(f)
        with open(log_path, "w") as f:
            json.dump(existing + log, f, indent=2)
        print(f"\n✅ Done! Moved {moved} files. Log saved to {LOG_FILE}")
    else:
        print(f"\n🔍 Dry run complete. {sum(1 for i in directory.iterdir() if i.is_file())} files would be moved.")


def undo(directory):
    log_path = Path(directory) / LOG_FILE
    if not log_path.exists():
        print("❌ No log file found. Cannot undo.")
        return

    with open(log_path) as f:
        log = json.load(f)

    if not log:
        print("❌ Nothing to undo.")
        return

    last_session = []
    last_time = None
    for entry in reversed(log):
        t = entry["timestamp"][:16]
        if last_time is None:
            last_time = t
        if t == last_time:
            last_session.append(entry)
        else:
            break

    print(f"\n↩️  Undoing {len(last_session)} moves...")
    for entry in last_session:
        src = Path(entry["moved_to"])
        dst = Path(entry["original"])
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"  Restored: {src.name} → {dst.parent.name}/")

    remaining = [e for e in log if e not in last_session]
    with open(log_path, "w") as f:
        json.dump(remaining, f, indent=2)

    print(f"\n✅ Undo complete.")


def main():
    parser = argparse.ArgumentParser(description="Smart File Organizer")
    parser.add_argument("directory", nargs="?", default=".", help="Target directory")
    parser.add_argument("--mode", choices=["type", "date", "size"], default="type",
                        help="Organization mode (default: type)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    parser.add_argument("--scan", action="store_true", help="Show stats without organizing")
    parser.add_argument("--undo", action="store_true", help="Undo last organize operation")

    args = parser.parse_args()

    if args.scan:
        scan_directory(args.directory)
    elif args.undo:
        undo(args.directory)
    else:
        organize(args.directory, mode=args.mode, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
