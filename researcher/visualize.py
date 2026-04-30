#!/usr/bin/env python3
"""Generate common research visualizations from data files."""

import argparse
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
    print("Error: matplotlib is not installed. Run: pip install matplotlib", file=sys.stderr)
    sys.exit(1)


def load_data(path: Path) -> pd.DataFrame:
    ext = path.suffix.lower()
    if ext == ".tsv":
        return pd.read_csv(path, sep="\t")
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".jsonl":
        return pd.read_json(path, lines=True)
    return pd.read_csv(path)


def plot_timeseries(df: pd.DataFrame, date_col: str, value_cols: list[str],
                    output: Path, title: str = "Time Series"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(date_col)

    fig, ax = plt.subplots(figsize=(12, 6))
    for col in value_cols:
        ax.plot(df[date_col], df[col], label=col, alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel(date_col)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                 output: Path, hue_col: str = None, title: str = "Scatter Plot"):
    fig, ax = plt.subplots(figsize=(10, 7))
    if hue_col and hue_col in df.columns:
        groups = df.groupby(hue_col)
        for name, group in groups:
            ax.scatter(group[x_col], group[y_col], label=name, alpha=0.6, s=30)
        ax.legend(title=hue_col, fontsize=8)
    else:
        ax.scatter(df[x_col], df[y_col], alpha=0.6, s=30)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")


def plot_bar(df: pd.DataFrame, cat_col: str, val_col: str,
             output: Path, agg: str = "mean", title: str = "Bar Chart"):
    agg_df = df.groupby(cat_col)[val_col].agg(agg).sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(10, max(4, len(agg_df) * 0.4)))
    agg_df.plot.barh(ax=ax, edgecolor="black", alpha=0.7)
    ax.set_title(f"{title} ({agg} of {val_col} by {cat_col})")
    ax.set_xlabel(f"{agg}({val_col})")
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")


def plot_box(df: pd.DataFrame, cat_col: str, val_col: str,
             output: Path, title: str = "Box Plot"):
    top_cats = df[cat_col].value_counts().head(15).index.tolist()
    subset = df[df[cat_col].isin(top_cats)]
    fig, ax = plt.subplots(figsize=(10, 6))
    subset.boxplot(column=val_col, by=cat_col, ax=ax, grid=False)
    ax.set_title(title)
    fig.suptitle("")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate research visualizations")
    parser.add_argument("file", help="Data file path")
    parser.add_argument("--type", choices=["timeseries", "scatter", "bar", "box", "hist"],
                        required=True, help="Plot type")
    parser.add_argument("--x", help="X-axis / date / category column")
    parser.add_argument("--y", nargs="+", help="Y-axis / value column(s)")
    parser.add_argument("--hue", help="Color-by column (scatter only)")
    parser.add_argument("--agg", default="mean", help="Aggregation for bar charts (default: mean)")
    parser.add_argument("--title", default="", help="Plot title")
    parser.add_argument("-o", "--output", default="plot.png", help="Output file path")
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    df = load_data(path)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    title = args.title or args.type.replace("_", " ").title()

    if args.type == "timeseries":
        if not args.x or not args.y:
            print("Error: --x (date column) and --y (value columns) required for timeseries", file=sys.stderr)
            sys.exit(1)
        plot_timeseries(df, args.x, args.y, output, title)

    elif args.type == "scatter":
        if not args.x or not args.y:
            print("Error: --x and --y required for scatter", file=sys.stderr)
            sys.exit(1)
        plot_scatter(df, args.x, args.y[0], output, hue_col=args.hue, title=title)

    elif args.type == "bar":
        if not args.x or not args.y:
            print("Error: --x (category) and --y (value) required for bar", file=sys.stderr)
            sys.exit(1)
        plot_bar(df, args.x, args.y[0], output, agg=args.agg, title=title)

    elif args.type == "box":
        if not args.x or not args.y:
            print("Error: --x (category) and --y (value) required for box", file=sys.stderr)
            sys.exit(1)
        plot_box(df, args.x, args.y[0], output, title)

    elif args.type == "hist":
        if not args.y:
            print("Error: --y (column) required for hist", file=sys.stderr)
            sys.exit(1)
        fig, ax = plt.subplots(figsize=(10, 6))
        for col in args.y:
            df[col].dropna().hist(bins=40, ax=ax, alpha=0.6, label=col, edgecolor="black")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(output, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved: {output}")


if __name__ == "__main__":
    main()
