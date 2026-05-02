# litsurvey — Literature Survey Skill

Produce a high-quality, synthesised literature survey from a BibTeX file.

---

## Invocation

```
/litsurvey <path-to-file.bib> [--topic "optional topic description"]
```

The `--topic` argument lets you focus the survey on a specific angle of the
bibliography (e.g. `"attention mechanisms in NLP"` from a broader set of deep-
learning papers).

---

## What this skill does

When invoked, Claude will:

1. **Fetch paper metadata** by running `fetch_papers.py` against the supplied
   `.bib` file.  This contacts the Semantic Scholar and CrossRef APIs to
   retrieve titles, abstracts, authors, citation counts, and open-access PDF
   URLs, then saves them in a `papers/` subdirectory **co-located with the
   `.bib` file**.

2. **Read and synthesise** the collected metadata to produce a structured
   literature survey that follows the quality criteria in `survey.md`.

3. **Write the survey** to `survey_output.md` **in the same folder as the
   `.bib` file** (or a name you specify).

---

## Step-by-step instructions for Claude

### Step 1 — Install dependency (if needed)

```bash
pip install bibtexparser --quiet
```

### Step 2 — Run the metadata fetcher

```bash
python fetch_papers.py <path-to-file.bib>
```

The output directory defaults to `<bib_dir>/papers/` (i.e., a `papers/`
subfolder next to the `.bib` file).  Pass `--output-dir` to override.

This produces:
- `<bib_dir>/papers/<key>.json` — one file per BibTeX entry
- `<bib_dir>/papers/papers.json` — master manifest with all records

### Step 3 — Read the manifest

Let `BIB_DIR` be the directory that contains the `.bib` file.
Read `<BIB_DIR>/papers/papers.json` and every individual
`<BIB_DIR>/papers/<key>.json` to build a full picture of the corpus.
Pay special attention to:
- `citation_count` / `influential_citation_count` — signals of impact
- `abstract` — primary source for synthesis
- `year` — for chronological mapping
- `open_access_pdf` — note which papers are downloadable

### Step 4 — Synthesise the survey

Apply every quality criterion from `survey.md`:

| Criterion | How to apply |
|:---|:---|
| **Comprehensive breadth** | Cover all entries; call out seminal vs. recent work |
| **Critical synthesis** | Group papers by theme/methodology, never list them verbatim |
| **Taxonomy** | Build at least one classification tree or thematic grouping |
| **Strengths & weaknesses** | Include a comparison table for the main approaches |
| **Future directions** | End with open challenges and a 5–10 year outlook |
| **Citations** | Use the BibTeX keys as citation handles, e.g. `[Vaswani2017]` |

### Step 5 — Write the survey document

Save the finished survey as `<BIB_DIR>/survey_output.md` (same folder as the
`.bib` file) with this structure:

```
# Literature Survey: <Topic>

## Abstract
## 1. Introduction & Scope
## 2. Historical Background
## 3. Taxonomy of Approaches
## 4. Key Methods & Results
   ### 4.1 <Theme A>
   ### 4.2 <Theme B>
   …
## 5. Comparative Analysis
   (include a Markdown table)
## 6. Open Challenges & Future Directions
## References
```

### Step 6 — Generate the LaTeX version

Run `write_latex.py` to convert `survey_output.md` into a compilable LaTeX
article with a proper bibliography drawn from `papers/papers.json`.  All
paths are expressed relative to `BIB_DIR`:

```bash
python write_latex.py \
    --survey  <BIB_DIR>/survey_output.md \
    --papers  <BIB_DIR>/papers/papers.json \
    --output  <BIB_DIR>/survey_output.tex \
    --title   "<Topic>" \
    --author  "<Author Name(s)>"
```

When `--papers` and `--output` are omitted, they default to
`<survey_dir>/papers/papers.json` and `<survey_dir>/survey_output.tex`
respectively (i.e., co-located with the `--survey` file).

Optional flags:

| Flag | Default | Notes |
|:---|:---|:---|
| `--doc-class` | `article` | Also accepts `report`, `IEEEtran`, `acmart` |
| `--author` | _(empty)_ | Pass a quoted string, e.g. `"Alice Smith, Bob Jones"` |
| `--output` | `<survey_dir>/survey_output.tex` | Any `.tex` path |

To compile to PDF (run twice so the table of contents and citations resolve):

```bash
pdflatex <BIB_DIR>/survey_output.tex
pdflatex <BIB_DIR>/survey_output.tex
```

### Step 7 — Report to the user

Summarise:
- Number of papers processed, how many had abstracts, how many have open-
  access PDFs.
- The thematic taxonomy you built.
- Absolute paths to both `<BIB_DIR>/survey_output.md` and
  `<BIB_DIR>/survey_output.tex`.

---

## Design principles (from survey.md)

- Write with a **bird's-eye view** — accessible to a newcomer, informative to
  an expert.
- **Synthesise**, don't annotate.  "Papers A, B, C all tackle X by doing Y,
  but differ in Z" beats three separate bullet points.
- Highlight **paradigm-shifting** papers (high `influential_citation_count`).
- Identify **gaps**: what the literature does *not* address.
- Use **Markdown tables** to compare approaches across key dimensions.

---

## Error handling

| Situation | Action |
|:---|:---|
| `bibtexparser` not installed | Bootstrap via `pip` inside `fetch_papers.py` |
| API rate-limit (HTTP 429) | Script waits 0.5 s between requests; re-run if still throttled |
| No abstract returned | Note the paper in the survey as "abstract unavailable" and rely on title/DOI |
| `.bib` file not found | Report the exact path and ask the user to confirm |

---

## Files in this skill

| File | Purpose |
|:---|:---|
| `SKILL.md` | This file — instructions for Claude |
| `fetch_papers.py` | Python script to fetch metadata via Semantic Scholar / CrossRef |
| `write_latex.py` | Python script to convert `survey_output.md` → `survey_output.tex` |
| `survey.md` | Quality criteria a good literature survey must satisfy |
| `README.md` | User-facing documentation for the `litsurvey` folder |
