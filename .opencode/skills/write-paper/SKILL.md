---
name: write-paper
description: Generate technical research papers using autonomous web research, source scoring, and persistent knowledge base
---

# Write Paper

Generate technical research papers using deep research methodology.

## What I do

1. Initialize a research workspace with topic, audience, and style parameters
2. Execute 7 research commands in parallel (web search, deep research, YouTube, podcast, notebooklm)
3. Score and deduplicate sources by credibility
4. Generate structured paper from approved outline
5. Save all artifacts to `deepwrite-output/<topic-slug>/`

## When to use me

Use when you need to write a technical paper or research article. Requires API keys for full functionality (GEMINI_API_KEY, PERPLEXITY_API_KEY, YOUTUBE_API_KEY).

## Commands

- `deepwrite init` - Initialize workspace
- `deepwrite search` - Web search via Perplexity
- `deepwrite research` - Deep research via Gemini
- `deepwrite youtube` - YouTube transcript search
- `deepwrite podcast` - Podcast research
- `deepwrite notebooklm` - NotebookLM research
- `deepwrite sources` - Score and deduplicate sources
- `deepwrite write` - Generate paper from outline
- `deepwrite status` - Check workspace status

## Output

Papers are saved to `deepwrite-output/<topic-slug>/`:
- `paper.md` - The generated paper
- `sources.json` - Scored sources
- `research-notes.md` - Research notes
- `outline.md` - Approved outline
