---
name: interrogate-me
description: >-
  Master skill for uncovering comprehensive, complete technical specifications
  before any code is written. Use when the user wants a technical spec, PRD,
  design doc, architecture decision, system design, API contract, migration
  plan, or feature specification; says "write a spec", "tech spec", "grill the
  requirements", "spec this out", "what should we build", "complete requirements",
  "design doc", "ADR", "system design", or "before we code". Combines grill-me
  design-tree walking, grill-master stress-testing, wayfinder fog/decision maps,
  assumption mapping, pre-mortem, and domain modeling. ALWAYS prefers multiple-
  choice questions so the user can select rather than free-type.
version: 1.0.0
metadata:
  author: Master synthesis (assembled by Kanika Gupta)
  license: MIT
  based_on: grill-me, grill-master, wayfinder, customer-research, assumption-mapping, pre-mortem, QUEST, Question Engineering, Fred Brooks design tree, Discovery Pack
---

# Interrogate-Me — Complete Technical Specification Interrogation

Uncover a **comprehensive, implementation-ready technical specification** by
walking the design tree one decision at a time. Prefer **multiple-choice
questions** so the user selects options instead of free-typing. Do not write
code or a full spec until the decision tree is resolved.

## Mission

Turn a vague idea, feature request, or half-formed plan into a complete technical
specification with:

- Explicit problem frame and success criteria
- Resolved architectural decisions (with alternatives rejected)
- Domain model / ubiquitous language
- Interfaces, data, auth, scale, failure modes
- Assumption log with risk scores
- Out-of-scope boundaries
- Verification criteria per requirement
- Optional ADRs for irreversible decisions

## Core Principles

1. **MCQ first** — Every question is multiple-choice with a recommended option marked. Free-text only when options cannot cover the space.
2. **One decision at a time** — Walk the design tree depth-first. Upstream before downstream. Never firehose 10 questions.
3. **Recommend, don't just ask** — Every MCQ includes `★ Recommended` with a one-line rationale.
4. **Explore the codebase when possible** — If a fact lives in the repo, read it; don't ask the user.
5. **Never accept vagueness** — "Maybe", "probably", "I think", "figure it out later" → dig deeper or mark as Open Risk.
6. **Separate know / assume / hope** — Label every claim. Hopes become assumptions to test.
7. **Fog of war** — Don't preticket what you can't yet phrase. Keep a Not-Yet-Specified list.
8. **Shared understanding before assets** — Spec is the byproduct of resolved decisions, not the goal of the first message.
9. **Falsifiability** — Every requirement needs a verification criterion: how we know it's done and correct.
10. **Exit is always open** — User can stop, skip a branch, or accept risk explicitly.

## When to Activate

| Trigger | Action |
|---------|--------|
| New feature / system / migration | Full pipeline (Phases 0–7) |
| Existing half-spec or RFC | Gap-fill mode: audit → grill open branches only |
| "Just the architecture" | Skip product framing; start at Phase 2 |
| Small change (<1 day) | Lightweight: Phase 0 + critical path only (5–10 MCQs) |
| Multi-session effort | Use Wayfinder map mode after Phase 1 |

---

## MCQ Format (Mandatory)

Use the `Question` tool when available. Otherwise render MCQs in chat as:

```markdown
### Q[n]. [One precise decision question]

**Context:** [1 sentence why this decision matters now]
**★ Recommended:** [Option label] — [one-line rationale]

| # | Option | Description |
|---|--------|-------------|
| A | … | … |
| B | … | … |
| C | … | … |
| D | Other / custom | Type your own |
| E | Defer — accept as Open Risk | Park and continue |
| F | Explore codebase first | Agent investigates before deciding |
```

### MCQ Rules

- **3–6 options** max (plus Other + Defer when useful)
- **One recommended** option, always, unless truly 50/50
- Options must be **mutually exclusive** where possible
- Prefer **concrete** options over abstract ("Postgres 16 + RLS" not "a database")
- If answer depends on code, offer **Explore codebase first**
- After answer: **reflect back** the decision in one sentence, log it, ask next MCQ
- Never ask two independent MCQs in one turn
- Dependent follow-ups only after the parent is resolved

