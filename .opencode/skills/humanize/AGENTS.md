# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Warp, etc.) working in this repository.

## What this repo is

A **Claude Code / OpenCode skill** implemented entirely as Markdown. The runtime artifact is `SKILL.md`: the agent reads its YAML frontmatter (metadata + allowed tools) followed by the editor prompt. There is no build step and no code to run.

## Key files

- `SKILL.md` — the skill itself. YAML frontmatter (`name`, `description`, `allowed-tools`) followed by the canonical, numbered pattern list with before/after examples. **This is the source of truth.**
- `README.md` — for humans: installation, usage, and a summary table of the patterns.
- `artifacts/patterns.json` — machine-readable catalog of the patterns (id, category, watch lists, fixes). Keep in sync with `SKILL.md` when patterns change.
- `artifacts/quickcheck.md` — rapid-scan checklist (a distillation of `SKILL.md`, not new rules).
- `artifacts/model-fingerprints.md` — per-model tell tables. Marked weak signal; keep the caveat header if you touch it.
- `scripts/humanize.py` — zero-dependency Python mechanical pre-pass. Only applies context-independent fixes (`--apply`); everything else is reported. Keep it stdlib-only and Python 3.8+.

## The maintenance contract

`SKILL.md` and `README.md` must stay in sync. When you change behavior or content:

- **Patterns:** the skill currently defines **47 numbered patterns**. If you add, remove, or renumber any, update the README pattern table, its "N Patterns Detected" heading, and every cross-reference in the same change. Keep numbering stable unless you are deliberately renumbering. If the change alters the word lists or fixes, update `artifacts/patterns.json` in the same commit.
- **Non-obvious fixes:** if you change the prompt to handle a tricky failure mode (a repeated mis-edit, an unexpected tone shift), document the behavior change in the relevant README section.

## Editing SKILL.md

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product. Edit it like a careful instruction document, not code.
