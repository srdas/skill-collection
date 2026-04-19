#!/usr/bin/env python3
"""Extract markdown content from URLs using the Tavily Extract API."""

import argparse
import json
import os
import sys

try:
    from tavily import TavilyClient
except ImportError:
    print("Error: tavily-python is not installed. Run: pip install tavily-python", file=sys.stderr)
    sys.exit(1)


def extract_markdown(urls: list[str], extract_depth: str = "basic") -> dict:
    """Extract markdown content from one or more URLs.

    Args:
        urls: List of URLs to extract content from (max 20).
        extract_depth: "basic" or "advanced" extraction depth.

    Returns:
        Dict with "results" and "failed_results" keys.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        api_key = input("TAVILY_API_KEY is not set. Enter your Tavily API key: ").strip()
        if not api_key:
            print("Error: No API key provided.", file=sys.stderr)
            sys.exit(1)

    client = TavilyClient(api_key=api_key)
    return client.extract(
        urls=urls,
        format="markdown",
        extract_depth=extract_depth,
    )


def main():
    parser = argparse.ArgumentParser(description="Extract markdown from URLs via Tavily Extract API")
    parser.add_argument("urls", nargs="+", help="One or more URLs to extract markdown from")
    parser.add_argument(
        "--depth",
        choices=["basic", "advanced"],
        default="basic",
        help="Extraction depth: basic (faster/cheaper) or advanced (more thorough). Default: basic",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output raw JSON response instead of formatted markdown",
    )
    args = parser.parse_args()

    if len(args.urls) > 20:
        print("Error: Maximum 20 URLs per request.", file=sys.stderr)
        sys.exit(1)

    response = extract_markdown(args.urls, extract_depth=args.depth)

    if args.output_json:
        print(json.dumps(response, indent=2))
        return

    for result in response.get("results", []):
        url = result.get("url", "unknown")
        content = result.get("raw_content", "")
        print(f"--- Source: {url} ---\n")
        print(content)
        print()

    for failed in response.get("failed_results", []):
        url = failed.get("url", "unknown")
        error = failed.get("error", "unknown error")
        print(f"FAILED: {url} - {error}", file=sys.stderr)

    if not response.get("results"):
        print("No content was successfully extracted.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