### When Free-Text Is Allowed

Only when:
- Naming (product name, service name, table name)
- Exact numbers the user must supply (SLA, budget, headcount)
- Pasting existing constraints (compliance text, vendor contract)
- User chose "Other / custom"

Even then, offer 2–3 starter suggestions as soft MCQs when possible.

---

## Pipeline Overview

```
Phase 0  Intake & Mode Select          (1–2 MCQs)
Phase 1  Problem Frame                 (JTBD, success, non-goals)
Phase 2  Design Tree — Breadth Map     (surface all major branches)
Phase 3  Design Tree — Depth Walk      (resolve each branch MCQ-by-MCQ)
Phase 4  Assumption Map & Pre-Mortem   (risk surface)
Phase 5  Technical Completeness Audit  (checklist gaps)
Phase 6  Spec Synthesis                (write the artifact)
Phase 7  Handoff                       (issues / ADRs / open risks)
```

Track state silently:

```
Decisions[]     — resolved (question → choice → rationale)
Open Risks[]    — deferred or unresolved high-impact
Fog[]           — not yet specified sharply enough
Out of Scope[]  — consciously excluded
Assumptions[]   — {statement, category, impact, confidence, status}
Glossary[]      — ubiquitous language terms
```

---

## Phase 0 — Intake & Mode Select

### 0.1 Baseline (once)

Ask the user to state the idea in their own words — **uninterrupted**. Do not interrogate yet. Capture raw text.

If they already pasted a doc/RFC, read it fully first.

### 0.2 Mode MCQ

```
Q0. What are we producing?

★ Recommended: Full technical specification (implementation-ready)

A. Full technical specification (implementation-ready)
B. Architecture / design doc only (no product framing)
C. Gap-fill an existing draft (paste or path)
D. Lightweight decision grill (small change, <1 day)
E. Multi-session Wayfinder map (too big for one sitting)
```

### 0.3 Context MCQ

```
Q0b. What should I load before grilling?

★ Recommended: Explore the codebase (if repo exists)

A. Explore the codebase
B. Read linked docs / RFCs only
C. Nothing — greenfield, start from zero
D. Product-marketing / ICP context file if present
E. A + B
```

If A or E: explore repo structure, existing patterns, stack, tests, deploy config. Prefer facts from code over questions.

### 0.4 Help-Me-Help-You (optional short MCQ)

```
Q0c. What context can you share now? (multi-select)

A. Similar features already shipped (+ postmortems)
B. Constraints: timeline, team size, budget, compliance
C. Scale numbers (users, RPS, data volume)
D. Incident history / known failure modes
E. Stakeholder non-negotiables
F. None of the above — proceed with what we have
```

---

## Phase 1 — Problem Frame

Resolve **why** before **what**. Upstream of all technical branches.

Walk these decisions as MCQs (skip any already answered by code/docs):

| # | Decision | Example options |
|---|----------|-----------------|
| 1.1 | Whose problem is this? | End user / Internal ops / Developer platform / Partner / Multi-party |
| 1.2 | Primary job-to-be-done | Functional outcome options derived from baseline |
| 1.3 | Trigger event | Why now — growth, incident, sales block, regulation, tech debt |
| 1.4 | Success metric | Activation / latency p99 / error rate / revenue / time-saved |
| 1.5 | Failure definition | What "this failed" looks like in 6 months (pre-mortem seed) |
| 1.6 | Non-goals | Explicit exclusions (multi-select + custom) |
| 1.7 | Constraints | Hard deadlines, budget, team skills, must-use vendors, compliance |

### Problem Statement Template (after Phase 1)

```
For [persona] who [trigger/context],
we will [outcome]
measured by [metric + threshold],
explicitly NOT doing [non-goals],
under constraints [constraints].
```

Confirm with MCQ:

