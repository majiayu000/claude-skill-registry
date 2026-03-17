---
name: grove-issues
description: Parse a brain dump of TODOs into properly structured GitHub issues with labels, components, and project board placement. Use when the user provides a batch of tasks, ideas, or TODOs that need to become trackable GitHub issues.
---

# Grove Issues

Turn a brain dump into a clean issue backlog. You receive a messy list of TODOs and produce properly labeled, well-structured GitHub issues ready for the Lattice Kanban board.

## When to Activate

- User provides a batch of TODOs, tasks, or ideas in a single message
- User explicitly calls `/grove-issues`
- User says something like "create issues for these" or "turn these into tickets"
- User pastes a list of things they want tracked

---

## The Pipeline

```
Brain Dump → Parse → Deduplicate → Create Issues → Label → Report
```

### Step 1: Parse the Brain Dump

Break the user's message into discrete, actionable issues. Each issue should represent ONE piece of work. If a TODO is too broad, split it. If two TODOs are the same thing, merge them.

**Parsing signals:**
- Numbered lists → one issue per item
- Bullet points → one issue per bullet
- Paragraphs separated by newlines → one issue per paragraph
- Comma-separated items → one issue per item
- Stream-of-consciousness → use judgment to split at logical boundaries

### Step 2: Check for Duplicates

Before creating any issue, search existing open issues for overlap:

```bash
gh issue list --state open --limit 100 --json number,title | jq -r '.[].title'
```

If a TODO matches an existing issue closely, skip it and note the existing issue number in your report. Don't create duplicates.

### Step 3: Determine Labels

Each issue gets up to 3 labels:

#### Component Labels (pick 1-3)

| Label | When to Apply |
|-------|---------------|
| `lattice` | Framework, monorepo, shared infrastructure, engine package |
| `heartwood` | Auth, sessions, passkeys, OAuth, identity |
| `arbor` | Admin panel, backend API, admin dashboard |
| `amber` | Images, CDN, R2 storage, JXL, media pipeline |
| `clearing` | Status page, health monitoring, uptime |
| `shade` | AI crawler protection, bot defense, rate limiting |
| `plant` | Pricing, billing, LemonSqueezy, storefront, signup |
| `ivy` | Email, Resend, notifications, messaging |
| `foliage` | Theming, design tokens, per-tenant customization |
| `curio` | Museum exhibits, content display, guestbook |
| `meadow` | Social features, community feed |
| `forests` | Forest page, community groves, property showcase |
| `vine` | Content relationships, margin notes, connections |
| `graft` | Feature flags, gradual rollout, A/B testing |
| `petal` | Content moderation, CSAM detection, PhotoDNA |
| `lumen` | AI assistant, LLM routing, AI gateway |
| `mycelium` | MCP servers, inter-service networking |
| `patina` | Backups, cold storage, data preservation |
| `landing` | Landing site, marketing pages, knowledge base |

#### Pattern Labels (pick 0-2, in addition to component labels)

Patterns are reusable architectural solutions. Apply when the issue involves implementing or extending a pattern.

| Label | When to Apply |
|-------|---------------|
| `pattern:firefly` | Ephemeral server infrastructure (ignite, illuminate, fade lifecycle) |
| `pattern:loom` | Durable Objects coordination (SessionDO, TenantDO, PostDO) |
| `pattern:prism` | Glassmorphism design system, seasonal theming, UI layers |
| `pattern:sentinel` | Load testing, scale validation, ramp-up testing |
| `pattern:songbird` | Prompt injection protection (canary, kestrel, robin layers) |
| `pattern:threshold` | Rate limiting, abuse prevention, graduated response |

#### Type Labels (pick exactly 1)

| Label | When to Apply |
|-------|---------------|
| `bug` | Something is broken or wrong |
| `feature` | New capability that doesn't exist yet |
| `enhancement` | Improvement to existing functionality |
| `security` | Security concern, vulnerability, hardening |
| `documentation` | Docs, guides, help articles |

#### Priority (only if explicitly stated by user)

Don't guess priority. Only apply if the user explicitly says something is urgent, critical, or low-priority.

### Step 4: Write the Issue Body

Use this template for every issue:

```markdown
## Summary
[1-3 sentences describing what needs to be done and why]

## Acceptance Criteria
- [ ] [Specific, verifiable criterion]
- [ ] [Another criterion]
- [ ] [Keep to 3-6 items]

## Context
- [Relevant technical context]
- [Dependencies or related issues if known]
- [Any constraints mentioned by the user]
```

**Writing guidelines:**
- Summary should answer "what" and "why" in plain language
- Acceptance criteria should be checkbox items that can be verified as done/not-done
- Context is optional but helpful for implementation details
- Keep the whole body under 20 lines. Concise beats comprehensive.
- Don't pad with boilerplate. If there's no useful context, skip that section.

### Step 5: Create the Issues

```bash
gh issue create \
  --title "Title in imperative mood" \
  --body "$(cat <<'EOF'
## Summary
...

## Acceptance Criteria
- [ ] ...

## Context
- ...
EOF
)" \
  --label "component1,type1"
```

**Title guidelines:**
- Imperative mood: "Add X" not "Adding X" or "X should be added"
- Specific: "Add glass overlay to Forest page sections" not "Forest page improvements"
- No `[FEATURE]` or `[BUG]` prefixes (labels handle categorization)
- Under 60 characters when possible

### Step 6: Report Back

After creating all issues, give the user a summary table:

```
Created X issues:

| # | Title | Labels |
|---|-------|--------|
| #531 | Add glass overlay to Forest page | forests, enhancement |
| #532 | Fix tooltip positioning on mobile | lattice, bug |
...

Skipped (duplicates of existing issues):
- "Cache purge tool" → already tracked in #527
```

---

## Edge Cases

### Vague TODOs

If a TODO is too vague to create a good issue ("fix the thing", "make it better"), ask the user for clarification rather than creating a bad issue. Group vague items and ask once.

### Huge Batches (20+)

For very large batches, create issues in groups of 10 to avoid rate limiting. Pause between batches.

### Mixed Priorities

If the user marks some items as urgent/first-focus vs backlog, note this in Context but don't apply priority labels unless they use explicit priority language.

### Implementation Details in the Brain Dump

If the user includes HOW to do something (not just WHAT), capture those details in the Context section. The acceptance criteria should still focus on the outcome, not the approach.

---

## Anti-Patterns

**Don't do these:**

- Don't create issues with only a title and no body
- Don't apply more than 3 component labels (if it touches everything, it's probably `lattice`)
- Don't guess at acceptance criteria you can't verify. "Works well" is not a criterion. "Renders correctly on mobile viewport" is.
- Don't create issues for things that are already done
- Don't pad issues with generic criteria like "code is well-documented" or "tests pass"
- Don't add `priority-critical` unless the user explicitly says something is critical/urgent

---

## Example

**User says:**
> ok so I need to: fix the broken image on the pricing page, add a dark mode toggle to the knowledge base, wire up the new health endpoint for blog-engine, and eventually we should think about adding RSS feeds to meadow

**You create:**

1. **"Fix broken image on pricing page"** — `plant`, `bug`
2. **"Add dark mode toggle to knowledge base"** — `landing`, `enhancement`
3. **"Wire health endpoint for blog-engine into Clearing"** — `clearing`, `feature`
4. **"Add RSS feed support to Meadow"** — `meadow`, `feature`

Each with proper Summary, Acceptance Criteria, and Context.

---

*A clean backlog is a calm mind. Turn the chaos into clarity.*
