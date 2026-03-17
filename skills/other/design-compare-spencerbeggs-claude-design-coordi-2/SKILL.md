---
name: design-compare
description: Compare doc versions across git history. Use when reviewing changes, tracking evolution, or understanding modifications.
allowed-tools: Read, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Version Comparison

Compares design document versions across git commits, branches, or tags to
track evolution and understand changes over time.

## Overview

This skill compares document versions by validating git references, loading
document content from different versions, performing line-by-line or
semantic diffs, analyzing changes for significance, and generating
comprehensive comparison reports with metrics and highlights.

## Quick Start

**Compare with main branch:**

```bash
/design-compare observability.md --ref=main
```

**Compare two commits:**

```bash
/design-compare doc.md --from=abc123 --to=def456
```

**Semantic comparison:**

```bash
/design-compare doc.md --ref=v1.0.0 --format=semantic
```

## Parameters

### Required

- `doc`: Document filename to compare

### Optional

- `module`: Module name (default: inferred from current context)
- `ref`: Git reference to compare against (commit, branch, tag) (default: main)
- `from`: Starting git reference for two-point comparison
- `to`: Ending git reference for two-point comparison
- `format`: Comparison format - unified, side-by-side, semantic, summary
  (default: unified)

## Workflow

High-level comparison process:

1. **Parse parameters** to determine document and comparison references
2. **Validate references** to ensure git refs exist and are accessible
3. **Load document versions** from current and historical git refs
4. **Perform comparison** using diff (unified, side-by-side) or semantic
   analysis
5. **Analyze changes** to extract metrics and categorize modifications
6. **Generate comparison report** with summary, frontmatter changes,
   structural changes, and content diff
7. **Highlight significant changes** (status changes, completeness jumps,
   major additions/removals)
8. **Format output** according to requested format
9. **Provide navigation** with git commands for further exploration

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step comparison workflow
- Git reference validation methods
- Document version loading from git
- Diff execution (line-by-line, side-by-side, semantic)
- Change analysis and metrics calculation
- Comparison report generation
- Significant change highlighting
- Git navigation commands
- Comparison modes (single ref, two refs, branch, tag)
- Advanced features (whitespace, context, word-level, stats)

**Load when:** Performing comparisons or need implementation details

### For Comparison Formats

See [comparison-formats.md](comparison-formats.md) for:

- Unified diff format and syntax
- Side-by-side comparison layout
- Semantic diff structure
- Summary format
- Format selection guidelines
- Color coding and highlighting

**Load when:** Need format specifications or output structure details

### For Usage Examples

See [examples.md](examples.md) for:

- Compare with main branch
- Compare two commits
- Semantic comparison
- No changes scenario
- Document doesn't exist in reference
- Error scenarios

**Load when:** User needs examples or clarification

## Error Handling

### Invalid Git Reference

```text
ERROR: Git reference not found: {ref}

Valid references:
- Commit hash: abc123
- Branch name: main, feature-branch
- Tag name: v1.0.0

Check: git log or git branch -a
```

### Document Not in Repository

```text
ERROR: Document not tracked by git

Document: {doc}

Ensure document is committed before comparing versions.
```

### No Changes Detected

```text
INFO: No changes between versions

Document: {module}/{doc}
References: {from} → {to}

The document is identical in both versions.
```

## Integration

Works well with:

- `/design-review` - Review documents before/after changes
- `/design-validate` - Validate both versions
- `/design-sync` - Understand sync evolution over time
- `/design-update` - See update history

## Success Criteria

A successful comparison:

- ✅ Git references validated
- ✅ Document versions loaded from both refs
- ✅ Diff performed successfully
- ✅ Changes analyzed and categorized
- ✅ Metrics calculated accurately
- ✅ Significant changes highlighted
- ✅ Clear comparison report generated
- ✅ Navigation commands provided
