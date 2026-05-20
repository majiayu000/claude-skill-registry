---
name: context-manager
description: "Audit and manage the full project context landscape: CLAUDE.md memory hierarchy, project documentation, markdown footprint, and content overlap. Detects project type, scores quality, flags stale docs, and reports total context cost. Trigger with 'audit context', 'audit memory', 'update CLAUDE.md', 'restructure memory', 'session capture', 'check project docs', 'markdown footprint', or 'what docs does this project need'."
compatibility: claude-code-only
---

# Context Manager

Manage the Claude Code memory hierarchy and audit the full markdown landscape of a project. Produces well-organised memory files, detects documentation overlap, and reports the total context footprint.

## Four Context Layers

| Layer | Location | Purpose | What this skill does |
|-------|----------|---------|---------------------|
| **Memory** | `./CLAUDE.md`, subdirs, `.claude/rules/*.md` | Project context, commands, architecture, rules | Audit, score, maintain |
| **Project docs** | `ARCHITECTURE.md`, `DATABASE_SCHEMA.md`, `API_ENDPOINTS.md`, `docs/**/*.md` | Technical documentation | Check existence per project type, flag staleness, detect CLAUDE.md overlap |
| **Session** | `SESSION.md`, `PROJECT_BRIEF.md` | Temporary progress tracking | Report presence + size (managed by dev-session) |
| **Public** | `README.md`, `CONTRIBUTING.md`, other root `.md` | Public-facing docs | Detect CLAUDE.md duplication |

Auto-memory (`~/.claude/projects/*/memory/MEMORY.md`) is also scanned for awareness but managed by Claude automatically.

## Operating Modes

### Mode 1: Session Capture

**When**: End of session, "capture learnings", "update CLAUDE.md with what we learned"

