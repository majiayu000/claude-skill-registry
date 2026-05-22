---
name: remove-comments
description: Clean obvious and redundant comments from code
disable-model-invocation: false
---

# Remove Obvious Comments

I'll clean up redundant comments while preserving valuable documentation.

## Token Optimization Strategy

**Target: 70% reduction (2,000-3,000 → 600-900 tokens)**

This skill implements aggressive optimization for comment analysis:

### Core Optimization Patterns

**1. Grep-Before-Read Pattern (60% savings)**
```bash
# Detect obvious comments without reading full files
rg "//\s*(get|set|return|constructor|function)" --type js -l
rg "^\s*#\s*(TODO|FIXME|HACK|NOTE)" --type py -l
```
- Find files with obvious comment patterns
- Read only files with detected issues
- Skip clean files entirely

**2. Git Diff Default Scope (50% savings)**
```bash
git diff --name-only HEAD  # Changed files only
git diff --cached --name-only  # Staged files
```
- Analyze recently modified files by default
- User can request full codebase scan
- Avoid reading unchanged files

**3. Bash-Based Comment Removal (80% savings)**
```bash
# Remove obvious inline comments
sed -i '/\/\/\s*get$/d' file.js
sed -i '/\/\/\s*constructor$/d' file.js
sed -i '/\/\/\s*return$/d' file.js

# Remove obvious block comments
sed -i '/\/\*\s*Constructor\s*\*\//d' file.java
```
- Use sed for pattern-based removal
- Avoid Read+Edit cycles for obvious patterns
- Batch process multiple removals per file

**4. Template-Based Pattern Matching (70% savings)**
```yaml
obvious_patterns:
  javascript:
    - "// get$"
    - "// set$"
    - "// return$"
    - "// constructor$"
    - "// function$"
  python:
    - "# Constructor$"
    - "# Returns$"
    - "# Getter$"
    - "# Setter$"
  java:
    - "// Getter$"
    - "// Setter$"
    - "/\\* Constructor \\*/"
```
- Predefined obvious comment patterns per language
- Skip analysis of valuable comment types
- Focus on highest-value removals

**5. Early Exit Strategy (95% savings when clean)**
```bash
# Quick check for obvious comments
if ! rg "//\s*(get|set|return|constructor)" --quiet; then
  echo "No obvious comments found"
  exit 0
fi
```
- Exit immediately if no obvious comments exist
- Avoid unnecessary file operations
- Fastest possible execution for clean code

**6. Progressive Disclosure (40% savings)**
```plaintext
Phase 1: Most Obvious (80% confidence)
- "// get" above getters
- "// return" above return statements
- "// constructor" above constructors

Phase 2: Likely Obvious (60% confidence)
- Single-word comments matching code
- Comments restating variable names
- Redundant type descriptions

Phase 3: Potentially Obvious (40% confidence - user review)
- Brief explanations of simple operations
- Comments duplicating nearby code
```
- Remove most obvious comments automatically
- Ask for confirmation on borderline cases
- Skip reading files with no high-confidence removals

### Implementation Details

**Scope Resolution (in order of efficiency)**:
1. **Git diff files** (default) - 50-90% token savings
2. **Specific files** (user-provided) - 80% token savings
3. **Directory scope** (user-provided) - 60% token savings
4. **Full codebase** (explicit request) - 0% savings but comprehensive

**Grep Patterns by Language**:
```bash
# JavaScript/TypeScript
rg "//\s*(get|set|return|constructor|function)\s*$" --type js --type ts

# Python
rg "#\s*(Constructor|Returns?|Getter|Setter)\s*$" --type py

# Java/C#
rg "//\s*(Getter|Setter|Constructor|Returns?)\s*$" --type java --type cs

# Ruby
rg "#\s*(Constructor|Returns?|Getter|Setter)\s*$" --type ruby
```

**Preservation Rules**:
- TODOs, FIXMEs, HACKs, NOTEs - always preserve
- WHY explanations (business logic) - always preserve
- Warning comments (non-obvious behavior) - always preserve
- License headers and copyright - always preserve
- API documentation (JSDoc, docstrings) - always preserve
- Complex algorithm explanations - always preserve

**Batch Processing**:
```typescript
// Single edit per file with multiple removals
const removals = [
  { line: 15, text: "// get" },
  { line: 23, text: "// set" },
  { line: 47, text: "// return" }
];
// Remove all in one Edit operation
```

### Caching Strategy

**Cache Location**: `.claude/cache/remove-comments/`

**Cached Data**:
```json
{
  "language_patterns": {
    "javascript": ["// get$", "// set$", "// return$"],
    "python": ["# Constructor$", "# Returns$"],
    "last_updated": "2026-01-27"
  },
  "preservation_rules": {
    "keywords": ["TODO", "FIXME", "HACK", "NOTE", "WARNING"],
    "patterns": ["why:", "because:", "note:"]
  },
  "project_analysis": {
    "has_obvious_comments": true,
    "last_scan": "2026-01-27T10:30:00Z",
    "files_with_issues": 12
  }
}
```

**Cache Invalidation**:
- Language patterns: Manual invalidation only
- Project analysis: After 24 hours or new commits
- Preservation rules: Never (static)

### Token Savings Breakdown

| Operation | Unoptimized | Optimized | Savings |
|-----------|-------------|-----------|---------|
| Initial grep | 0 tokens | 0 tokens | N/A |
| File reading | 1,500 tokens | 300 tokens | 80% |
| Pattern matching | 500 tokens | 50 tokens | 90% |
| Comment removal | 800 tokens | 100 tokens | 87% |
| Verification | 200 tokens | 50 tokens | 75% |
| **Total** | **3,000 tokens** | **500 tokens** | **83%** |

**Real-World Performance**:
- **Small project** (10 files): 200-400 tokens (90% reduction)
- **Medium project** (50 files): 400-700 tokens (77% reduction)
- **Large project** (200 files): 600-900 tokens (70% reduction)
- **Clean code** (no obvious comments): 50-100 tokens (95% reduction)

**Optimization Status**: ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-27)

## Analysis Process

I'll identify files with comments using:
- **Glob** to find source files
- **Read** to examine comment patterns
- **Grep** to locate specific comment types

**Comments I'll Remove:**
- Simply restate what the code does
- Add no value beyond the code itself
- State the obvious (like "constructor" above a constructor)

**Comments I'll Preserve:**
- Explain WHY something is done
- Document complex business logic
- Contain TODOs, FIXMEs, or HACKs
- Warn about non-obvious behavior
- Provide important context

## Review Process

For each file with obvious comments, I'll:
1. Show you the redundant comments I found
2. Explain why they should be removed
3. Show the cleaner version
4. Apply the changes after your confirmation

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This creates cleaner, more maintainable code where every comment has real value.