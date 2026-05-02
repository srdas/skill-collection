---
name: researcher
description: Read all files in a folder, formulate a research question, perform empirical analysis, present results with visualizations, generate a reproducible Jupyter notebook, and produce a LaTeX paper
---

# Researcher Skill

## Trigger

Activate when the user asks to:
- Analyze or investigate files in a folder or directory
- Do research or empirical analysis on a dataset or collection of documents
- Explore a folder of mixed-format files (PDF, CSV, TXT, MD, JSON, etc.)
- "What can we learn from these files?"
- Generate insights, summaries, or visualizations from a data folder

Also invocable manually with `/researcher <folder_path>`.

## Behavior

When pointed at a folder, perform a complete research workflow:

### Phase 1: Inventory and Ingestion

1. **Scan the folder** to identify all files and their types. Run the helper script:
   ```bash
   python3 researcher/read_files.py <folder_path> --summary
   ```
2. **Read file contents** into a unified markdown representation:
   ```bash
   python3 researcher/read_files.py <folder_path>
   ```
   For recursive scanning of subfolders, add `-r`:
   ```bash
   python3 researcher/read_files.py <folder_path> -r
   ```
3. **Report the inventory** to the user: what files were found, their types, sizes, and a brief content preview.

### Phase 2: Research Question Formulation

4. **Examine the content** across all ingested files. Look for:
   - Themes, patterns, or topics that span multiple files
   - Quantitative data that can be analyzed statistically
   - Relationships between different files or data sources
   - Temporal patterns, trends, or anomalies
   - Gaps or inconsistencies worth investigating

5. **Propose 2-3 research questions** to the user. Each question should:
   - Be answerable from the available data
   - Require synthesis across multiple files or data dimensions
   - Lead to concrete, presentable findings
   - Example: "Is there a significant correlation between X and Y in the dataset?"
   - Example: "How has the distribution of Z changed across the time periods covered?"
   - Example: "What are the dominant themes across these documents, and how do they relate?"

6. **Confirm with the user** which research question(s) to pursue, or accept their alternative question.

### Phase 3: Analysis

7. **For structured data (CSV, TSV, JSON, JSONL)**, use the analysis helper:
   ```bash
   python3 researcher/analyze_csv.py <file> --plots -o <output_dir>
   ```
   This produces:
   - Summary statistics (shape, types, distributions, missing values)
   - Correlation matrices for numeric columns
   - Distribution histograms, scatter matrices, and bar charts

8. **For text/document data (PDF, TXT, MD, TEX)**, perform qualitative analysis:
   - Identify key themes, entities, and arguments
   - Count and categorize recurring concepts
   - Extract quantitative claims or data points embedded in text
   - Compare and contrast across documents

9. **For mixed collections**, combine both approaches:
   - Use structured data to test hypotheses
   - Use text documents for context and interpretation
   - Cross-reference findings across file types

10. **Generate visualizations** as needed using the visualization helper:
    ```bash
    python3 researcher/visualize.py <data_file> --type <plot_type> --x <col> --y <col> -o <output.png>
    ```
    Available plot types:
    - `timeseries` — line plots over a date column (`--x date_col --y val_col1 val_col2`)
    - `scatter` — scatter plot with optional color grouping (`--x col1 --y col2 --hue group_col`)
    - `bar` — aggregated bar chart (`--x category --y value --agg mean|sum|count`)
    - `box` — box plot by category (`--x category --y value`)
    - `hist` — histogram (`--y col1 col2`)

### Phase 4: Results

11. **Present findings** in a structured report:

    ```
    ## Research Question
    [The question being investigated]

    ## Data Sources
    [List of files used and their roles in the analysis]

    ## Methodology
    [Brief description of the analytical approach]

    ## Findings
    [Key results with supporting evidence]
    [Embed any generated visualizations]

    ## Discussion
    [Interpretation of findings, limitations, and caveats]

    ## Conclusion
    [Direct answer to the research question]
    ```

12. **Show visualizations** inline by reading the generated PNG files so the user can see them directly.

### Phase 5: Notebook Generation

13. **Create a Jupyter notebook** (`research_notebook.ipynb`) in the output directory that reproduces all figures and analysis. The notebook should contain:
    - A markdown cell with the research question and data source descriptions
    - Code cells that load the data, perform the analysis, and generate each figure
    - Markdown cells between code cells explaining each step and interpreting results
    - All plots should be generated inline with `%matplotlib inline`
    - Use `plt.savefig()` in each plot cell to also save figures as PDF files (for LaTeX inclusion) alongside the inline display
    - A final markdown cell summarizing key findings

    Use the `NotebookEdit` tool to create and populate the notebook cell by cell. The notebook should be fully self-contained and re-runnable.

14. **Verify the notebook** by running it:
    ```bash
    jupyter nbconvert --to notebook --execute research_notebook.ipynb --output research_notebook_executed.ipynb
    ```
    If execution fails, fix the notebook and re-run until it succeeds. Confirm that all figure PDF files were generated.

### Phase 6: LaTeX Paper Generation

