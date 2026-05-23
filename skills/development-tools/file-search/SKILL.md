---
name: file-search
description: "Search for files and content in a codebase. Use when investigating a codebase, finding patterns, or locating specific files. Not for reading file content or simple directory listing."
user-invocable: true
---

# File Search

Modern file search using fd, ripgrep (rg), and fzf for large codebases. Hierarchy: ripgrep (90% content search), fd (8% file discovery), fzf (2% interactive selection).

## Tool Selection

**ripgrep** (Primary - 90% of tasks)

- Content search, pattern matching, code analysis
- SIMD optimized, multi-threaded, .gitignore aware
- Recognition: "Know what content to find?" → Use ripgrep

**fd** (Secondary - 8% of tasks)

- File discovery, extension filtering, recent changes
- Simple syntax, colorized output, intuitive
- Recognition: "Need to find files, not content?" → Use fd

**fzf** (Tertiary - 2% of tasks)

- Interactive exploration, manual navigation, preview selection
- Fuzzy matching, preview windows, multi-select
- Recognition: "Need human selection from results?" → Use fzf

**Decision flow:** ripgrep first → add fd if needed → fzf only when interaction is essential.

## ripgrep (Priority 1)

```bash
rg "TODO"                    # Simple search
rg -i "error"                # Case-insensitive
rg -F "exact phrase"         # Literal string (faster, no regex)
```

**By file type:**

```bash
rg -t py "import"            # Python files only
rg -t js -t ts "async"       # JS and TS
rg -t md "ripgrep"           # Markdown files
```

**Context control:**

```bash
rg -C 3 "function"           # 3 lines before/after
rg -B 5 "class"              # 5 lines before
rg -A 2 "return"             # 2 lines after
```

**Output modes:**

```bash
rg -l "TODO"                 # File names only
rg -c "TODO"                 # Count per file
rg -n "pattern"              # Line numbers
rg --json "pattern"          # Structured output (for AI parsing)
```

## fd Integration (Priority 2)

**Find by name:**

```bash
fd config                    # Files containing "config"
fd -e py                     # Python files
fd "test.*\.js$"            # Regex pattern
```

**By type:**

```bash
fd -t f config               # Files only
fd -t d src                  # Directories only
fd -t l                      # Symlinks only
```

**Time-based filters:**

```bash
fd --changed-within 1d       # Modified in last day
fd --changed-before 2024-01-01  # Modified before date
fd --size +10M               # Files larger than 10MB
```

## fzf (Priority 3)

```bash
fd | fzf                     # Find and select
fd | fzf --preview 'bat --color=always {}'
rg -l "pattern" | fzf --preview 'rg -C 3 "pattern" {}'
```

## Combined Workflows

```bash
fd -e py -x rg "async def" {}     # Search Python files for async def
fd -t f -x rg -l "TODO" {}        # Find files with TODO
rg -l "pattern" | fzf --preview 'rg -C 3 "pattern" {}' | xargs vim
```

## Large Codebase Optimization

```bash
# Smart scoping (respects .gitignore automatically)
rg "pattern" --follow --hidden -g '!{.git,node_modules,dist}/**/*'

# Parallel processing
find . -type f -name "*.py" | xargs -P 8 rg "pattern"

# Find large files first
fd -t f -x du -h {} | sort -hr | head -20

# Extract specific line ranges
rg -n "pattern" | head -50          # First 50 matches
rg --json "pattern"                 # JSON output for structured parsing
```

## Quick Reference

| Task                    | Command                                                |
| ----------------------- | ------------------------------------------------------ |
| Content search          | `rg -C 3 "pattern"`                                    |
| Find files with pattern | `rg -l "pattern"`                                      |
| Search by file type     | `rg -t py "pattern"`                                   |
| Case-insensitive        | `rg -i "pattern"`                                      |
| Files by extension      | `fd -e py`                                             |
| Recent files            | `fd --changed-within 1d`                               |
| Interactive selection   | `fd \| fzf`                                            |
| JSON output             | `rg --json "pattern"`                                  |
| Large codebase          | `rg "pattern" --follow -g '!{node_modules,.git}/**/*'` |

## Performance

| Use Case           | ripgrep        | fd        | grep     | find |
| ------------------ | -------------- | --------- | -------- | ---- |
| Content search     | 10-100x faster | N/A       | Baseline | N/A  |
| File by extension  | 5-20x faster   | Fastest   | 1x       | 1x   |
| .gitignore respect | Automatic      | Automatic | No       | No   |
| Multi-threading    | Yes            | No        | No       | No   |
| SIMD optimized     | Yes (NEON)     | Yes       | No       | No   |

**Recognition:** "Need maximum performance on large codebases?" → Use ripgrep with proper flags.

## For Complex Searches

When simple search is insufficient (unknown terminology, too many/too few results), use **iterative-retrieval**:

```
# Basic search (this skill)
rg "authentication"

# Iterative retrieval with progressive refinement
/search "authentication patterns"
```

**iterative-retrieval** provides:

- **4-phase loop**: DISPATCH → EVALUATE → REFINE → LOOP
- **Relevance scoring**: 0-1 score for each file
- **Progressive refinement**: Search query evolves based on results
- **Termination conditions**: Max 3 iterations, 3+ high-relevance files found

**When to use:**

- Initial search returns >20 files (too many)
- Initial search returns <3 files (too few)
- Domain-specific terminology is unknown
- Context gap is unclear

For simple searches: Use this skill (file-search) directly.
For complex searches: Use iterative-retrieval (uses file-search as initial dispatch).

---

<critical_constraint>
MANDATORY: Use ripgrep for content search (90% of tasks)
MANDATORY: Use fd for file discovery (8% of tasks)
MANDATORY: Use fzf only for interactive selection (2% of tasks)
MANDATORY: Prefer resource/accessibility IDs over XPath for element discovery
No exceptions. Correct tool selection prevents wasted effort.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
