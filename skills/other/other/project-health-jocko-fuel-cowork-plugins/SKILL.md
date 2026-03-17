---
name: project-health
description: Assess health and structure of a Jocko Fuel project
user-invocable: true
---

You are helping the user assess the health of a Jocko Fuel project in the Claude Code workspace.

Follow these steps:

### Step 1: Identify the Project

Ask the user which project to assess. If not specified, use the current working directory. Valid projects are in `/Users/gd/Documents/Agents/ClaudeCode/`.

### Step 2: Run Health Checks

Evaluate the project against these criteria:

**Structure**
- Does `CLAUDE.md` exist and reference `@AGENTS.md`?
- Does `AGENTS.md` exist with proper navigation content?
- Is the file count at root level reasonable (< 15 files)?
- Are there temporal naming anti-patterns (NEW_, V2_, UPDATED_)?

**Git Status**
- Is the project on the main branch?
- Are there uncommitted changes?
- Is the local branch up to date with remote?

**Dependencies**
- If Python: does `pyproject.toml` exist with `uv.lock`?
- If Node: does `package.json` exist with lock file?
- Are there stale or missing dependencies?

**Testing**
- Do test files exist?
- Is there a test runner configured?

**Documentation**
- Are ABOUTME headers present on source files?
- Is README.md present and current?

### Step 3: Score and Report

Present findings as:

| Category | Score | Issues |
|----------|-------|--------|
| Structure | Pass/Warn/Fail | Details |
| Git | Pass/Warn/Fail | Details |
| Dependencies | Pass/Warn/Fail | Details |
| Testing | Pass/Warn/Fail | Details |
| Documentation | Pass/Warn/Fail | Details |

### Step 4: Recommendations

List specific, actionable fixes ranked by priority. Reference the project-structure rules from `CLAUDE.md` where relevant.

### Error Handling

- If the project path doesn't exist, show available projects from the root directory
- If git commands fail, note the issue but continue with other checks
