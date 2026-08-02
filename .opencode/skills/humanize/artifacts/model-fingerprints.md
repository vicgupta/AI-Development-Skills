# Model Fingerprints

Weak, noisy evidence. Use this only as background color alongside SKILL.md's real patterns and artifacts.

## Read this first

- **Artifacts (§43) are strong evidence. Style fingerprints are not.** Every model changes behavior between releases, with temperature, and with system prompts, so any single model's "voice" below can be wrong on the text in front of you.
- Never conclude "this was written by Model X" from style. Decide on **clusters** of the real patterns in SKILL.md.
- These heuristics reflect public observations through 2025-2026 and will drift.

## Quick reference

| Model | Common style tells | Common artifact tells |
|-------|-------------------|----------------------|
| ChatGPT | Em dashes, "certainly", "delve", "robust", "leverage", "foster", stock transitions ("Moreover", "Additionally"), sentences clustered 15-25 words, "It's worth noting", "When it comes to" | `turn0search0`, `[cite: N]`, `oaicite` / `oai_citation`, `attributableIndex`, `[span_N]` (web/search answers) |
| Claude | More hedged and balanced ("both perspectives have merit"), can open with "I'd", "Some argue... others...", gentle "Interestingly", occasional "One might", fewer em dashes than ChatGPT | None standard (no built-in citation UI artifacts) |
| Gemini | List-heavy, bold headers, mechanical transitions ("Overall", "Here's how"), bullet overload, occasional emoji, "delve" and "unlock" also appear | `[file name="..."]`, attachment markers in some products |
| Grok | "causal", "empirical", "correlate", "underscore", research-hedging tone, "Let's dive in" | `grok_card`, `grok_render_citation_card_json` |
| DeepSeek | Formal, somewhat Chinese-English influenced sentence rhythm, heavy on "this paper", "comprehensive" | Lenticular-bracket citations `【87†L55-67】`, `【citation:...】` |
| Perplexity | List-answer format, cite-heavy, "Here is what I found" | `【...†L...】` citation brackets, `turn0search0`-style markers |
| Generic AI editor / copilot | Diff-anchored text (§30), edit-summary phrasing (§47), markdown leaking into plain prose (§44) | `[attached_file:N]`, `ppl-ai-file-upload`, `:::writing`, ```` ```wikitext ```` |

## What this is good for

- **Raising suspicion, not proving anything.** If text carries DeepSeek-style brackets, check §46 citations rigorously.
- **Choosing which artifacts to grep for.** When a user says "this came from Perplexity," grep the Perplexity row before the others.
- **Prioritizing verification.** Artifact-heavy outputs deserve citation checks before any style discussion.

## What this is NOT good for

- Saying "this is ChatGPT because of the em dashes" (em dashes are also a §14 hard cut).
- Distinguishing models whose prose has been rewritten or heavily edited by a human.
- Anything requiring legal-grade certainty.

If you must bet, bet on artifacts and on the objective patterns (SKILL.md §34-47), not on whose "voice" it resembles.
