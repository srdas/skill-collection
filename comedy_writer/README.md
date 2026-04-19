# md-scraper

## Files

**`.claude/skills/md-scraper/SKILL.md`** - The Claude Code skill definition that:
- Proactively triggers when you mention extracting, scraping, fetching, or converting any URL to markdown
- Can also be invoked manually with `/md-scraper <url>`
- Pre-authorizes the necessary Bash commands so extraction runs without per-call approval

**`extract_md.py`** - The Python helper script that:
- Uses the Tavily Extract API (`tavily-python` SDK) to pull markdown from URLs
- Supports 1-20 URLs per invocation
- Has `--depth basic|advanced` for controlling extraction thoroughness
- Has `--json` for raw API output
- Handles errors gracefully (missing API key, missing package, failed URLs)

## Setup required

1. **Install the dependency**: `pip install tavily-python`
2. **Set your API key**: `export TAVILY_API_KEY="tvly-YOUR_KEY"` (free key at https://www.tavily.com/)

## Usage

- Ask naturally: *"extract the markdown from https://example.com"*
- Or invoke directly: `/md-scraper https://example.com`
- Batch extraction: `/md-scraper https://example.com https://example.org`

**`.claude/skills/comedy-writer/SKILL.md`** - A Claude Code skill that:
- Ingests markdown content from a local file or URL
- Writes a short standup comedy joke (2-4 sentences) grounded in real details from the content
- Never hallucates — every joke references specific facts, names, or quotes from the source
- Fetches URL content directly via WebFetch (no Tavily API or `extract_md.py` dependency needed)

### Comedy Writer usage

- From a file: `/comedy-writer TheDowofPooh.md`
- From a URL: `/comedy-writer https://example.com/article`
- Ask naturally: *"write a standup joke about this article"*, *"roast this markdown"*
