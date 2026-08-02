---
name: deepwrite
description: Generate opinionated white papers from deep research. Use when the user says "/deepwrite", "write a white paper", "research and write about [topic]", or "deep research on [topic]". Produces 5-10 page executive-style papers with autonomous web research, source trust scoring, and a persistent knowledge base.
---

# deepwrite — Deep Research to White Papers

You are executing the deepwrite pipeline. Follow each step precisely and do not skip stages.

## Argument Parsing

Parse the user's input to extract:

| Argument | Required | Default | How to extract |
|----------|----------|---------|----------------|
| `topic` | Yes | — | The main quoted string or first argument after `/deepwrite` |
| `--sources` | No | None | File paths or URLs listed after `--sources` flag |
| `--output-dir` | No | `./deepwrite-output/` | Path after `--output-dir` flag |
| `--tone` | No | `visionary` | One of: `visionary`, `analytical`, `technical` |

If no topic is provided, ask the user for one before proceeding.

## Step 1: Setup

1. Set the output directory. Default: `./deepwrite-output/`
2. Create a slug from the topic (lowercase, hyphens, max 50 chars). Example: "LLM Fine-Tuning vs RAG" → `llm-fine-tuning-vs-rag`
3. Create the paper folder: `{output-dir}/{slug}/`
4. Create the folder structure:
   ```
   {slug}/
     paper.md
     outline.md
     sources.json
     research-notes.md
   ```
5. Announce to the user: "Starting deepwrite pipeline for: {topic}"
6. Show estimated time: "This will take 5-10 minutes for thorough research."

## Step 2: Consult Knowledge Base

Run the KB search script to find relevant prior research:

```bash
python3 .opencode/skills/deepwrite/scripts/kb.py search "{topic}"
```

> The KB script is bundled with this skill at `scripts/kb.py` (same directory as this SKILL.md). If the path above doesn't resolve, locate it relative to this file and run it directly.

- If results are returned, read the matching entries and hold them in context
- These will be used to enrich the outline and section content
- Do NOT show KB results to the user (internal enrichment only)
- If the KB is empty or returns no matches, proceed without prior context

## Step 3: Ingest User-Provided Sources

If `--sources` was provided:

1. For each file path: read the file content using the Read tool
2. For each URL: fetch the content using WebFetch
3. Tag all user-provided sources as **Tier 0 (primary/authoritative)** — they override web findings on conflicting points
4. Extract key claims, data points, and arguments from each source
5. Write a summary of each user source to `research-notes.md`

## Step 4: Autonomous Web Research

Execute a comprehensive research sweep. This is the most critical stage — be thorough.

### Search Strategy

Run **at minimum 15 searches**, varying the query angles:

1. **Core topic searches** (3-4 searches):
   - `{topic} 2026`
   - `{topic} latest research`
   - `{topic} analysis`
   - `{topic} trends`

2. **Technical depth searches** (3-4 searches):
   - `{topic} technical deep dive`
   - `{topic} architecture comparison`
   - `{topic} benchmarks performance`
   - `{topic} implementation guide`

3. **Expert opinion searches** (2-3 searches):
   - `{topic} expert analysis`
   - `{topic} industry perspective`
   - `{topic} thought leadership`

4. **Counterargument searches** (2-3 searches):
   - `{topic} challenges limitations`
   - `{topic} criticism drawbacks`
   - `{topic} alternatives`

5. **Data and evidence searches** (2-3 searches):
   - `{topic} statistics data`
   - `{topic} case study`
   - `{topic} market research report`

6. **Emerging/forward-looking searches** (2-3 searches):
   - `{topic} future predictions`
   - `{topic} roadmap upcoming`
   - `{topic} next generation`

### For Each Search Result

Use WebSearch for discovery, then WebFetch to read the most promising results.

- Aim to deeply read at least **15-20 sources**
- For each source, extract: title, URL, publish date, key claims, data points, quotes
- For paywalled content: extract title, abstract, preview text. Note "(abstract only)" or "(preview only)"
- Skip sources that are primarily promotional or have no substantive content

### Progress Reporting

After every 5 searches, report progress to the user:
```
Research progress: {n} searches completed, {m} quality sources found so far...
```

## Step 5: Source Trust Scoring

Score every source (both user-provided and web-discovered):

| Tier | Score | Source Type | Examples |
|------|-------|-------------|----------|
| 0 | 100 | User-provided (primary) | Files/URLs the user explicitly passed |
| 1 | 90 | Official docs, specs, RFCs | python.org, RFC documents, official APIs |
| 2 | 80 | Peer-reviewed, research labs | arXiv papers, Google Research, OpenAI blog |
| 3 | 70 | Reputable tech blogs | Engineering blogs (Netflix, Stripe, Uber), established publications |
| 4 | 50 | General articles, tutorials | Medium posts, dev.to, Stack Overflow, tutorials |
| 5 | 30 | Forums, social media, unknown | Reddit, HN comments, unknown blogs |

For contradictory claims between sources: **most recent source wins**. If dates are the same, higher-tier source wins.

Write the scored source list to `sources.json`:

```json
[
  {
    "title": "Source Title",
    "url": "https://...",
    "date": "2026-01-15",
    "trust_tier": 2,
    "trust_score": 80,
    "access": "full",
    "key_claims": ["claim 1", "claim 2"],
    "data_points": ["stat 1", "stat 2"]
  }
]
```

### Thin Research Check

If fewer than 8 credible sources (tier 0-3) were found:

