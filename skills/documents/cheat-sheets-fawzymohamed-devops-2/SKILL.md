---
name: cheat-sheets
description: Expert knowledge for creating effective cheat sheets with PDF export. Activate when creating/editing cheat sheet content, designing quick reference sheets, or working with PDF export functionality. (project)
globs:
  - "content/**/*cheat-sheet*.md"
  - "app/components/CheatSheet*.vue"
  - "app/composables/useCheatSheetPdf.ts"
---

# Cheat Sheet Authoring Skill

Expert knowledge for creating effective, scannable quick reference sheets for the DevOps LMS.

## Cheat Sheet Philosophy

Cheat sheets are NOT lesson summaries. They are **reference tools** designed for:
- Quick lookup during work
- Memory reinforcement after learning
- Print-and-post desk references

## File Structure

### Location & Naming
- **Path**: `content/{phase}/{topic}/99.cheat-sheet.md`
- **URL**: `/phase-1-sdlc/sdlc-models/cheat-sheet`
- The `99.` prefix ensures it appears last in navigation

### Required Frontmatter

```yaml
---
title: "SDLC Models - Quick Reference"
description: "Key concepts, comparisons, and decision guides for SDLC models"
estimatedMinutes: 5
difficulty: beginner  # Match the topic's average difficulty
learningObjectives:
  - "Quick reference for all SDLC model concepts"
isCheatSheet: true
cheatSheetTopic: "SDLC Models"
---
```

**Required fields:**
- `isCheatSheet: true` - Triggers cheat sheet layout and PDF export
- `cheatSheetTopic` - Human-readable topic name for PDF metadata

## Content Structure Templates

### Template 1: Concept Comparison (Best for methodology topics)

```markdown
## Key Terminology

| Term | Definition |
|------|------------|
| Term 1 | Brief, clear definition |
| Term 2 | Brief, clear definition |

## Quick Comparison

| Aspect | Option A | Option B | Option C |
|--------|----------|----------|----------|
| Best For | Use case | Use case | Use case |
| Team Size | Small | Medium | Large |
| Flexibility | High | Medium | Low |

## Decision Guide

**Choose A when:**
- Condition 1
- Condition 2

**Choose B when:**
- Condition 1
- Condition 2
```

### Template 2: Command Reference (Best for tool topics)

```markdown
## Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `cmd1` | What it does | `cmd1 --flag value` |
| `cmd2` | What it does | `cmd2 arg1 arg2` |

## Common Patterns

### Pattern Name
```bash
# Step 1: Description
command1

# Step 2: Description
command2 --flag
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| Error message | Why it happens | How to fix |
```

### Template 3: Process Reference (Best for workflow topics)

```markdown
## Process Overview

> **Quick Summary:** Brief 1-sentence description of the overall process flow.

## Step-by-Step Quick Reference

### Step 1: Name
- Key action 1
- Key action 2
- **Output**: What this produces

### Step 2: Name
- Key action 1
- Key action 2
- **Output**: What this produces

## Best Practices Checklist

- [ ] Practice 1
- [ ] Practice 2
- [ ] Practice 3
```

## Critical Rules

### No Illustrations in Cheat Sheets

**IMPORTANT:** Cheat sheets must NEVER contain illustrations (MDC components like `IllustrationLinearFlow`, `IllustrationChecklist`, `IllustrationPyramid`, etc.).

**Why:**
- Cheat sheets are designed for **quick scanning and reference**
- Illustrations add visual complexity that slows down lookup
- PDF export is optimized for text and tables, not complex SVGs
- Keep cheat sheets pure text/tables for maximum portability

**Instead of illustrations, use:**
- Tables for comparisons and structured data
- Numbered lists for sequential steps
- Blockquotes for process summaries
- Code blocks for command sequences

### Interview Quick Hits Required

**IMPORTANT:** Every cheat sheet MUST include an "Interview Quick Hits" section containing common interview questions and concise answers for the topic.

**Placement:** Near the end of the cheat sheet, before any "Common Pitfalls" or "Troubleshooting" section.

**Format:**
```markdown
## Interview Quick Hits

