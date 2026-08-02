# Humanize Quick Check

A one-page rapid-scan checklist for eyeballing text before the full SKILL.md pass. Work top to bottom; each step is cheap. Stop to fix when you hit a hit. Remember the rule from Detection Guidance: decide on **clusters**, not single words.

## Pass 1: Artifacts (strongest, ~10 seconds)

- [ ] Search for model artifact strings: `turn0search0`, `[cite: `, `【`, `oaicite`, `oai_citation`, `attributableIndex`, `[span_`, `grok_card`, `:::writing`, `:::system`, `[attached_file`, `ppl-ai-file-upload`, ```` ```wikitext ````.
- [ ] Search for markdown in plain prose: `**bold**`, backticks, `[text](url)`, `# headings`, `---` rules.
- [ ] Search for citation red flags: `utm_source=chatgpt.com`, `utm_source=perplexity`, `referrer=grok.com`, `↩`, `[citation needed]`.
- [ ] Count heading levels: any `##` followed directly by `####`? Any thematic break right before a heading?

## Pass 2: Punctuation and formatting (~20 seconds)

- [ ] `—` or `–` anywhere? Cut them (hard constraint, SKILL.md §14).
- [ ] Emoji anywhere? Remove.
- [ ] Curly quotes `“ ” ‘ ’`? Straighten (weak alone, counts in clusters).
- [ ] Bold used more than twice to emphasize? Reduce.
- [ ] `**Header:**`-style list items? Convert to prose.

## Pass 3: Word-level tells (~30 seconds)

- [ ] Scan for AI vocabulary: delve, tapestry, testament, pivotal, vibrant, landscape, showcasing, underscores, intricate, interplay, garner, foster, crucial.
- [ ] Scan for register bias: utilize, commence, demonstrate, numerous, subsequently, endeavor, in order to.
- [ ] Scan for positivity framing: empowers, unlocks, transforms, revolutionizes, thrives, inspiring, uplifting.
- [ ] Scan for filler/hedges: in order to, due to the fact that, it is important to note, could potentially possibly.
- [ ] Scan for meta-commentary: the real question is, at its core, let's dive in, here's what you need to know, it's worth noting, interestingly.
- [ ] Count hyphens: high-quality, data-driven, cross-functional in predicate position? Drop the hyphen there.

## Pass 4: Rhythm and structure (~30 seconds)

- [ ] Read one paragraph aloud. Are the sentences all 15-25 words with an even beat? Vary them.
- [ ] Do three paragraphs in a row have nearly identical lengths? Break it up.
- [ ] Is the conclusion just the introduction restated? Cut or make it specific.
- [ ] Is every sentence "correct" with zero contractions, zero dropped "that", zero colloquial words? Let some humanity in.
- [ ] Do the paragraphs say the same thing twice with different words (treadmill)? Cut the restatement.
- [ ] Does the writer take a side anywhere, or refuse to conclude everywhere? A human makes judgment calls.

## Pass 5: The 30-second test

- [ ] Ask: "Could a person who cares about the topic have written this?" If the only answer is "an AI that read Wikipedia on the topic," it needs another pass.

## Scoring

| Hits | Action |
|------|--------|
| 0-2, isolated | Probably fine; do not gut it (see SKILL.md What NOT to flag). |
| 3-5, clustered | Run the full SKILL.md rewrite pass. |
| 6+ or any artifact hit (Pass 1) | Full rewrite, and verify every citation independently. |
