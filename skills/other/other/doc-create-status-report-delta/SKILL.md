---
name: doc-create-status-report-delta
description: "{{ 𝚫𝚫𝚫 }} Create a status report that knows what you've done since the last one"
model: haiku
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(git:*)"]
---

<task overview="Generate a project status report by analyzing the current state of the codebase, roadmaps, and recent work." destination="docs/status-reports/" >
<filename format="{PROJECT-REPORT-NUMBER}_{YY-MM-DD-HHMM}_{RECENT}.md" example="003_26-01-13-1545_xml-validation-added.md" >
| Component | Description | Example |
|-----------|-------------|---------|
| PROJECT-REPORT-NUMBER | 3-digit incrementing number across all reports | `001`, `002`, `015` |
| YY-MM-DD-HHMM | Date and time (24hr) | `26-01-13-1430` |
| RECENT | Most significant change, max 3 words, kebab-case | `csv-parser-complete` |
To determine PROJECT-REPORT-NUMBER, check existing reports in the output directory.
</filename>
<instructions>
1. **Read the roadmap** at `docs/roadmaps/mvp.md` to understand milestones and progress
2. **Check recent work records** in `docs/dev-log/work-records/` for recent activity
3. **Review git history** for recent commits and changes
4. **Identify blockers** from any TODO comments, failing tests, or documented issues
5. **Read the previous status report** in `docs/dev-log/status-reports/` to understand what was last reported as completed, in progress, and upcoming
</instructions>
<output-format template-path="~/.claude/doc-templates/status-report.md">
Report should exactly mirror template structure.
</output-format>
<guidelines>
- **Audience**: One dev, one non-dev - explain capabilities, not implementation
- **Section 1 (What Happened)**: 2-3 sentences, big picture narrative
- **Section 2 (Shipped)**: 3-5 concrete deliverables described by what they do
- **Section 3 (Currently Working On)**: Honest about current state, no percentages
- **Section 4 (Up Next)**: 2-4 items, acknowledge uncertainty
- **Section 5 (Worth Remembering)**: Include meaningful context - decisions, dead ends, learnings
- Group related work (e.g. "CSV parser with validation and tests")
- Avoid jargon - explain technical terms when used (e.g. "API endpoints (web addresses the app uses)")
- No sub-bullets or nested lists
- Use British English
</guidelines>
</task>
