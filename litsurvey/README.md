# litsurvey

A Claude Code skill that turns a **BibTeX file** into a structured, synthesised
literature survey — complete with thematic taxonomy, comparative tables, and
future-directions analysis.

---

## Quick start

```bash
# 1. Copy your .bib file into this folder (or point to it by path)
cp ~/references/my_papers.bib .

# 2. In Claude Code, invoke the skill
/litsurvey my_papers.bib --topic "transformer architectures in NLP"
```

Claude will fetch paper metadata, synthesise the content, and write all
outputs — `papers/`, `survey_output.md`, and `survey_output.tex` — **into
the same folder as the input `.bib` file**.

```bash
# 3. Compile to PDF (requires a LaTeX distribution)
pdflatex ~/references/survey_output.tex && pdflatex ~/references/survey_output.tex
```

---

## How it works

```
my_papers.bib
      │
      ▼
fetch_papers.py          ← queries Semantic Scholar & CrossRef APIs
      │
      ▼
<bib_dir>/papers/
  ├── papers.json        ← master manifest (title, abstract, citations, …)
  ├── Author2023.json
  └── …
      │
      ▼
Claude synthesises       ← follows quality criteria in survey.md
      │
      ├── <bib_dir>/survey_output.md    ← Markdown survey
      │
      ▼
write_latex.py           ← converts Markdown + papers.json to LaTeX
      │
      ▼
<bib_dir>/survey_output.tex        ← compilable LaTeX article
      │
      ▼
pdflatex (×2)            ← produces <bib_dir>/survey_output.pdf
```

### Metadata collected per paper

| Field | Source |
|:---|:---|
| Title, abstract, year | Semantic Scholar / CrossRef |
| Authors | Semantic Scholar / CrossRef |
| Citation count | Semantic Scholar |
| Influential citation count | Semantic Scholar |
| Open-access PDF URL | Semantic Scholar (Unpaywall-backed) |

---

## Files

| File | Description |
|:---|:---|
| `SKILL.md` | Full instructions Claude follows when the skill is invoked |
| `fetch_papers.py` | Python 3.9+ script — no heavy dependencies beyond `bibtexparser` |
| `write_latex.py` | Python 3.9+ script — converts `survey_output.md` to a compilable `.tex` file |
| `survey.md` | Reference document defining what makes a high-quality survey |
| `README.md` | This file |

---

## Requirements

- Python 3.9 or later
- `bibtexparser` (`fetch_papers.py` installs it automatically if missing)
- Internet access to reach the Semantic Scholar and CrossRef APIs
- A LaTeX distribution (e.g. [TeX Live](https://www.tug.org/texlive/) or
  [MiKTeX](https://miktex.org/)) to compile the generated `.tex` file to PDF

No API key is required for Semantic Scholar's public rate-limited tier
(~100 req / 5 min).  For large bibliographies (> 200 entries), consider
[requesting an API key](https://www.semanticscholar.org/product/api) for higher
limits.

---

## Output format

Both a Markdown and a LaTeX version are produced in the same folder as the
input `.bib` file.

`survey_output.md` follows this structure:

1. **Abstract** — one-paragraph overview
2. **Introduction & Scope** — research question, included/excluded topics
3. **Historical Background** — how the field evolved
4. **Taxonomy of Approaches** — thematic / methodological classification
5. **Key Methods & Results** — grouped analysis by theme
6. **Comparative Analysis** — Markdown table of approaches vs. metrics
7. **Open Challenges & Future Directions** — gaps and 5–10 year outlook
8. **References** — all BibTeX keys used

`survey_output.tex` is a compilable LaTeX article with:

- `\tableofcontents` and proper `\section` / `\subsection` hierarchy
- Markdown tables converted to `tabular` environments
- Inline citations `[Key2023]` converted to `\cite{Key2023}`
- A `\thebibliography` block auto-generated from `papers/papers.json`
- Configurable document class (`article`, `report`, `IEEEtran`, `acmart`)

Compile to PDF (from the folder containing the `.bib` file):

```bash
pdflatex survey_output.tex
pdflatex survey_output.tex   # second pass resolves TOC and citations
```

---

## Tips

- **Snowballing:** after the initial survey, check which papers have the
  highest `citation_count` and manually inspect their reference lists
  (backward snowballing) and Google Scholar "Cited by" pages (forward
  snowballing) to catch important work not in your `.bib` file.

- **Focused surveys:** use `--topic` to restrict the synthesis to a sub-area
  even if your `.bib` file is broader.

- **Re-running:** the `papers/` directory is reused on subsequent runs; delete
  it to force a fresh API fetch.

---

## Example

```bash
/litsurvey attention_mechanisms.bib --topic "self-attention in vision models"
```

Produces `survey_output.md` covering ~30 papers, organised into themes such as
*Patch-based attention*, *Hybrid CNN-Transformer*, and *Efficient attention
variants*, with a comparison table on accuracy, parameter count, and inference
speed.

To also get a camera-ready LaTeX version with a specific document class:

```bash
python write_latex.py \
    --survey  ~/references/survey_output.md \
    --papers  ~/references/papers/papers.json \
    --output  ~/references/survey_output.tex \
    --title   "Self-Attention in Vision Models: A Survey" \
    --author  "Your Name" \
    --doc-class IEEEtran
```
