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

1. **During your work session**: Note down the session path displayed at startup
   - Claude Code shows: `Session: /path/to/.claude/projects/.../session-id.jsonl`
   - Save this path for later

2. **Exit the work session**: The final transcript is automatically saved

3. **Start a new session**: Begin fresh to run the recap
   ```
   claude
   ```

4. **Invoke session-recap with the path**:
   ```
   Recap the session at /path/to/session-id.jsonl
   ```
   Or:
   ```
   /second-brain:session-recap /path/to/session-id.jsonl
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

## Quick Reference

| Input | Output |
|-------|--------|
| Session folder path | Daily log + extracted docs |
| Current conversation | Daily log + extracted docs |

| Document Type | Cross-Refs Required |
|---------------|-------------------|
| Technical docs | 10-15 (MUST) |
| Reflections | 5-8 (MUST) |

---

## RFC 2119 Keywords

This skill uses RFC 2119 keywords:
- **MUST**: Absolute requirement, cannot be skipped
- **SHOULD**: Valid exceptions may exist but require conscious weighing
- **MAY**: Truly optional

---

## Workflow

### Phase 1: ANALYZE

**Goal**: Load session data and extract facts.

#### 1.1 Load Session Data

**If session folder provided**:
```bash
# Find latest segment
LATEST_SEGMENT=$(ls -d "$SESSION_FOLDER"/segment-* 2>/dev/null | grep -v 'segment-final' | sort -t- -k2 -n | tail -1)
[ -z "$LATEST_SEGMENT" ] && [ -d "$SESSION_FOLDER/segment-final" ] && LATEST_SEGMENT="$SESSION_FOLDER/segment-final"

# Read transcript
TRANSCRIPT="$LATEST_SEGMENT/transcript.jsonl"
```

**If no folder**: Analyze current conversation context.

#### 1.2 Detect Project

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

#### 2.4 Insight Classification (SHOULD complete when insights exist)

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
4. **Process reflections** - **MUST if Phase 2.1 decision = required** OR insight reveals workflow/anti-pattern
5. **Daily session log** - MUST (always required, includes all insights)

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
---
```

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

#### 5.2 Update MOC Canvas (MUST complete when MOC modified)

**MUST** update canvas when MOC files modified:
```bash
./scripts/generate_moc_canvas.sh "$MOC_PATH"
```

Creates visual JSON Canvas representation of knowledge relationships.

---

## Decision Reference

### When Reflection is REQUIRED

| Session Characteristic | Reflection Required |
|-----------------------|-------------------|
| Debugging occurred | MUST |
| Problem-solving with investigation | MUST |
| New pattern discovered | MUST |
| Workflow friction encountered | SHOULD |
| Simple file edits only | MAY skip |
| Documentation-only changes | MAY skip |

### When to Create Each Document Type

| Document Type | Create When |
|---------------|-------------|
| Concept | New pattern/principle discovered |
| Component | New class/interface/behavior documented |
| Best Practice | Reusable methodology identified |
| Reflection | See decision gate above |
| Daily Log | Always (every session) |

---

## Scripts Reference

| Script | Purpose | Phase |
|--------|---------|-------|
| `parse_transcript.sh` | Extract data from session transcript | 1.2, 1.3 |
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
| `generate_moc_canvas.sh` | Create MOC visualization canvas | 5.2 |

---

## Common Mistakes

### Mistake 1: Skipping Reflections

**Symptom**: Only technical docs created, no reflections.
**Cause**: Treating "OPTIONAL" as "skip if unsure".
**Fix**: Complete Phase 2.1 decision gate explicitly.

### Mistake 2: Insufficient Cross-References

**Symptom**: Document has < 10 WikiLinks.
**Cause**: Skipping cross-reference discovery.
**Fix**: Run `search_cross_references.sh` before writing.

### Mistake 3: Premature Completion

**Symptom**: Declaring done without verification.
**Cause**: Not running Phase 4 checklist.
**Fix**: MUST run `verify_session_recap.sh` before declaring complete.

See [common-mistakes.md](references/common-mistakes.md) for full list.

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

- [Templates](references/templates.md)
- [Cross-Reference Guide](references/cross-reference-guide.md)
- [Quality Standards](references/quality-standards.md)
- [Completion Checklist](references/completion-checklist.md)
- [Common Mistakes](references/common-mistakes.md)
- [Distillation Guide](references/distillation-guide.md)