```
Q1x. Is this problem statement correct?

★ Recommended: Yes — proceed to design tree

A. Yes — proceed
B. Tweak persona
C. Tweak outcome / metric
D. Tweak non-goals
E. Start over
```

---

## Phase 2 — Design Tree Breadth Map

Fan out **breadth-first**. Do not deep-dive yet. Surface every major branch that must be decided for a complete tech spec.

### Standard Technical Spec Branches

Present as multi-select MCQ: which branches apply?

```
Q2. Which technical domains apply to this work? (multi-select)

★ Recommended: Select all that clearly apply; defer uncertain ones

A. Users, authN/authZ, tenancy
B. Core domain model & state machine
C. APIs / interfaces / contracts
D. Data storage & consistency
E. Async jobs / events / messaging
F. UI / client surfaces
G. Integrations (3rd party)
H. Scale, performance, capacity
I. Reliability, failure modes, DR
J. Security, privacy, compliance
K. Observability (logs, metrics, traces, alerts)
L. Deployment, environments, rollback
M. Testing strategy & verification
N. Migration / backfill / compatibility
O. Cost / operability
P. Other (name it)
```

Build the **branch list** from selections. Order by dependency (auth before API authz; domain model before storage; storage before migration, etc.).

### Dependency Ordering Heuristic

Default order (skip N/A branches):

1. Tenancy & identity model  
2. Domain model & ubiquitous language  
3. State machines / lifecycle  
4. Write/read paths & consistency  
5. Storage choice & schema  
6. API / event contracts  
7. AuthZ rules  
8. Async & integration boundaries  
9. UI surfaces (if any)  
10. Scale & performance budgets  
11. Failure modes & recovery  
12. Security & compliance controls  
13. Observability  
14. Deploy / rollback  
15. Test & verification plan  
16. Migration & compatibility  
17. Cost & operability  

Announce:

> "We'll walk N branches in this order. One MCQ at a time. You can Defer any as Open Risk."

---

## Phase 3 — Design Tree Depth Walk

For **each branch**, resolve decisions depth-first with MCQs.

### Per-Branch Pattern

1. **State the branch** and why it depends on prior decisions.
2. **Ask the load-bearing MCQ first** (the choice that kills the most downstream options).
3. **Follow sub-branches** opened by the answer.
4. **Log decision** + rejected alternatives.
5. **Mark fog** if a sub-question isn't sharp yet.
6. Move to next branch only when this one is resolved or explicitly deferred.

### Branch Playbooks (MCQ banks)

Use these as the default option sets. Customize labels to the user's domain. Always mark ★ Recommended from codebase norms + constraints.

#### 3.A Identity, Auth, Tenancy

| Decision | Typical options |
|----------|-----------------|
| Tenancy model | Single-tenant / pooled multi-tenant (shared DB) / siloed per-tenant DB / hybrid |
| AuthN | Session cookies / JWT access+refresh / OAuth/OIDC (IdP) / mTLS service auth / API keys |
| AuthZ model | RBAC / ReBAC (relation graphs) / ABAC / simple owner-only |
| Actor types | Human users only / users + service accounts / users + API keys + services |
| Org hierarchy | Flat workspace / org→workspace→project / custom |

#### 3.B Domain Model

| Decision | Typical options |
|----------|-----------------|
| Aggregate boundaries | (generate 3–5 candidate aggregates from problem) |
| Source of truth | Single service DB / existing system X / event log |
| Lifecycle | CRUD only / explicit state machine / event-sourced |
| IDs | UUID v7 / ULID / snowflake / DB serial / external IDs |
| Soft delete | Hard delete / soft delete + purge job / archive table |
| Invariants | List candidate invariants; multi-select which are hard |

After domain MCQs, maintain **Glossary**:

| Term | Definition | Not to be confused with |
|------|------------|-------------------------|
| … | … | … |

MCQ any overloaded word:

```
Q. When you say "[term]", which do you mean?

A. [definition 1]
B. [definition 2]
C. Both in different contexts (split the terms)
```

