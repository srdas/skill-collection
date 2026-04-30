# Researcher Skill

A Claude Code skill that reads all files in a folder — PDFs, CSVs, text, markdown, JSON, and more — formulates research questions, performs empirical analysis, and presents results with visualizations.

## Origin Prompt

> Write a new skill that when pointed to a folder, will read all the files therein, which could be of multiple types, e.g., pdf, csv, txt, md, etc., and then produce some empirical analysis of these files, beginning with a research question, doing the analysis, and then providing the results with visualizations, if any. If Python code is needed for any of the activities, such as reading csv files into pandas, using matplotlib for visualizations, converting files into markdown, etc., please write the code in `.py` files and cover their use in the SKILL.md file.

## Workflow

1. **Inventory** — Scan the target folder and catalog all supported files
2. **Ingest** — Read and convert files into a unified text/data representation
3. **Question** — Propose research questions based on what's in the data
4. **Analyze** — Run statistical analysis on structured data; perform qualitative analysis on documents
5. **Visualize** — Generate plots (histograms, scatter plots, correlations, time series, bar charts)
6. **Report** — Present findings in a structured report with embedded visualizations

## Python Helper Scripts

| Script | Purpose |
| --- | --- |
| `read_files.py` | Scan a folder and read files of all supported types into markdown/text |
| `analyze_csv.py` | Statistical analysis of tabular data (CSV, TSV, JSON) with auto-generated plots |
| `visualize.py` | Generate specific plot types (timeseries, scatter, bar, box, histogram) |

### `read_files.py`

Reads files from a folder and outputs their content as markdown.

```bash
# Show a summary of files in a folder
python3 read_files.py ~/data/my-project/ --summary

# Read all files and output as markdown
python3 read_files.py ~/data/my-project/

# Recursive scan with JSON output
python3 read_files.py ~/data/my-project/ -r --json
```

Supported file types: `.csv`, `.tsv`, `.json`, `.jsonl`, `.pdf`, `.txt`, `.md`, `.html`, `.xml`, `.yaml`, `.yml`, `.tex`, `.rst`, `.py`, `.r`, `.sql`, `.log`

### `analyze_csv.py`

Performs statistical analysis on tabular data files.

```bash
# Summary statistics
python3 analyze_csv.py data.csv

# Summary stats with auto-generated plots
python3 analyze_csv.py data.csv --plots -o ./output/

# JSON output for programmatic use
python3 analyze_csv.py data.csv --json
```

Generates: distribution histograms, scatter matrices, correlation heatmaps, categorical bar charts.

### `visualize.py`

Generates specific plot types from data files.

```bash
# Time series
python3 visualize.py data.csv --type timeseries --x date --y price volume -o timeseries.png

# Scatter plot with color grouping
python3 visualize.py data.csv --type scatter --x age --y income --hue education -o scatter.png

# Bar chart with aggregation
python3 visualize.py data.csv --type bar --x department --y salary --agg median -o bars.png

# Box plot
python3 visualize.py data.csv --type box --x region --y revenue -o boxplot.png

# Histogram
python3 visualize.py data.csv --type hist --y height weight -o histogram.png
```

## Installation

```bash
pip install pandas matplotlib pymupdf tabulate
```

- **pandas** — required for all tabular data analysis
- **matplotlib** — required for visualizations
- **pymupdf** — required only for reading PDF files
- **tabulate** — required for markdown table formatting

## Folder Structure

```
researcher/
├── README.md              # This file
├── read_files.py          # File ingestion script
├── analyze_csv.py         # Statistical analysis script
├── visualize.py           # Visualization script
└── skills/
    └── SKILL.md           # Claude Code skill definition
```

## Usage

Point the skill at any folder:

```
/researcher ~/path/to/folder
```

The skill will inventory the files, propose research questions, and — after confirmation — perform the analysis and present a structured report with visualizations.
