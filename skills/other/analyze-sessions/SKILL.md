---
name: analyze-sessions
description: Analyze session logs to discover automation opportunities. Use periodically to find patterns in your Claude Code usage that could be automated. Use periodically after multiple sessions to find automation opportunities.
argument-hint: "[--project <name>] [--targets-only]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

Analyze recorded session data from ALL Claude Code projects to identify patterns and automation opportunities.

## Arguments

- `--project <name>` — Analyze only sessions from the named project (matches the `project` field, which is the basename of the working directory)
- `--targets-only` — Exclude toolkit sessions; only analyze target projects

## Data Location

Session logs are stored centrally in `~/.claude/logs/sessions.jsonl` in JSONL format (one compact JSON object per line).

Each entry contains:
```json
{"session_id":"...","timestamp":"2026-01-23T12:00:00Z","project":"project-name","cwd":"/path/to/project","transcript_path":"/path/to/transcript"}
```

The session-end-logger hook is installed at the user level (`~/.claude/hooks/session-end-logger.sh`) so it captures sessions from every project.

## Analysis Process

Copy this checklist and track progress:

```
Analyze Sessions Progress:
- [ ] Step 1: Read session logs
- [ ] Step 2: Calculate statistics (grouped by project)
- [ ] Step 3: Identify target projects
- [ ] Step 4: Analyze transcripts
- [ ] Step 5: Find automation opportunities
- [ ] Step 6: Cross-project insights
- [ ] Step 7: Generate report
```

### 1. Read Session Logs

Read `~/.claude/logs/sessions.jsonl` and parse all entries.

If `--project <name>` was given, filter to entries where `project` matches.
If `--targets-only` was given, identify toolkit projects (see step 3) and exclude them.

If the file doesn't exist or is empty:
```
NO SESSION DATA
===============
No sessions have been logged yet.

Session logging is installed at the user level (~/.claude/hooks/session-end-logger.sh).
Run a few Claude Code sessions in any project, then run /analyze-sessions again.

If the hook is not installed, run /install-hooks and select "session-end-logger".
```

### 2. Calculate Statistics (Grouped by Project)

```
SESSION ANALYSIS
================

Total sessions: {N}
Date range: {earliest} to {latest}
Unique projects: {count}

Sessions per project:
- {project1}: {count} sessions ({first_date} – {last_date})
- {project2}: {count} sessions ({first_date} – {last_date})
```

### 3. Identify Target Projects

Scan `~/Projects/` for directories containing `.claude/toolkit-version.json`.
These are toolkit target projects. All other projects are either the toolkit itself or standalone.

```
Project Classification:
  Toolkit: {toolkit project name}
  Target projects: {list of target project names}
  Other: {list of other project names}
```

### 4. Analyze Transcripts (If Available)

For each session with an accessible transcript_path:

1. Read the transcript file
2. Look for these patterns:

**Manual Interventions:**
- `AskUserQuestion` tool calls — Questions asked during sessions
- Text containing "manually", "by hand", "human must"
- Repeated similar questions across sessions

**Common Blockers:**
- Text containing "BLOCKED", "blocked", "waiting for"
- Error patterns that recur
- Missing credentials/env vars

**Tool Usage Patterns:**
- Count of each tool type used
- Sequences of tools that repeat

**Workflow Friction:**
- "cd" into directories (wrong directory issues)
- Repeated file lookups (missing context)
- Re-reading same files multiple times

### 5. Identify Automation Opportunities

Based on patterns found, identify:

**High Impact (Repeated across 3+ sessions):**
- Manual steps that could be automated with curl/Bash
- Questions that could be pre-answered in AGENTS.md
- Browser checks that could use Playwright

**Medium Impact (Repeated 2 times):**
- Verification steps that could be codified
- Setup steps that could be scripted

**Low Impact (Single occurrence but notable):**
- One-off manual interventions that might recur

### 6. Cross-Project Insights

Compare patterns across projects:

```
CROSS-PROJECT COMPARISON
========================

| Project | Sessions | Avg Questions/Session | Top Blocker | Autonomy Level |
|---------|----------|-----------------------|-------------|----------------|
| {proj}  | {N}      | {avg}                 | {blocker}   | {High/Med/Low} |

Autonomy Level = High (0-1 questions/session), Med (2-3), Low (4+)
```