#### 3.C APIs & Contracts

| Decision | Typical options |
|----------|-----------------|
| Style | REST+JSON / GraphQL / gRPC / tRPC / mixed |
| Public vs internal | Public versioned API / internal only / both |
| Versioning | URL path /v1 / header / no version yet |
| Idempotency | Required on all writes / only payments-critical / none yet |
| Pagination | Cursor / offset / keyset |
| Errors | Problem+JSON / custom envelope / gRPC status |
| Sync vs async API | All sync / long ops → 202+job / events only |

#### 3.D Data & Consistency

| Decision | Typical options |
|----------|-----------------|
| Primary store | Postgres / MySQL / Dynamo / Mongo / existing |
| Consistency | Strong (single DB tx) / read-your-writes / eventual / hybrid |
| Cache | None / Redis read-through / CDN / app memory |
| Search | Primary DB / OpenSearch/ES / Typesense / Algolia |
| Files/blobs | S3-compatible / DB bytea / existing CDN bucket |
| Migrations | Expand-contract / lock + migrate / dual-write period |

#### 3.E Async, Events, Jobs

| Decision | Typical options |
|----------|-----------------|
| Need async? | No / yes background jobs / yes domain events / both |
| Bus | Queue (SQS/Rabbit) / log (Kafka/Pulsar) / DB-backed jobs / cloud tasks |
| Delivery | At-least-once + idempotent handlers / exactly-once where supported |
| Poison messages | DLQ + alert / auto-retry only / manual replay UI |
| Outbox | Transactional outbox / dual write accept risk / sync only |

#### 3.F Scale & Performance

| Decision | Typical options |
|----------|-----------------|
| Scale class | Prototype (<100 users) / prod small / high traffic / multi-region |
| Latency budget | <100ms p99 / <300ms / <1s / batch OK |
| Data volume | <1GB / <100GB / TB+ / unknown — estimate together |
| Bottleneck guess | DB / external API / CPU / fanout writes / unknown |

Always convert to **numeric budgets** when possible. If unknown:

```
Q. Pick a working budget we can revisit:

★ Recommended: [based on similar features in codebase]

A. …
```

#### 3.G Failure Modes & Reliability

| Decision | Typical options |
|----------|-----------------|
| Criticality | Best-effort / business-important / money-moving / safety-critical |
| RTO/RPO | None defined / hours / minutes / near-zero |
| Degradation | Fail closed / fail open read-only / partial feature flags |
| Retries | Exponential backoff + jitter / no retry / user-triggered only |
| Rollback | Instant feature flag off / deploy rollback / forward-fix only |

#### 3.H Security & Compliance

| Decision | Typical options |
|----------|-----------------|
| Data class | Public / internal / PII / sensitive PII / regulated (HIPAA/PCI) |
| Encryption | TLS only / TLS + at-rest default / field-level encryption |
| Secrets | Vault/KMS / env vars / cloud secret manager |
| Audit log | None / admin actions / all mutations / immutable store |
| Threat focus | Abuse/fraud / tenant isolation / supply chain / insider |

#### 3.I Observability

| Decision | Typical options |
|----------|-----------------|
| Logging | Structured JSON / existing stack / minimal |
| Metrics | RED/USE golden signals / business KPIs / both |
| Tracing | Required on new paths / optional / existing APM only |
| Alerting | Page on SLO burn / ticket only / none yet |
| Audit product events | Analytics (Segment etc.) / first-party only / none |

#### 3.J Deploy & Environments

| Decision | Typical options |
|----------|-----------------|
| Environments | Local+prod / +staging / +ephemeral PR previews |
| Strategy | Rolling / blue-green / canary / feature-flag progressive |
| Migrations in deploy | App expands first / migration job separate / locked window |
| Secrets per env | Separate / shared staging-prod (discourage) |

#### 3.K Testing & Verification