| Question | Answer |
|----------|--------|
| What is X? | Concise 1-2 sentence answer |
| When would you use Y? | Brief explanation with context |
| What's the difference between A and B? | Key distinctions in simple terms |
| Why is Z important? | Business/technical value in brief |
```

**Guidelines:**
- Include 4-8 questions per cheat sheet
- Focus on questions commonly asked in technical interviews
- Keep answers concise (1-3 sentences max)
- Cover fundamentals, comparisons, and "why" questions
- Tailor questions to the topic type (concept, tool, or workflow)

## Writing Guidelines

### Content Density

| Do | Don't |
|----|-------|
| Tables for comparisons | Paragraphs of text |
| Bullet points for lists | Long explanations |
| Code blocks for commands | Inline code for everything |
| Short, scannable sections | Wall of text |

### Table Best Practices

```markdown
<!-- GOOD: Clear headers, aligned columns -->
| Model | Speed | Quality |
|-------|-------|---------|
| A     | Fast  | Medium  |
| B     | Slow  | High    |

<!-- BAD: Too wide, too much text -->
| Model | Description and full explanation of when to use this model |
|-------|-----------------------------------------------------------|
```

### Code Block Formatting

```markdown
<!-- GOOD: Short, focused examples -->
```bash
git checkout -b feature/name
```

<!-- BAD: Full scripts or tutorials -->
```bash
# First you need to...
# Then you should...
# After that...
```
```

### Visual Hierarchy

1. **H2 (`##`)** for major sections
2. **H3 (`###`)** for subsections
3. **Bold** for key terms in lists
4. **Code** for commands, paths, values
5. Tables for structured data

## PDF Export Considerations

### Page Break Awareness
- Keep related content together
- Tables may break across pages - keep them concise
- Test export with `Download PDF` button

### Print Readability
- Sufficient contrast (dark text on light)
- Readable font sizes (no tiny text)
- Logical reading flow

### Content Length
- Aim for 1-3 printed pages
- More is NOT better for reference sheets
- If too long, split by subtopic

## Quality Checklist

Before finalizing a cheat sheet:

- [ ] `isCheatSheet: true` in frontmatter
- [ ] `cheatSheetTopic` matches topic name
- [ ] **No illustrations** (no MDC illustration components)
- [ ] **Interview Quick Hits section included** (4-8 Q&A pairs)
- [ ] Scannable in under 30 seconds
- [ ] Tables used for comparisons
- [ ] No paragraphs longer than 2 sentences
- [ ] Code examples are copy-pasteable
- [ ] PDF export tested and readable
- [ ] No quiz section (cheat sheets don't have quizzes)
- [ ] Difficulty set appropriately

## Example: Complete Cheat Sheet

```markdown
---
title: "Git Branching - Quick Reference"
description: "Essential Git branching commands and strategies"
estimatedMinutes: 5
difficulty: beginner
learningObjectives:
  - "Quick reference for Git branching operations"
isCheatSheet: true
cheatSheetTopic: "Git Branching"
---

## Essential Commands

| Command | Purpose |
|---------|---------|
| `git branch` | List branches |
| `git branch name` | Create branch |
| `git checkout name` | Switch branch |
| `git checkout -b name` | Create and switch |
| `git merge name` | Merge branch |
| `git branch -d name` | Delete branch |

## Branching Strategies

| Strategy | Best For | Complexity |
|----------|----------|------------|
| GitHub Flow | Small teams | Low |
| GitFlow | Release cycles | High |
| Trunk-based | CI/CD heavy | Medium |

## Quick Patterns

### Feature Branch
```bash
git checkout -b feature/name
# ... work ...
git push -u origin feature/name
```

### Hotfix
```bash
git checkout -b hotfix/name main
# ... fix ...
git checkout main && git merge hotfix/name
```

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Working on main | Always branch first |
| Forgetting to pull | `git pull` before branch |
| Long-lived branches | Merge frequently |

## Interview Quick Hits

| Question | Answer |
|----------|--------|
| What is a branch in Git? | A lightweight pointer to a commit that allows parallel development without affecting the main codebase |
| What's the difference between `git merge` and `git rebase`? | Merge preserves history with a merge commit; rebase replays commits for a linear history |
| When would you use feature branches? | When developing new features in isolation to avoid breaking the main branch |
| How do you resolve a merge conflict? | Edit the conflicted files to choose the correct changes, then stage and commit |
```

## Components Reference

### CheatSheetLayout.vue
- Renders cheat sheet content with reference-style layout
- Includes PDF download button
- No "Mark Complete" button
- Uses `#cheat-sheet-content` ID for PDF capture

### CheatSheetPdfButton.vue
- Download button with loading state
- Error display if PDF generation fails

### useCheatSheetPdf.ts
- `downloadCheatSheet(title, slug)` - Generate and download PDF
- `isGenerating` - Loading state
- `error` - Error message if failed
