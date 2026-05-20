---
name: review-ai-writing
description: Detect AI-generated writing patterns in developer text — docs, docstrings, commit messages, PR descriptions, and code comments. Use when reviewing any text artifact for authenticity and clarity.
autoContext:
  whenUserAsks:
    - ai writing
    - ai-generated
    - sounds like ai
    - writing quality
    - humanize
    - robotic writing
    - chatgpt
dependencies:
  - docs-style
---

# AI Writing Detection for Developer Text

Detect patterns characteristic of AI-generated text in developer artifacts. These patterns reduce trust, add noise, and obscure meaning.

## Pattern Categories

| Category | Reference | Key Signals |
|----------|-----------|-------------|
| Content | `references/content-patterns.md` | Promotional language, vague authority, formulaic structure, synthetic openers |
| Vocabulary | `references/vocabulary-patterns.md` | AI word tiers, copula avoidance, rhetorical devices, synonym cycling, commit inflation |
| Formatting | `references/formatting-patterns.md` | Boldface overuse, emoji decoration, heading restatement |
| Communication | `references/communication-patterns.md` | Chat leaks, cutoff disclaimers, sycophantic tone, apologetic errors |
| Filler | `references/filler-patterns.md` | Filler phrases, excessive hedging, generic conclusions |
| Code Docs | `references/code-docs-patterns.md` | Tautological docstrings, narrating obvious code, "This noun verbs", exhaustive enumeration |

## Scope

Scan these artifact types:

| Artifact | File Patterns | Notes |
|----------|--------------|-------|
| Markdown docs | `*.md` | READMEs, guides, changelogs |
| Docstrings | `*.py`, `*.ts`, `*.js`, `*.go`, `*.swift`, `*.rs`, `*.java`, `*.kt`, `*.rb`, `*.ex` | Language-specific docstring formats |
| Code comments | Same as docstrings | Inline and block comments |
| Commit messages | `git log` output | Use synthetic path `git:commit:<sha>` |
| PR descriptions | GitHub PR body | Use synthetic path `git:pr:<number>` |

### What NOT to Scan

- Generated code (lock files, compiled output, vendor directories)
- Third-party content (copied license text, vendored docs)
- Code itself (variable names, string literals used programmatically)
- Test fixtures and mock data

## Detection Rules

### High-Confidence Signals (Always Flag)

These patterns are strong indicators of AI-generated text:

1. **Chat leaks** — "Certainly!", "I'd be happy to", "Great question!", "Here's" as sentence opener
2. **Cutoff disclaimers** — "As of my last update", "I cannot guarantee"
3. **High-signal AI vocabulary** — delve, utilize (as "use"), whilst, harnessing, paradigm, synergy
4. **"This noun verbs" in docstrings** — "This function calculates", "This method returns"
5. **Synthetic openers** — "In today's fast-paced", "In the world of"
6. **Sycophantic code comments** — "Excellent approach!", "Great implementation!"

### Medium-Confidence Signals (Flag in Context)

Flag when 2+ appear together or pattern is repeated:

1. **Low-signal AI vocabulary clusters** — 3+ words from the low-signal list in one section
2. **Formulaic structure** — Rigid intro-body-conclusion in a README section
3. **Heading restatement** — First sentence after heading restates the heading
4. **Excessive hedging** — "might potentially", "could possibly", "it seems like it may"
5. **Synonym cycling** — Same concept called different names within one section
6. **Boldface overuse** — More than 30% of sentences contain bold text

### Low-Confidence Signals (Note Only)

Mention but don't flag as issues:

1. **Emoji in technical docs** — May be intentional project style
2. **Filler phrases** — Some are common in human writing too
3. **Generic conclusions** — May be appropriate for summary sections
4. **Commit inflation** — Some teams prefer descriptive commits

## False Positive Warnings

Do NOT flag these as AI-generated:

| Pattern | Why It's Valid |
|---------|----------------|
| "Ensure" in security docs | Standard term for security requirements |
| "Comprehensive" in test coverage discussion | Accurate technical descriptor |
| Formal tone in API reference docs | Expected register for reference material |
| "Leverage" in financial/business domain code | Domain-specific meaning, not AI filler |
| Bold formatting in CLI help text | Standard convention |
| Structured intro paragraphs in RFCs/ADRs | Expected format for these document types |
| "This module provides" in Python `__init__.py` | Idiomatic Python module docstring |
| Rhetorical questions in blog posts | Appropriate for informal content |

## Integration

### With `beagle-core:review-verification-protocol`

Before reporting any finding:

1. Read the surrounding context (full paragraph or function)
2. Confirm the pattern is AI-characteristic, not just formal writing
3. Check if the project has established conventions that match the pattern
4. Verify the suggestion improves clarity without changing meaning

### With `beagle-core:llm-artifacts-detection`

Code-level patterns (tautological docstrings, obvious comments) overlap with `llm-artifacts-detection`'s style criteria. When both skills are loaded:

- `review-ai-writing` focuses on **writing style** (how it reads)
- `llm-artifacts-detection` focuses on **code artifacts** (whether it should exist at all)
- If `.beagle/llm-artifacts-review.json` exists, skip findings already captured there

## Output Format

Report each finding as:

```text
[FILE:LINE] ISSUE_TITLE
- Category: content | vocabulary | formatting | communication | filler | code_docs
- Type: specific_pattern_name
- Original: "the problematic text"
- Suggestion: "the improved text" or "delete"
- Risk: Low | Medium
- Fix Safety: Safe | Needs review
```

### Risk Levels

- **Low** — Filler phrases, obvious comments, emoji. Removing improves clarity with no meaning change.
- **Medium** — Vocabulary swaps, structural changes, docstring rewrites. Meaning could shift if done carelessly.

### Fix Safety

- **Safe** — Mechanical replacement or deletion. No judgment needed.
- **Needs review** — Rewrite requires understanding context. Human should verify the replacement preserves intent.
