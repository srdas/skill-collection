#!/usr/bin/env python3
"""
write_latex.py — Convert survey_output.md + papers/papers.json to a LaTeX article.

Usage:
    python write_latex.py [--survey survey_output.md] [--papers papers/papers.json]
                          [--output survey_output.tex] [--title "My Survey"]
                          [--author "Author Name"] [--doc-class article]
"""

import re
import json
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Markdown → LaTeX conversion helpers
# ---------------------------------------------------------------------------

def _escape(text: str) -> str:
    """Escape LaTeX special characters (except those we handle structurally)."""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("{",  r"\{"),
        ("}",  r"\}"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]
    for char, replacement in replacements:
        text = text.replace(char, replacement)
    return text


def _inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code, citations) to LaTeX."""
    # Restore & that was part of table structure — handled separately
    # Citations: [Key2023] → \cite{Key2023}
    text = re.sub(r"\[([A-Za-z][A-Za-z0-9_:+-]*\d{4}[a-z]?)\]", r"\\cite{\1}", text)

    # Bold+italic: ***text***
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\\textbf{\\textit{\1}}", text)
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*",  r"\\textit{\1}", text)
    text = re.sub(r"_([^_]+)_",   r"\\textit{\1}", text)
    # Inline code: `text`
    text = re.sub(r"`([^`]+)`", r"\\texttt{\1}", text)
    # Markdown links: [label](url) → label\footnote{url}
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1\\footnote{\\url{\2}}", text)

    return text


# ---------------------------------------------------------------------------
# Table conversion
# ---------------------------------------------------------------------------

def _convert_table(lines: list[str]) -> list[str]:
    """Convert a block of markdown table lines to a LaTeX longtable."""
    rows = []
    for line in lines:
        if re.match(r"^\s*\|[-:| ]+\|\s*$", line):
            continue  # separator row
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    if not rows:
        return []

    ncols = max(len(r) for r in rows)
    col_spec = "|" + "l|" * ncols

    out = [
        r"\begin{center}",
        r"\begin{tabular}{" + col_spec + r"}",
        r"\hline",
    ]
    for i, row in enumerate(rows):
        # Pad short rows
        while len(row) < ncols:
            row.append("")
        latex_cells = " & ".join(_inline(_escape(c)) for c in row)
        out.append(latex_cells + r" \\")
        out.append(r"\hline")
        if i == 0:
            # Re-add \hline after header for double-rule effect
            out.append(r"\hline")

    out += [r"\end{tabular}", r"\end{center}", ""]
    return out


# ---------------------------------------------------------------------------
# List conversion
# ---------------------------------------------------------------------------

def _flush_list(items: list[str], ordered: bool) -> list[str]:
    env = "enumerate" if ordered else "itemize"
    out = [f"\\begin{{{env}}}"]
    for item in items:
        out.append(f"  \\item {_inline(_escape(item))}")
    out.append(f"\\end{{{env}}}")
    return out


# ---------------------------------------------------------------------------
# Core converter
# ---------------------------------------------------------------------------

def md_to_latex(md_text: str, doc_title: str, doc_author: str, doc_class: str) -> str:
    lines = md_text.splitlines()

    preamble = [
        f"\\documentclass[12pt]{{{doc_class}}}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T1]{fontenc}",
        "\\usepackage{lmodern}",
        "\\usepackage{microtype}",
        "\\usepackage{hyperref}",
        "\\usepackage{url}",
        "\\usepackage{longtable}",
        "\\usepackage{booktabs}",
        "\\usepackage{graphicx}",
        "\\usepackage{geometry}",
        "\\geometry{margin=1in}",
        "",
        f"\\title{{{_escape(doc_title)}}}",
        f"\\author{{{_escape(doc_author)}}}",
        "\\date{\\today}",
        "",
        "\\begin{document}",
        "\\maketitle",
        "\\tableofcontents",
        "\\newpage",
        "",
    ]

    body: list[str] = []
    i = 0
    in_list: list[str] = []
    list_ordered = False
    table_lines: list[str] = []
    in_table = False
    in_verbatim = False

    def flush_pending():
        nonlocal in_list, table_lines, in_table
        if in_list:
            body.extend(_flush_list(in_list, list_ordered))
            in_list = []
        if in_table and table_lines:
            body.extend(_convert_table(table_lines))
            table_lines = []
            in_table = False

    while i < len(lines):
        line = lines[i]

        # --- fenced code blocks ---
        if line.strip().startswith("```"):
            flush_pending()
            if not in_verbatim:
                body.append(r"\begin{verbatim}")
                in_verbatim = True
            else:
                body.append(r"\end{verbatim}")
                in_verbatim = False
            i += 1
            continue

        if in_verbatim:
            body.append(line)
            i += 1
            continue

        # --- markdown table detection ---
        if re.match(r"^\s*\|", line):
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            body.extend(_convert_table(table_lines))
            table_lines = []
            in_table = False
            # fall through to process current line

        # --- headings ---
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            flush_pending()
            depth = len(m.group(1))
            title_text = _inline(_escape(m.group(2)))
            cmd = {1: "section", 2: "section", 3: "subsection", 4: "subsubsection"}[depth]
            body.append(f"\\{cmd}{{{title_text}}}")
            body.append("")
            i += 1
            continue

        # --- horizontal rule ---
        if re.match(r"^[-*_]{3,}\s*$", line):
            flush_pending()
            body.append(r"\medskip\noindent\rule{\linewidth}{0.4pt}\medskip")
            i += 1
            continue

        # --- unordered list items ---
        m = re.match(r"^(\s*)[-*+]\s+(.*)", line)
        if m:
            if in_list and list_ordered:
                flush_pending()
            list_ordered = False
            in_list.append(m.group(2))
            i += 1
            continue

        # --- ordered list items ---
        m = re.match(r"^(\s*)\d+[.)]\s+(.*)", line)
        if m:
            if in_list and not list_ordered:
                flush_pending()
            list_ordered = True
            in_list.append(m.group(2))
            i += 1
            continue

        # --- blank line ---
        if line.strip() == "":
            flush_pending()
            body.append("")
            i += 1
            continue

        # --- blockquote ---
        if line.startswith(">"):
            flush_pending()
            content = line.lstrip("> ").strip()
            body.append(r"\begin{quote}")
            body.append(_inline(_escape(content)))
            body.append(r"\end{quote}")
            i += 1
            continue

        # --- normal paragraph line ---
        flush_pending()
        body.append(_inline(_escape(line)))
        i += 1

    flush_pending()
    if in_verbatim:
        body.append(r"\end{verbatim}")

    return "\n".join(preamble + body + ["", "\\end{document}", ""])


# ---------------------------------------------------------------------------
# Bibliography builder
# ---------------------------------------------------------------------------

def build_bibliography(papers: list[dict]) -> list[str]:
    """Generate a \thebibliography block from the papers manifest."""
    if not papers:
        return []

    lines = [f"\\begin{{thebibliography}}{{{len(papers)}}}"]
    for p in papers:
        key = p.get("key", "unknown")
        authors = ", ".join(p.get("authors") or []) or "Unknown Author"
        title   = p.get("title", "Untitled")
        year    = p.get("year", "")
        doi     = p.get("doi") or ""
        url     = p.get("open_access_pdf") or ""

        cite_url = f"\\url{{{doi}}}" if doi else (f"\\url{{{url}}}" if url else "")
        entry = f"  {_escape(authors)}. \\textit{{{_escape(title)}}}. {_escape(str(year))}."
        if cite_url:
            entry += f" {cite_url}."

        lines.append(f"\\bibitem{{{key}}}")
        lines.append(entry)
    lines.append("\\end{thebibliography}")
    return lines


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert survey_output.md to a LaTeX article."
    )
    parser.add_argument("--survey",   default=None,
                        help="Path to the markdown survey (default: <bib_dir>/survey_output.md)")
    parser.add_argument("--papers",   default=None,
                        help="Path to papers manifest (default: <survey_dir>/papers/papers.json)")
    parser.add_argument("--output",   default=None,
                        help="Output .tex file (default: <survey_dir>/survey_output.tex)")
    parser.add_argument("--title",    default="Literature Survey",
                        help="Document title")
    parser.add_argument("--author",   default="",
                        help="Author name(s)")
    parser.add_argument("--doc-class", default="article",
                        choices=["article", "report", "IEEEtran", "acmart"],
                        help="LaTeX document class (default: article)")
    args = parser.parse_args()

    survey_path = Path(args.survey) if args.survey else Path("survey_output.md")
    if not survey_path.exists():
        print(f"Error: survey file not found: {survey_path}")
        raise SystemExit(1)

    survey_dir = survey_path.parent
    md_text = survey_path.read_text(encoding="utf-8")

    # Try to extract title from first # heading if not supplied
    doc_title = args.title
    if doc_title == "Literature Survey":
        m = re.search(r"^#\s+(.+)", md_text, re.MULTILINE)
        if m:
            doc_title = m.group(1).strip()

    latex = md_to_latex(md_text, doc_title, args.author, args.doc_class)

    # Inject bibliography before \end{document}
    papers_path = Path(args.papers) if args.papers else survey_dir / "papers" / "papers.json"
    if papers_path.exists():
        papers = json.loads(papers_path.read_text(encoding="utf-8"))
        bib_lines = build_bibliography(papers)
        latex = latex.replace("\\end{document}", "\n".join(bib_lines) + "\n\\end{document}")
    else:
        print(f"Warning: papers manifest not found at {papers_path}; skipping bibliography.")

    out_path = Path(args.output) if args.output else survey_dir / "survey_output.tex"
    out_path.write_text(latex, encoding="utf-8")
    print(f"Wrote LaTeX survey → {out_path}")
    print(f"Compile with:  pdflatex {out_path}  (run twice for TOC/refs)")


if __name__ == "__main__":
    main()
