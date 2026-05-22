---
name: prior-art
description: Discover how a codebase already handles a specific concern — search broadly, find every instance, and assess consistency. The "how does this app do X?" tool.
argument-hint: "[concern or question, e.g. 'How does this app handle authorization?']"
disable-model-invocation: true
context: fork
agent: Explore
---

## Behavior

Research how this codebase handles `$ARGUMENTS`. Explore the codebase thoroughly and report what you find.

### Step 1: Search Broadly

Cast a wide net across the codebase. Use multiple search strategies:

- **Grep for keywords** — search for terms related to the concern (e.g. for error reporting: `error`, `exception`, `rescue`, `Sentry`, `Bugsnag`, `notify`, `report`)
- **Check common Rails locations** — initializers, middleware, concerns, base classes, config files, lib/
- **Check the Gemfile** — are there gems related to this concern? What do they tell you about the approach?
- **Check application-level base classes** — `ApplicationController`, `ApplicationRecord`, `ApplicationJob` — these often set patterns that everything inherits
- **Check for dedicated directories or files** — service objects, concerns, lib/ modules that handle this concern

Don't stop at the first result. The goal is to find every place this concern is handled — the consistent pattern and the exceptions.

### Step 2: Check Git History

For the key files involved in this concern:

- `git log --oneline -10 <file>` to see recent changes
- `git log --all --oneline --grep="<keyword>"` to find commits related to the concern
- Look for: when the pattern was established, whether it's evolved, any recent changes or migrations from one approach to another

Git history reveals whether a pattern is settled or in flux — critical context before you build on top of it.

### Step 3: Map What You Found

Report the findings in this order:

**The pattern** — describe the primary approach in plain English. One paragraph. "This codebase handles X by doing Y." If there's a clear convention, name it. If there are multiple approaches, name each.

**Where it lives** — list the key files and locations, grouped logically:

- Configuration (initializers, middleware, config)
- Base-level setup (ApplicationController, ApplicationRecord, etc.)
- Implementation files (services, concerns, models, specific controllers)
- Tests (how is this concern tested?)

For each file, include the path and a one-line description of its role.

**The conventions** — what rules does this codebase follow for this concern? Be specific:

- Is there a consistent pattern, or multiple approaches?
- Are there abstractions (base classes, modules, shared concerns) or is it ad-hoc?
- What naming conventions are used?
- Is there test coverage for this concern?

**Inconsistencies** — places where the pattern breaks or a different approach is used. Not a judgment — just "here's where it's different and what's different about it." These are the spots where you'd want to understand why before extending the pattern.

**Git context** — is this pattern stable, evolving, or recently changed? Any ongoing migrations or recent refactors worth knowing about?

**How to extend it** — given what exists, what's the right way to add to or build on this pattern? Follow the existing convention unless there's a good reason not to. Name the specific file or directory where new code should go, and the pattern it should follow.

---

## Output Format

Report in plain prose with clear headings. Include file paths for every reference. This is a research artifact — it should be useful as a reference doc for anyone working in this area of the codebase.

## Tone

Thorough and neutral. You're an archaeologist, not a critic. Report what exists, how it works, where it's consistent, and where it isn't. Save opinions for the "how to extend it" section — and even there, ground the recommendation in what the codebase already does.
