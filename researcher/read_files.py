#!/usr/bin/env python3
"""Read files of various types from a folder and convert them to plain text / markdown."""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".jsonl",
    ".pdf", ".html", ".htm", ".xml", ".yaml", ".yml",
    ".log", ".tex", ".rst", ".py", ".r", ".sql",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path, delimiter: str = ",") -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    if not rows:
        return "(empty CSV)"
    header = rows[0]
    lines = [f"**Columns ({len(header)}):** " + ", ".join(header)]
    lines.append(f"**Rows:** {len(rows) - 1}")
    lines.append("")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    preview_rows = rows[1:21]
    for row in preview_rows:
        padded = row + [""] * (len(header) - len(row))
        lines.append("| " + " | ".join(padded[:len(header)]) + " |")
    if len(rows) - 1 > 20:
        lines.append(f"\n*... and {len(rows) - 21} more rows (showing first 20)*")
    return "\n".join(lines)


def read_json(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        keys = list(data[0].keys())
        lines = [f"**JSON array** with {len(data)} records"]
        lines.append(f"**Keys:** {', '.join(keys)}")
        lines.append("")
        lines.append("| " + " | ".join(keys) + " |")
        lines.append("| " + " | ".join("---" for _ in keys) + " |")
        for record in data[:20]:
            vals = [str(record.get(k, ""))[:60] for k in keys]
            lines.append("| " + " | ".join(vals) + " |")
        if len(data) > 20:
            lines.append(f"\n*... and {len(data) - 20} more records (showing first 20)*")
        return "\n".join(lines)
    return json.dumps(data, indent=2)[:5000]


def read_jsonl(path: Path) -> str:
    lines_raw = path.read_text(encoding="utf-8", errors="replace").strip().split("\n")
    records = []
    for line in lines_raw:
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if not records:
        return "(empty JSONL)"
    if isinstance(records[0], dict):
        keys = list(records[0].keys())
        lines = [f"**JSONL** with {len(records)} records"]
        lines.append(f"**Keys:** {', '.join(keys)}")
        lines.append("")
        lines.append("| " + " | ".join(keys) + " |")
        lines.append("| " + " | ".join("---" for _ in keys) + " |")
        for record in records[:20]:
            vals = [str(record.get(k, ""))[:60] for k in keys]
            lines.append("| " + " | ".join(vals) + " |")
        if len(records) > 20:
            lines.append(f"\n*... and {len(records) - 20} more records*")
        return "\n".join(lines)
    return "\n".join(str(r) for r in records[:20])


def read_pdf(path: Path) -> str:
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            return f"[PDF file: {path.name} — install PyMuPDF to extract text: pip install pymupdf]"
    doc = pymupdf.open(str(path))
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            pages.append(f"### Page {i + 1}\n\n{text.strip()}")
    doc.close()
    return "\n\n".join(pages) if pages else "(PDF contained no extractable text)"


def read_file(path: Path) -> dict:
    ext = path.suffix.lower()
    try:
        if ext == ".pdf":
            content = read_pdf(path)
        elif ext == ".csv":
            content = read_csv(path, delimiter=",")
        elif ext == ".tsv":
            content = read_csv(path, delimiter="\t")
        elif ext == ".json":
            content = read_json(path)
        elif ext == ".jsonl":
            content = read_jsonl(path)
        else:
            content = read_text(path)
    except Exception as e:
        content = f"[Error reading {path.name}: {e}]"

    return {
        "filename": path.name,
        "extension": ext,
        "size_bytes": path.stat().st_size,
        "content": content,
    }


def scan_folder(folder: Path, recursive: bool = False) -> list[dict]:
    results = []
    pattern = "**/*" if recursive else "*"
    for p in sorted(folder.glob(pattern)):
        if not p.is_file():
            continue
        if p.name.startswith("."):
            continue
        if p.suffix.lower() in SUPPORTED_EXTENSIONS:
            results.append(read_file(p))
    return results


def main():
    parser = argparse.ArgumentParser(description="Read files from a folder and output their content as markdown")
    parser.add_argument("folder", help="Path to folder containing files to analyze")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan subfolders recursively")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output as JSON instead of markdown")
    parser.add_argument("--summary", action="store_true", help="Print only a summary of files found")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: {folder} is not a directory.", file=sys.stderr)
        sys.exit(1)

    results = scan_folder(folder, recursive=args.recursive)

    if not results:
        print(f"No supported files found in {folder}", file=sys.stderr)
        print(f"Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}", file=sys.stderr)
        sys.exit(1)

    if args.summary:
        print(f"## File Summary for `{folder}`\n")
        print(f"**Total files:** {len(results)}\n")
        by_ext = {}
        for r in results:
            by_ext.setdefault(r["extension"], []).append(r)
        print("| Extension | Count | Files |")
        print("| --- | --- | --- |")
        for ext, files in sorted(by_ext.items()):
            names = ", ".join(f["filename"] for f in files)
            print(f"| {ext} | {len(files)} | {names} |")
        sys.exit(0)

    if args.output_json:
        print(json.dumps(results, indent=2))
        return

    print(f"# Files from `{folder}`\n")
    print(f"**{len(results)} files** found.\n")
    for r in results:
        print(f"---\n## {r['filename']} ({r['extension']}, {r['size_bytes']:,} bytes)\n")
        print(r["content"])
        print()


if __name__ == "__main__":
    main()
