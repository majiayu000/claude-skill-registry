---
name: pre-mortem
description: Imagine the project has already shipped and failed catastrophically — work backwards from the failure to identify the most likely causes BEFORE building. Forces concrete risk identification, not vague "what could go wrong" lists.
when_to_use: |
  Apply BEFORE implementation begins:
  - architect, after writing ARCH but before gate:plan
  - pm, while breaking work into tasks (Pre-mortem section in PLAN-*.md)
  - security-officer, when threat-modeling
  - any time the feature is irreversible or high-blast-radius
effort: medium
allowed-tools: Read, Write
paths:
  - "docs/plans/**"
  - "docs/architecture/**"
  - "docs/threat-models/**"
---

# Pre-mortem — fail-it-before-you-build-it

A retrospective for a project that hasn't happened yet. Surfaces real
risks that "list every risk" prompts miss.

Originated in Gary Klein's research at MIT Sloan, now standard at AWS
and other ops-mature orgs.

## The 5-step pre-mortem

### Step 1. Imagine you're 6 months in the future

The project shipped. It is a clear, public failure. There's a Reddit
thread about it. The CEO is asking what went wrong.

### Step 2. Write the post-mortem newspaper headline

One sentence. Concrete. Specific. Examples:

- ❌ Bad: "We had some quality issues."
- ✅ Good: "On 2026-09-12, the Stripe webhook handler deduplicated by raw body hash, so 30K customers were double-charged after Stripe retried delivery during a network blip."

The headline forces you to name the failure mode SPECIFICALLY.

### Step 3. List every individual reason this exact failure happened

Brainstorm 10-15 reasons. Be specific. Each item should reference:
- A real component / file
- A real failure mode (race condition, schema mismatch, expired credential)
- A real human factor (oncall didn't see alert, runbook was outdated)

Reject hand-waves like "testing was insufficient." Replace with "we
didn't write a property-based test for the dedup-key collision case."

### Step 4. Rank by likelihood × severity

For each cause, score:
- **Likelihood:** 1-5 (1=once-in-a-decade, 5=monthly)
- **Severity:** 1-5 (1=cosmetic, 5=data loss / regulatory breach)
- **Risk score:** likelihood × severity

Top 3 by risk score → these are your highest-priority mitigations.

### Step 4b. Classify risks — Tigers / Paper Tigers / Elephants

After scoring, classify each risk into one of three types:

**🐯 Tigers** — Real problems you personally believe could derail the project
- Based on evidence, past experience, or clear logic
- Should keep you awake at night
- Require concrete action
- Classify each Tiger by urgency:
  - **Launch-Blocking**: Must be resolved before shipping (broken core feature, regulatory blocker, data integrity risk)
  - **Fast-Follow**: Must be resolved within 30 days post-launch (performance issues, secondary features)
  - **Track**: Monitor post-launch, fix if it becomes an issue (edge cases, nice-to-haves)

**📄 Paper Tigers** — Concerns others might raise that you don't believe are real risks
- Valid-sounding on the surface but unlikely or overblown
- Not worth significant resource investment
- Worth documenting to align stakeholders and avoid repeated debates
- For each: explain WHY you don't believe it's a real risk

**🐘 Elephants** — Things the team knows about but isn't discussing openly
- Uncomfortable concerns: technical debt, team tension, unrealistic timeline, design that nobody likes
- Uncertain — you're not sure if it's a problem, but nobody is investigating
- Deserve explicit surfacing before launch — silent elephants become Tigers post-launch

### Step 5. For each top-3 cause, write a guardrail in the plan

Each guardrail is a concrete change to the plan:
- A test that would have caught it
- A circuit breaker / feature flag
- A runbook entry
- A monitoring alert with specific SLO

If a top-3 cause CANNOT be mitigated within the time/budget, escalate to
the user: "This plan accepts the risk of X with no mitigation."

## Template — add to PLAN-*.md

```markdown
## Pre-mortem

Six months from now, this project failed. Headline:

> <one-sentence failure headline>

### Top reasons (likelihood × severity)

| Cause | L | S | Risk | Mitigation in plan |
|---|---|---|---|---|
| <specific cause> | 4 | 5 | 20 | <Task #N: write idempotency test> |
| ... | | | | |

### 🐯 Tigers (real risks — require action)

| Tiger | Classification | Mitigation | Owner | Due |
|-------|---------------|-----------|-------|-----|
| <risk> | Launch-Blocking | <concrete action> | <team/person> | <date> |
| <risk> | Fast-Follow | <concrete action> | <team/person> | <date> |
| <risk> | Track | <monitoring approach> | <owner> | post-launch |

### 📄 Paper Tigers (overblown — document to align stakeholders)

- **<concern>**: Not a real risk because <reason>. If <condition> changes, revisit.

### 🐘 Elephants (unspoken — needs open discussion)

- **<concern>**: Nobody is talking about this. Suggested conversation: "<how to raise it>".

### Accepted risks (no mitigation)

- <risk> — accepted because <budget/scope reason>. Owner: <name>.
```

## Common failure modes by archetype

Quick start — most-common pre-mortem causes per archetype:

| Archetype | Common failure |
|---|---|
| fintech / commerce | Idempotency-key collision; double-charge during retry storm |
| healthcare | PHI leak via debug log; BAA not signed with vendor |
| web3 | Oracle staleness; flash-loan exploit on bonding curve |
| mlops | Training/serving skew; model drift undetected |
| iot-embedded | OTA bricks devices in a region with no recovery path |
| data-platform | Late-arriving data overwrites correct values |
| ai-system / agent-product | Prompt injection exfiltrates other users' data |
| enterprise-saas | Cross-tenant data leak via RLS gap |
| cli-tool | Destructive flag with no confirmation (rm -rf equivalent) |
| library | Breaking change in minor version bump |

## Anti-patterns in pre-mortems

❌ **Vague risks.** "Performance might be a problem." Be specific: which
operation, at what load, what's the SLO.

❌ **Cosmic risks.** "AWS could go down." Yes, but that's not actionable.
Focus on what you can mitigate.

❌ **Defensive list.** Listing risks you've already mitigated to look
thorough. Only list risks the current plan does NOT yet address.

❌ **Skip the headline.** Without the headline, the team won't believe
the failure scenario is real.

## When to skip

- **nano project_size** — pre-mortem is overhead.
- **Pure refactor with full test coverage** — guardrails already exist.
- **Bug-fix with one-line repro** — risk is well-bounded.
