---
name: skill-router
description: >
  · Route user requests to the right installed skill with minimal loading. Triggers: 'which skill',
  'skill routing', 'choose skill', 'skill overlap', 'trigger conflict'. Not for creating skills (use skill-creator).
license: MIT
compatibility: "None - works with any Agent Skills collection"
metadata:
  source: iuliandita/skills
  date_added: "2026-05-01"
  effort: medium
  argument_hint: "<request-or-skill-list>"
---

# Skill Router

Route a user request to the smallest useful skill set. Prefer one primary skill. Use a short
ordered set only when the request genuinely spans independent domains.

## When to use

- User asks which skill applies to a request
- A request appears to match multiple skill descriptions
- A skill description or trigger list is causing routing confusion
- You need to explain why one adjacent skill is a better fit than another

## When NOT to use

- Creating or rewriting a skill - use **skill-creator**
- Batch improving a collection - use **skill-refiner**
- Capturing feature ideas or competitive backlog items - use **roadmap**
- Implementing domain work after routing - use the selected domain skill
- Routing requests to understand or optimize a skill's own trigger text - use **skill-creator** (Mode 4)

---

## AI Self-Check

Before returning a routing decision, verify:

- [ ] User intent is stated in one sentence
- [ ] Hard trigger words were checked against the available skill descriptions
- [ ] "Not for" routing hints were checked before choosing
- [ ] One primary skill is selected unless the task truly spans multiple domains
- [ ] Near misses are explained only when useful
- [ ] The next action is clear: invoke a skill, ask a question, or proceed without a skill
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: close matches are checked for trigger theft, missing exclusions, and process-skill precedence before the final route
- [ ] **Spec claims verified**: claims about installed skills, trigger descriptions, or routing metadata are checked against the current collection

---

## Performance

- Read skill metadata first; open full `SKILL.md` files only for close matches.
- Prefer two or three near matches over scanning every reference file.
- Stop once the selected skill has enough confidence for the next action.

## Best Practices

- Route by the user's intended work, not by incidental keywords.
- Respect explicit user skill requests even if another skill might also apply.
- Use ordered skill sets when process skills must precede domain skills.
- **Ordered vs Parallel:** use `Ordered` when output of the first skill is input to the second (e.g., a review/reframe step that shapes the domain work). Use `Parallel` when the subtasks are independent and neither depends on the other's output. A process skill is one whose primary purpose is shaping, evaluating, or transforming intent rather than producing a domain artifact - examples in the installed collection: **jekyll-hyde** (critical reframing), **code-review** (evaluation before fixes). See `references/routing-patterns.md` for examples.

## Workflow

### Step 1: Restate intent

Reduce the request to one concrete task statement.

### Step 2: Identify hard matches

Check skill names, trigger words, file types, tools, and explicit user mentions.

### Step 3: Apply exclusions

Read "When NOT to use" and "Not for" hints for close matches. Remove skills whose exclusions fit
the request.

### Step 4: Choose the route

Return one of:

- `Primary: <skill>` when one skill is enough
- `Ordered: <skill-1> -> <skill-2>` when a process skill must run before a domain skill
- `Parallel: <skill-a>, <skill-b>` when independent domains can be worked separately
- `No skill` when no available skill materially helps

### Step 5: Explain briefly

Give the reason in one or two sentences. Include near misses only if they prevent confusion.

For examples, see `references/routing-patterns.md`.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** SKILL-ROUTER
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content (e.g., a routing-conflict audit across the installed skill set), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/skill-router/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content** (its primary routing-decision mode), respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **skill-creator** - create, review, or optimize skill files after routing identifies skill-library work.
- **skill-refiner** - batch-improve a skill collection with scoring and iteration; this skill only chooses routes.
- **full-review** and **deep-audit** - orchestrate repo audits after routing identifies broad review intent.
- **roadmap** - capture product or feature ideas; route there when the request is backlog shaping rather than skill selection.

## Rules

1. Prefer one primary skill.
2. Do not load reference files during routing unless the main skill file is ambiguous.
3. Do not invent skills that are not installed.
4. Do not let broad words like "review", "test", or "frontend" override explicit exclusions.
5. After routing, stop routing and let the selected skill govern the next work.
