---
name: blogger
description: Write a high-quality tech blog post. Use this skill whenever the user asks to "write a blog post", "draft a tech article", "create a tutorial post", or any request to produce a blog-style piece for a developer or technical audience.
version: 1.0.0
---

# Tech Blog Writing Guide

This skill produces clear, well-structured tech blog posts that balance technical accuracy with readability. Apply it when drafting tutorials, architecture deep-dives, framework reviews, or any post aimed at developers.

---

## 1. Hook: Lead With the Problem

Tech readers arrive with a specific question. Answer it immediately.

- **State the problem first.** What pain point does this post address?
- **Promise the solution.** Make clear upfront that this post delivers the answer.
- **Identify the audience.** One sentence on prerequisites ("This guide assumes basic familiarity with Docker") sets expectations and filters readers who will actually benefit.

Do not open with a long anecdote, a history lesson, or a generic statement about how important the topic is.

---

## 2. Structure for Scanning

Developers skim before they read. The structure must reward skimming.

- **Meaningful subheadings.** A reader scrolling through headers alone should understand the full narrative arc.
- **Bullet points and numbered lists** for steps, pros/cons, and feature comparisons — not for every paragraph.
- **Bold text** to surface key terms, commands, and critical warnings.
- **Short paragraphs.** Three to five sentences max. Break early.

---

## 3. Code Snippets: Minimal and Runnable

Code blocks are often the reason someone found the post. Treat them with care.

- **Cut ruthlessly.** Show only the lines that matter; use `...` to indicate omitted boilerplate.
- **Specify the language** for syntax highlighting (` ```python `, ` ```bash `, etc.).
- **Test every snippet** in a clean environment before publishing. Broken code destroys credibility instantly.
- **Link to a working repo** whenever the complete context is too large to embed.

---

## 4. Explain the "Why," Not Just the "How"

Generic how-to content is everywhere. Perspective is scarce.

- For every command or design choice, say why this approach over the alternatives.
- Share gotchas, edge cases, and real mistakes — these are the lines readers bookmark and share.
- If there is a common wrong way to do this, name it and explain what breaks.

---

## 5. Visual Aids for Complex Flows

One good diagram can replace five paragraphs of dense prose.

- **Architecture diagrams** for system overviews (Mermaid.js, Excalidraw, or similar).
- **Request/response flow diagrams** for API or network concepts.
- **Before/after performance charts** when benchmarking is the point.

Add a diagram when the text requires the reader to hold more than two moving parts in their head at once.

---

## Pre-Publish Checklist

| Check | What to Verify |
|---|---|
| **Copy-paste test** | Every code snippet runs in a clean environment without modification. |
| **Mobile test** | Code blocks scroll cleanly on a small screen; no horizontal overflow breaks layout. |
| **Jargon check** | Every acronym is defined on first use, or linked to authoritative documentation. |
| **Call to action** | The conclusion invites discussion, links to related posts, or tells the reader what to do next. |

---

## Practical Instructions

When asked to write a tech blog post:

1. Identify the single core problem this post solves and open with it.
2. Draft a one-sentence audience qualifier (experience level, assumed tools/knowledge).
3. Outline the post as headers first — confirm the narrative flows logically before writing prose.
4. Write each section with the scan-first reader in mind: heading → key point → detail.
5. For any code block, verify it is minimal, language-tagged, and correct.
6. For each technical choice made, include a sentence on why — not just what.
7. Close with a concrete next step: a repo link, a follow-up post, a question for the comments.
8. Run through the pre-publish checklist before finalizing.
