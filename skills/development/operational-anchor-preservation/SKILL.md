---
name: operational-anchor-preservation
description: >
  Use before you shorten, compress, or rewrite the BODY of an existing SKILL.md
  or agent .md — the moment you are about to cut text to reduce length. First
  inventory the file's operational anchors (exact code / command / API snippets,
  fail-closed workflow guards, and rule / threshold statements), preserve every
  one, then judge the rewrite by expected downstream task cost (exploration,
  debugging, recovery tokens) rather than by the resulting line count. A shorter
  skill that strips an anchor makes the agent MORE expensive per task, so length
  is never the objective and rewrite is not compression. Backed by Preserving
  Operational Anchors When Compressing Agent Instructions (arxiv 2606.09421v2).
  Triggers on shortening or refactoring a skill or agent body.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "shorten or compress this SKILL.md"
  - "rewrite an agent body to reduce length"
  - "refactor a skill without losing what makes it work"
updated: 2026-07-18
status: ACTIVE
source: arxiv 2606.09421v2 (Preserving Operational Anchors When Compressing Agent Instructions)
---

# Operational Anchor Preservation

When you rewrite, compress, or shorten the body of an existing SKILL.md or agent
`.md`, first find its **operational anchors** — the exact fragments the agent
executes against — preserve every one, and score the rewrite by expected task
cost, not by line count. This is a heuristic lens, not a deterministic gate:
there is no universally best compression, so the objective is a body the
downstream agent can act on cheaply, not a shorter file.

## Why

In this self-modifying system a skill body is not documentation — it is the
procedure the agent loads and follows. `skill-forge` edits these bodies,
`skill-integration` proposes new ones from repeated tool sequences, and
`token-budget` pressure during convoy work is a standing reason to trim them.
The failure mode: a rewrite that drops an exact command, a fail-closed guard, or
a numeric branch reads as a clean 40% cut but forces the next agent to re-grep a
path, re-derive a flag, or trip a chokepoint to rediscover a rule it deleted.
Those re-exploration and recovery tokens dwarf the tokens saved. Length went
down; cost per task went up. That is a lossy edit wearing the mask of cleanup.

## Data classes touched

Skill and agent files (`project-claude/skills/**`, `.claude/skills/**`,
`.claude/agents/*.md`) — **project-internal**. A sub-class is safety-critical: a
body may encode `security-hygiene` guards, `ProcessContext`/`LoaderContext`
chokepoint requirements, or a boundary sentence that references a **never-surface**
record (private origins, Fox Companies IP, credentials, Center Camp trust rules).
Boundary rule: never strip a safety-critical guard or a never-surface boundary
statement to save length, and never let removed text leak a protected value into
the commit message, diff comment, or the rewrite itself. Rewrites of a
safety-critical body escalate (below), they do not auto-apply.

## How

1. **Confirm scope.** This fires only when the intent is to *reduce* the body of
   an existing skill/agent. Frontmatter-only change → hand to
   `skill-frontmatter-doctor` and stop. Expanding or authoring new content → no
   anchors are at removal risk, stop. Sanitizing a STRANGER untrusted file →
   that is `skill-injection-guardian`'s static pass, not a cost-aware rewrite.

2. **Inventory anchors from the CURRENT body, before editing.** Tag every
   fragment in three classes:
   - **Code/API** — anything inside a fenced block; inline-backticked commands;
     file paths (contain `/` or a dot-extension); tool/function names; ALL_CAPS
     env vars; CLI flags. Preserve **character-exact**.
   - **Guard** — any sentence carrying MUST / NEVER / fail closed / escalate /
     do-not-auto / chokepoint / HITL / never-surface / boundary. Preserve as an
     enforceable imperative at **equal modal strength**.
   - **Rule/threshold** — any number, if/then conditional, decision branch,
     invariant, or formula. Preserve the **number and the branch structure**.

3. **Rewrite may reflow prose, not anchors.** Collapse redundant narration,
   merge examples, cut restatement — but each inventoried anchor must reappear
   with equal force. If a rewrite would drop or soften one, that is a behaviour
   change, not compression: restore it or go to escalation.

4. **Score by expected task cost.** Ask: would removing this fragment force the
   agent into ≥1 extra exploratory tool call (re-grep a path, re-derive a
   command, trip a guard to relearn it, replan a recovery)? If yes, it is an
   anchor — keep it, whatever it costs in lines. Accept the rewrite only when the
   full inventory survives AND expected task cost is non-increasing. Line
   reduction is a side effect of that, never its acceptance criterion.

### Robustness rule

Judge by **effect, not surface phrasing**. A rewrite that keeps the words but
turns "MUST escalate on conflict" into "consider escalating" has destroyed a
guard anchor even though the diff looks small. Conversely, a terser sentence
that preserves the enforceable effect and the exact command is a valid cut. Do
not score by diff size or word overlap — score by whether the agent can still do
the task without rediscovering what you removed.

## Confidence / failure model

This wraps an LLM **judgment** — "is this fragment load-bearing?" and "does this
raise task cost?" are semi-decidable, not a deterministic check, and it reduces
rather than eliminates the risk of silently degrading a skill. Fail-closed
default: when uncertain whether a fragment is an anchor, **treat it as one and
keep it** — a retained non-anchor costs a few tokens; a dropped anchor costs the
next agent a debugging loop. For any rewrite touching shared repo state (a skill
two convoy branches both edited — `refinery-merge` never auto-resolves that,
neither do you), sensitive/never-surface memory, or a safety-critical guard, do
not auto-apply: surface it via `mayor-coordinator` escalation for operator review.

## When to skip

- Frontmatter-only edit → `skill-frontmatter-doctor` owns it.
- The edit adds or expands content — nothing is being removed.
- The target is README/docs/prose the agent reads but does not execute — this is
  scoped to instruction bodies the agent LOADS and follows.
- You are curating footprint, not text: if a skill should shrink because it is
  net-negative, that is a retire/repair decision for `skill-causal-curation`,
  not a lossy rewrite of a skill worth keeping.

## Integration

- `skill-frontmatter-doctor` — frontmatter-only sibling; this covers the body it
  does not touch.
- `skill-causal-curation` — the keep/repair/retire layer; if compression keeps
  failing to preserve anchors, the honest move is retire/repair there, not a
  smaller lossy body here.
- `skill-forge` — this runs inside forge's edit step, before validate → critique
  → ship, so a shipped skill is never quietly hollowed out.
- `skill-counterfactual-audit` — after a rewrite passes this gate, its paired
  with/without probe confirms behaviour did not regress.