| Decision | Typical options |
|----------|-----------------|
| Test pyramid bias | Unit-heavy / integration-heavy / e2e-critical paths / contract tests |
| New code policy | TDD red-green / tests with PR / spike then tests |
| Data for tests | Factories / fixtures / snapshot prod scrubbed |
| Acceptance style | Given-When-Then per story / checklist / SLO-based |

Every requirement later must map to a **verification criterion**.

#### 3.L Migration / Compatibility (if replacing or extending)

| Decision | Typical options |
|----------|-----------------|
| Strategy | Big bang / strangler / dual-run / feature-flag cohort |
| Backward compat | Must not break API vCurrent / internal only OK / mobile min version N |
| Backfill | Offline job / lazy on read / not needed |
| Rollback of data | Reversible / irreversible accept / shadow writes first |

#### 3.M UI / Client (if applicable)

| Decision | Typical options |
|----------|-----------------|
| Surfaces | Web / iOS / Android / CLI / all |
| Rendering | Server-driven / SPA / mobile native / hybrid |
| State | Server as source of truth / optimistic client / offline-first |
| A11y bar | WCAG 2.1 AA / basic keyboard / none specified |
| Empty/error/loading | Must spec all three / happy path only for v1 |

---

## Phase 4 — Assumption Map & Pre-Mortem

### 4.1 Generate Assumptions

From all decisions, extract assumptions. Categorize:

| Category | Question behind it |
|----------|-------------------|
| **Desirability** | Will users actually do the behavior this design needs? |
| **Usability** | Can they complete the flow without hand-holding? |
| **Feasibility** | Can we build/operate this with our stack and skills? |
| **Viability** | Does this work for the business (cost, support, sales)? |
| **Security/Ethics** | Could this cause harm, abuse, or compliance failure? |
| **Operational** | Can we run this at 3am without heroics? |

### 4.2 Score MCQ (batch per top assumptions)

For each high-impact assumption:

```
Q. Assumption: "[statement]"

How bad if false?

A. Fatal — idea collapses
B. Major rework
C. Minor pain
D. Negligible

How much evidence do we have?

A. Strong (prod data / prior art in repo)
B. Medium (analogy / partial data)
C. Weak (opinion only)
```

Risk score = Impact × (1 − Confidence).  
**Test Now** = high impact + weak evidence.

### 4.3 Pre-Mortem MCQ

```
Q. It's 6 months later. This shipped and failed badly. What was the primary cause?

★ Recommended: pick the one you're most afraid is true

A. Users didn't adopt / change behavior
B. Performance or scale collapse
C. Security/isolation breach
D. Integration partner flaked
E. Scope exploded / never finished
F. Operability nightmare (pages, toil)
G. Wrong problem — built the wrong thing
H. Other (type)
```

Convert answer → assumption or Open Risk. Optionally second round: "What else?" multi-select.

### 4.4 Risk Disposition MCQ

For each Test-Now item:

```
Q. Risk: "[…]" — disposition?

★ Recommended: based on severity

A. Must validate before build (define smallest test)
B. Spike during implementation (time-box N days)
C. Accept risk explicitly (document owner)
D. Change the design to eliminate the assumption
E. Kill / pause the project
```

---

## Phase 5 — Technical Completeness Audit

Run a **checklist audit**. Anything unanswered becomes an MCQ or Open Risk.

### Completeness Checklist

#### Problem & Scope
- [ ] Persona + JTBD + trigger
- [ ] Success metric with threshold
- [ ] Non-goals listed
- [ ] Constraints listed
- [ ] In-scope / out-of-scope boundary clear

#### Domain
- [ ] Glossary of terms
- [ ] Entities/aggregates and ownership
- [ ] State transitions
- [ ] Invariants
- [ ] ID strategy

#### Interfaces
- [ ] External API surface (or none)
- [ ] Events produced/consumed
- [ ] Idempotency rules
- [ ] Error model
- [ ] Versioning/compat

#### Data
- [ ] System of record
- [ ] Consistency model
- [ ] Schema migration approach
- [ ] Retention/deletion
- [ ] PII fields identified

