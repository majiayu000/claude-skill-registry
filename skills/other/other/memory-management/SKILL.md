---
name: memory-management
description: 'Persist SEO/GEO campaign context across Claude sessions with automatic hot-list, active work, and archive tiers. 项目记忆/跨会话'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when reviewing, archiving, or cleaning up campaign memory. Also when the user asks to check saved findings, manage hot cache, or archive old data."
argument-hint: "[review|archive|cleanup]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - project-memory
    - context-management
    - campaign-tracking
    - session-context
    - hot-cache
    - 项目记忆
    - プロジェクト記憶
    - 프로젝트메모리
    - memoria-proyecto
  triggers:
    - "remember project context"
    - "save SEO data"
    - "refresh wiki index"
    - "build wiki index"
    - "remember this for next time"
    - "what did we decide last time"
    - "what do we know so far"
    - "project status"
    - "wiki lint"
    - "项目记忆管理"
    - "跨会话记忆"
    - "刷新wiki索引"
    - "保存进度"
    - "上次说了什么"
    - "プロジェクト記憶"
    - "wikiインデックス更新"
    - "프로젝트 메모리"
    - "세션 기억"
    - "memoria del proyecto"
    - "guardar progreso"
    - "memória do projeto"
    - "gerenciar memória"
---

# Memory Management
This skill implements a three-tier memory system (HOT/WARM/COLD) for SEO and GEO projects. HOT memory (80 lines max) loads automatically every session via the SessionStart hook. WARM memory loads on demand per skill. COLD memory is archived data queried only when explicitly requested. The skill manages the full lifecycle: capture, promote, demote, and archive.

## What This Skill Does

Manages a three-tier memory lifecycle (HOT/WARM/COLD) with automatic promotion, demotion, and archival. Also maintains the wiki index layer, open-loop tracking, and cross-skill aggregation.

## Quick Start

Start with one of these prompts. Finish with a hot-cache update plan and a handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Initialize Wiki Index

```
Refresh wiki index
```

```
Build wiki index for [project name]
```

Generates `memory/wiki/index.md` from existing WARM files. Required once to enable wiki features; subsequent refreshes happen automatically.

### Initialize Memory Structure

```
Set up SEO memory for [project name]
```

```
Initialize memory structure for a new [industry] website optimization project
```

### Update After Analysis

```
Update memory after ranking check for [keyword group]
```

```
Refresh hot cache with latest competitor analysis findings
```

### Query Stored Context

```
What are our hero keywords?
```

```
Show me the last ranking update date for [keyword category]
```

```
Look up our primary competitors and their domain authority
```

### Promotion and Demotion

```
Promote [keyword] to hot cache
```

```
Archive stale data that hasn't been referenced in 30+ days
```

### Glossary Management

```
Add [term] to project glossary: [definition]
```

```
What does [internal jargon] mean in this project?
```

## Skill Contract

**Expected output**: a memory update plan, hot-cache changes, and a short handoff summary.

- **Reads**: current campaign facts, new findings from other skills, approved decisions, and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md).
- **Writes**: updates to `memory/hot-cache.md`, `memory/open-loops.md`, `memory/decisions.md`, and related `memory/` folders. Manages WARM-to-COLD archival in `memory/archive/`. Compiles `memory/wiki/index.md` (auto-refreshed) and wiki compiled pages (user-confirmed). **Sole writer of wiki (with delegated auto-refresh)**: `memory-management` owns all wiki writes semantically. For performance, the narrowly-scoped `memory/wiki/index.md` auto-refresh is delegated to the PostToolUse hook in [hooks/hooks.json](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/hooks/hooks.json). Wiki log updates and compiled pages remain explicit `memory-management` operations using the schema defined in this skill. **Auditor handoff archiving** (v7.1.0+): when triggered by a direct user request or an auditor's explicit "Save these results?" yes-response, append a structured block to `memory/audits/YYYY-MM.md`. The Stop hook never initiates memory writes. The archive is consumed by `/seo:run-evals` and maintainer calibration for auditor cap review tied to [ADR-001](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/decisions/2026-04-adr-001-inline-auditor-runbook.md). See [references/examples.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/examples.md) for the exact archive block format and rules.
- **Promotes**: durable strategy, blockers, terminology, entity candidates, and major deltas. Applies temperature lifecycle rules: promote to HOT on high reference frequency, demote on staleness.
- **Next handoff**: use the `Next Best Skill` below when the project memory baseline is ready for active work.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Temperature Lifecycle Rules

