#!/usr/bin/env python3
"""Mechanical pre-pass for the humanize skill.

Reads text (stdin or --file), reports AI tells against the SKILL.md pattern
catalog, and optionally applies only the SAFE mechanical fixes.

Report mode (default, no --apply) prints pattern hits with line numbers so a
human or an LLM can make the judgment calls. Nothing is rewritten.

Apply mode (--apply) performs only context-independent fixes and prints the
edited text to stdout while the hit report goes to stderr. Everything else in
the catalog is reported, not rewritten, because it needs judgment.

Usage:
  humanize.py < text.txt                 # report only
  humanize.py --file text.txt            # report only
  humanize.py --file text.txt --apply    # apply safe fixes + report to stderr
  humanize.py --file text.txt --json     # machine-readable report

Requires Python 3.8+ and only the standard library.
"""

import argparse
import json
import re
import sys

EM_DASH = "\u2014"
EN_DASH = "\u2013"
CURLY = {
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
}

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE00-\U0000FE0F]"
)

ARTIFACT_TOKENS = [
    "turn0search0", "turn0search", "oaicite", "oai_citation",
    "attributableIndex", "grok_card", "grok_render_citation_card_json",
    "ppl-ai-file-upload", ":::writing", ":::system", ":::user",
    ":::assistant", "```wikitext",
]

ARTIFACT_RE = [
    re.compile(r"\[\s*cite\s*:\s*\d+\s*\]"),
    re.compile(r"\[#?\s*\d+\s*\]"),
    re.compile(r"\u3010[^\u3011]*\u3011"),
    re.compile(r"\[\s*span_\d+\s*\]"),
    re.compile(r"\[\s*attached_file\s*:\s*\d+\s*\]"),
    re.compile(r"\[\s*image\s*:[^\]]*\]"),
    re.compile(r"\[\s*file\s+name\s*=\s*[\"'][^\"']*[\"']\s*\]"),
    re.compile(r"\+\d+\s*$"),
]

MARKDOWN_BOLD_RE = re.compile(r"\*\*[^*]+\*\*|__[^_]+__")
MARKDOWN_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MARKDOWN_HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
MARKDOWN_RULE_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$", re.MULTILINE)
MARKDOWN_ITALIC_RE = re.compile(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)")

FILLER_REPLACEMENTS = [
    (re.compile(r"\bIn order to\b", re.IGNORECASE), "To"),
    (re.compile(r"\bDue to the fact that\b", re.IGNORECASE), "Because"),
    (re.compile(r"\bAt this point in time\b", re.IGNORECASE), "Now"),
    (re.compile(r"\bIn the event that\b", re.IGNORECASE), "If"),
    (re.compile(r"\bhas the ability to\b", re.IGNORECASE), "can"),
    (re.compile(r"\bIt is important to note that\b", re.IGNORECASE), ""),
]

WATCH_LISTS = {
    7: ["actually", "additionally", "align with", "crucial", "delve",
        "emphasizing", "enduring", "enhance", "fostering", "garner",
        "interplay", "intricate", "pivotal", "showcase", "tapestry",
        "testament", "underscore", "valuable", "vibrant"],
    37: ["utilize", "commence", "demonstrate", "obtain", "additional",
         "subsequently", "approximately", "authored", "transported",
         "numerous", "endeavor", "ascertain"],
    38: ["empowers", "unlocks", "transforms", "revolutionizes",
         "redefines", "thrives", "inspiring", "uplifting"],
    40: ["in today's rapidly evolving", "in an era where", "in the realm of",
         "in the world of", "when it comes to", "in the fast-paced world of",
         "it's no secret that"],
    41: ["it's important to note", "it's worth noting", "it should be noted",
         "interestingly", "needless to say", "as one might expect",
         "unsurprisingly"],
    27: ["the real question is", "at its core", "in reality",
         "what really matters", "fundamentally", "the deeper issue",
         "the heart of the matter"],
    28: ["let's dive in", "let's explore", "let's break this down",
         "here's what you need to know", "now let's look at",
         "without further ado"],
    33: ["honestly?", "here's the thing", "the thing is", "let's be honest",
         "real talk"],
    20: ["i hope this helps", "of course!", "certainly!", "you're absolutely right",
         "would you like", "want me to", "should i continue", "let me know"],
    22: ["great question!", "you're absolutely right", "that's an excellent point"],
    21: ["as of my", "up to my last training", "based on available information",
         "not publicly available", "maintains a low profile",
         "keeps personal details private", "it is believed that"],
    25: ["the future looks bright", "exciting times lie ahead",
         "journey toward excellence", "major step in the right direction"],
    47: ["addressing reviewer feedback", "while preserving", "while retaining",
         "made sure to include sourced content", "ensured compliance"],
}