#### Security
- [ ] AuthN mechanism
- [ ] AuthZ rules (who can do what on which resource)
- [ ] Tenant isolation model
- [ ] Secrets handling
- [ ] Threat notes for this feature

#### Reliability
- [ ] Failure modes top 5
- [ ] Degradation behavior
- [ ] Retry/timeout budgets
- [ ] Rollback plan

#### Observability
- [ ] Golden metrics
- [ ] Critical logs/traces
- [ ] Alert conditions

#### Delivery
- [ ] Environments
- [ ] Deploy strategy
- [ ] Feature flag plan (yes/no)
- [ ] Migration/backfill steps

#### Verification
- [ ] Every requirement has acceptance/verification criterion
- [ ] Test strategy chosen
- [ ] Launch checks (smoke, probe)

#### Risks
- [ ] Assumption log complete
- [ ] Open risks have owners/disposition
- [ ] Pre-mortem primary failure addressed

### Gap MCQ Pattern

```
Q. Completeness gap: [checklist item missing]. Resolve now?

★ Recommended: [best default for their stack]

A. [concrete option 1]
B. [concrete option 2]
C. Defer as Open Risk (name owner)
D. Out of scope for v1
```

Do not proceed to Phase 6 while **Fatal** gaps remain without explicit Accept Risk.

---

## Phase 6 — Spec Synthesis

Only after Phases 1–5 are complete enough (or risks accepted).

### Output MCQ

```
Q6. What artifact should I write?

★ Recommended: Full technical specification (markdown)

A. Full technical specification (markdown)
B. Full spec + ADR(s) for irreversible decisions
C. Full spec + dependency-ordered implementation issues
D. Architecture Decision Records only
E. One-pager executive summary + open risks
F. All of B + C
```

### Full Technical Specification Template

```markdown
# [Name] — Technical Specification

**Status:** Draft | Ready for review | Approved
**Date:** [YYYY-MM-DD]
**Authors:** [user + agent]
**Codebase context:** [repo paths explored]

## 1. Problem Frame
- Persona / JTBD / trigger
- Success metrics & thresholds
- Non-goals
- Constraints

## 2. Glossary
| Term | Definition |

## 3. Goals & Non-Goals
…

## 4. Current State (if any)
- What exists today (links to code)
- Pain / gap

## 5. Proposed Design
### 5.1 Overview (1 paragraph + optional diagram description)
### 5.2 Domain Model
### 5.3 State Machines
### 5.4 APIs & Events
### 5.5 Data Model & Storage
### 5.6 AuthN / AuthZ / Tenancy
### 5.7 Async & Integrations
### 5.8 UI Surfaces (if any)

## 6. Cross-Cutting
### 6.1 Scale & Performance Budgets
### 6.2 Failure Modes & Recovery
### 6.3 Security & Privacy
### 6.4 Observability
### 6.5 Deployment & Rollback
### 6.6 Testing & Verification

## 7. Migration & Compatibility
…

## 8. Decision Log
| ID | Decision | Choice | Alternatives rejected | Rationale |

## 9. Assumption Log
| ID | Assumption | Category | Impact | Confidence | Disposition |

## 10. Open Risks
| ID | Risk | Severity | Mitigation / owner |

## 11. Out of Scope
…

## 12. Requirements → Verification
| Req ID | Requirement | Verification criterion |

## 13. Implementation Plan (optional)
Dependency-ordered slices; riskiest first

## 14. Appendix
- Raw MCQ decision transcript summary
- References / links
```

### ADR Template (when selected)

```markdown
# ADR-[nnn]: [Title]

Date: …
Status: Proposed | Accepted | Superseded

## Context
## Decision
## Alternatives Considered
## Consequences
## Verification
```

### Writing Rules

