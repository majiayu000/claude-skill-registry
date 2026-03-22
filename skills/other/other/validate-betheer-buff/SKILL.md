---
name: buff-validate
description: This skill should be used when the user asks to "validate the code", "check code quality", "run /buff:validate", "review for issues", "find bugs", "check for security issues", "lint the code", "check complexity", "validate the project", "run project-wide validation", "quick validate", "validate session changes", "check cross-file coherence", "show quality trend", or any request for high-sensitivity code quality analysis. Supports project-wide scanning, --quick (graph-guided), --session (session-modified files only), and cross-file coherence analysis with quality trending. Also auto-invoked by /buff:execute as part of the dev loop.
version: 0.2.0
argument-hint: "[file or directory] [--fix] [--high-only] [--quick] [--session]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# buff-validate v2

Project-wide quality engine with cross-file coherence and trending. Performs high-sensitivity static analysis across five dimensions: correctness, security, complexity, style, and coherence. Reports findings with severity and actionable fixes. Never a blunt "rewrite everything" — precise, targeted, ranked.

## Analysis dimensions

### 1. Correctness
Bugs, logic errors, and runtime risks:
- Null/undefined access without guards
- Off-by-one errors in loops and array access
- Unhandled async errors (missing await, unhandled Promise rejection)
- Incorrect comparison operators (`==` vs `===`, `is` vs `==` in Python)
- Type mismatches at function boundaries
- Missing return statements in non-void functions
- Race conditions in async code

### 2. Security
OWASP-aligned security checks:
- SQL injection via string concatenation
- XSS via unsanitized innerHTML or dangerouslySetInnerHTML
- Hardcoded secrets, API keys, passwords in source
- Unvalidated user input reaching filesystem, shell, or database
- Insecure deserialization
- Missing authentication/authorization checks on routes
- Sensitive data logged to console

### 3. Complexity
Maintainability signals:
- Functions > 50 lines (split candidates)
- Cyclomatic complexity > 10 (too many branches)
- Nesting depth > 4 levels (extract logic)
- Files > 300 lines (split candidates)
- Duplicated logic (3+ similar blocks = extract function)
- Parameter lists > 5 arguments (use object/struct)

### 4. Style
Consistency and clarity:
- Naming violations (detected vs. project convention from Counterfeit)
- Dead code (unreachable branches, unused variables/imports)
- Magic numbers/strings without named constants
- Inconsistent error handling patterns within the same file

### 5. Coherence
Cross-file analysis — structural integrity across the project:

| Signal | Detection | Severity |
|---|---|---|
| Broken imports — import from module that doesn't export symbol | `graph.json` cross-reference | HIGH |
| Circular dependencies — A→B→C→A | `graph.json` import chain | MED |
| Inconsistent interfaces — same concept named differently | Grep for similar patterns | MED |
| Orphaned exports — exported but never imported | `graph.json` exports vs imports | LOW |
| Architectural layer violation — import breaks decided architecture | `decisions.json` + `graph.json` | MED |
| Stale tests — source exports changed but test file unchanged | `graph.json` coverage data | MED |

## Scope resolution

| Invocation | Scope |
|---|---|
| `/buff:validate` | Project-wide scan (all source files) |
| `/buff:validate src/auth.ts` | Single file |
| `/buff:validate src/` | All files in directory |
| `/buff:validate --session` | All files modified in current session (`.buff/session.log`) |
| `/buff:validate --quick` | Graph-guided smart scan (changed files + dependents) |
| `/buff:validate --high-only` | Report only high-severity findings |
| `/buff:validate --fix` | Report + auto-fix high-severity findings |

Flags combine: `/buff:validate src/ --fix --high-only` scans directory, fixes only high findings.

## `--quick` mode

Graph-guided smart scan. Uses `graph.json` to prioritize what to scan:

1. **Changed files** — files changed since last validate (`git diff`)
2. **Dependents of changed files** — from `graph.json` `imported_by` fields
3. **Files with prior HIGH findings** — from `learnings.json` past scan results
4. **High-complexity files** — from `graph.json` lines count

Skip unchanged, no-dependent, recently-clean files. Cuts scan time 60-80% while catching the findings that matter. Ideal for mid-session checks.

## Counterfeit pre-read

Before scanning, read these files to inform analysis:

- `~/.buff/memory/patterns.json` — known issue patterns (avoid false positives, catch known-bad patterns)
- `~/.buff/memory/corrections.json` — past mistakes (what was flagged incorrectly before, what was missed)
- `.buff/memory/graph.json` — structural data for coherence checks (imports, exports, dependency chains)

If any file is missing or empty, skip it silently — never fail on missing counterfeit data.

## Workflow

1. **Pre-read counterfeit** — load patterns, corrections, graph data
2. **Determine scope** — project-wide (default), file, directory, `--session`, or `--quick`
3. **Read each file in scope**
4. **Run analysis across all five dimensions** (coherence only runs when graph.json exists)
5. **Rank findings by severity**
6. **Report findings table**
7. **Write scan results to counterfeit** (learnings.json)
8. If `--fix` flag: apply fixes for high-severity findings automatically

## Quality trending

After each scan, write a scan record to `.buff/memory/learnings.json`:

```json
{
  "type": "validate_scan",
  "date": "2026-03-21",
  "scope": "project-wide",
  "findings": { "high": 0, "med": 3, "low": 7 },
  "coherence": { "broken_imports": 0, "circular_deps": 1, "orphaned_exports": 4 },
  "trend": "improving"
}
```

**Trend calculation:** Compare current scan to the last 3 scans in learnings.json:
- **improving** — high findings decreased or total findings decreased by 20%+
- **stable** — findings within 10% of previous average
- **degrading** — high findings increased or total findings increased by 20%+

If no prior scans exist, trend = `"baseline"`.

## Output format

```
## Validation — [scope] · [N files, N lines analyzed]

| File | Line | Dimension | Severity | Finding | Fix |
|---|---|---|---|---|---|
| auth.ts | L42 | Security | HIGH | Raw SQL string concat | Use parameterized query |
| auth.ts | L87 | Correctness | HIGH | Missing await on async call | Add await |
| router.ts | L12 | Complexity | MED | Function is 73 lines | Extract validatePermissions() |
| — | — | Coherence | MED | Circular dep: auth→db→auth | Break cycle via interface |
| utils.ts | L5 | Style | LOW | Unused import 'path' | Remove import |
| — | — | Coherence | LOW | 4 orphaned exports | Remove or document intent |

Summary: 2 high · 1 medium · 3 low
Trend: improving (was 3 high · 2 med · 5 low last scan)
Coherence: 1 circular deps · 4 orphaned exports
Auto-fixable: 1 of 2 high findings
```

Always sort: HIGH first, then MED, then LOW. Within each level, sort by file then line. Coherence findings (no specific line) go at the end of their severity group.

## Auto-fix behavior (`--fix`)

Apply fixes only for:
- Unused imports — remove
- Dead code — remove
- Missing `await` on clearly async calls — add
- Hardcoded magic numbers with obvious names — extract to const

Never auto-fix:
- Security findings (require understanding of data flow — show fix, don't apply)
- Complex refactors
- Anything that changes behavior, not just style
- Coherence findings (require architectural decisions)

For every auto-fix applied, print:
```
Fixed: [file]:[line] — [what was fixed]
```

## Integration with buff loop

When called from `/buff:execute` (validate phase):
- Scope = all files in `.buff/session.log` modified this session
- High findings block the execute loop — must be resolved before commit
- Med/low findings are reported but do not block
- Results appended to `.buff/session.log`

## Severity definitions

| Severity | Definition | Action |
|---|---|---|
| HIGH | Bug, security issue, data loss risk, crash path | Fix before commit |
| MED | Performance issue, missing error handling, complexity warning | Fix or document decision |
| LOW | Style inconsistency, minor naming, optional improvement | Fix at discretion |

## Writes to counterfeit

After scanning, write results to counterfeit memory:

- **Scan results** → `.buff/memory/learnings.json` — full scan record with findings counts, coherence stats, and trend
- **Recurring patterns** → `~/.buff/memory/corrections.json` — if a pattern appears 3+ times across scans, record it as a generalizable correction
- **File stats** → `.buff/memory/graph.json` — update file-level stats (lines, complexity, last-validated timestamp)

## Correction detection

Watch for the user disagreeing with findings (rejection, replacement, redirect). Follow the correction capture mechanism defined in `counterfeit` SKILL.md — detect signals, record to `learnings.json` + `corrections.json`, promote to `patterns.json` at 2+ occurrences. Use `skill: "validate"` when writing correction entries. Learn from corrections to reduce false positives over time.