SAFE_CHECKS = {
    14: ("em/en dashes", [EM_DASH, EN_DASH, " -- "]),
    18: ("emojis", [EMOJI_RE]),
    19: ("curly quotes", ["\u201c", "\u201d", "\u2018", "\u2019"]),
    23: ("filler phrases", list(FILLER_REPLACEMENTS)),
    43: ("model artifacts", list(ARTIFACT_RE) + ARTIFACT_TOKENS),
    44: ("markdown leaks", None),
}


def _token_hits(line, tokens):
    hits = []
    for token in tokens:
        if isinstance(token, re.Pattern):
            if token.search(line):
                hits.append(str(token.pattern))
        elif isinstance(token, str):
            if token in line:
                hits.append(token)
    return hits


def _phrase_hits(line):
    hits = []
    for pid, phrases in WATCH_LISTS.items():
        for phrase in phrases:
            if re.search(r"\b" + re.escape(phrase) + r"\b", line, re.IGNORECASE):
                hits.append((pid, phrase))
    return hits


def _safe_hits(line):
    hits = []
    for pid, (label, checks) in SAFE_CHECKS.items():
        if checks is None:
            matched = bool(
                MARKDOWN_BOLD_RE.search(line)
                or MARKDOWN_CODE_RE.search(line)
                or MARKDOWN_LINK_RE.search(line)
                or MARKDOWN_HEADING_RE.search(line)
                or MARKDOWN_RULE_RE.search(line)
            )
        else:
            matched = bool(_token_hits(line, checks))
        if matched:
            hits.append((pid, label))
    return hits


def scan(text):
    lines = text.splitlines()
    found = {"phrase": {}, "safe": {}}
    for lineno, line in enumerate(lines, start=1):
        for pid, phrase in _phrase_hits(line):
            found["phrase"].setdefault(pid, []).append((lineno, phrase))
        for pid, label in _safe_hits(line):
            found["safe"].setdefault(pid, []).append((lineno, label))
    return found, len(lines)


def apply_safe_fixes(text):
    for ch, repl in CURLY.items():
        text = text.replace(ch, repl)
    text = re.sub(r"\s+--\s*|\s+--$", ", ", text)
    text = re.sub(r"\s+%s\s+" % re.escape(EM_DASH), ", ", text)
    text = text.replace(EM_DASH, ", ")
    text = re.sub(r"(?<!\d)\s+%s\s+(?!\d)" % re.escape(EN_DASH), ", ", text)
    text = text.replace(EN_DASH, "-")
    text = EMOJI_RE.sub("", text)
    for token in ARTIFACT_TOKENS:
        text = text.replace(token, "")
    for rx in ARTIFACT_RE:
        text = rx.sub("", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = MARKDOWN_BOLD_RE.sub(lambda m: m.group(0)[2:-2], text)
    text = MARKDOWN_ITALIC_RE.sub(r"\1", text)
    text = MARKDOWN_CODE_RE.sub(lambda m: m.group(0)[1:-1], text)
    text = MARKDOWN_HEADING_RE.sub("", text)
    for rx, repl in FILLER_REPLACEMENTS:
        text = rx.sub(repl, text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\s+,", ",", text)
    return text.strip()


def render_hits(found):
    parts = []
    for kind in ("safe", "phrase"):
        for pid in sorted(found[kind]):
            entries = found[kind][pid]
            lines = sorted({ln for ln, _ in entries})
            samples = " / ".join(s for _, s in entries[:3])
            parts.append(f"  \u00a7{pid}: {len(entries)} hit(s) (lines {lines})  <{samples}>")
    return "\n".join(parts) if parts else "  none"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Report or apply safe mechanical humanize fixes."
    )
    parser.add_argument("--file", help="input file; defaults to stdin")
    parser.add_argument("--apply", action="store_true",
                        help="apply safe mechanical fixes and print the result")
    parser.add_argument("--json", action="store_true",
                        help="emit the hit report as JSON")
    args = parser.parse_args(argv)

    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    found, _ = scan(text)

    if args.json:
        report = {
            "skill": "humanize",
            "mode": "report",
            "hits": {f"{kind}:{pid}": entries for kind in found for pid, entries in found[kind].items()},
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if args.apply:
        print(apply_safe_fixes(text))
        print("\n[report]\n" + render_hits(found), file=sys.stderr)
        return 0

    print(render_hits(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
