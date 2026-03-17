---
name: progressive-disclosure
description: Template and guide for restructuring large documentation files into token-efficient directory structures. Reduces context bloat by 40-60% while maintaining accessibility.
---

# Progressive Disclosure for Documentation

A pattern for restructuring large documentation files into slim indexes with on-demand subdirectories, reducing always-included context by 40-60%.

## Problem

Large documentation files (500+ lines, 5k+ tokens) that are always included in context:
- Waste context budget on rarely-needed content
- Slow down response times
- Crowd out more relevant information
- Create cognitive overload

## Solution

Split monolithic docs into:
1. **Slim index** (~20% of original) - Always included, provides overview + navigation
2. **Detail directories** - On-demand loading when specific topics needed

## Structure

```txt
Before:
  TOOLS.md (~11k tokens always included)
  ├── Section 1 (rarely needed)
  ├── Section 2 (rarely needed)
  ├── ... (15+ sections)
  └── Section N (rarely needed)

After:
  tools/
  ├── README.md (~4k tokens always included)  # Slim index
  ├── topic1/README.md   # Detailed docs (~1k tokens each)
  ├── topic2/README.md   # Loaded on-demand
  └── .../README.md      # etc.
```

## When to Use

**Good candidates for progressive disclosure:**
- Files > 500 lines or 5k tokens
- Files always included in context (via gptme.toml or similar)
- Files with distinct sections that are rarely needed together
- Documentation with both overview and detailed reference content

**Keep as single file when:**
- File is < 200 lines
- Content is frequently needed together
- Structure is already lean
- Users commonly need complete view

## Implementation Guide

### Step 1: Analyze Current Structure

Count tokens and identify sections:

```bash
# Count lines and estimate tokens
wc -l LARGE_FILE.md
# Rough: 1 line ≈ 8 tokens

# Identify sections (look for ## headers)
grep "^## " LARGE_FILE.md | head -20
```

### Step 2: Create Directory Structure

```bash
# Create topic directories
mkdir -p topic_dir/{topic1,topic2,topic3}
```

### Step 3: Write Slim Index (README.md)

The index should contain:
- Brief overview (2-3 paragraphs max)
- Quick reference/cheatsheet (most common operations)
- Navigation links to detailed docs
- When to read which section

**Example slim index structure:**

```txt
# Topic Name

Brief overview of what this covers and core concepts.

## Quick Reference

| Command | Description |
|---------|-------------|
| cmd1    | Most common operation |
| cmd2    | Second most common |
| cmd3    | Third most common |

## Detailed Documentation

For specific topics, see:

- **Topic 1** (topic1/README.md) - When you need X
- **Topic 2** (topic2/README.md) - When you need Y
- **Topic 3** (topic3/README.md) - When you need Z

## Principles

1. Core principle 1
2. Core principle 2
3. Core principle 3
```

### Step 4: Create Detail Files

Each topic README should:
- Be self-contained for its topic
- Include examples and use cases
- Cross-reference related topics
- Stay under ~200 lines (~1.5k tokens)

### Step 5: Update Configuration

Update gptme.toml (or equivalent) to include the slim index:

```toml
[context]
# Before: included entire large file
# files = ["LARGE_FILE.md"]

# After: include only slim index
files = ["topic_dir/README.md"]
```

## Example: TOOLS.md Migration

**Before:**
- `TOOLS.md`: 1380 lines, ~11k tokens, always included
- 15+ sections covering shell, git, github, context, etc.

**After:**
- `tools/README.md`: 200 lines, ~1.5k tokens (slim index)
- `tools/{shell,git,github,context,...}/README.md`: ~150 lines each
- Agent reads detailed docs only when working on specific topics

**Result:** 44% reduction in always-included context

## Benefits

1. **Token Efficiency**: 40-60% reduction in always-included tokens
2. **Faster Responses**: Less context to process
3. **Better Focus**: Agent sees relevant content when needed
4. **Maintainability**: Smaller files easier to update
5. **Claude-Style Organization**: Similar to Anthropic's skill folders

## Anti-patterns to Avoid

1. **Too many small files**: Don't split into 50+ tiny files
2. **Deep nesting**: Keep to 2 levels max (index + details)
3. **Orphan content**: Ensure all detail files linked from index
4. **Missing quick reference**: Index must have actionable content
5. **Over-splitting**: Some content should stay together

## Related

- [Issue #49](https://github.com/gptme/gptme-contrib/issues/49) - Original proposal
