# MD Scraper Skill

## Trigger

Activate proactively when the user asks to:
- Extract, scrape, fetch, or convert a URL to markdown
- Pull content from a webpage
- Get the markdown version of a site or article
- Download or capture page content as text

Also invocable manually with `/md-scraper <url>`.

## Behavior

1. **Validate input**: Ensure the user provides 1-20 valid URLs.
2. **Run the extraction script**: Execute the helper script located at `extract_md.py` in the project root:
   ```bash
   python3 extract_md.py <url1> [url2 ...] [--depth basic|advanced] [--json]
   ```
3. **Present results**: Display the extracted markdown content to the user. If any URLs failed, report those failures clearly.

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--depth` | `basic`, `advanced` | `basic` | Controls extraction thoroughness. Use `advanced` for pages with complex layouts or heavy JS rendering. |
| `--json` | (flag) | off | Output raw JSON API response instead of formatted markdown. |

## Prerequisites

- `tavily-python` must be installed: `pip install tavily-python`
- `TAVILY_API_KEY` environment variable must be set (free key at https://www.tavily.com/)

## Constraints

- Maximum 20 URLs per invocation.
- If `TAVILY_API_KEY` is not set, inform the user and provide instructions to set it.
- If `tavily-python` is not installed, inform the user and provide the install command.
- Do not modify or rewrite extracted content — return it verbatim as the API provides it.
- Report failed URLs to the user with the error reason.

## Pre-authorized Commands

The following commands are pre-authorized and should run without per-call approval:

```
python3 extract_md.py *
pip install tavily-python
```

## Examples

**Single URL**:
```
/md-scraper https://example.com/article
```
Runs: `python3 extract_md.py https://example.com/article`

**Multiple URLs with advanced depth**:
```
/md-scraper https://example.com https://example.org --depth advanced
```
Runs: `python3 extract_md.py https://example.com https://example.org --depth advanced`

**JSON output**:
```
/md-scraper https://example.com --json
```
Runs: `python3 extract_md.py https://example.com --json`
