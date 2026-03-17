---
name: architect
description: Architectural refactoring - analyze codebase structure, detect architectural smells (god modules, circular deps, coupling), propose restructuring plan, safely move/rename files with git history, update imports, simplify architecture. Use when asked to "restructure", "reorganize", "simplify architecture", "move files", "split module", "fix structure", "reduce coupling", "reorganize folders", "clean up architecture", "refactor structure", "restructurer", "reorganiser", "simplifier".
argument-hint: "[-a] [-e] [-s] <scope or description>"
---

<objective>
Analyze codebase architecture, detect structural smells, and safely restructure code while preserving git history and updating all imports.
</objective>

<quick_start>
**Restructure a specific area:**
```bash
/architect src/components
```

**Full codebase audit + restructure:**
```bash
/architect -a full codebase restructure
```

**Audit only (no changes):**
```bash
/architect -s audit auth module
```

**What it does:**
1. AUDIT: Scans structure, detects architectural smells (god modules, circular deps, coupling)
2. DESIGN: Proposes restructuring plan with file moves, splits, renames
3. RESTRUCTURE: Executes safely with `git mv`, import migration, incremental commits
4. VERIFY: Build, tests, import validation
</quick_start>

<parameters>

| Flag | Description |
|------|-------------|
| `-a` | Auto mode: skip confirmations, execute full workflow |
| `-e` | Economy mode: no subagents, direct tools only |
| `-s` | Save mode: output to `.claude/output/architect/` |
| `--audit-only` | Stop after audit step (no restructuring) |
| `--dry-run` | Show proposed changes without executing |
| `--standalone` | Use built-in RESTRUCTURE + VERIFY instead of APEX handoff |

<examples>
```bash
/architect src/components              # Audit + design → APEX handoff
/architect -a reorganize api layer     # Auto mode
/architect -e simplify auth module     # Economy mode
/architect -s --audit-only src/        # Audit and save report
/architect --dry-run split user module # Preview changes
/architect --standalone src/components # Built-in restructure + verify
```
</examples>

</parameters>

<workflow>
```
DEFAULT:      AUDIT → DESIGN → HANDOFF (saves design context, suggests /apex)
--standalone: AUDIT → DESIGN → RESTRUCTURE → VERIFY

AUDIT    ─ Detect smells, map dependencies, measure complexity
DESIGN   ─ Propose structure, file moves, module splits
HANDOFF  ─ Save design context file, offer APEX implementation
RESTRUCTURE ─ git mv, update imports, incremental commits (--standalone)
VERIFY   ─ Build, test, import validation (--standalone)
```
</workflow>

<state_variables>

| Variable | Type | Description |
|----------|------|-------------|
| `{scope}` | string | Target area to restructure |
| `{task_id}` | string | Kebab-case identifier |
| `{auto_mode}` | boolean | Skip confirmations |
| `{economy_mode}` | boolean | No subagents |
| `{save_mode}` | boolean | Save outputs |
| `{audit_only}` | boolean | Stop after audit |
| `{dry_run}` | boolean | Preview only |
| `{standalone_mode}` | boolean | Use built-in restructure + verify |
| `{smells}` | array | Detected architectural smells |
| `{dependency_map}` | object | File dependency graph |
| `{move_plan}` | array | Planned file operations |

</state_variables>

<reference_files>

| File | When Loaded |
|------|-------------|
| `references/architecture-smells.md` | Always (step-01) |
| `references/architecture-patterns.md` | Step-02 (design phase) |
| `references/restructuring-techniques.md` | Step-03 (execution phase) |

</reference_files>

<entry_point>

Load `steps/step-01-audit.md`

</entry_point>

<step_files>

| Step | File | Purpose |
|------|------|---------|
| 01 | `step-01-audit.md` | Structure analysis + smell detection |
| 02 | `step-02-design.md` | Restructuring plan |
| 03 | `step-03-handoff.md` | Save design context + offer APEX (default) |
| 03-alt | `step-03-restructure.md` | Safe execution (`--standalone` only) |
| 04-alt | `step-04-verify.md` | Build + validation (`--standalone` only) |

</step_files>

<execution_rules>
- Load one step at a time
- NEVER move files without reading them first
- ALWAYS use `git mv` to preserve history
- ALWAYS update imports after every move
- Use parallel agents in step-01 and step-03 (unless economy mode)
- Incremental commits after each logical group of changes
- Build must pass before marking complete
</execution_rules>

<success_criteria>
- Architectural smells correctly identified
- Dependency map accurately captures relationships
- Restructuring plan approved before execution
- All file moves use `git mv` (history preserved)
- All imports updated across codebase
- No circular dependencies introduced
- Build passes without errors
- Tests pass (if tests exist)
- Cleaner, simpler structure achieved
</success_criteria>