1. Warn the user: "Only {n} high-quality sources found for this topic. The paper will proceed but may have limited depth in some areas."
2. Add a metadata note to the paper folder
3. Continue with generation

## Step 6: Compile Research Notes

Write `research-notes.md` with all findings organized by theme/subtopic:

```markdown
# Research Notes: {topic}

## Key Findings

### Theme 1: [auto-detected theme]
- Finding from Source A (Tier 2, 2026-01-15)
- Finding from Source B (Tier 3, 2025-12-20)
...

### Theme 2: [auto-detected theme]
...

## Data Points & Statistics
- [stat] — Source: [title] ([tier], [date])
...

## Notable Quotes
- "[quote]" — [author], [source]
...

## Contradictions Found
- [Topic]: Source A says X (2025-11) vs Source B says Y (2026-01) → Using Source B (more recent)
...
```

## Step 7: Generate Outline

Based on research notes, KB context, and the topic, generate a structured outline.

### Outline Structure

The outline should follow this pattern (adapt sections to the topic):

```markdown
# {Paper Title}

> {One-line thesis — opinionated, forward-looking}

## Executive Summary
<!-- 2-3 paragraphs: thesis, key findings, recommendations -->

## {Section 1: Context/Background}
<!-- Set the stage — what's the current state? -->

## {Section 2: Core Analysis}
<!-- The meat — data, comparisons, technical depth -->

## {Section 3: Implications / So What?}
<!-- What this means for practitioners/the industry -->

## {Section 4: Forward Look}
<!-- Where this is heading — the visionary stance -->

## {Section 5: Recommendations}
<!-- Actionable takeaways -->

## Sources
<!-- Auto-generated from sources.json -->
```

Write the outline to `{paper-folder}/outline.md`.

Then tell the user:

```
Outline written to: {path}/outline.md

Please review and edit the outline in your editor:
- Reorder sections by moving them around
- Rename section headings
- Add new sections with a ## heading and <!-- description -->
- Delete sections you don't want

When you're done editing, confirm here to continue.
```

Use AskUserQuestion to wait for the user's confirmation:
- Question: "Have you finished editing the outline? I'll read it back and expand each section."
- Options: "Yes, continue" / "Skip outline editing, use as-is"

## Step 8: Read Approved Outline

Read back the `outline.md` file. The user may have:
- Reordered sections
- Renamed headings
- Added new sections
- Removed sections
- Left it unchanged

Use the current state of the file as the definitive structure.

## Step 9: Expand Sections

For each section in the approved outline, generate full prose.

### Writing Guidelines

**Tone: Opinionated and visionary** (unless overridden by `--tone`)

- **visionary** (default): Take clear stances. "The future belongs to..." not "It remains to be seen whether..." Write like an a16z or Sequoia partner memo — confident, forward-looking, backed by evidence.
- **analytical**: Data-driven, neutral, McKinsey/Gartner style. "The data suggests..." with balanced perspectives.
- **technical**: Deep technical content, accessible to senior engineers. Stripe/Cloudflare engineering blog style.

### Per-Section Rules

1. **Executive Summary**: Write LAST (after all other sections), synthesizing the full paper. 2-3 dense paragraphs.
2. **All other sections**:
   - Ground every claim in a specific source from research-notes.md
   - Include concrete data points, numbers, and examples
   - When taking a stance, acknowledge the counterargument briefly then explain why your position is stronger
   - Use subheadings (###) to break up long sections
   - Target 1-2 pages per section (roughly 400-800 words)

### Progress

After expanding each section, report: "Expanded: {section name} ({n}/{total})"

## Step 10: Assemble Final Paper

Combine all expanded sections into `paper.md`:

1. Paper title as H1
2. Thesis as a blockquote
3. All sections in outline order
4. Source appendix at the end

### Source Appendix Format

```markdown
## Sources

1. **{Title}** — {Publication/Author}, {Date}
   {URL}
   {Brief description of what was used from this source}

2. ...
```

- Number all sources sequentially
- Note paywalled sources: "(abstract only)"
- Include all sources that contributed to the paper (typically 15-25)

## Step 11: Update Knowledge Base

After the paper is complete, index the research into the KB:

```bash
python3 .opencode/skills/deepwrite/scripts/kb.py add \
  --topic "{topic}" \
  --paper-folder "{slug}" \
  --sources-file "{paper-folder}/sources.json" \
  --notes-file "{paper-folder}/research-notes.md"
```

This extracts key findings, keywords, and source metadata into the KB for future papers.

## Step 12: Final Report

Present the results to the user:

```
deepwrite complete!

Paper:          {path}/paper.md
Outline:        {path}/outline.md
Sources:        {path}/sources.json ({n} sources)
Research Notes: {path}/research-notes.md

Knowledge base updated with {m} new findings.

To convert to other formats:
  pandoc {path}/paper.md -o paper.pdf
  pandoc {path}/paper.md -o paper.docx
```

---

## Error Recovery

- If web search fails mid-research: report the error, continue with sources gathered so far
- If a WebFetch fails for a specific URL: skip it, note in research-notes.md
- If KB script fails: warn the user, continue without KB (non-blocking)
- If fewer than 5 sources found: ask the user if they want to proceed or provide additional sources

## Important Notes

- NEVER fabricate sources, statistics, or quotes. Every claim must trace to a real source.
- NEVER hallucinate URLs. Only use URLs that appeared in actual search results or were provided by the user.
- If you cannot find enough evidence for a section, say so honestly in the paper rather than filling with vague claims.
- The paper should read as authoritative analysis, not as an AI-generated summary. Vary sentence structure, use specific details, and take clear positions.
