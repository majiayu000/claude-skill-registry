---
name: sync-to-copilot
version: 2.0.0
description: '[AI & Tools] Sync Claude Code knowledge to GitHub Copilot instructions. Creates/updates .github/copilot-instructions.md (project-specific) + .github/instructions/common-protocol.instructions.md (generic protocols) + per-group instruction files. Two-tier architecture: script generates structure, AI enriches with file-extracted summaries.'
tags:
    - ai-tools
    - sync
    - copilot
    - github-copilot
    - workflow
    - configuration
---

# Skill: sync-to-copilot

Sync Claude Code knowledge to GitHub Copilot instructions. Two-tier output: project-specific + common protocol.

---

## Quick Summary

**Purpose:** Keep Copilot instructions in sync with Claude Code workflows, dev rules, and project-reference docs.

**Architecture (Two-Tier):**

1. `.github/copilot-instructions.md` — **Project-specific** (always loaded by Copilot)
    - TL;DR golden rules, decision table
    - Project-reference docs index with READ prompts
    - Key file locations, dev commands

2. `.github/instructions/common-protocol.instructions.md` — **Generic protocols** (applyTo: `**/*`)
    - Prompt protocol, before-editing rules
    - Workflow catalog (from workflows.json)
    - Workflow execution protocol
    - Development rules (from development-rules.md)

3. `.github/instructions/{group}.instructions.md` — **Per-group** (applyTo: file patterns)
    - Enhanced summaries per doc with READ prompts
    - Groups: backend, frontend, styling, testing, project

**What gets synced:**

- Workflow catalog (from workflows.json) — **SCRIPT-GENERATED**
- Dev rules (from development-rules.md) — **SCRIPT-GENERATED**
- Project-reference summaries (from copilot-registry.json) — **SCRIPT-GENERATED**
- Enriched section headings and key patterns — **AI-GENERATED** (this skill)

**Usage:**

```
/sync-to-copilot
```

**Script:** `.claude/scripts/sync-copilot-workflows.cjs`

---

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## When to Use This Skill

Trigger this skill when:

- **Workflows added/modified** — After editing `.claude/workflows.json`
- **Development rules changed** — After editing `.claude/workflows/development-rules.md`
- **Project-reference docs updated** — After modifying files in `docs/project-reference/`
- **Registry entries changed** — After editing `docs/copilot-registry.json`
- **Regular maintenance** — Quarterly sync to ensure Copilot parity
- **Copilot setup** — First-time Copilot instructions creation

---

## Workflow

### Phase 1: Script Generation (Automated)

```bash
node .claude/scripts/sync-copilot-workflows.cjs
```

This generates:

- `.github/copilot-instructions.md` — project-specific with registry summaries
- `.github/instructions/common-protocol.instructions.md` — generic protocols
- `.github/instructions/{group}.instructions.md` — per-group instruction files
- Removes old `.github/common.copilot-instructions.md` if it exists

### Phase 2: AI Enrichment (This Skill)

After the script runs, the AI MUST enrich the generated instruction files:

1. **For each per-group instruction file** in `.github/instructions/`:
    - Read the corresponding `docs/project-reference/*.md` source file
    - Extract the `##` section headings from the source file
    - Add a "Key Sections" list under each doc entry showing the headings
    - Keep it concise — headings only, no content duplication

2. **For `.github/copilot-instructions.md`**:
    - Verify the TL;DR golden rules in `docs/copilot-registry.json` → `projectInstructions.goldenRules` still match CLAUDE.md
    - Check if any new project-reference files exist but are missing from `docs/copilot-registry.json`
    - If missing entries found, add them to the registry and re-run the script

3. **For `docs/copilot-registry.json`**:
    - Verify each `summary` field accurately describes the current file content
    - Update stale summaries based on actual file content
    - Add entries for any new `docs/project-reference/*.md` files

### Phase 3: Verification

Check that:

- [x] `.github/copilot-instructions.md` contains project-specific content
- [x] `.github/instructions/common-protocol.instructions.md` contains protocols + workflow catalog
- [x] Per-group instruction files contain READ prompts
- [x] No old `common.copilot-instructions.md` file remains
- [x] Workflow count matches workflows.json
- [x] All project-reference files are represented in the registry

---

## AI Enrichment Protocol

When enriching per-group instruction files, follow this pattern for each doc entry:

```markdown
## [Doc Title](relative/path)

**Summary:** One-line summary from registry.

**Key Sections:**

- Section 1 Name
- Section 2 Name
- Section 3 Name
- ...

> **READ** `docs/project-reference/filename.md` when: trigger description
```

**Rules:**

- Extract ONLY `##` level headings from the source file (not `###` or deeper)
- Do NOT copy content — just list heading names
- Keep the READ prompt from the registry `whenToRead` field
- If a file is very large (>30KB), note the file size: `(~59KB - read relevant sections)`

---

## Output Files

| File                                                     | Type                                    | Content                                        |
| -------------------------------------------------------- | --------------------------------------- | ---------------------------------------------- |
| `.github/copilot-instructions.md`                        | Project-specific                        | TL;DR + project-reference index + READ prompts |
| `.github/instructions/common-protocol.instructions.md`   | Generic (applyTo: `**/*`)               | Prompt protocol + workflow catalog + dev rules |
| `.github/instructions/backend-csharp.instructions.md`    | Backend (applyTo: `**/*.cs`)            | Backend doc summaries + READ prompts           |
| `.github/instructions/frontend-angular.instructions.md`  | Frontend (applyTo: `**/*.ts,**/*.html`) | Frontend doc summaries + READ prompts          |
| `.github/instructions/styling-scss.instructions.md`      | Styling (applyTo: `**/*.scss,**/*.css`) | Styling doc summaries + READ prompts           |
| `.github/instructions/testing.instructions.md`           | Testing (applyTo: `**/*Test*/**,...`)   | Testing doc summaries + READ prompts           |
| `.github/instructions/project-reference.instructions.md` | Cross-cutting (applyTo: `**/*`)         | General project doc summaries + READ prompts   |

---

## Copilot Limitations

**Copilot can't enforce protocols like Claude Code hooks:**

- No blocking operations (edit-enforcement, search-before-code)
- Relies on LLM instruction-following (not guaranteed)
- Protocols are advisory, not enforced
- No runtime context injection — all context must be in instruction files

**Benefits:**

- Consistent guidance across AI tools
- Same workflow detection for Claude and Copilot users
- READ prompts enable on-demand context loading
- Automated sync reduces configuration drift

---

## Troubleshooting

### Issue: "workflows.json not found"

**Solution:** Ensure you're running from project root

### Issue: Missing project-reference files in registry

**Solution:** Add entries to `docs/copilot-registry.json`, then re-run script

### Issue: Stale summaries

**Solution:** Run this skill — AI will read files and update summaries

---

## Related Skills

- `/ai-dev-tools-sync` — Broader Claude/Copilot sync (skills, prompts, agents)
- `/sync-copilot-workflows` — Workflow-only sync (subset of this skill)

---

## References

- **Script:** `.claude/scripts/sync-copilot-workflows.cjs`
- **Registry:** `docs/copilot-registry.json`
- **Sources:** `.claude/workflows.json`, `.claude/workflows/development-rules.md`
- **Main output:** `.github/copilot-instructions.md`
- **Instruction files:** `.github/instructions/*.instructions.md`
