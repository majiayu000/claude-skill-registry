---
name: optimizing-bash-scripts
description: Analyzes bash scripts for performance bottlenecks, coding standards, and modern tool replacements. Use when optimizing shell scripts, consolidating scripts, or preparing for production. Triggers include "optimize bash", "shellcheck", "script performance", or "consolidate scripts".
allowed-tools: Bash, Read, Edit, Grep, Glob
user-invocable: true
---

# Bash Script Optimizer

Analyze and optimize bash scripts according to strict standards: performance, modern tooling, consolidation patterns.

## Quick Start

**Analyze a script:**

```bash
python3 scripts/analyze.py path/to/script.sh
```

**Optimize workflow:**

1. Run analyzer on target script(s)
1. Review issues by priority: critical → performance → optimization → standards
1. Apply fixes systematically
1. Validate with shellcheck
1. Test functionality
1. Measure improvement

## Core Standards

Scripts must include:

```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar
IFS=$'\n\t' LC_ALL=C
```

**Style:** 2-space indent, minimal blank lines, short CLI args, quoted variables

**Native bash:** arrays, `[[ ]]` tests, parameter expansion, process substitution

**Modern tools (prefer → fallback):**

- fd/fdfind → find
- rg → grep
- sd → sed
- fzf for interactive
- jaq → jq
- choose → cut/awk
- parallel → xargs -P
- gh → git
- aria2/axel → curl → wget

See `references/standards.md` for complete specification.

## Analysis Categories

**Critical:** Must fix (security, correctness)

- Parsing ls output
- Unquoted variables
- eval usage
- Wrong shebang

**Performance:** Significant impact

- Unnecessary cat pipes
- Excessive subshells/forks
- Sequential vs parallel opportunities
- Uncached expensive operations

**Optimization:** Modern alternatives

- find → fd (3-5x faster)
- grep → rg (10x+ faster)
- sed → sd (cleaner syntax)
- Legacy tool replacement opportunities

**Standards:** Code quality

- [ ] vs \[[ ]\]
- echo vs printf
- Indentation (2-space)
- function syntax (prefer `fn(){}`)

## Consolidation Patterns

**When to consolidate multiple scripts:**

- Shared validation/setup logic
- Common function libraries
- Similar workflows with parameter variations
- Reduce maintenance burden

**Unified entry point pattern:**

```bash
mode=${1:-}
case $mode in
  action1) shift; action1_fn "$@";;
  action2) shift; action2_fn "$@";;
  *) die "Usage: $0 {action1|action2}";;
esac
```

**Shared library extraction:**
Extract common functions to `lib/common.sh`, source in scripts.

**Configuration-driven logic:**
Replace script proliferation with data structures (assoc arrays).

See `references/patterns.md` for detailed consolidation strategies.

## Optimization Workflow

### 1. Baseline Analysis

Run analyzer on all target scripts. Prioritize by issue count/severity.

### 2. Quick Wins

- Replace cat pipes: `cat f | grep` → `grep < f`
- Convert tests: `[ ]` → `[[ ]]`
- Quote variables: `$var` → `"$var"`
- Add missing options: `set -euo pipefail`

### 3. Tool Modernization

Replace legacy tools where available:

```bash
# Check availability
command -v fd &>/dev/null && use_fd=1

# Fallback pattern
if [[ $use_fd ]]; then
  fd -tf '\.sh$'
else
  find . -type f -name '*.sh'
fi
```

### 4. Performance Optimization

- **Batch operations:** Collect items, process in parallel
- **Cache results:** Avoid repeated expensive calls
- **Reduce forks:** Use bash builtins vs external commands
- **Process substitution:** `< <(cmd)` vs `cmd |`

### 5. Consolidation

If analyzing multiple related scripts:

- Extract shared functions
- Unify entry points
- Create configuration-driven logic
- Document migration

### 6. Validation

- Shellcheck clean
- Bash execution test
- Functionality verification
- Performance measurement (time, profiling)

## Common Refactorings

**Remove unnecessary subshells:**

```bash
# Before: count=$(cat file | wc -l)
# After: count=$(wc -l < file)
# Better: mapfile -t lines < file; count=${#lines[@]}
```

**Parallel processing:**

```bash
# Before: for f in *.txt; do process "$f"; done
# After: printf '%s\n' *.txt | rust-parallel -j"$(nproc)" process
```

**Parameter expansion over sed:**

```bash
# Before: echo "$file" | sed 's/\.txt$//'
# After: printf '%s\n' "${file%.txt}"
```

**Batch I/O:**

```bash
# Before: while read line; do echo "prefix $line" >> out; done < in
# After:
output=()
while read -r line; do output+=("prefix $line"); done < in
printf '%s\n' "${output[@]}" > out
```

## Token Efficiency

Compress documentation:

- **Cause → effect:** `⇒` notation
- **Lists:** ≤7 items
- **Minimize whitespace:** Prefer compact over verbose

Example:

```bash
# Verbose (44 tokens)
# This function checks if the required tools are available
# in the system PATH and exits with an error if any are missing.
# It takes a list of tool names as arguments.

# Compact (16 tokens)
# Verify required tools exist ⇒ exit if missing
```

## Tips

- Analyze before bulk edits
- Test incrementally, not all at once
- Keep shellcheck clean at each step
- Measure performance impact when optimizing
- Document consolidation rationale
- Maintain fallback chains for tools

## Resources

- `scripts/analyze.py` - Automated script analyzer
- `references/standards.md` - Complete coding standards
- `references/patterns.md` - Optimization patterns and consolidation strategies
