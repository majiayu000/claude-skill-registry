<!-- SOURCE-OF-TRUTH: shared/references/mcp_integration_patterns.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# MCP Integration Patterns

Use these only when a skill edits code/config/scripts/tests or makes semantic decisions from existing code. They are not required for docs-only, community, planning-only, external research, runtime verification, benchmark, or profiling work.

## Patterns

| Pattern | Use When | Flow |
|---------|----------|------|
| Outline-first read | unfamiliar code or large text file | `outline` or narrow `read_file` ranges before full reads |
| Verified edit | repository text mutation | `read_file(edit_ready=true)` -> `edit_file(base_revision)` -> verify/check changes |
| Semantic impact | public API, route, class, function, architecture, or non-trivial edit | `index_project` -> `analyze_edit_region` or symbol inspection |
| Semantic diff review | reviewing implementation risk | `analyze_changes` or scoped `changes` |
| Bulk literal cleanup | same replacement across several files | preview/dry-run first, then apply narrowly |

## Skill Integration

For code-editing skills, require `mcp_tool_preferences.md` and this file only when host-level instructions do not already provide equivalent MCP policy. Otherwise, state the local tool need inline and rely on the host policy.

For semantic code reasoning, use `hex-graph` only after narrowing the project/path enough for useful results. For raw method-call or string patterns, use text search first.

---
**Version:** 3.0.0
**Last Updated:** 2026-03-20
