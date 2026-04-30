---
name: explore
description: "Read-only codebase exploration: discovery, structural reading, and emission of architecture/pattern/tooling/dependency summaries. Use whenever the user wants to understand existing code, map files, trace function flow, locate symbols, or build pre-implementation context for a repo-local task. Defers to ODIN's Dispatch-First protocol (1/3/5 Explore-agent escalation). Invoke for any of: \"explore\", \"find where X is\", \"how does X work in the code\", \"map the codebase\", \"what files handle Y\", architecture/pattern/tooling context on a local repo — even without naming /explore."
---

# Explore Command

Read-only codebase orientation. Emit architecture, pattern, tooling, and dependency summaries for a repo-local task. Do NOT write, edit, or commit files.

## When to Apply / NOT

**Apply:**
- Pre-implementation codebase orientation (feature, fix, refactor)
- File and symbol mapping — "where is X defined", "what uses Y"
- Architectural surveys — module boundaries, control flow, coupling
- Dependency tracing — import graphs, transitive deps, config files

**NOT apply:**
- External library docs, SDK APIs, or framework behavior — use a doc-retrieval workflow instead
- User wants a packed repo file as a deliverable artifact
- Implementation, editing, or committing anything

## Process

1. **Scope** — parse the task. Identify files/dirs/concerns. State scope explicitly before dispatching.
2. **Dispatch decision** — for multi-file or uncertain tasks: dispatch Explore agent(s) instead of reading directly. Escalation: 1 agent for single-concern known scope; 3 agents for multiple concerns or unknown scope; 5 agents for cross-module or architectural survey. Auto-skip (direct reads allowed) only for single file under 50 LOC.
3. **Discovery** — token-efficient flags mandatory:
   - File discovery: `fd -e <ext> --max-results 50`
   - Symbol search: `ast-grep run -p 'PATTERN' -l <lang> -C 1` or `git --no-pager grep -n -C 2 'pattern'`
   - Content preview: `bat -P -p -n -r START:END file` or `Read -offset -limit`
   - Directory structure: `eza --tree --level=2`
4. **Synthesis** — emit all Required Output sections. No file writes.
5. **Heavy-codebase escape hatch** — scope > 50 files: use a codebase-packing tool if available as an internal analysis aid (not handed to the user as output); search the packed output for targeted extraction.

## Required Output

Emit all 8 sections. Omit a section only when genuinely not applicable; state why.

### Task Understanding

Brief restatement of the task and identified scope boundaries.

### Architecture Context

```
[Module/Layer Name]
- path/to/file.ts:L10-50 — [Purpose] — [Relevance]
- path/to/interface.ts — [Purpose] — [Relevance]
```

### Pattern Context

```
[Pattern Category]
- path/to/reference.ts — [Pattern description] — [How to apply]
```

### Tooling Context

```
- Build: [command] — [when to run]
- Test: [command] — [scope/coverage]
- Lint: [command] — [config location]
```

### Dependency Map

```
Internal:
- module-a -> module-b (reason)

External:
- library-name@version — [usage context]
```

### Critical Files Summary

Prioritized list of files most relevant to the task:

| Priority | File | Purpose | Action Hint |
|----------|------|---------|-------------|
| P0 | path/to/core.ts | Core logic | Modify |
| P1 | path/to/types.ts | Type definitions | Extend |
| P2 | path/to/utils.ts | Helpers | Reference |

### Constraints & Considerations

- [Constraint 1]: [Impact on implementation]
- [Constraint 2]: [Impact on implementation]

### Recommended Next Steps

1. [First action with specific file reference]
2. [Second action with specific file reference]

## Tool Restrictions

**Allowed (read-only):** `eza`, `fd`, `ast-grep` (find-only), `git grep`, `rg`, `bat`, `tokei`, `Read`, `codebase_search`, and any available codebase-analysis or codebase-packing MCP tooling

**Banned:** `Edit`, `Write`, `mcp__edit__edit_file`, `git commit`, any state-mutating bash command

## Anti-Patterns

- Reading whole files when line ranges suffice — use `bat -r` or `Read -offset -limit`
- Grepping/globbing before dispatching Explore agents on multi-file tasks — dispatch first
- Bypassing token-efficient flags — `bat -P -p -n`, `rg -l`, `fd --max-results 50`
- Re-entering a router or orchestrator skill from within this leaf skill — forbidden (recursion guard)