> See [references/promotion-demotion-rules.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/promotion-demotion-rules.md) for the full promotion/demotion table and action procedures.

### Hook Integration

This skill's behavior is reinforced by the library's prompt-based hooks:
- **SessionStart**: loads `memory/hot-cache.md`, reminds of stale open loops; loads `memory/wiki/<project>/index.md` (or global `index.md`) if it exists; provides light-user guidance based on Quick Status when `next_action` items are available
- **PostToolUse**: after any WARM file write, silently refreshes `memory/wiki/index.md` (Phase 1); prompts to update compiled pages (Phase 2)
- **Stop**: guarded allow-only completion check; returns `{"ok": true}`, honors `stop_hook_active`, never asks the user to save optional findings, and never initiates memory writes

## Data Sources

With tools: auto-populate from ~~SEO tool, ~~analytics, ~~search console. Without tools: ask user for keywords, competitors, metrics, campaigns, and terminology. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests SEO memory management:

### 1. Initialize Memory Structure

For new projects, create the directory structure defined in the [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md). Key directories: `memory/` (decisions, open-loops, glossary, entities, research, content, audits, monitoring) plus `memory/wiki/` (auto-managed compiled index with optional per-project subdirectories).

> **Templates**: [hot-cache-template.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/hot-cache-template.md) · [glossary-template.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/glossary-template.md) · [Wiki design archive](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/proposal-wiki-layer-v3.md)

### Wiki Layer

`memory-management` owns the wiki schema. Hook-delegated index refreshes may update only `memory/wiki/index.md` and `memory/wiki/<project>/index.md`. Wiki log updates remain explicit `memory-management` operations. Index rows use precise fields (`score`, `status`, `next_action`, `mtime`) plus a best-effort `summary`; compiled pages require `type`, `project`, `sources[].path`, `sources[].hash`, and `last_compiled` frontmatter.

### 2. Context Lookup Flow

When a user references something unclear, follow this lookup sequence:

**Step 1: Check `memory/hot-cache.md` (hot cache)**
- Is it in active keywords?
- Is it in primary competitors?
- Is it in current priorities or campaigns?

**Step 2: Check Wiki Index** (`memory/wiki/index.md` or project-level) — locate relevant WARM files

**Step 3: Check memory/glossary.md**
- Is it defined as project terminology?
- Is it a custom segment or shorthand?

**Step 4: Check Cold Storage**
- Search `memory/archive/` first for dated `YYYY-MM-DD-` archived files.
- If the archive points to a source category, follow that trail back to `memory/research/`, `memory/audits/`, or `memory/monitoring/`.
- Treat COLD findings as historical unless refreshed by the current session.

**Step 5: Ask User**
- If not found in any layer, ask for clarification
- Log the new term in glossary if it's project-specific

