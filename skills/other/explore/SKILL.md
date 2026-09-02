---
name: explore
description: 'Use when asked to explore the codebase to map structure, symbols, and dependencies. Produces a structured orientation report with architecture, pattern, tooling, dependency, and critical-file sections.'
---

# Explore

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User says "explore", "find where X is", "how does X work in the code", or "map the codebase" for repo-local orientation. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | A structured orientation report in chat; may dispatch Explore subagents. No state mutation. |
| Done | All 8 output sections emitted or applicability stated, scope declared, and dispatch/escalation rules followed. |

## Inputs

- Task text (supplied): the orientation question or concern to map.
- Repo working tree (supplied by environment): read-only access to the local checkout.
- Optional: specific files, directories, or concerns used to bound scope before dispatch.

## Procedure

1. **Scope.** Parse the task; identify the files, directories, and concerns in scope. State the scope explicitly before any dispatch or read. Done when: the scope is stated explicitly before any dispatch or read.
2. **Dispatch decision.** For multi-file or uncertain tasks, dispatch Explore subagents instead of reading directly. Escalation: 1 subagent for a single-concern known scope; 3 subagents for multiple concerns or unknown scope; 5 subagents for a cross-module or architectural survey. Auto-skip (direct reads allowed) only for a single file under 50 LOC. Dispatch first; do not grep or glob a multi-file task before dispatching. Done when: the dispatch decision is made with the correct escalation tier, or direct reads are selected for a single file under 50 LOC.
3. **Discovery with token-efficient flags.** File discovery: `fd -e <ext> --max-results 50`. Symbol search: `ast-grep run -p 'PATTERN' -l <lang> -C 1` or `git --no-pager grep -n -C 2 'pattern'`. Content preview: `bat -P -p -n -r START:END file` or read with offset/limit. Directory structure: `eza --tree --level=2`. Done when: discovery is completed using token-efficient flags.
4. **Synthesis.** Emit all 8 output sections below. Omit a section only when genuinely not applicable and state why. Done when: all 8 output sections are emitted or omitted with a stated reason.
5. **Heavy-codebase escape hatch.** When scope exceeds 50 files, use a codebase-packing tool only as an internal analysis aid; never give packed output to the user. Search the packed output for targeted extraction. If no packing tool is available, narrow scope and state the narrowing. Done when: the heavy-codebase escape hatch is applied or scope is narrowed with a stated reason.
6. **Tool restrictions.** Allowed (read-only): `eza`, `fd`, `ast-grep` (find-only), `git grep`, `rg`, `bat`, `tokei`, `Read`, `codebase_search`, and any available codebase-analysis or codebase-packing MCP tooling. Banned: `Edit`, `Write`, `mcp__edit__edit_file`, `git commit`, and any state-mutating bash command. Done when: only allowed tools are used and no banned tool is invoked.
7. **Recursion guard.** Do not re-enter a router or orchestrator skill from within this leaf skill. Done when: no router or orchestrator skill is re-entered.

## Failure and recovery
- Scope too large (> 50 files). Apply the heavy-codebase escape hatch; if no packing tool is available, narrow scope, state the narrowing, and proceed with the reduced scope.
- Empty or missing source. For each affected section, state that it does not apply and explain why rather than fabricating content.
- Dispatch failure. Return a partial result containing the sections that could be filled; never claim the done predicate holds when required sections are missing.
- Banned mutating tool attempted. Stop immediately, do not perform the mutation, and report the attempt. No rollback is needed because no mutation occurs.
- Blocked / non-converged result. Terminal classification stating which sections could not be filled and the concrete reason.

## Output
A structured orientation report with 8 sections in order: task understanding, architecture context, pattern context, tooling context, dependency map, critical files summary, constraints and considerations, and recommended next steps, omitting a section only when not applicable with a stated reason.
