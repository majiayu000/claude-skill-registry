---
name: ipps-deep-research
description: Apply when conducting deep research on technologies, APIs, frameworks, or other software development topics requiring systematic investigation
---

# Deep Research Skill

Systematic research patterns for in-depth investigation of software development topics.

## Table of Contents

**Core**
- [When to Use](#when-to-use)
- [MUST-NOT-FORGET](#must-not-forget)
- [Output Format](#output-format)

**Patterns**
- [MEPI vs MCPI](#mepi-vs-mcpi) - When to use quick vs exhaustive research
- [Source Hierarchy](#source-hierarchy) - Priority order for sources
- [Verification Labels](#verification-labels) - How to mark claims

**Strategies**
- [Technology/API Research (MCPI)](RESEARCH_STRATEGY_TECH_MCPI.md) - 6-phase exhaustive documentation
- [Quick Research (MEPI)](#research-strategies) - Abbreviated approach for low-stakes

**Planning & Tracking**
- [Planning Structure](#planning-structure) - STRUT vs TASKS
- [Time Tracking](#time-tracking) - Net research time calculation

**Reference**
- [Tool Reference](RESEARCH_TOOLS.md) - Source collection, PDF processing, transcription
- [Source ID Format](#source-id-format) - How to cite sources
- [File Naming Conventions](#file-naming-conventions) - Prefix rules for documents

## When to Use

**Deep research (this skill):**
- "Should we use X or Y for our project?"
- "How does X work internally?"
- "What are the production considerations for X?"
- Multi-source synthesis required
- Exhaustive documentation needed

**Quick lookup (not this skill):**
- "What's the syntax for X?"
- "How do I install Y?"
- Single-source answers

## MUST-NOT-FORGET

- Start with assumptions check - write down what you think you know before researching
- Primary sources > secondary sources > community opinions
- Document all sources with URLs and access dates
- Flag information age (APIs change rapidly)
- Distinguish facts from opinions from assumptions
- Version-match community sources to subject version
- Create INFO document for findings
- **Always create STRUT** for research session orchestration
- **Track time** - log task start/end for net research time calculation
- **Track credits** - detect model via screenshot, log switches, calculate usage
- **Never auto-switch models** - respect user's model selection throughout research

## Global Patterns

### MEPI vs MCPI

**MEPI** (Most Executable Point of Information) - Default
- Present 2-3 curated options
- Filter and recommend
- Use for: reversible decisions, time-constrained, action-oriented

**MCPI** (Most Complete Point of Information) - Exception
- Present exhaustive options
- Document everything
- Use for: irreversible decisions, high-stakes, archival reference

### Source Hierarchy

1. **Official PDFs/papers** - Legislation, specs, whitepapers, academic papers (often not available as web)
2. **Official documentation** - Authoritative, version-specific
3. **Official blog/changelog** - Announcements, rationale
4. **GitHub repo** - Source code, issues, PRs, discussions
5. **Conference talks by maintainers** - Design decisions, roadmap
6. **Reputable tech blogs** - Analysis, comparisons
7. **Stack Overflow** - Specific problems (verify currency)
8. **Community forums/Discord** - Anecdotes, edge cases

**Source Persistence**: Download and store all sources in session folder for later reference. Web content changes - PDFs and local copies ensure reproducibility.

### Verification Labels

- `[VERIFIED]` - Confirmed from official documentation
- `[ASSUMED]` - Inferred but not explicitly stated
- `[TESTED]` - Manually tested by running code
- `[PROVEN]` - Confirmed from multiple independent sources
- `[COMMUNITY]` - Reported by community sources (cite source ID)

### Source ID Format

```
[TOPIC]-IN01-SC-[SOURCE]-[DOCNAME]
```

Examples:
- `GRPH-IN01-SC-MSFT-APIOVERVIEW` - Microsoft Graph official docs
- `GRPH-IN01-SC-SO-RATELIMIT` - Stack Overflow rate limit discussion
- `GRPH-IN01-SC-GH-ISSUE1234` - GitHub issue #1234

### File Naming Conventions

- `__` prefix (double underscore): Master/index documents (SOURCES, TOC, TEMPLATE)
- `_` prefix (single underscore): Topic content files (INFO documents)
- No prefix: Tracking files (TASKS, NOTES, PROBLEMS, PROGRESS)

### Information Currency

- Note version numbers for all API/library info
- Check last updated date on documentation
- Cross-reference with changelog for breaking changes
- Mark stale info with `[STALE: YYYY]` tag

## Research Strategies

Available research strategies (each has its own file):

- **Technology/API Research (MCPI)** - [RESEARCH_STRATEGY_TECH_MCPI.md](RESEARCH_STRATEGY_TECH_MCPI.md) - Exhaustive API/framework documentation

**Quick research (MEPI-style) until full strategy implemented:**
For reversible/low-stakes decisions, use abbreviated approach:
1. Phase 1 (Preflight): 5-10 sources max, skip community deep-dive
2. Skip Phases 2-4 (no TOC, template, or TASKS)
3. Phase 5: Create single `_INFO_[TOPIC].md` with findings
4. Phase 6: Quick `/verify`, done

Future strategies (not yet implemented):
- Technology Research (MEPI) - Quick technology evaluation
- Decision Research - Choose between options
- Problem-Solving Research - Debug and fix issues

## Tool Reference

See [RESEARCH_TOOLS.md](RESEARCH_TOOLS.md) for:
- Source collection tools (search_web, read_url_content, Playwright)
- Document processing tools (pdf-tools)
- Transcription tools (llm-transcription)
- Tool selection flowchart
- Common workflows

## Planning Structure

**STRUT** (high-level orchestration) - REQUIRED for all research:
- Tracks phases, objectives, deliverables, transitions
- Contains time log for net research time
- Created at research start, updated at phase transitions
- File: `STRUT_[TOPIC].md` in session folder

**TASKS** (low-level execution) - Created in Phase 4:
- Flat list of individual research tasks with durations
- Each task: file to create, sources to use, done-when criteria
- Tracks task timing: `[HH:MM-HH:MM]` per task
- File: `TASKS.md` in session folder

## Time Tracking

**Net research time** = active work time, excluding pauses.

**STRUT time log format:**
```
## Time Log
Started: 2026-01-30 09:00
Ended: 2026-01-30 14:30

Active intervals:
- 09:00-10:30 (Phase 1-3)
- 11:00-12:15 (Phase 4-5)
- 13:00-14:30 (Phase 5-6)

Net research time: 4h 15m
```

**TASKS timing format:**
```
- [x] TK-01: Research auth [10:00-10:45] 45m
- [x] TK-02: Research limits [10:15-11:00] 45m (parallel)
```

**Rules:**
- Pause detection: Gap > 30min in file timestamps = pause (don't count)
- Parallel tasks: Overlapping intervals count once, not doubled
- Log start time when beginning task, end time when completing

## Credit Tracking (Mandatory)

**Workflow:**
1. At phase start: `simple-screenshot.ps1` → detect model from Windsurf header
2. Lookup cost in `windsurf-model-registry.json`
3. Log model + timestamp in STRUT Credit Tracking section
4. At session end: calculate total estimated credits

**STRUT Credit Tracking format:**
```
## Credit Tracking
Phase 1: Claude Opus 4.5 (Thinking) [5x] - 09:00
Phase 2: Claude Opus 4.5 (Thinking) [5x] - 09:30
Phase 4: Claude Sonnet 4.5 [2x] - 10:15 (user switched)
Phase 5: Claude Sonnet 4.5 [2x] - 10:45
Phase 6: Claude Sonnet 4.5 [2x] - 11:30

Estimated credits: (2 phases × 5x) + (3 phases × 2x) = 16 units
```

**Rules:**
- **Never auto-switch models** - respect user's model selection
- Detect via screenshot only - passive observation
- Log when model changes (user-initiated)
- Registry: `[DEVSYSTEM_FOLDER]/skills/windsurf-auto-model-switcher/windsurf-model-registry.json`

## Output Format

Deep research outputs an INFO document. Key sections:

1. **Research Question** - What we're investigating
2. **Key Findings** - MEPI-style summary (2-3 main points) or MCPI exhaustive list
3. **Detailed Analysis** - Full investigation results
4. **Limitations and Known Issues** - From community sources
5. **Sources** - All references with quality indicators
6. **Recommendations** - Actionable conclusions

## Usage

1. Determine research type (MEPI quick vs MCPI exhaustive)
2. Read this SKILL.md for core principles
3. Read the appropriate strategy file
4. Read RESEARCH_TOOLS.md for tool guidance
5. Follow the strategy's phases systematically
6. Output findings as INFO document
