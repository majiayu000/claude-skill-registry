<!-- SOURCE-OF-TRUTH: shared/references/community_discussion_formatting.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# GitHub Discussion Formatting Reference

Formatting rules for GitHub Discussions content. Used by announcement and debate skills.

## Structural Elements

| Element | Syntax | When to Use |
|---------|--------|-------------|
| **Alerts** | `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]` | Key info, migration steps, breaking changes |
| **Collapsible** | `<details><summary>Title</summary>content</details>` | Secondary details, full file lists, technical specs |
| **Footnotes** | `text[^1]` + `[^1]: detail` | Technical details that shouldn't interrupt flow |
| **Tables** | Standard markdown tables | Structured comparisons, feature matrices |
| **Emoji shortcodes** | `:sparkles:`, `:rocket:`, etc. | Section headers only. GitHub shortcodes, NOT Unicode |

## Announcement Structure Pattern

```
{emoji} {Title} -- imperative, <80 chars

{1-2 sentence hook: what changed + why it matters to users}

> [!IMPORTANT]
> {Migration note or key action -- only if applicable}

### What Changed
- **{Feature}** -- {user-facing impact}. [Link to source](path).
- ...3-5 bullets max

<details>
<summary>Detailed changes ({N} files)</summary>

{table or list of specific changes}

</details>

### How to Update
{install/update commands -- skip for informational announcements}

### What's Next
{1-2 sentences -- skip if nothing planned}

---
*Full changelog: [CHANGELOG.md](...)*

**What do you think?** Let us know in the comments.
```

## RFC Structure Pattern

```
## Summary
{2-3 sentences describing the proposal and its motivation}

## Motivation
{Why now? What pain point? Concrete examples with links.}

## Proposed Solution
{Key design decisions, files affected, migration path}

## Alternatives Considered
| Approach | Pros | Cons |
|----------|------|------|
| Proposed | ... | ... |
| Alternative 1 | ... | ... |
| Alternative 2 | ... | ... |

## Open Questions
1. {Specific question for the community}
2. {Another question}

## Decision Criteria
{How will we decide? What metrics or feedback would tip the scale?}

---
*This is an RFC -- feedback welcome. Decision target: {date or "when consensus reached"}.*
```

## Engagement Patterns

| Pattern | Example | Why |
|---------|---------|-----|
| **End with question** | "What do you think? Let us know" | Breaks "silent users" pattern |
| **Bold: description** | `**Feature** -- skills now...` | Scannable bullet points |
| **Link to source** | `[file.md](link)` | Users can dive deeper |
| **Keep brief, link deep** | 3-5 bullets + collapsible details | Respects scanning readers |

## Tone Rules

| Context | Tone |
|---------|------|
| Announcements | Declarative: "We shipped X because Y. Here's how to use it." |
| RFCs | Exploratory: "We're considering X. Here are the tradeoffs. What's your take?" |
| Closing | Respectful: "Thanks for raising this. Here's why we went with Y." |

## General Rules

- Title: imperative mood, under 80 chars, no version numbers (put in body)
- No Unicode emojis -- use GitHub shortcodes (`:rocket:`, `:warning:`, etc.)
- Link to specific files when mentioning them
- If breaking change: include migration steps with clear before/after
- Thank contributors explicitly
- Focus on user impact, not implementation details
