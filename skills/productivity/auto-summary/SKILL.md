---
name: auto-summary
context: fork
skill: auto-summary
model: haiku
description: Batch populate summary fields using content analysis
tags: [activity/governance, domain/tooling, automation]
---

# /auto-summary

Batch populate the `summary` frontmatter field on notes where it is null or missing. The summary field is the highest-value AI triage field — it enables fast note discovery without reading full content.

## Usage

```
/auto-summary                    # Process all notes with null summary
/auto-summary <path>             # Process specific file or folder
/auto-summary --dry-run          # Preview summaries without applying
/auto-summary --type Concept     # Only process specific note type
/auto-summary --limit 50         # Process at most 50 notes
```

## Instructions

### Phase 1: Find Notes Needing Summary

Use Grep to find notes with null or missing summary:

```bash
# Find notes with summary: null
Grep for "summary: null" in *.md files

# Also find notes with no summary field at all
# (These should have had summary added by template cleanup)
```

Filter results:
- Exclude `Templates/`, `.obsidian/`, `.claude/`, `Archive/`, `Attachments/`
- Exclude Daily notes (journals don't need summaries)
- If `--type` specified, filter by frontmatter type
- Sort by type for batch efficiency

### Phase 2: Generate Summaries (Parallel)

Launch parallel Haiku sub-agents, batching 20 notes per agent:

For each note, the agent should:

1. **Read the full note** (frontmatter + body)
2. **Generate a one-line summary** following these rules:

#### Summary Writing Rules

- **Length:** 10-25 words. One sentence. No period at the end
- **Voice:** Active, descriptive. State what the note IS or DOES
- **Content:** Capture the core purpose, not details
- **Avoid:** Starting with "This note...", "A document about...", "Summary of..."
- **Include:** Key entities, technologies, or decisions where relevant

#### Summary Patterns by Type

| Type | Pattern | Example |
|------|---------|---------|
| Concept | What X is | `Continuous Airworthiness Management Organisation responsible for aircraft safety compliance` |
| Pattern | How to do X | `Event-driven architecture pattern using Kafka for real-time system integration` |
| Meeting | What was discussed/decided | `Alpha sprint review covering data migration progress and API blockers` |
| ADR | What was decided and why | `Selected AWS Bedrock over Azure OpenAI for AlertHub safety processing` |
| Project | What the project delivers | `SAP to DataPlatform data integration enabling unified engineering analytics` |
| System | What the system does | `MRO Vendor MRO platform managing aircraft maintenance scheduling` |
| Person | Role and context | `Solutions Architect in Engineering IT, Alpha project lead` |
| Task | What needs to be done | `Implement Kafka consumer for Alpha work order events` |
| Incubator | What idea is being explored | `Exploring voice-activated Claude Code workflows for hands-free note capture` |
| Research | What question was investigated | `Analysis of vault structure identifying efficiency improvements for human and AI workflows` |
| Reference | What the resource covers/teaches | `AWS documentation on Bedrock guardrails for AI model safety` |
| Email | What the email communicates | `Proposal to Beta programme board for Claude Code adoption across architecture team` |

3. **Return** — list of (filepath, summary) tuples

### Phase 3: Apply Summaries

For each note with a generated summary:

1. Read current frontmatter
2. If `summary: null` — replace with generated summary (quoted string)
3. If no summary field — add `summary:` field after tags
4. Write updated file using Edit tool

**Format:**
```yaml
summary: "Continuous Airworthiness Management Organisation responsible for aircraft safety compliance"
```

Always quote the summary value since it may contain special YAML characters (colons, brackets).

### Phase 4: Report

```markdown
## Auto-Summary Results

**Notes processed:** {{count}}
**Summaries added:** {{added_count}}
**Notes skipped:** {{skipped_count}} (already has summary or insufficient content)

### By Type
| Type | Summarised | Avg Length |
|------|-----------|------------|
| Concept | 45 | 15 words |
| Meeting | 80 | 18 words |
| ADR | 30 | 20 words |

### Sample Summaries
| Note | Summary |
|------|---------|
| {{note}} | {{summary}} |
| {{note}} | {{summary}} |
```

## Safety

- Always use `--dry-run` first for vault-wide operations
- Never overwrite existing non-null summaries
- Commit to git before running
- If note body is too short (<50 words), skip rather than guess
- Summary is additive only — never removes existing summaries

## Quality Checks

After running, verify quality by:
1. Spot-check 10-15 summaries across different types
2. Ensure summaries are accurate (not hallucinated)
3. Check length (10-25 words target)
4. Verify no YAML quoting issues

## Related Skills

- `/summarize` — Detailed single-note summarisation
- `/quality-report` — Includes summary coverage metrics
- `/auto-tag` — Companion batch field population skill