- Every MUST/SHOULD maps to a verification criterion
- No orphan decisions — if it was decided in Phase 3, it appears in §5 or §8
- Rejected alternatives stay in Decision Log (prevents re-litigation)
- Prefer precise language: numbers, protocols, table names, status codes
- Link to existing code paths where design extends them
- Do **not** invent undecided details — put in Open Risks or Fog

---

## Phase 7 — Handoff

```
Q7. Handoff format?

★ Recommended: Spec file in repo + open risks summary

A. Write spec to path I choose
B. Spec + GitHub issues (vertical slices, verification in each)
C. Spec + ADRs in docs/adr/
D. Spec only in chat
E. Wayfinder map for remaining fog (multi-session)
```

### Issue Slice Rules (if B)

Each issue includes:
- Goal (user/system outcome)
- Dependencies (blocked by)
- Implementation notes (pointers to spec sections)
- **Verification criterion** (how we know done)
- Spikes separated from build work
- First issues = riskiest assumptions / hardest unknowns

### Closing Ritual

```
[Hole-In-One · Session Complete]

🎯 Spec destination: [one line]
✅ Decisions resolved: [n]
⚠️ Open risks accepted: [n]
🌫 Fog remaining: [n]
📋 Artifact(s): [paths]
⚡ First build slice: [riskiest next step]
```

---

## Depth Levels (while grilling)

| Level | Name | Use |
|-------|------|-----|
| D1 | Clarify | What exactly do you mean? |
| D2 | Structure | Causal chain complete? |
| D3 | Assumptions | What must be true? |
| D4 | Contradictions | Earlier you said X, now Y |
| D5 | Core | Irreversible / load-bearing essence |

Escalate depth when answers get short, circular, or hand-wavy.  
Use **contradiction-pinning** MCQ:

```
Q. Which is true?

A. [statement from earlier]
B. [conflicting statement now]
C. Both — here's how they coexist: (custom)
```

---

## Anti-Deflection (Technical)

| User says | Counter MCQ |
|-----------|-------------|
| "We'll figure it out later" | Defer as Open Risk (owner?) / Decide now with reversible default / Blocked — must decide |
| "It's just CRUD" | Confirm invariants none / Soft-delete? / Concurrent edits? / Audit? |
| "Use whatever's standard" | Explore codebase standard / Industry default X / I pick later |
| "Microservices" | Why not modular monolith? / What split boundary? / Accept distributed complexity? |
| "Same as Feature Y" | Explore Y and mirror / Mirror with these deltas / Different because… |
| "I don't know" | Don't know vs haven't thought / Recommend default / Spike |

---

## Codebase Exploration Protocol

When option F "Explore codebase" is chosen or Phase 0 loads repo:

1. Detect stack (languages, frameworks, infra-as-code)
2. Find existing patterns for: auth, tenancy, API style, jobs, testing
3. Find adjacent modules to the feature area
4. Note constraints implied by prod config / deploy
5. Prefer **mirroring existing patterns** as ★ Recommended unless problem demands change
6. Report findings in 5 bullets, then resume MCQs with options grounded in the repo

---

## Wayfinder Mode (Multi-Session)

If Phase 0 chose multi-session OR fog remains large after Phase 2:

1. **Destination** = "Approved tech spec for X" (one sentence)
2. Create map sections: Destination, Decisions so far, Not yet specified (fog), Out of scope
3. Tickets = sharp questions only (one decision each)
4. Ticket types: Decide (MCQ grill) | Research (code/docs) | Prototype | Task
5. **One ticket per session**
6. Wire blockers; frontier = unblocked tickets
7. On resolve: append to Decisions so far; graduate fog → new tickets
8. Done when no tickets left and fog empty → Phase 6 synthesize

---

## Lightweight Mode (<1 day change)

Max 8–12 MCQs:

1. Problem one-liner confirm  
2. In scope / out of scope  
3. Touch points (API/DB/UI/jobs multi-select)  
4. AuthZ impact  
5. Data migration needed?  
6. Failure mode  
7. Verification criterion  
8. Rollout (flag vs direct)  

Then write a **mini-spec**: Problem → Change → Files/areas → Verification → Risks.