15. **Generate a LaTeX paper** (`paper.tex`) in the output directory that synthesizes the chat report and figures into a complete academic paper. The paper should follow this structure:

    ```latex
    \documentclass[11pt]{article}
    \usepackage{graphicx, booktabs, amsmath, hyperref, natbib, geometry}
    \geometry{margin=1in}

    \title{[Descriptive title derived from the research question]}
    \author{[User's name if known, otherwise leave as placeholder]}
    \date{\today}

    \begin{document}
    \maketitle

    \begin{abstract}
    [Concise summary: motivation, method, key findings, and conclusion — 150-250 words]
    \end{abstract}

    \section{Introduction}
    [Background context, motivation, and the specific research question]

    \section{Data}
    [Description of data sources, file types, sizes, and any preprocessing steps]

    \section{Methodology}
    [Analytical approach: statistical methods, tools used, and rationale]

    \section{Results}
    [Key findings with embedded figures and tables]
    % Include figures generated by the notebook:
    % \begin{figure}[htbp]
    %   \centering
    %   \includegraphics[width=0.8\textwidth]{figure_name.pdf}
    %   \caption{Descriptive caption.}
    %   \label{fig:figure_name}
    % \end{figure}

    \section{Discussion}
    [Interpretation of results, comparison with expectations, limitations, and caveats]

    \section{Conclusion}
    [Direct answer to the research question and potential future directions]

    \end{document}
    ```

16. **Populate the paper** using content from the chat report (Phase 4) and reference all figures generated by the notebook (Phase 5). Specifically:
    - Convert all findings, methodology, and discussion from the chat report into LaTeX prose
    - Include every generated figure using `\includegraphics` with proper captions and labels
    - Format any tabular results using `booktabs` tables
    - Add cross-references between text and figures/tables using `\ref{}`
    - Ensure all figure PDF paths are relative to the paper's directory

17. **Compile the paper** to verify it builds:
    ```bash
    cd <output_dir> && pdflatex -interaction=nonstopmode paper.tex && pdflatex -interaction=nonstopmode paper.tex
    ```
    Run pdflatex twice to resolve cross-references. If compilation fails, fix the LaTeX source and re-compile. Show the compiled PDF to the user by reading it.

## Supported File Types

| Extension | How it's processed |
| --- | --- |
| `.csv`, `.tsv` | Parsed as tabular data with pandas; full statistical analysis |
| `.json`, `.jsonl` | Parsed as structured data; array-of-objects treated as tabular |
| `.pdf` | Text extracted via PyMuPDF; analyzed as document |
| `.txt`, `.md`, `.rst`, `.tex` | Read as plain text; analyzed as document |
| `.html`, `.htm`, `.xml` | Read as text; tags preserved for structure |
| `.yaml`, `.yml` | Read as text/config |
| `.py`, `.r`, `.sql` | Read as code; analyzed for logic and comments |
| `.log` | Read as text; analyzed for patterns and events |

## Prerequisites

Required Python packages:
```bash
pip install pandas matplotlib pymupdf tabulate jupyter nbconvert
```

- **pandas** — data analysis (required for CSV/JSON analysis and visualizations)
- **matplotlib** — plot generation (required for visualizations)
- **pymupdf** — PDF text extraction (required only if analyzing PDFs)
- **tabulate** — markdown table formatting for pandas (required for summary stats)
- **jupyter** — notebook creation and execution (required for Phase 5)
- **nbconvert** — notebook execution and validation (required for Phase 5)

Required system packages for LaTeX compilation (Phase 6):
```bash
# macOS
brew install --cask mactex-no-gui
# or minimal: brew install basictex

# Ubuntu/Debian
sudo apt-get install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended

# Alternatively, install tectonic (lightweight):
# brew install tectonic  OR  cargo install tectonic
```

If a package is missing, the scripts will report which one to install and continue with reduced functionality where possible. If LaTeX is not installed, generate the `.tex` file and inform the user they can compile it manually or install a TeX distribution.

## Pre-authorized Commands

The following commands are pre-authorized and should run without per-call approval:

```
python3 researcher/read_files.py *
python3 researcher/analyze_csv.py *
python3 researcher/visualize.py *
pip install pandas matplotlib pymupdf tabulate jupyter nbconvert
jupyter nbconvert --to notebook --execute *
pdflatex -interaction=nonstopmode *
```

## Constraints

- Always propose research questions to the user before starting analysis — do not assume what the user wants to investigate.
- Ground all findings in the actual data. Never fabricate statistics, trends, or patterns.
- When data is insufficient to answer a question, say so explicitly rather than speculating.
- Report limitations: sample size, missing data, selection bias, confounding variables.
- Label all visualizations with clear titles, axis labels, and legends.
- For large datasets (>10,000 rows), work with summaries and samples rather than printing raw data.
- Keep the final report concise — detailed tables and raw output go in appendices, not the main narrative.
- The Jupyter notebook must be self-contained: include all imports, data loading, and figure generation so it runs independently of the helper scripts.
- Save all notebook figures as both PNG (for inline display) and PDF (for LaTeX inclusion) using `plt.savefig()`.
- The LaTeX paper must compile cleanly with standard `pdflatex` — avoid packages that require XeLaTeX or LuaLaTeX unless the user requests them.
- All figure paths in the LaTeX paper must be relative and match the filenames saved by the notebook.
- Do not fabricate references or citations. Only include a bibliography if the user provides source material that warrants citation.

## Examples

**Single CSV dataset:**
```
/researcher ~/data/sales/
```
→ Scans folder, finds `sales_2024.csv` and `regions.csv`, proposes questions about regional sales patterns, generates correlation plots and trend analysis. Creates a notebook reproducing all figures and a LaTeX paper with the full write-up.

**Mixed document collection:**
```
/researcher ~/projects/literature-review/papers/
```
→ Reads PDFs and markdown notes, identifies common themes, produces a synthesis of findings across papers with a structured summary. Generates a notebook for any quantitative analysis and a LaTeX paper synthesizing the literature review.

**Multi-format research folder:**
```
/researcher ~/research/climate-study/ 
```
→ Ingests CSV data files, PDF reports, and markdown field notes. Proposes questions linking quantitative measurements to qualitative observations. Produces statistical analysis with visualizations, a reproducible Jupyter notebook, and a compiled LaTeX paper ready for submission.