1. Review the conversation for discoveries worth preserving:
   - Commands that worked (or didn't)
   - Gotchas and workarounds found
   - Architecture decisions made
   - Configuration quirks discovered
   - Patterns that would help future sessions
2. Categorise each discovery using the placement decision tree below
3. Draft all changes as diffs in a single batch
4. Present the batch — apply after a single yes/no confirmation

**Keep it concise**: one line per concept. No verbose explanations, no generic advice.

### Mode 2: Full Audit

**When**: "audit context", "audit memory", "check project docs", periodic maintenance, working in a neglected project

1. Run the audit script:
   ```bash
   python3 plugins/dev-tools/skills/context-manager/scripts/audit_memory.py [repo-path]
   ```
2. Review the output:
   - **Memory layer**: CLAUDE.md sizes, quality scores, rules file sizes
   - **Project docs**: existence, staleness, overlap with CLAUDE.md
   - **Session/public**: presence and size
   - **Markdown footprint**: total KB by layer
   - **Overlap warnings**: sections duplicated between files
3. Generate changes autonomously — create, update, or flag files as needed
4. Present all changes as a single batch for approval
5. Apply approved changes
6. Check if the commit capture hook is installed — if not, offer to set it up (see [references/commit-hook.md](references/commit-hook.md))

For large repos, delegate to a sub-agent:
```
Task(subagent_type: "general-purpose",
  prompt: "Run python3 plugins/dev-tools/skills/context-manager/scripts/audit_memory.py /path/to/repo
           and summarise the findings.")
```

### Mode 3: Restructure

**When**: "restructure memory", root CLAUDE.md over 200 lines, first-time memory setup

1. Run full audit (Mode 2) first
2. Split oversized files:
   - Extract topic sections from root CLAUDE.md into `.claude/rules/<topic>.md`
   - Extract directory-specific content into sub-directory CLAUDE.md files
   - Move detailed technical content from CLAUDE.md to `docs/` or `ARCHITECTURE.md` if it's reference material, not operational context
3. Resolve overlaps: if CLAUDE.md duplicates ARCHITECTURE.md or docs/, remove the duplication
4. Create missing documentation files based on project type
5. Present the restructure plan, apply after approval

## Placement Decision Tree

```
Would this still apply if I switched to a completely different project?
├── YES → ~/.claude/rules/<topic>.md
│         (correction rules, API patterns, coding standards)
└── NO  → Is it specific to a subdirectory?
    ├── YES → <dir>/CLAUDE.md
    │         (integrations, directory-specific gotchas)
    └── NO  → Is it reference documentation or operational context?
        ├── Reference → ARCHITECTURE.md or docs/
        │               (system design, schemas, detailed flows)
        └── Operational → ./CLAUDE.md (project root)
                          (identity, stack, commands, critical rules)
```

## Size Targets

| File Type | Target | Maximum |
|-----------|--------|---------|
| Root CLAUDE.md | 50-150 lines | 200 |
| Sub-directory CLAUDE.md | 15-50 lines | 80 |
| Rules topic file | 20-80 lines | 120 |

## What Belongs Where

### Root CLAUDE.md
- Project name, purpose, owner
- Tech stack summary
- Build/deploy/test commands (copy-paste ready)
- Directory structure overview
- Critical "never do X" rules
- Key integrations and secrets locations

### Sub-directory CLAUDE.md
- External service integrations for that component
- Non-obvious configuration specific to this area
- Directory-specific commands
- Gotchas when working in this directory

**Don't create when**: parent covers it, directory is self-explanatory, content would be under 10 lines.

### .claude/rules/ topic files
- Correction rules bridging training cutoff (e.g. API changes, deprecated patterns)
- Coding patterns and standards
- Platform-specific formatting rules
- Error prevention patterns

### docs/ and ARCHITECTURE.md
- Detailed system architecture (component diagrams, data flows)
- Database schemas and migration guides
- API endpoint catalogues
- Content that Claude should read on demand, not every session

**Rule of thumb**: If it's needed every session, put it in CLAUDE.md. If it's reference material consulted occasionally, put it in docs/.

### What to delete
- Content Claude already knows from training
- Verbose explanations of standard frameworks
- Changelogs or version history (use git)
- Duplicated content (between CLAUDE.md and docs/, ARCHITECTURE.md, or README.md)
- "TODO" items that were never completed
- Generic advice not specific to the project

## Project Type Detection

The audit script detects project type from file presence and suggests appropriate documentation:

| Indicator | Type | Suggested Docs |
|-----------|------|---------------|
| `wrangler.jsonc` / `wrangler.toml` | Cloudflare Worker | ARCHITECTURE.md |
| `vite.config.*` + `.tsx` files | Vite/React | ARCHITECTURE.md |
| `next.config.*` | Next.js | ARCHITECTURE.md |
| MCP patterns in `src/index.ts` | MCP Server | ARCHITECTURE.md, API_ENDPOINTS.md |
| `src/routes/` or `src/api/` | API Project | API_ENDPOINTS.md, DATABASE_SCHEMA.md |
| Drizzle/Prisma config | Database | DATABASE_SCHEMA.md |

All projects get CLAUDE.md. Additional docs only when the project type warrants them. See [references/project-types.md](references/project-types.md) for full detection heuristics and doc templates.

## Autonomy Rules

- **Just do it**: Run audit, detect project type, identify gaps, draft changes
- **Brief confirmation**: Apply changes (single batch yes/no, not item-by-item)
- **Ask first**: Delete existing content, major restructures (moving 50+ lines), create new project docs from scratch where there's ambiguity about content

## Quality Scoring

The audit script scores each CLAUDE.md on 6 criteria (100 points):

| Criterion | Points | What it measures |
|-----------|--------|-----------------|
| Commands/Workflows | 20 | Build, test, deploy documented |
| Architecture Clarity | 20 | Structure, relationships, entry points |
| Non-Obvious Patterns | 15 | Gotchas, quirks, warnings |
| Conciseness | 15 | Dense content, no filler |
| Currency | 15 | References valid, commands work |
| Actionability | 15 | Copy-paste ready, real paths |

See [references/quality-criteria.md](references/quality-criteria.md) for the full rubric.

## Reference Files

| When | Read |
|------|------|
| Scoring CLAUDE.md quality | [references/quality-criteria.md](references/quality-criteria.md) |
| Detecting project type and expected docs | [references/project-types.md](references/project-types.md) |
| Creating new CLAUDE.md or rules files | [references/templates.md](references/templates.md) |
| Setting up automatic capture on commit | [references/commit-hook.md](references/commit-hook.md) |

## Scripts

- `scripts/audit_memory.py` — Scan all four layers, score quality, detect project type, report footprint and overlap
  - `python3 audit_memory.py [repo-path]` — human-readable report
  - `python3 audit_memory.py [repo-path] --json` — structured JSON output
