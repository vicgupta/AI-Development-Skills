# Hole-In-One

A collection of reusable skills, agents, and configurations for AI-assisted software development. Includes structured workflows (skills), role-based agents (planning, coding, evaluating), and an opencode config to tie it all together.

## Skills

| Skill | Description |
|-------|-------------|
| [interrogate-me](./.opencode/skills/interrogate-me/) | Complete technical specification interrogation — turns vague ideas into implementation-ready specs via MCQ-driven design tree walking |

## Agents

Three specialized agents that work together in a pipeline: **Plan → Code → Evaluate**.

| Agent | Purpose | Permissions |
|-------|---------|-------------|
| [planning-agent](./.opencode/agents/planning-agent.md) | Requirements gathering, specs, PRDs, technical design docs | Read-only (no edits, no shell) |
| [coding-agent](./.opencode/agents/coding-agent.md) | Production-ready code from specifications | Full access (edit + shell) |
| [evaluating-agent](./.opencode/agents/evaluating-agent.md) | Code review, security audit, quality assessment | Read-only (no edits, no shell) |

### Workflow

```
User idea → planning-agent (spec) → coding-agent (implementation) → evaluating-agent (review)
```

The planning-agent never writes code. The coding-agent never writes specs. The evaluating-agent never rewrites — only reports. Each agent is scoped to its job.

## Configuration

The `opencode.jsonc` file configures the agents for use with [opencode](https://opencode.ai):

```jsonc
{
  "agent": {
    "planning-agent": {
      "mode": "primary",
      "model": "opencode-go/qwen3.7-plus",
      "permission": { "edit": "deny", "bash": "deny" }
    },
    "coding-agent": {
      "mode": "primary",
      "model": "opencode-go/kimi-k2.7-code",
      "permission": { "edit": "allow", "bash": "allow" }
    },
    "evaluating-agent": {
      "mode": "primary",
      "model": "opencode-go/deepseek-v4-flash",
      "permission": { "edit": "deny", "bash": "deny" }
    }
  }
}
```

## Structure

```
hole-in-one/
├── README.md
├── opencode.jsonc
├── .opencode/
│   ├── agents/
│   │   ├── planning-agent.md
│   │   ├── coding-agent.md
│   │   └── evaluating-agent.md
│   └── skills/
│       └── interrogate-me/SKILL.md
```

## Adding a Skill

1. Create a new directory `.opencode/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter (name, description, version, metadata)
3. Define the workflow phases, MCQ formats, and output templates
4. Update this README

## Adding an Agent

1. Create a new `.md` file in `.opencode/agents/`
2. Add YAML frontmatter with `description` and `mode`
3. Define the agent's approach, constraints, and example flow
4. Add a corresponding entry in `opencode.jsonc` with model and permissions
5. Update this README

## License

MIT
