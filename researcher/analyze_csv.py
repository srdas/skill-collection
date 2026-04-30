#!/usr/bin/env python3
"""Analyze CSV/TSV files: summary statistics, correlations, distributions, and visualizations."""

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is not installed. Run: pip install pandas", file=sys.stderr)
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def load_data(path: Path) -> pd.DataFrame:
    ext = path.suffix.lower()
    if ext == ".tsv":
        return pd.read_csv(path, sep="\t")
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".jsonl":
        return pd.read_json(path, lines=True)
    return pd.read_csv(path)


def summary_stats(df: pd.DataFrame) -> str:
    lines = []
    lines.append(f"**Shape:** {df.shape[0]} rows x {df.shape[1]} columns\n")

    lines.append("### Column Types\n")
    lines.append("| Column | Type | Non-null | Unique | Sample values |")
    lines.append("| --- | --- | --- | --- | --- |")
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        unique = df[col].nunique()
        samples = df[col].dropna().head(3).tolist()
        sample_str = ", ".join(str(s)[:30] for s in samples)
        lines.append(f"| {col} | {dtype} | {non_null}/{len(df)} | {unique} | {sample_str} |")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("\n### Numeric Summary\n")
        desc = df[numeric_cols].describe().round(4)
        lines.append(desc.to_markdown())

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        lines.append("\n### Categorical Summary\n")
        for col in cat_cols[:10]:
            vc = df[col].value_counts().head(10)
            lines.append(f"\n**{col}** (top {min(10, len(vc))} of {df[col].nunique()} unique):\n")
            for val, count in vc.items():
                pct = count / len(df) * 100
                lines.append(f"- {val}: {count} ({pct:.1f}%)")

    if len(numeric_cols) >= 2:
        lines.append("\n### Correlation Matrix\n")
        corr = df[numeric_cols].corr().round(3)
        lines.append(corr.to_markdown())

    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        lines.append("\n### Missing Values\n")
        lines.append("| Column | Missing | % |")
        lines.append("| --- | --- | --- |")
        for col, count in missing.items():
            pct = count / len(df) * 100
            lines.append(f"| {col} | {count} | {pct:.1f}% |")

    return "\n".join(lines)


def generate_plots(df: pd.DataFrame, output_dir: Path, prefix: str = "plot") -> list[str]:
    if plt is None:
        return ["(matplotlib not installed — skipping visualizations)"]

    created = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if numeric_cols:
        n = min(len(numeric_cols), 12)
        cols_to_plot = numeric_cols[:n]
        ncols = min(3, n)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
        if nrows * ncols == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        for i, col in enumerate(cols_to_plot):
            ax = axes[i]
            df[col].dropna().hist(bins=30, ax=ax, edgecolor="black", alpha=0.7)
            ax.set_title(col, fontsize=10)
            ax.set_xlabel("")
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        fig.suptitle("Numeric Distributions", fontsize=14, y=1.02)
        fig.tight_layout()
        path = output_dir / f"{prefix}_distributions.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        created.append(str(path))

    if len(numeric_cols) >= 2:
        n = min(len(numeric_cols), 8)
        cols_to_plot = numeric_cols[:n]
        try:
            from pandas.plotting import scatter_matrix
            fig, axes = plt.subplots(figsize=(3 * n, 3 * n))
            plt.close(fig)
            fig = plt.figure(figsize=(3 * n, 3 * n))
            ax_array = scatter_matrix(df[cols_to_plot].dropna(), figsize=(3 * n, 3 * n), alpha=0.5, diagonal="hist")
            fig = ax_array[0][0].get_figure()
            fig.suptitle("Scatter Matrix", fontsize=14, y=1.02)
            path = output_dir / f"{prefix}_scatter_matrix.png"
            fig.savefig(path, dpi=100, bbox_inches="tight")
            plt.close(fig)
            created.append(str(path))
        except Exception:
            pass

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(max(6, len(numeric_cols)), max(5, len(numeric_cols) * 0.8)))
        im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticklabels(corr.columns, fontsize=8)
        for i in range(len(corr)):
            for j in range(len(corr)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
        fig.colorbar(im, ax=ax, shrink=0.8)
        ax.set_title("Correlation Heatmap")
        fig.tight_layout()
        path = output_dir / f"{prefix}_correlation.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        created.append(str(path))

    for col in cat_cols[:4]:
        vc = df[col].value_counts().head(15)
        if len(vc) < 2:
            continue
        fig, ax = plt.subplots(figsize=(8, max(4, len(vc) * 0.4)))
        vc.plot.barh(ax=ax, edgecolor="black", alpha=0.7)
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel("Count")
        fig.tight_layout()
        path = output_dir / f"{prefix}_bar_{col}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        created.append(str(path))

    return created


def main():
    parser = argparse.ArgumentParser(description="Analyze CSV/TSV/JSON data files")
    parser.add_argument("file", help="Path to data file (CSV, TSV, JSON, JSONL)")
    parser.add_argument("-o", "--output-dir", default=".", help="Directory for plot output (default: current dir)")
    parser.add_argument("--plots", action="store_true", help="Generate visualization plots")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output summary as JSON")
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    if not path.is_file():
        print(f"Error: {path} is not a file.", file=sys.stderr)
        sys.exit(1)

    df = load_data(path)
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.output_json:
        info = {
            "file": str(path),
            "shape": list(df.shape),
            "columns": list(df.columns),
            "dtypes": {col: str(dt) for col, dt in df.dtypes.items()},
            "missing": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include="number").columns) > 0 else {},
        }
        print(json.dumps(info, indent=2, default=str))
    else:
        print(f"# Analysis: `{path.name}`\n")
        print(summary_stats(df))

    if args.plots:
        prefix = path.stem.replace(" ", "_")
        created = generate_plots(df, output_dir, prefix=prefix)
        print(f"\n### Generated Plots\n")
        for p in created:
            print(f"- `{p}`")


if __name__ == "__main__":
    main()
