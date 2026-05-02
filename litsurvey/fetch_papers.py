#!/usr/bin/env python3
"""
fetch_papers.py — Fetch paper metadata and abstracts from a BibTeX file.

Usage:
    python fetch_papers.py <input.bib> [--output-dir papers]

For each BibTeX entry, the script:
  1. Queries the Semantic Scholar API (by DOI, arXiv ID, or title search).
  2. Falls back to the CrossRef API for DOI-based metadata.
  3. Saves a per-paper JSON file with title, abstract, authors, citation
     count, year, and an open-access PDF URL when available.
  4. Writes a master manifest (papers.json) that summarises all results.
"""

import json
import time
import argparse
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------
try:
    import bibtexparser
except ImportError:
    import subprocess, sys
    print("Installing bibtexparser …")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bibtexparser"])
    import bibtexparser

# ---------------------------------------------------------------------------
# API constants
# ---------------------------------------------------------------------------
SS_BASE = "https://api.semanticscholar.org/graph/v1"
CROSSREF_BASE = "https://api.crossref.org/works"
SS_FIELDS = (
    "title,abstract,year,authors,externalIds,"
    "citationCount,openAccessPdf,influentialCitationCount"
)
_UA = "litsurvey/1.0 (academic research; mailto:researcher@example.com)"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _get(url: str, timeout: int = 20) -> dict | None:
    """GET a URL and return parsed JSON, or None on any error."""
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Semantic Scholar lookup
# ---------------------------------------------------------------------------

def _ss_lookup(doi: str | None, arxiv_id: str | None, title: str | None) -> dict | None:
    """Try DOI → arXiv ID → title-search, return first hit."""
    for identifier, prefix in [(doi, "DOI"), (arxiv_id, "ARXIV")]:
        if identifier:
            url = f"{SS_BASE}/paper/{prefix}:{urllib.parse.quote(identifier)}?fields={SS_FIELDS}"
            data = _get(url)
            if data and "paperId" in data:
                return data
            time.sleep(0.3)

    if title:
        url = (
            f"{SS_BASE}/paper/search"
            f"?query={urllib.parse.quote(title)}&fields={SS_FIELDS}&limit=1"
        )
        data = _get(url)
        if data and data.get("data"):
            return data["data"][0]

    return None


# ---------------------------------------------------------------------------
# CrossRef fallback
# ---------------------------------------------------------------------------

def _crossref_lookup(doi: str) -> dict | None:
    if not doi:
        return None
    data = _get(f"{CROSSREF_BASE}/{urllib.parse.quote(doi)}")
    if not data:
        return None
    msg = data.get("message", {})
    titles = msg.get("title") or []
    date_parts = (msg.get("published", {}).get("date-parts") or [[None]])[0]
    return {
        "title": titles[0] if titles else "",
        "abstract": msg.get("abstract", ""),
        "year": date_parts[0],
        "authors": [
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in msg.get("author", [])
        ],
    }


# ---------------------------------------------------------------------------
# BibTeX field helpers
# ---------------------------------------------------------------------------

def _clean(s: str) -> str:
    return s.replace("{", "").replace("}", "").strip()


def _extract_arxiv_id(entry: dict) -> str | None:
    for field in ("eprint", "url", "howpublished"):
        val = entry.get(field, "")
        if "arxiv" in val.lower():
            parts = val.rstrip("/").split("/")
            candidate = parts[-1]
            if candidate:
                return candidate
    if entry.get("archiveprefix", "").lower() == "arxiv" and entry.get("eprint"):
        return entry["eprint"].strip()
    return None


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_bib(bib_path: str, output_dir: str) -> list[dict]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    with open(bib_path, encoding="utf-8") as fh:
        library = bibtexparser.load(fh)

    print(f"Found {len(library.entries)} entries in {bib_path}\n")
    manifest: list[dict] = []

    for entry in library.entries:
        key = entry.get("ID", "unknown")
        title = _clean(entry.get("title", ""))
        doi = _clean(entry.get("doi", ""))
        arxiv_id = _extract_arxiv_id(entry)
        year = entry.get("year", "")

        print(f"[{key}] {title[:72]}")

        ss = _ss_lookup(doi or None, arxiv_id, title)
        time.sleep(0.5)

        cr: dict | None = None
        if not ss and doi:
            cr = _crossref_lookup(doi)

        record: dict = {
            "key": key,
            "title": title,
            "year": year,
            "doi": doi or None,
            "arxiv_id": arxiv_id,
            "abstract": "",
            "authors": [],
            "citation_count": None,
            "influential_citation_count": None,
            "open_access_pdf": None,
            "semantic_scholar_id": None,
        }

        if ss:
            record["abstract"] = ss.get("abstract") or ""
            record["citation_count"] = ss.get("citationCount")
            record["influential_citation_count"] = ss.get("influentialCitationCount")
            record["semantic_scholar_id"] = ss.get("paperId")
            oa = ss.get("openAccessPdf") or {}
            record["open_access_pdf"] = oa.get("url")
            record["authors"] = [a.get("name", "") for a in (ss.get("authors") or [])]
            if not record["year"]:
                record["year"] = str(ss.get("year") or "")
        elif cr:
            record["abstract"] = cr.get("abstract", "")
            record["authors"] = cr.get("authors", [])
            if not record["year"] and cr.get("year"):
                record["year"] = str(cr["year"])

        status = (
            f"  abstract={'yes' if record['abstract'] else 'no'}, "
            f"pdf={'yes' if record['open_access_pdf'] else 'no'}, "
            f"citations={record['citation_count']}"
        )
        print(status)

        (out / f"{key}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False)
        )
        manifest.append(record)

    manifest_path = out / "papers.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\nSaved {len(manifest)} records → {manifest_path}")
    return manifest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch paper metadata from a BibTeX file via Semantic Scholar / CrossRef."
    )
    parser.add_argument("bib_file", help="Path to the .bib input file")
    parser.add_argument(
        "--output-dir", default=None,
        help="Directory for per-paper JSON files (default: <bib_dir>/papers/)"
    )
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = str(Path(args.bib_file).parent / "papers")
    process_bib(args.bib_file, args.output_dir)


if __name__ == "__main__":
    main()
