---
name: help
description: Show available Claude Code commands, skills, and the GitHub Mobile workflow for NighTrip development.
disable-model-invocation: true
argument-hint: ""
---

# Claude Code — NighTrip Quick Reference

Provide a clear, formatted summary of all available commands and workflows.

---

## Available Slash Commands (Skills)

| Command | What It Does |
|---------|-------------|
| `/implement-feature [description or issue#]` | Full SDD workflow: explore → write failing specs → implement → verify |
| `/fix-issue [issue-number]` | Reproduce bug with failing test → fix → verify |
| `/review-pr [pr-number]` | Thorough code review: Rails conventions, security, test coverage |
| `/help` | Show this reference |

---

## GitHub Mobile Workflow

### Starting a Task from Mobile

**Option A — Label Trigger (for new features/bugs):**
1. Create an Issue using the template (Feature Request, Bug Report, etc.)
2. Describe what you want clearly
3. Add the `approved` label → Claude starts working automatically

**Option B — Comment Trigger (for quick instructions):**
1. Open any Issue or PR
2. Write a comment with `@claude [your instruction]`
3. Claude responds and implements

### Common Mobile Patterns

```
# On an issue — ask Claude to implement it
@claude implement this feature

# On a PR — ask Claude to fix a review comment
@claude fix the RuboCop offense in spots_controller.rb

# On a PR — get a full code review
/review-pr

# On an issue — ask Claude to write specs first
@claude write the failing specs for this feature

# Ask Claude anything about the codebase
@claude explain how Turbo Streams are used in the comments feature
```

---

## Label Reference

| Label | Meaning | Who Sets It |
|-------|---------|-------------|
| `proposal` | Claude proposed an approach | Auto (Issue template) |
| `approved` | Approved — Claude starts work | **You** |
| `in-progress` | Claude is implementing | Auto (workflow) |
| `needs-review` | PR ready for your review | Claude |
| `auto-merge` | Merge automatically after CI | You (optional) |
| `bug` | Bug report | Auto (Issue template) |
| `maintenance` | Maintenance task | Auto (Issue template) |

---

## SDD Quick Summary

Always: **Specs first → Fail → Implement → Pass → Lint → Security → PR**

1. Write failing RSpec specs
2. Run `bundle exec rspec <spec-file>` → must fail
3. Implement minimal code
4. Run `bundle exec rspec` → all green
5. Run `bin/rubocop -a` → no offenses
6. Run `bin/brakeman --no-pager` → no warnings
7. Create PR with `needs-review` label

---

## Useful `@claude` Prompts from Mobile

- `@claude what does [file/feature] do?` — Get explanations
- `@claude add a spec for [scenario]` — Add missing test coverage
- `@claude refactor [specific code]` — Targeted refactoring
- `@claude is this PR safe to merge?` — Quick security/quality check
- `@claude create a PR for this issue` — Generate PR from issue branch
