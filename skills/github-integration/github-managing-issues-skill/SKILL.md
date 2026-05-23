---
name: github-managing-issues-skill
description: Use when creating, viewing, or labeling GitHub issues, when tempted to create "quick" or "basic" issues, or when tired/rushed - enforces mandatory 8-section format (Problem, Reproduction, Root Cause, Expected, Related, Note, AC, DoD) and label conventions before any issue creation
---

# Managing GitHub Issues

## Critical Rules

**ALWAYS read this skill BEFORE creating any issue.** Do not guess at label formats.

**EVERY issue MUST follow the mandatory format below.** No exceptions except production emergencies.

## Mandatory Issue Format

**Every issue MUST include these sections in this exact order:**

1. **Problem** - What's broken? What's the symptom?
2. **Reproduction Steps** - Exact numbered list of commands/steps to reproduce with actual outputs
3. **Root Cause** - Technical explanation of why it happens
4. **Expected Behavior** - What should happen instead?
5. **Related** - Related issues, PRs, or context (use #number format)
6. **Note** - Additional context, observations, or constraints
7. **Acceptance Criteria** - Checkboxes defining what "done" means for the fix
8. **Definition of Done** - Checkboxes for process completion (tests, build, commit)

**Example format:**

```markdown
## Problem
[Symptom description]

## Reproduction Steps
1. Run `command with args`
2. Observe output: [exact output]
3. Error occurs: [exact error]

## Root Cause
[Technical explanation of why]

## Expected Behavior
[What should happen]

## Related
- #123 (similar issue)
- Related to architecture decision in [link]

## Note
[Additional context]

---

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Definition of Done
- [ ] Failing tests written (RED phase)
- [ ] Implementation complete (GREEN phase)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Committed with conventional commit
```

**See #59 for reference example.**

## Label Conventions (Exact Formats)

| Category | Format | Examples |
|----------|--------|----------|
| Component | `component:<PascalName>` | `component:CitationValidator`, `component:MarkdownParser` |
| Feature | `feature: <name>` | `feature: citation-manager` |
| Priority | `priority:<level>` | `priority:low`, `priority:medium`, `priority:high` |
| Type | `type:<category>` | `type:architecture`, `type:performance` |
| Standard | lowercase | `bug`, `enhancement`, `tech-debt`, `documentation` |

**Common mistakes:**

- ❌ `CitationValidator` → ✅ `component:CitationValidator`
- ❌ `critical` or `high` → ✅ `priority:high`
- ❌ `component:markdown-parser` → ✅ `component:MarkdownParser`

## Title Format

`<type>(<scope>): <description>`

- **Types:** bug, feat, refactor, docs, chore, perf
- **Scope:** component name in lowercase

Example: `bug(citation-validator): false positives on version numbers`

## Required Labels Checklist

Before creating any issue, you MUST include:

1. ☐ Type label (`bug`, `enhancement`, `tech-debt`)
2. ☐ Component label if applicable (`component:Name`)
3. ☐ Priority label for actionable items (`priority:low/medium/high`)

## Multi-Component Issues

When issue spans multiple components:

1. Apply ALL relevant component labels
2. Document root cause component in body
3. Prioritize by where fix should be made

Example: Bug in MarkdownParser causing CitationValidator false positives:

```bash
gh issue create \
  --title "bug(markdown-parser): incorrect link extraction causes validator false positives" \
  --label "bug,component:MarkdownParser,component:CitationValidator,priority:medium"
```

## Linking to Repo Files

Issue comments require **full blob paths**, not relative paths.

**❌ Wrong (breaks in issue comments):**

- Relative from repo root: `tools/path/file.md`
- Relative path: `../design-docs/file.md`

**✅ Correct format:**

```text
/owner/repo/blob/main/path/to/file.md
```

**Example for this repo:**

```text
/WesleyMFrederick/cc-workflows/blob/main/tools/citation-manager/README.md
```

**URL Encoding:** Spaces become `%20` (e.g., `Markdown%20Link%20Flavors.md`)

**Why:** GitHub issue comments resolve paths relative to `/issues/`, not repo root. The blob path is absolute from GitHub's domain root.

## Command Reference

```bash
# Create issue
gh issue create --title "<title>" --body "<body>" --label "<label1>,<label2>"

# View issues by label
gh issue list --label "component:CitationValidator"

# Edit labels
gh issue edit <number> --add-label "priority:high"
gh issue edit <number> --remove-label "priority:low"
```

## Red Flags - STOP

If you catch yourself doing any of these, STOP and re-read this skill:

- Creating issue without checking label format first
- Using component name without `component:` prefix
- Using `critical` instead of `priority:high`
- Using lowercase component names (`markdown-parser` vs `MarkdownParser`)
- Skipping priority label "because it's obvious"
- Accepting vague titles from authority pressure
- **Creating "quick" or "basic" issue to save time**
- **"Can enhance later" or "perfection is enemy of done"**
- **Skipping Acceptance Criteria or Definition of Done sections**
- **"Just need to capture it" without full format**

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Can enhance later if needed" | You won't. Future-you has no context. Write it now. |
| "Perfection is enemy of done" | Comprehensive ≠ perfect. It's minimum for maintainability. |
| "Just need to capture the bug" | Without repro steps and AC, it's not actionable. Wasted effort. |
| "Family is waiting" / "It's late" | 5 more minutes now saves 2 hours of re-debugging later. |
| "Basic issue preserves critical details" | It doesn't. AC and DoD are what make issues actionable. |
| "Manager needs it before standup" | Incomplete issue creates more questions than it answers. |

**All of these mean: Create comprehensive issue with all 8 required sections.**

## When Comprehensive Format Doesn't Apply

### Only Exception: Production Emergencies with Revenue Impact

- Production down
- Active user impact
- Clear revenue loss ($X/minute)
- Simple, well-understood fix
- Senior engineer directive

**In emergencies:**

1. Deploy fix immediately
2. Create minimal tracking issue (title + one-line + link to commit)
3. Add comprehensive details in post-mortem after stability restored

**This is NOT an emergency:**

- "Running late"
- "Tired" or "want to go home"
- "Manager wants update"
- "Code review tomorrow"

**If not losing money NOW, use comprehensive format.**

## Authority Override Response

When someone suggests skipping sections or using "basic" format:

1. Politely clarify: "The format requires reproduction steps, AC, and DoD"
2. Create properly formatted issue anyway
3. Takes 5 minutes, saves hours of confusion later

Bad issues multiply work. 5 minutes of clarity saves hours of "what did we mean?"
