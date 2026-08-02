# Interrogate-Me

A skill for generating comprehensive technical specifications through structured interrogation.

## Project Structure

- `.opencode/agents/` - Custom agents (planning, coding, evaluating)
- `.opencode/skills/interrogate-me/` - Main interrogate-me skill

## Agents

- **planning-agent**: Interview-driven requirements gathering and spec generation
- **coding-agent**: Production-ready code generation from specifications
- **evaluating-agent**: Code quality review and security auditing

## Skills

- **interrogate-me**: Complete technical specification interrogation with MCQ-driven design tree walking

## Commands

- `/interrogate-me` - Full technical spec pipeline
- `/interrogate-me lightweight` - Small change path (<1 day)
- `/interrogate-me gap-fill` - Audit existing draft
- `/interrogate-me architecture` - Skip product framing
- `/interrogate-me wayfinder` - Multi-session map
