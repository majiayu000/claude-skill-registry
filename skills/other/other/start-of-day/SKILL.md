---
name: start-of-day
description: Comprehensive daily project sync - checks git repos, analyzes all code, reads documentation, and provides status report. Use when user says "start of day", "daily sync", "project status", or at beginning of work session.
---

# Start of Day - Universal Project Sync

This skill performs a comprehensive analysis of the **current working directory** to get you synced up at the start of each day. It works on any project.

## What This Skill Does

1. **Git Repository Check**
   - Detects if current directory is a git repo
   - Fetches and pulls latest changes if behind
   - Reports current branch and status
   - Shows recent commits

2. **Codebase Analysis**
   - Reads all key files in the project
   - Identifies tech stack and architecture
   - Reviews project structure
   - Identifies what's built vs pending

3. **Documentation Review**
   - Reads all markdown files
   - Reviews any documentation folders
   - Identifies action items and TODOs

4. **Status Report**
   - Git sync summary
   - Project overview
   - Key files and structure
   - Recommended next steps

## Execution Steps

### Step 1: Git Repository Check

Check if the current working directory (or any subdirectories) contains git repos:

```bash
# Check if current directory is a git repo
git status 2>/dev/null

# If it's a repo, fetch and check status
git fetch origin 2>/dev/null
git status -sb

# Check if behind remote
git rev-list HEAD..@{u} --count 2>/dev/null

# Pull if behind
git pull

# Show recent commits
git log --oneline -10
```

If the current directory is not a git repo, check subdirectories for git repos and report on each.

### Step 2: Read Project Files

Read key files to understand the project:

1. **Configuration files** (use Glob to find, then Read):
   - `package.json`, `requirements.txt`, `Cargo.toml`, etc.
   - `.env.example`, config files
   - `README.md`, `CONTRIBUTING.md`

2. **Source code structure** (use Glob):
   - Find main entry points
   - Identify src/lib/app directories
   - Map out the project structure

3. **Documentation** (use Glob + Read):
   - All `*.md` files
   - Any `docs/` folder contents
   - Implementation plans, specs

### Step 3: Codebase Exploration

Use the **Explore agent** to thoroughly analyze the codebase:
- Technology stack (frameworks, languages)
- Project architecture
- Key components and their purposes
- Dependencies and their versions
- What's implemented vs TODO comments

### Step 4: Generate Report

Provide a structured report:

#### A. Git Status
- Current branch
- Sync status (up to date / pulled X commits)
- Recent commits
- Any uncommitted changes

#### B. Project Overview
- Tech stack
- Project structure
- Key files and entry points
- Dependencies

#### C. Documentation Summary
- Key docs found
- Important notes
- TODOs and action items

#### D. Recommended Next Steps
- What to focus on
- Pending work identified
- Any issues to address

## Tool Usage

This skill uses:
- `Bash` - For git operations
- `Glob` - To find files by pattern
- `Read` - To read file contents
- `Task` with `Explore` agent - For deep code analysis
- `TodoWrite` - To track analysis progress

## Important Notes

- **Works on current directory** - No hardcoded paths
- **Adapts to any project** - Detects project type automatically
- **Pulls git updates** - Keeps you in sync with remote
- **Reads all relevant files** - Builds full context

## Activation Triggers

This skill activates when user says:
- "start of day"
- "daily sync"
- "start the day"
- "project status"
- "sync me up"
- "get me up to speed"
