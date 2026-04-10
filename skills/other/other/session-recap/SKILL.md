---
name: session-recap
description: Document Claude Code sessions by extracting knowledge into cross-referenced documentation. Triggers on "recap the session", "summarize the work", or after significant code changes.
user-invocable: true
---

# Session Recap

Systematically document Claude Code sessions into the knowledge bank.

**Knowledge Bank Location**: Read from `~/.claude/plugins/config/second-brain/config.json`. Configure via `skills/common/setup_kb_path.sh --configure`.

**Philosophy**: Knowledge Bank = BRAIN, not ARCHIVE. Preserve workflows, edge cases, decisions—not verbose traces. Target 95% size reduction, 100% actionable knowledge.

---

## Invocation

### Recommended Workflow

**Important**: Session recap should run in a **new session** after the work session ends. This ensures the full transcript is captured.

1. **Exit the work session**: The SessionEnd hook automatically saves transcript segments and builds `session.md` as a hub note with links to all artifacts.

2. **Start a new session**: Begin fresh to run the recap
   ```
   claude
   ```

3. **Invoke session-recap with the session folder**:
   ```
   Recap the session at {KB_PATH}/_sessions/YYYY-MM-DD/{session_id}/
   ```
   Or:
   ```
   /second-brain:session-recap {KB_PATH}/_sessions/YYYY-MM-DD/{session_id}/
   ```

### Legacy: Raw Transcript Path

If no session folder exists (e.g., hooks were not configured), you can still provide a raw `.jsonl` transcript path:
```
Recap the session at /path/to/session-id.jsonl
```

### Why a New Session?

Running session-recap in the same session would miss the final conversation context. The transcript must be fully saved before knowledge extraction can begin.

### Manual Invocation
- **Slash command**: `/second-brain:session-recap`
- **Skill tool**: `Skill({ skill: "second-brain:session-recap" })`

### Visibility Settings

| Setting | Value | Effect |
|---------|-------|--------|
| `user-invocable` | `true` | Visible in slash menu, Skill tool allowed |

---

## RFC 2119 Keywords

This skill uses RFC 2119 keywords:
- **MUST**: Absolute requirement, cannot be skipped
- **SHOULD**: Valid exceptions may exist but require conscious weighing
- **MAY**: Truly optional

---

## Full Recap — No Shortcuts

Every session recap executes all 5 phases completely — no exceptions. A daily log alone is not a recap; it's a log entry. The knowledge bank compounds from extracted concepts, reflections, and best practices, not from session summaries. Skipping phases produces a diary, not a brain.

Even when processing many sessions, each session gets its own full Phase 2.1 reflection gate, Phase 2.4 source ingestion plan, and Phase 3 document creation. Do not batch sessions into a single daily log or skip phases for throughput.

## Batch Recap

When recapping multiple sessions (e.g., "recap all sessions since March 29"):

1. **Discover** — list all sessions in date range, read each session.md for metadata
2. **Triage** — skip sessions with no transcript, trivial (<5 user messages), or already recapped
3. **Process chronologically** — full 5-phase workflow per session, each gets its own daily log + extracted docs
4. **Parallelize when independent** — different projects/topics can use parallel agents; same investigation thread should be sequential for cross-references
5. **Integrate once at end** — index regeneration and log append after all sessions, not per session

---

## Workflow

### Phase 1: ANALYZE

**Goal**: Load session data and extract facts.

#### 1.1 Load Session Data

**If session folder provided**:

First, read `session.md` as the hub note for both metadata and content navigation:
```bash
obsidian vault="knowledge-bank" read path="_sessions/{date}/{session_id}/session.md"
```

**Frontmatter metadata** (supplements later phases):
- `project`, `session_name`, `tags`, `summary`, `duration_seconds`, `started_at`, `ended_at`, `transcript_source`

**Body navigation** — follow session.md body sections:

| Section | Content | How to use |
|---------|---------|------------|
| `## Generated Artifacts` | WikiLinks to docs in `docs/` | Read for additional context |
| `## Transcript` | Source path to original `.jsonl` | Use for `parse_transcript.sh` |
| `## Compaction Points` | Line counts per segment boundary | Context on session length/compaction |
| `## Memory Snapshot` | WikiLinks to memory/*.md | Read auto-memory for project context |

Then locate the transcript:
```bash
# Preferred: read transcript_source from session.md frontmatter (v2.1+)
TRANSCRIPT_SOURCE=$(read_frontmatter_prop "$SESSION_FOLDER/session.md" "transcript_source")

if [ -n "$TRANSCRIPT_SOURCE" ] && [ -f "$TRANSCRIPT_SOURCE" ]; then
    TRANSCRIPT="$TRANSCRIPT_SOURCE"
else
    # Fallback for old sessions: find latest segment copy
    LATEST_SEGMENT=$(ls -d "$SESSION_FOLDER"/segment-* 2>/dev/null | grep -v 'segment-final' | sort -t- -k2 -n | tail -1)
    [ -z "$LATEST_SEGMENT" ] && [ -d "$SESSION_FOLDER/segment-final" ] && LATEST_SEGMENT="$SESSION_FOLDER/segment-final"
    TRANSCRIPT="$LATEST_SEGMENT/transcript.jsonl"
fi
```

**If no folder (current conversation mode)**: Skip session.md reading. Analyze current conversation context.

#### 1.2 Detect Project

If session.md `project` property is set (non-empty) → use it directly.

Otherwise → fall back to transcript parsing:
```bash
./scripts/parse_transcript.sh "$TRANSCRIPT" project
```

| Path Pattern | Project | KB Location |
|--------------|---------|-------------|
| `/.claude/` | cc | `projects/cc/` |

#### 1.3 Extract Session Facts

```bash
./scripts/parse_transcript.sh "$TRANSCRIPT" all
```

Extracts: user requests, files read, files modified, commands, errors, subagents, **insights**.

#### 1.4 Detect Session Sources (SHOULD complete when session folder provided)

Scan session.md body sections and transcript for ingestible knowledge:

```bash
./scripts/detect_session_sources.sh "$SESSION_FOLDER" "$TRANSCRIPT"
```

Outputs classified sources, one per line: `artifact|<path>|<description>` or `reference|<path>|<description>`.

| session.md Section | What it contains | Ingest as |
|---|---|---|
| `## Generated Artifacts` | Docs in `docs/` (designs, plans, research, investigations, SOPs) | artifact — high-value, already distilled |
| `## Plans` | Claude Code plan files (architectural decisions, implementation approaches) | artifact — captures decision rationale |
| `## Memory Snapshot` | Auto-memory files (project context, lessons learned) | reference — supplements context |
| Transcript | Non-code files read (.md, .pdf, .txt) and URLs fetched (WebFetch) | reference — external knowledge consumed |

Record the classified list for Phase 2.5.

---

### Phase 2: PLAN

**Goal**: Determine what to document and whether reflection is required.

#### 2.1 Reflection Decision Gate (MUST complete)

Answer these questions:

| Question | Answer |
|----------|--------|
| 1. Did this session involve debugging or problem-solving? | YES / NO |
| 2. Did this session discover a workflow pattern? | YES / NO |
| 3. Did this session encounter tool/process friction? | YES / NO |

**Decision**:
- **If ANY answer is YES** → MUST create at least 1 reflection
- **If ALL answers are NO** → MAY skip reflections

Record decision for Phase 4 verification.

#### 2.2 Search Cross-References (MUST complete before Phase 3)

```bash
./scripts/search_cross_references.sh "keyword"
```

Target 10-15 cross-references distributed across:
- Concepts (3-5)
- Components (3-5)
- Best Practices (1-2)
- Recent Sessions (1-2)
- MOCs (1-2)

See [cross-reference-guide.md](references/cross-reference-guide.md) for methodology.

#### 2.3 External Document Distillation (MUST complete when investigation docs exist)

**If external investigation documents exist (100+ KB)**:

1. **MUST** detect documents for distillation:
```bash
./scripts/detect_external_docs.sh "$SESSION_FOLDER"
```

2. **MUST** analyze distillation requirements:
```bash
./scripts/analyze_for_distillation.sh "$DOC_PATH"
```

See [distillation-guide.md](references/distillation-guide.md) for detailed methodology.

#### 2.4 Source Ingestion Plan (SHOULD complete when sources detected in 1.4)

For each source detected in Phase 1.4, decide:

| Decision | When | Action |
|----------|------|--------|
| **Ingest as KB doc** | High-value, reusable knowledge (design doc, investigation, best practice) | Create concept/component/best-practice doc (5-8 WikiLinks) |
| **Distill and ingest** | Large source (>100KB) needing reduction | Apply [distillation-guide.md](references/distillation-guide.md), then create doc |
| **Skip** | Transient, already covered by daily log, or not knowledge-bearing | Note in daily log only |

Guidelines:
- **Artifacts** in `docs/` are high-value by default — they were already distilled during the session
- **Plans** capture decision rationale — ingest when they document non-obvious architectural choices
- **Memory snapshots** supplement context but rarely need their own KB doc — skip unless they contain unique project insights
- **External references** need judgment — don't ingest the entire article, extract its key insights relevant to the session's work

Record decisions for Phase 3 creation.

#### 2.5 Insight Classification (SHOULD complete when insights exist)

If insights were extracted in Phase 1.3, classify each:

| Insight Content | Classification | Action |
|-----------------|----------------|--------|
| Reveals architectural pattern | Concept | SHOULD create concept doc |
| Describes component behavior | Component | SHOULD update/create component doc |
| Documents methodology | Best Practice | SHOULD create best practice doc |
| Reveals workflow pattern | Reflection | SHOULD create reflection |
| Identifies anti-pattern | Reflection | SHOULD create reflection |
| General educational context | Daily Log | MUST include in daily log |

**Record classifications for Phase 3.**

---

### Phase 3: CREATE

**Goal**: Write documentation in priority order.

#### Priority Order

1. **Concept docs** - MUST if patterns discovered OR insight reveals architecture
2. **Component docs** - MUST if components modified OR insight describes behavior
3. **Best practice docs** - SHOULD if methodology identified OR insight documents technique
4. **Artifact-derived docs** - SHOULD if Phase 2.4 decision = ingest (from session `docs/` artifacts, plans). Use 5-8 WikiLinks. Frontmatter: `source-type: artifact`, `ingested-from: {path}`
5. **Reference-derived docs** - MAY if Phase 2.4 decision = ingest (from external references). Use 5-8 WikiLinks. Frontmatter: `source-type: reference`, `ingested-from: {path or URL}`
6. **Process reflections** - **MUST if Phase 2.1 decision = required** OR insight reveals workflow/anti-pattern
7. **Daily session log** - MUST (always required, includes all insights)

#### Document Locations

| Type | Location | Template |
|------|----------|----------|
| Concept | `{KB}/projects/{project}/concepts/` | [concept-template.md](references/concept-template.md) |
| Component | `{KB}/projects/{project}/components/` | [component-template.md](references/component-template.md) |
| Best Practice | `{KB}/projects/{project}/best-practices/` | [best-practice-template.md](references/best-practice-template.md) |
| Reflection | `{KB}/reflections/{category}/` | [process-reflection-template.md](references/process-reflection-template.md) |
| Daily Log | `{KB}/daily-log/YYYY-MM-DD [Topic].md` | [daily-log-template.md](references/daily-log-template.md) |

#### Reflection Categories

| Category | Folder | Trigger |
|----------|--------|---------|
| Architecture Patterns | `architecture-patterns/` | Threading, state, design patterns |
| Development Workflow | `development-workflow/` | Utility discovery, test-first, deps |
| Anti-Patterns | `anti-patterns/` | Wrong approaches, confusion |
| DX Improvements | `dx-improvements/` | Search gaps, missing docs, tools |

> **Note**: These are example categories. The system discovers reflection categories dynamically from subdirectories in `{KB}/reflections/`. Create any category folders that fit your workflow.

#### Cross-Reference Requirements

Every document MUST include:
- **Technical docs**: 10-15 WikiLinks (minimum 10)
- **Reflections**: 5-8 WikiLinks (minimum 5)

Verify with:
```bash
./scripts/count_wikilinks.sh document.md
```

#### YAML Frontmatter (MUST include)

```yaml
---
title: Document Title
aliases: [Alt 1, Alt 2]
tags: [category, topic]
type: concept|component|best-practice|daily-log|reflection
created: YYYY-MM-DD
modified: YYYY-MM-DD
project: Claude Code
session-folder: _sessions/YYYY-MM-DD/{session_id}
source-type: session|artifact|reference    # Optional: how this knowledge entered the KB
ingested-from: /path/to/source.md          # Optional: provenance for artifact/reference docs
---
```

The `session-folder` field applies to ALL recap-created docs (daily log, concepts, components, best practices, reflections). It creates a reverse reference — Obsidian's backlinks panel on `session.md` will show all KB docs extracted from that session. Omit if no session folder was provided (current conversation mode).

#### Obsidian Syntax (MUST invoke when obsidian skills installed)

When obsidian skills are available, **MUST** invoke before creating knowledge bank documents:

```
/obsidian:obsidian-markdown
```

This ensures proper Obsidian Flavored Markdown syntax for:
- WikiLinks: `[[Note]]`, `[[Note#Heading]]`, `[[Note|Display]]`
- Callouts: `> [!note]`, `> [!warning]`, `> [!tip]`, etc.
- Properties (YAML frontmatter)
- Tags: `#tag`, `#nested/tag`
- Embeds: `![[Note]]`, `![[image.png]]`
- Block references: `[[Note#^block-id]]`

**Verification**: Check if obsidian skills exist in available skills list before creating documents.

---

### Phase 4: VERIFY

**Goal**: Confirm all requirements met before declaring complete.

#### 4.1 Run Verification Script (MUST complete)

```bash
./scripts/verify_session_recap.sh \
  --kb-path "$KB_PATH" \
  --project "$PROJECT" \
  --daily-log "YYYY-MM-DD [Topic].md" \
  --reflection-required  # or --no-reflection based on Phase 2.1
```

#### 4.2 Validate Obsidian Syntax (MUST complete)

```bash
./scripts/validate_obsidian_syntax.sh "$DAILY_LOG_PATH"
./scripts/validate_obsidian_syntax.sh "$REFLECTION_PATH"  # if reflection created
```

**MUST** validate:
- Frontmatter required fields (title, tags, type, created)
- Callout syntax (`[!note]`, `[!warning]`, etc.)
- WikiLink format and heading anchors

#### 4.3 Verification Checklist

**Documentation** (MUST verify):
- [ ] Daily session log created
- [ ] Cross-references ≥ 10 in daily log
- [ ] YAML frontmatter present

**Reflection Gate** (MUST verify):
- [ ] Phase 2.1 decision recorded
- [ ] If decision = required → reflection exists
- [ ] Reflection has ≥ 5 cross-references

**Quality** (MUST verify):
- [ ] No broken WikiLinks
- [ ] Code references include file paths and line numbers

**Syntax Validation** (MUST verify):
- [ ] `validate_obsidian_syntax.sh` exits with code 0 for daily log
- [ ] `validate_obsidian_syntax.sh` exits with code 0 for reflections (if created)

**Index Maintenance** (MUST verify):
- [ ] Obsidian Base indices regenerated for project
- [ ] Knowledge Bank index regenerated (`_meta/index.md`)
- [ ] Operation log entry appended (`_meta/log.md`)
- [ ] MOC Canvas updated (if MOC modified)

#### 4.4 MOC Updates (conditional)

**If new categories or significant content**: Add links to relevant MOC.

---

### Phase 5: MAINTAIN

**Goal**: Update knowledge bank indices and visualizations.

#### 5.1 Regenerate Obsidian Base Indices (MUST complete when new docs created)

**MUST** regenerate indices when new documents added to knowledge bank:
```bash
./scripts/generate_knowledge_base.sh --project "$PROJECT"
```

Generates queryable indices for concepts, components, practices, and sessions.

#### 5.2 Regenerate Knowledge Bank Index (MUST complete when new docs created)

Without this, newly created docs won't appear in `_meta/index.md` and knowledge-bank-lookup can't discover them via the unified catalog:
```bash
source skills/common/generate_index.sh
generate_index "$KB_PATH"
```

#### 5.3 Append Operation Log (MUST complete)

The operation log feeds kb-lint's staleness detection and provides an audit trail of what changed when:
```bash
source skills/common/obsidian_helpers.sh
append_kb_log "$KB_PATH" "ingest" "session-recap" "Created: [list created docs]. Updated: [list updated docs]"
```

#### 5.4 Update MOC Canvas (MUST complete when MOC modified)

**MUST** update canvas when MOC files modified:
```bash
./scripts/generate_moc_canvas.sh "$MOC_PATH"
```

Creates visual JSON Canvas representation of knowledge relationships.

---

## Scripts Reference

| Script | Purpose | Phase |
|--------|---------|-------|
| `parse_transcript.sh` | Extract data from session transcript | 1.2, 1.3 |
| `detect_session_sources.sh` | Detect ingestible references and artifacts | 1.4 |
| `detect_project.sh` | Auto-detect project from path | 1.2 (internal) |
| `search_cross_references.sh` | Find cross-reference targets | 2.2 |
| `detect_external_docs.sh` | Scan for investigation documents | 2.3 |
| `analyze_for_distillation.sh` | Analyze docs for distillation | 2.3 |
| `count_wikilinks.sh` | Count WikiLinks in document | 3 |
| `verify_session_recap.sh` | Final verification gate | 4.1 |
| `validate_obsidian_syntax.sh` | Validate Obsidian markdown syntax | 4.2 |
| `validate_cross_references.sh` | Check for broken WikiLinks | 4.3 |
| `verify_quality.sh` | Verify document quality | 4.3 |
| `generate_knowledge_base.sh` | Generate Obsidian Base indices | 5.1 |
| `generate_index.sh` | Regenerate `_meta/index.md` content catalog | 5.2 |
| `append_kb_log` | Append operation entry to `_meta/log.md` | 5.3 |
| `generate_moc_canvas.sh` | Create MOC visualization canvas | 5.4 |

---

## Completion Criteria

Session recap is complete when:

1. ✅ `verify_session_recap.sh` exits with code 0
2. ✅ Daily log created with ≥ 10 cross-references
3. ✅ Reflection created (if Phase 2.1 decision = required)
4. ✅ All documents have YAML frontmatter
5. ✅ No broken WikiLinks
6. ✅ Obsidian syntax validation passes
7. ✅ Knowledge bank indices updated (if new docs created)

**Only then declare**: "✅ Session Recap Complete"

---

## Resources

- [KB Schema](_meta/schema.md) — Unified conventions for all KB documents (document types, frontmatter, WikiLinks, naming)
- [Templates](references/templates.md)
- [Cross-Reference Guide](references/cross-reference-guide.md)
- [Quality Standards](references/quality-standards.md)
- [Completion Checklist](references/completion-checklist.md)
- [Common Mistakes](references/common-mistakes.md) — top 3: skipping reflections, insufficient cross-refs, premature completion
- [Decision Reference](references/completion-checklist.md) — when reflection is required, when to create each doc type
- [Distillation Guide](references/distillation-guide.md)
