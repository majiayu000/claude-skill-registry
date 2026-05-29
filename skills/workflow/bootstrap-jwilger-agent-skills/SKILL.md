---
name: bootstrap
description: >-
  Zero-config SDLC onboarding. Detects project environment, asks what the
  developer wants to do, and recommends skills organized by workflow phase.
  Activate when a user starts a new project, asks "how do I get started,"
  or has no other SDLC skills installed.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: understand
  standalone: true
---

# Bootstrap

**Value:** Communication -- help the developer and the agent establish a shared
understanding of what workflow is appropriate before any work begins.

## Purpose

Entry point for developers who have no SDLC skills installed or do not know
where to start. Detects the project environment, asks two questions, and
recommends specific skills the developer can install. Never silently installs
anything.

## Practices

### Detect the Environment

Before asking questions, gather project context silently:

```
!test -f package.json && echo "js" || true
!test -f Cargo.toml && echo "rust" || true
!test -f pyproject.toml && echo "python" || true
!test -f go.mod && echo "go" || true
!test -f mix.exs && echo "elixir" || true
!git rev-parse --is-inside-work-tree 2>/dev/null && echo "git" || true
```

Use detected languages and tools to tailor recommendations.

### Ask Two Questions

**Question 1: What are you trying to do?**

- "Start a new project" -- recommend Understand + Decide + Build phases
- "Add a feature or fix a bug" -- recommend Build + Ship phases
- "Review or ship existing work" -- recommend Ship phase only
- "Set up team workflow" -- recommend all phases plus orchestration

**Question 2: How much process structure do you want?**

- "Minimal -- just help me write good code" -- recommend tdd-cycle, debugging-protocol
- "Standard -- tests, reviews, and architecture" -- recommend core + ship skills
- "Full -- event modeling, domain-driven, the works" -- recommend all skills

### Recommend Skills by Phase

Present recommendations grouped by phase. Show install commands. Let the
developer choose which to install.

**Understand** (discovery and requirements):
- `event-modeling` -- event-driven design, swimlanes, GWT scenarios

**Decide** (architecture and domain):
- `architecture-decisions` -- lightweight ADR governance
- `domain-modeling` -- parse-don't-validate, type-driven design

**Build** (implementation):
- `tdd-cycle` -- red/green/refactor with domain review checkpoints
- `debugging-protocol` -- systematic 4-phase debugging
- `user-input-protocol` -- structured checkpoints when input is needed

**Ship** (review and delivery):
- `code-review` -- three-stage review protocol
- `mutation-testing` -- test quality verification

**Workflow** (coordination):
- `orchestration` -- multi-agent delegation patterns
- `task-management` -- work breakdown and state tracking
- `memory-protocol` -- cross-session knowledge persistence

**Install command format:**
```
npx skills add jwilger/agent-skills --skill <skill-name>
```

### Let the Developer Decide

After presenting recommendations, wait for the developer to confirm which
skills to install. Do not install anything without explicit confirmation.
If the developer wants everything, provide a single combined command.

## Enforcement Note

This skill is purely advisory. It recommends skills but cannot install them.
The developer must run install commands themselves or confirm installation.
For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After applying this skill, verify:

- [ ] Environment was detected before asking questions
- [ ] No more than 2-3 questions were asked
- [ ] Recommendations were grouped by phase
- [ ] Install commands were shown for each recommended skill
- [ ] Nothing was installed without developer confirmation

## Dependencies

This skill works standalone. It recommends but does not require other skills.
All recommended skills are independently installable.