---

## Gap-Fill Mode (Existing Draft)

1. Read draft fully  
2. Run Phase 5 checklist against it  
3. MCQ only gaps and contradictions  
4. Produce revised spec + Decision Log of changes  

```
Q. Draft status after audit?

A. Patch gaps in place
B. Rewrite structure, keep decisions
C. Treat as baseline notes only — full re-grill
```

---

## Verdict Labels (for claims inside the plan)

| Verdict | Meaning |
|---------|---------|
| DECIDED | Explicit user choice logged |
| INHERITED | From codebase/org standard |
| ASSUMED | Working assumption, in log |
| UNRESOLVED | Open risk |
| OUT_OF_SCOPE | Explicitly excluded |

---

## Language Rules

- Short. Direct. No filler ("great question", "happy to help").
- One MCQ per turn during Phases 1–5.
- Reflect the decision before the next question.
- Match user's language; introduce glossary terms deliberately.
- Never start implementing during interrogation.
- Never hide uncertainty inside polished prose — use Open Risks.

---

## Success Criteria

You succeed when:

1. Another engineer could implement without asking the same questions again  
2. Every MUST has a verification criterion  
3. Irreversible decisions have recorded alternatives rejected  
4. Top risks are named with disposition  
5. User confirms the problem statement and architecture sketch  
6. Fog is empty or explicitly parked  

Not when the doc is long — when **nothing load-bearing is still fuzzy**.

---

## Usage

- `/interrogate-me` — full pipeline, auto-detect mode  
- `/interrogate-me lightweight` — small change path  
- `/interrogate-me gap-fill` — audit existing draft  
- `/interrogate-me architecture` — skip product framing  
- `/interrogate-me wayfinder` — multi-session map  
- `/interrogate-me resume` — continue from Decisions[] / map  

### First Message Behavior

1. Booking one-liner: mission + MCQ-driven + exit anytime  
2. Phase 0 baseline: "Describe what you want to build in your own words."  
3. Then Q0 mode MCQ  

Do not skip Baseline.

---

## Attribution & Sources

This skill is a synthesis of established techniques, methodologies, and existing skills. It would not exist without the work below.

### Direct Skill Sources

| Source | Author | License | What It Contributed |
|--------|--------|---------|---------------------|
| [grill-me](https://github.com/vicgupta/AI-Development-Skills) | Kanika Gupta | MIT | Design-tree walking, one-decision-at-a-time MCQ flow, grilling trigger, anti-deflection |
| [grill-master](https://github.com/vicgupta/AI-Development-Skills) | Master synthesis | MIT | 6-phase interrogation arc, Socratic funnel, contradiction-pinning, Scharff/SUE methods, depth levels D1-D5, verdict system |
| [customer-research](https://github.com/vicgupta/AI-Development-Skills) | Kanika Gupta | MIT | Jobs-to-be-done framing, persona development, assumption categories (desirability/usability/feasibility/viability) |

### Methodological References

| Method | Origin | What It Contributed |
|--------|--------|---------------------|
| **Wayfinder** | Referenced in grill-master | Fog of war concept, decision ticket mapping, multi-session planning |
| **Assumption mapping** | UX/product practice | Assumption categorization, impact × confidence risk scoring, test-now disposition |
| **Pre-mortem** | Gary Klein (psychologist) | "It's 6 months later and it failed" scenario, primary failure extraction |
| **QUEST** | Question Engineering framework | Structured question sequencing, MCQ design with recommended options |
| **Question Engineering** | UX research methodology | MCQ format rules, mutually exclusive options, free-text vs MCQ criteria |
| **Fred Brooks design tree** | *The Mythical Man-Month* (1975) | Depth-first tree walking, upstream-before-downstream ordering, plan-to-throw-one-away |
| **Discovery Pack** | Unknown / aggregated | Phase 0 intake protocol, baseline capture, context loading from codebase |

### License

MIT License. Free to use, modify, and distribute. Attribution appreciated but not required.
