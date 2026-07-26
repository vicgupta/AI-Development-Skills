# AI Development Skills

A collection of reusable skills and workflows for AI-assisted software development. Each skill is a self-contained `SKILL.md` file that defines a structured process for a specific task — from technical specification to customer research to copywriting.

## Skills

| Skill | Description |
|-------|-------------|
| [hole-in-one](./hole-in-one/) | Complete technical specification interrogation — turns vague ideas into implementation-ready specs via MCQ-driven design tree walking |

## How It Works

Each skill follows the same pattern:
- **Trigger** — when to activate (specific phrases, user intents)
- **Phases** — structured steps to follow
- **Output** — what artifact to produce

Skills are designed to be loaded into AI coding assistants (Claude, Cursor, etc.) and executed as interactive workflows.

## Structure

```
AI-Development-Skills/
├── README.md
└── <skill-name>/
    └── SKILL.md
```

## Adding a Skill

1. Create a new directory named after the skill
2. Add a `SKILL.md` file with YAML frontmatter (name, description, version, metadata)
3. Define the workflow phases, MCQ formats, and output templates
4. Update this README

## License

MIT
