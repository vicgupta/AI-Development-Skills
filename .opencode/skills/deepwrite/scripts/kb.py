#!/usr/bin/env python3
"""
deepwrite Knowledge Base Manager

Usage:
    kb.py init                              Initialize KB directory structure
    kb.py search "<query>"                  Search KB for relevant entries
    kb.py add --topic "..." --paper-folder "..." --sources-file "..." --notes-file "..."
    kb.py list                              List all KB entries
    kb.py stats                             Show KB statistics
"""

import json
import os
import sys
import uuid
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

KB_DIR = Path.home() / ".deepwrite" / "kb"
ENTRIES_DIR = KB_DIR / "entries"
INDEX_FILE = KB_DIR / "index.json"


def ensure_dirs():
    KB_DIR.mkdir(parents=True, exist_ok=True)
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(json.dumps({"entries": []}, indent=2))


def load_index():
    ensure_dirs()
    return json.loads(INDEX_FILE.read_text())


def save_index(index):
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def extract_keywords(text):
    """Extract meaningful keywords from text using simple TF heuristics."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "need", "dare",
        "this", "that", "these", "those", "it", "its", "they", "them", "their",
        "we", "us", "our", "you", "your", "he", "him", "his", "she", "her",
        "not", "no", "nor", "as", "if", "then", "than", "when", "where",
        "what", "which", "who", "whom", "how", "all", "each", "every", "both",
        "few", "more", "most", "other", "some", "such", "only", "own", "same",
        "so", "very", "just", "about", "above", "after", "again", "also",
        "any", "because", "before", "between", "during", "into", "through",
        "up", "out", "over", "under", "here", "there", "once", "while",
    }
    words = re.findall(r'[a-z][a-z0-9\-]+', text.lower())
    words = [w for w in words if w not in stop_words and len(w) > 2]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(30)]


def keyword_overlap_score(query_keywords, entry_keywords):
    """Score similarity between two keyword lists."""
    if not query_keywords or not entry_keywords:
        return 0.0
    q_set = set(query_keywords)
    e_set = set(entry_keywords)
    intersection = q_set & e_set
    union = q_set | e_set
    jaccard = len(intersection) / len(union) if union else 0
    # Boost by how many query terms were matched
    query_coverage = len(intersection) / len(q_set) if q_set else 0
    return (jaccard * 0.4) + (query_coverage * 0.6)


def recency_weight(created_at_str):
    """Weight more recent entries higher. Returns multiplier 0.5-1.0."""
    try:
        created = datetime.fromisoformat(created_at_str)
        days_old = (datetime.now() - created).days
        if days_old <= 7:
            return 1.0
        elif days_old <= 30:
            return 0.9
        elif days_old <= 90:
            return 0.8
        elif days_old <= 180:
            return 0.7
        elif days_old <= 365:
            return 0.6
        else:
            return 0.5
    except (ValueError, TypeError):
        return 0.5


# --- Commands ---

def cmd_init():
    ensure_dirs()
    config_file = KB_DIR.parent / "config.json"
    if not config_file.exists():
        config = {
            "default_tone": "visionary",
            "default_output_dir": "./deepwrite-output/",
            "created_at": datetime.now().isoformat()
        }
        config_file.write_text(json.dumps(config, indent=2))
    print("Knowledge base initialized.")
    print(f"  KB directory: {KB_DIR}")
    print(f"  Entries:      {ENTRIES_DIR}")
    print(f"  Index:        {INDEX_FILE}")


def cmd_search(query):
    index = load_index()
    if not index["entries"]:
        print("[]")
        return

    query_keywords = extract_keywords(query)
    scored = []

    for entry_meta in index["entries"]:
        kw_score = keyword_overlap_score(query_keywords, entry_meta.get("keywords", []))
        r_weight = recency_weight(entry_meta.get("created_at", ""))
        final_score = kw_score * r_weight

        if final_score > 0.05:
            scored.append({
                "id": entry_meta["id"],
                "topic": entry_meta["topic"],
                "score": round(final_score, 4),
                "created_at": entry_meta.get("created_at", ""),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:5]

    if not top:
        print("[]")
        return

    # Load full entries for top matches
    results = []
    for match in top:
        entry_file = ENTRIES_DIR / f"{match['id']}.json"
        if entry_file.exists():
            entry = json.loads(entry_file.read_text())
            entry["_match_score"] = match["score"]
            results.append(entry)

    print(json.dumps(results, indent=2))


def cmd_add(args):
    topic = None
    paper_folder = None
    sources_file = None
    notes_file = None

    i = 0
    while i < len(args):
        if args[i] == "--topic" and i + 1 < len(args):
            topic = args[i + 1]
            i += 2
        elif args[i] == "--paper-folder" and i + 1 < len(args):
            paper_folder = args[i + 1]
            i += 2
        elif args[i] == "--sources-file" and i + 1 < len(args):
            sources_file = args[i + 1]
            i += 2
        elif args[i] == "--notes-file" and i + 1 < len(args):
            notes_file = args[i + 1]
            i += 2
        else:
            i += 1

    if not topic:
        print("Error: --topic is required", file=sys.stderr)
        sys.exit(1)

    # Build KB entry
    entry_id = str(uuid.uuid4())[:8]
    keywords = extract_keywords(topic)

    # Extract additional keywords and findings from sources and notes
    findings = []
    source_count = 0

    if sources_file and os.path.exists(sources_file):
        try:
            sources = json.loads(Path(sources_file).read_text())
            source_count = len(sources)
            for src in sources:
                for claim in src.get("key_claims", []):
                    findings.append({
                        "claim": claim,
                        "source_url": src.get("url", ""),
                        "source_title": src.get("title", ""),
                        "trust_tier": src.get("trust_tier", 4),
                        "date": src.get("date", ""),
                    })
                # Add keywords from source titles
                if src.get("title"):
                    keywords.extend(extract_keywords(src["title"]))
        except (json.JSONDecodeError, KeyError):
            pass

    if notes_file and os.path.exists(notes_file):
        try:
            notes_content = Path(notes_file).read_text()
            keywords.extend(extract_keywords(notes_content))
        except IOError:
            pass

    # Deduplicate keywords
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    keywords = unique_keywords[:50]

    entry = {
        "id": entry_id,
        "topic": topic,
        "keywords": keywords,
        "findings": findings[:100],  # Cap at 100 findings
        "paper_folder": paper_folder or "",
        "source_count": source_count,
        "created_at": datetime.now().isoformat(),
    }

    # Write entry file
    ensure_dirs()
    entry_file = ENTRIES_DIR / f"{entry_id}.json"
    entry_file.write_text(json.dumps(entry, indent=2))

    # Update index
    index = load_index()
    index["entries"].append({
        "id": entry_id,
        "topic": topic,
        "keywords": keywords,
        "created_at": entry["created_at"],
    })
    save_index(index)

    print(f"Added KB entry: {entry_id}")
    print(f"  Topic:    {topic}")
    print(f"  Keywords: {len(keywords)}")
    print(f"  Findings: {len(findings)}")
    print(f"  Sources:  {source_count}")


def cmd_list():
    index = load_index()
    if not index["entries"]:
        print("Knowledge base is empty.")
        return

    print(f"Knowledge Base: {len(index['entries'])} entries\n")
    for entry in sorted(index["entries"], key=lambda x: x.get("created_at", ""), reverse=True):
        print(f"  [{entry['id']}] {entry['topic']}")
        print(f"           Created: {entry.get('created_at', 'unknown')}")
        print(f"           Keywords: {', '.join(entry.get('keywords', [])[:8])}...")
        print()


def cmd_stats():
    index = load_index()
    entries = index.get("entries", [])

    total_entries = len(entries)
    total_findings = 0
    total_sources = 0
    all_keywords = Counter()

    for entry_meta in entries:
        entry_file = ENTRIES_DIR / f"{entry_meta['id']}.json"
        if entry_file.exists():
            entry = json.loads(entry_file.read_text())
            total_findings += len(entry.get("findings", []))
            total_sources += entry.get("source_count", 0)
        for kw in entry_meta.get("keywords", []):
            all_keywords[kw] += 1

    print("deepwrite Knowledge Base Statistics")
    print("=" * 40)
    print(f"Total entries:  {total_entries}")
    print(f"Total findings: {total_findings}")
    print(f"Total sources:  {total_sources}")
    print(f"Unique keywords: {len(all_keywords)}")
    if all_keywords:
        print(f"\nTop keywords:")
        for kw, count in all_keywords.most_common(10):
            print(f"  {kw}: {count}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        cmd_init()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: kb.py search \"<query>\"", file=sys.stderr)
            sys.exit(1)
        cmd_search(sys.argv[2])
    elif command == "add":
        cmd_add(sys.argv[2:])
    elif command == "list":
        cmd_list()
    elif command == "stats":
        cmd_stats()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
