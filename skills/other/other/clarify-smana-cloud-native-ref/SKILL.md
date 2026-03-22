---
name: clarify
description: Resolve [NEEDS CLARIFICATION] markers in specs with structured options
allowed-tools: Read, Edit, Glob
---

# Clarify Skill

Resolve `[NEEDS CLARIFICATION: ...]` markers in specification files with structured decision options.

## Usage

```
/clarify                    # Clarify most recent active spec
/clarify docs/specs/001-valkey/spec.md  # Clarify specific spec
```

## Purpose

When filling out a spec, mark uncertain decisions with `[NEEDS CLARIFICATION: question?]`. This skill:

1. Finds all clarification markers in the spec
2. Presents structured options for each question
3. Updates the spec with `[CLARIFIED: answer]` after user decision

## Workflow

### 1. Find Spec File

If no file specified, find the most recently modified active spec:

```bash
find docs/specs -name "spec.md" \
  -not -path "*/done/*" \
  -not -path "*/templates/*" \
  -type f 2>/dev/null | \
  xargs ls -t 2>/dev/null | head -1
```

### 2. Extract Clarification Markers

Find all `[NEEDS CLARIFICATION: ...]` patterns:

```bash
grep -n '\[NEEDS CLARIFICATION:' "$SPEC_FILE"
```

Pattern: `\[NEEDS CLARIFICATION: ([^\]]+)\]`

### 3. Present Structured Options

For each clarification marker, generate 2-3 options based on:
- Platform patterns (existing compositions, conventions)
- Security implications
- Operational considerations
- Common industry practices

**Format for each question**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Q1: [Question from marker]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Context: [Brief analysis of the decision]

  | Option | Answer | Implications |
  |--------|--------|--------------|
  | A | [Suggestion 1] | [Trade-off/consideration] |
  | B | [Suggestion 2] | [Trade-off/consideration] |
  | C | Custom | User provides own answer |

  Recommendation: [A/B] - [Brief rationale]
```

### 4. Update Spec After User Decision

Replace the marker with the clarified answer:

**Before**:
```markdown
- [NEEDS CLARIFICATION: Should cache support cross-namespace access?]
```

**After**:
```markdown
- [CLARIFIED: No, cache is namespace-scoped for security isolation per zero-trust principles]
```

Use the Edit tool to make this replacement.

## Option Generation Guidelines

When generating options, consider:

### Security Perspective
- Zero-trust networking (default deny, explicit allow)
- Least privilege (minimal permissions)
- Secrets management (External Secrets, not hardcoded)
- Network policies (CiliumNetworkPolicy)

### Platform Engineering Perspective
- Consistency with existing compositions (App, SQLInstance)
- Resource naming conventions (`xplane-*` prefix)
- API design patterns
- KCL best practices (no mutation pattern)

### SRE Perspective
- Health checks and observability
- Resource limits and scaling
- Failure modes and recovery
- Operational complexity

### PM Perspective
- User experience simplicity
- Progressive disclosure (simple defaults, advanced options)
- Scope management

## Example Session

**Input spec has**:
```markdown
- [NEEDS CLARIFICATION: What should be the default eviction policy for cache?]
- [NEEDS CLARIFICATION: Should high availability be mandatory or optional?]
```

**Skill presents**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Q1: What should be the default eviction policy for cache?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Context: Eviction policy determines what happens when cache
  memory is full. Common policies: LRU (Least Recently Used),
  LFU (Least Frequently Used), TTL-based.

  | Option | Answer | Implications |
  |--------|--------|--------------|
  | A | LRU (allkeys-lru) | Best for general use, predictable behavior |
  | B | volatile-lru | Only evicts keys with TTL set, safer for persistent data |
  | C | Custom | Specify your own policy |

  Recommendation: A - LRU is the most common default, works well
  for caching scenarios, and is well-understood by operators.

Your choice (A/B/C or custom answer): _
```

**User responds**: "A"

**Skill updates spec**:
```markdown
- [CLARIFIED: LRU (allkeys-lru) - Best for general use, predictable eviction behavior]
```

## Handling Multiple Clarifications

Process clarifications one at a time to maintain focus. After each:
1. Update the spec file
2. Move to next clarification
3. Report progress: "Resolved 2/3 clarifications"

## When All Resolved

```
All clarifications resolved in docs/specs/001-valkey/spec.md

Summary of decisions:
  1. Eviction policy: LRU (allkeys-lru)
  2. High availability: Optional, enabled via ha: true

Next steps:
  - Run ./scripts/validate-spec.sh to verify spec completeness
  - Complete Review Checklist (4 personas)
  - Begin implementation
```

## Related Skills

- `/spec` - Create new specification
- `/spec-status` - View pipeline overview
- `/create-pr` - Create PR when implementation complete