Identify:
- Which projects need more AGENTS.md guidance (high question rate)
- Which projects have more context overflows (re-reading patterns)
- Common patterns that appear in multiple projects (shared automation opportunities)
- Skills from the toolkit that are underused in target projects

### 6b. Review Findings Before Writing

Before writing the report file, output a summary of key findings to the user:

```
SESSION ANALYSIS PREVIEW
========================
Sessions analyzed: {N}
Top patterns found: {count}

Key findings:
1. {finding 1}
2. {finding 2}
3. {finding 3}

Writing full report to .claude/logs/ANALYSIS_REPORT.md...
```

This gives the user visibility before the file is written.

### 7. Generate Report

Write analysis to `.claude/logs/ANALYSIS_REPORT.md` (in the toolkit):

```markdown
# Session Analysis Report

Generated: {timestamp}
Sessions analyzed: {N}
Date range: {earliest} to {latest}

## Summary

- Total sessions: {N}
- Projects: {list}
- Common patterns identified: {count}

## Per-Project Breakdown

### {Project Name} ({N} sessions)

**Type:** Toolkit | Target | Other
**Date range:** {first} – {last}
**Key patterns:**
- {pattern 1}
- {pattern 2}

## Cross-Project Insights

### Autonomy Levels
| Project | Sessions | Questions/Session | Autonomy |
|---------|----------|-------------------|----------|
| {proj}  | {N}      | {avg}             | {level}  |

### Shared Patterns
- {pattern that appears across multiple projects}

## Automation Opportunities

### High Priority

#### 1. {Pattern Name}
**Occurrences:** {N} sessions
**Projects:** {list of projects where this appears}
**Pattern:** {description of what keeps happening}
**Suggested Automation:**
- {specific automation approach}
- {implementation hint}

#### 2. {Pattern Name}
...

### Medium Priority

#### 1. {Pattern Name}
...

### Low Priority

#### 1. {Pattern Name}
...

## Recommended Actions

1. **Create new skill:** {skill name} — {what it would automate}
2. **Add to AGENTS.md:** {guidance to add}
3. **Create hook:** {hook description}

## Raw Statistics

### Questions Asked (AskUserQuestion)
| Question Pattern | Count | Projects |
|-----------------|-------|----------|
| {pattern} | {N} | {list} |

### Tools Used
| Tool | Total Uses | Avg per Session |
|------|------------|-----------------|
| {tool} | {N} | {avg} |

### Blockers Encountered
| Blocker Type | Count | Resolution |
|--------------|-------|------------|
| {type} | {N} | {how resolved} |
```

### 8. Output Summary

After writing the report:

```
ANALYSIS COMPLETE
=================

Analyzed: {N} sessions across {M} projects
Report: .claude/logs/ANALYSIS_REPORT.md

Key Findings:
- {top finding 1}
- {top finding 2}
- {top finding 3}

Cross-Project:
- {cross-project insight 1}
- {cross-project insight 2}

Recommended next steps:
1. Review .claude/logs/ANALYSIS_REPORT.md for full details
2. Consider creating skills for high-priority patterns
3. Update AGENTS.md with guidance for common questions
```

## Error Handling

**If `~/.claude/logs/` directory doesn't exist:**
- Create the directory structure: `mkdir -p ~/.claude/logs`
- Report that no sessions have been logged yet
- Suggest running /install-hooks to set up session logging

**If session log file is malformed:**
- Skip malformed lines and continue processing valid entries
- Report the count of skipped entries in the output
- Note: "X entries skipped due to malformed data"

**If transcript files are inaccessible:**
- Continue analysis without transcript data
- Mark transcript-dependent insights as "Limited (transcripts unavailable)"
- Report which transcripts couldn't be read

**If no patterns are found:**
- Report "No automation opportunities identified"
- Suggest that more sessions may be needed for meaningful patterns
- Provide guidance: "Run /analyze-sessions again after 5+ additional sessions"

**If ANALYSIS_REPORT.md cannot be written:**
- Output the report to the terminal instead
- Report the write failure with the specific error
- Suggest checking directory permissions

## Limitations

- Transcript files may not be accessible (permissions, deleted)
- Analysis quality depends on session data available
- Some patterns require human judgment to identify
- Cross-project analysis requires the user-level hook to be installed