- **Decision provenance (v8.0.1+)**: when loading `memory/decisions.md`, verify each entry has `approved_by: user`. Entries with `approved_by: skill_inferred` or missing field are treated as **ADVISORY** — surface to user before using as authoritative. Auditor-class skills (content-quality-auditor, domain-authority-auditor) MUST ignore non-user-approved decisions when determining verdict. See [skill-contract.md §Promotion Rules](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

Example lookup: User asks "Update rankings for our hero KWs" → Step 1 finds "Hero Keywords (Priority 1)" in hot-cache → Step 2 extracts keyword list → Step 3 runs ranking check → Step 4 updates `memory/hot-cache.md` and `memory/monitoring/rank-history/YYYY-MM-DD-ranks.csv`.

### 3. Promotion & Demotion Logic

> **Reference**: See [references/promotion-demotion-rules.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/promotion-demotion-rules.md) for detailed promotion/demotion triggers (keywords, competitors, metrics, campaigns) and the action procedures for each.

### 4. Update Triggers, Archive Management & Cross-Skill Integration

> **Reference**: See [references/update-triggers-integration.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/update-triggers-integration.md) for the complete update procedures after ranking checks, competitor analyses, audits, and reports; monthly/quarterly archive routines; and integration points with all 8 connected skills (keyword-research, rank-tracker, competitor-analysis, content-gap-analysis, seo-content-writer, content-quality-auditor, domain-authority-auditor).

### 5. Memory Hygiene Checks

When invoked for review or cleanup:

1. **Line count check**: Count lines in `memory/hot-cache.md`. If >80, list oldest entries for archival.
2. **Byte check**: If hot-cache exceeds 25KB, warn and recommend trimming long entries.
3. **Staleness scan**: List memory files older than 30 days that have not been referenced. Recommend archival for files >90 days.
4. **Frontmatter audit**: Check that all memory files (except hot-cache.md) have `name`, `description`, and `type` in their frontmatter. Report any missing fields.

### 6. Save Results

Ask "Save these results for future sessions?" — if yes, write `YYYY-MM-DD-<topic>.md` to `memory/`. Auto-save veto issues to `memory/hot-cache.md`.

## Examples, Advanced Features & Practical Limitations

> **Reference**: See [references/examples.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/examples.md) for three complete examples (hero keyword rankings, glossary lookup, e-commerce project init), advanced features (smart context loading, memory health check, bulk promotion/demotion, memory snapshot, cross-project memory, wiki lint), and practical limitations (concurrent access, cold storage retrieval, data freshness, wiki compilation).

## GDPR / Privacy Compliance

`memory/` may store third-party personal data — entity names, founder bios, LinkedIn profiles, author/journalist names surfaced by `entity-optimizer` or research skills. Under GDPR Art 4(1) (applies to **processing of personal data of EU/EEA/UK residents** regardless of where the controller is located), these qualify as "personal data". The user is the data controller. Non-EU users without EU/EEA/UK data subjects may still face analogous obligations under CCPA/CPRA (California), PIPEDA (Canada), LGPD (Brazil), or other national regimes. **Not legal advice.**

### Retention policy
- WARM files: archive to `memory/archive/` after 90 days unreferenced (default lifecycle)
- COLD archive: never auto-deleted, but eligible for Art 17 erasure requests
- All files: user MUST honor Art 17 requests from data subjects (individuals named in memory)

### Deletion flow (Art 17 / CCPA §1798.105)
Invoke: `memory-management purge <entity-name-or-slug>`

This skill then:
1. Greps all files under `memory/` (including `memory/archive/`) for the entity name, slug, or domain
2. Presents matches to user for confirmation
3. Deletes matching entries from `memory/entities/<slug>.md`, `memory/entities/candidates.md`, and surfaces references in other files for manual review
4. Logs the purge to `memory/audits/gdpr-purges.md` with date + subject requested

### Lawful basis reminder
Before writing a third-party person to `memory/entities/`, the user must have one lawful basis per GDPR Art 6 (where GDPR applies — see scope note above): `consent`, `legitimate_interest`, `contract`, or equivalent. Advisory — this skill does not enforce, and does not substitute for legal review.

## Reference Materials

- [references/examples.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/examples.md) — Worked examples, advanced features, practical limitations, and the auditor handoff archive block format & rules
- [references/promotion-demotion-rules.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/promotion-demotion-rules.md) — Full promotion/demotion table and action procedures
- [references/update-triggers-integration.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/update-triggers-integration.md) — Update procedures, archive routines, and cross-skill integration points
- [CORE-EEAT Content Benchmark](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/core-eeat-benchmark.md) — Content quality scoring stored in memory
- [CITE Domain Rating](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/cite-domain-rating.md) — Domain authority scoring stored in memory

## Next Best Skill

Primary: [keyword-research](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/SKILL.md) — seed or refresh campaign strategy with current demand signals.
