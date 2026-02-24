# 📁 Smart File Organizer

> Automatically sorts files in any directory by type, date modified, or size — with dry-run preview, undo support, and JSON logging.

---

## 📌 Description

A CLI tool that organizes messy directories by moving files into auto-created subfolders. Supports 3 sorting modes, a safe dry-run preview, full undo functionality using a JSON log, and directory scan stats.

---

## 🛠️ Tech Stack

- Python 3.x
- Standard Library only (`os`, `shutil`, `json`, `pathlib`, `argparse`)

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
python file_organizer.py --help
```

---

## 💻 Usage

```bash
# Organize current directory by file type (default)
python file_organizer.py .

# Organize by date modified
python file_organizer.py /path/to/folder --mode date

# Organize by file size
python file_organizer.py /path/to/folder --mode size

# Preview without moving anything
python file_organizer.py . --dry-run

# View directory stats
python file_organizer.py . --scan

# Undo last operation
python file_organizer.py . --undo
```

---

## 📂 Output Structure (Type Mode)

```
folder/
├── Images/
├── Videos/
├── Documents/
├── Code/
├── Archives/
├── Others/
└── organizer_log.json
```

---

## 🎮 Features

| Feature | Details |
|---|---|
| Sort Modes | By type, date modified, file size |
| Dry Run | Preview moves without executing |
| Undo | Revert last organize session |
| Logging | JSON log of all moves |
| Scan | Stats on file distribution |
| Conflict Handling | Auto-renames duplicate filenames |

---

## 🧠 Concepts Covered

- File I/O and `pathlib`
- CLI with `argparse`
- JSON-based logging and undo systems
- Directory traversal and file metadata

---

## 📄 License

MIT
