---
name: ln-612-semantic-content-auditor
description: "Checks document semantic content against SCOPE and project goals, coverage gaps, off-topic content, SSOT. Use when auditing documentation relevance."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Semantic Content Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing semantic fitness of project documentation.

## Purpose & Scope

- Verify document content matches stated SCOPE and declared document kind
- Check content **aligns with project goals** (value contribution)
- Return structured findings to coordinator with severity, location, fix suggestions
- Does NOT verify facts against codebase

## Target Documents

Called ONLY for project documents (not reference/tasks):

| Document | Verification Focus |
|----------|-------------------|
| `AGENTS.md` / `CLAUDE.md` | Entry instructions stay scoped, navigable, and free of off-topic content |
| `docs/README.md` | Navigation scope correct, descriptions relevant |
| `docs/documentation_standards.md` | Standards applicable to this project type |
| `docs/principles.md` | Principles relevant to project architecture |
| `docs/project/requirements.md` | Requirements scope complete, no stale items |
| `docs/project/architecture.md` | Architecture scope covers all layers |
| `docs/project/tech_stack.md` | Stack scope matches project reality |
| `docs/project/api_spec.md` | API scope covers all endpoint groups |
| `docs/project/database_schema.md` | Schema scope covers all entities |
| `docs/project/design_guidelines.md` | Design scope covers active components |
| `docs/project/infrastructure.md` | Infrastructure scope covers all deployment targets |
| `docs/project/runbook.md` | Runbook scope covers setup + operations |

**Excluded:** `docs/tasks/`, `docs/reference/`, `docs/presentation/`, `tests/`

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`, `references/docs_quality_contract.md`, and `references/markdown_read_protocol.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives from coordinator per invocation:

| Field | Description |
|-------|-------------|
| `doc_path` | Path to document to audit (e.g., `docs/project/architecture.md`) |
| `output_dir` | Directory for report output (from contextStore) |
| `project_root` | Project root path |
| `tech_stack` | Detected technology stack |

`hex-line` is optional for this doc-only worker. Use it to outline large markdown files when available; otherwise continue with built-in `Read/Grep/Glob/Bash` and do not block on MCP availability.

## Workflow

### Phase 1: Header and Contract Extraction

1. Read document header and top sections first
2. Parse:
   - `SCOPE`
   - `DOC_KIND`
   - `DOC_ROLE`
   - `READ_WHEN`
   - `SKIP_WHEN`
   - `PRIMARY_SOURCES`
3. If no SCOPE tag, infer from document type
4. Infer expected `DOC_KIND` from the shared contract when missing
5. Record stated purpose and routing boundaries

### Phase 2: Doc-Kind-Aware Semantic Audit

Judge the document according to its kind:

| DOC_KIND | Main semantic question |
|----------|------------------------|
| `index` | Does it route efficiently and avoid deep factual overload? |
| `reference` | Is it precise, complete enough, and easy to lookup? |
| `how-to` | Is the procedure actionable and sequenced correctly? |
| `explanation` | Does it build the right mental model and rationale? |
| `record` | Does it preserve the decision trace and consequences? |

Analyze the document against stated scope and kind:

| Check | Finding Type |
|-------|--------------|
| Section not serving scope | OFF_TOPIC |
| Scope aspect not covered | MISSING_COVERAGE |
| Excessive detail beyond scope | SCOPE_CREEP |
| Content duplicated elsewhere | SSOT_VIOLATION |

**Agent instruction file checks** (applies when the audited file is `AGENTS.md` or `CLAUDE.md`):

| Check | Finding Type | Severity | Recommendation |
|-------|--------------|----------|----------------|
| Style / formatting rules (indentation, quote style, trailing whitespace, naming conventions) | NOT_A_LINTER | WARN | Move to Biome, Prettier, Ruff, EditorConfig, or a Claude Code Stop hook. Instruction files are loaded into every session and cost tokens against the ~100-imperative budget; deterministic tools do this for free. |
| Conditional / non-universal rules at the root (`when working on src/api/...`, `if modifying the billing service`, `for the Z service`) | NON_UNIVERSAL_RULE | WARN | Move to `.claude/rules/*.md` with a `paths:` frontmatter filter (Anthropic built-in path scoping). Non-universal rules bias Claude Code toward ignoring the entire file via the `<system-reminder>` wrapper. |
| Self-Improvement Loop rule pointing at a manual `tasks/lessons.md` | OBSOLETE_PATTERN | WARN | Delete. Claude Code's built-in auto memory at `~/.claude/projects/<project>/memory/` already does this; a parallel hand-maintained convention wastes context. |

All three WARN only — they require human judgment (intentional style rule? conditional scope that's actually project-wide?). Cite `references/agent_instructions_writing_guide.md` in every finding.

Read strategy:
- header + top sections first
- read only the body sections needed for judgment
- read the full file only when the semantic judgment is unsafe without it

**Scoring:**
- 10/10: All content serves scope, scope fully covered
- 8-9/10: Minor off-topic content or small gaps
- 6-7/10: Some sections not aligned, partial coverage
- 4-5/10: Significant misalignment, major gaps
- 1-3/10: Document does not serve its stated purpose

### Phase 3: SCORING & REPORT

Calculate final score based on scope alignment:

```
overall_score = weighted_average(coverage, relevance, focus)
```

Coverage: how completely the scope is addressed. Relevance: how much content serves the scope. Focus: absence of off-topic content.

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-612--{doc-slug}.md` where `doc-slug` is derived from document filename (e.g., `architecture`, `tech_stack`, `agents_md`).

With `category: "Semantic Content"` and checks: scope_alignment, not_a_linter, non_universal_rule, obsolete_pattern (the last three fire only on AGENTS.md / CLAUDE.md targets).

Return summary per `references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-612--architecture.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Read progressively:** Use section-first reading; full reads only when needed for safe judgment
- **Scope inference:** If no SCOPE tag, use document filename to infer expected scope
- **Doc-kind aware:** Judge by document purpose, not one generic rubric
- **No false positives:** Better to miss an issue than report incorrectly
- **Location precision:** Always include line number for findings
- **Actionable fixes:** Every finding must have concrete fix suggestion
- **No fact-checking:** Do NOT verify paths, versions, endpoints against code
- **Shared class registry:** Document boundaries come from `docs_quality_contract.md`; do not invent alternate scope rules per file

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] Header contract extracted or inferred
- [ ] Content-scope alignment analyzed (OFF_TOPIC, MISSING_COVERAGE, SCOPE_CREEP, SSOT_VIOLATION)
- [ ] Semantic judgment applied according to DOC_KIND
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-612--{doc-slug}.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `references/audit_output_schema.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-03-01
