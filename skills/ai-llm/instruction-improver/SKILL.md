---
name: instruction-improver
description: >-
  Search memex for user feedback patterns (frustration, corrections, praise,
  successful outcomes) to identify recurring mistakes and wins, then generate
  CLAUDE.md or AGENTS.md improvements.
allowed-tools:
  - 'Bash(memex:*)'
---
# Instruction Improver

Mine conversation history for user feedback patterns (frustrations, corrections, praise, successes) and update CLAUDE.md files with learnings.

## End Goal

**The purpose of this skill is to update CLAUDE.md files.** Either:
- `~/.claude/CLAUDE.md` (user-level, applies to all projects)
- `.claude/CLAUDE.md` or `CLAUDE.md` (project-level, applies to current project)

**CRITICAL: Ask scope upfront.** Before doing any analysis, ask the user:

> Which CLAUDE.md would you like me to improve?
> 1. **User-level** (`~/.claude/CLAUDE.md`) - applies to all projects
> 2. **Project-level** (`.claude/CLAUDE.md` or `CLAUDE.md`) - applies to current project only
> 3. **Both** - analyze and propose changes for both files

This determines which file(s) to read, which patterns are relevant, and where to propose changes.

**CRITICAL:** Before making ANY changes to CLAUDE.md:
1. Ask the user which scope they want (user, project, or both)
2. Read the existing CLAUDE.md file(s) to understand current rules
3. Present findings and proposed additions to the user
4. Get explicit user approval before editing
5. Never duplicate or contradict existing rules

## Execution Strategy

Use a "leader + explorer" pattern with subagents:

1. **Leader (you):** Orchestrate the analysis, synthesize findings, propose changes
2. **Explore agents:** Spawn to search memex, fetch sessions, and gather evidence

Example flow:
```
Leader: "I'll analyze your conversation history for patterns. Launching explore agents..."
  -> Explore agent 1: Search for frustration patterns
  -> Explore agent 2: Search for positive patterns
  -> Explore agent 3: Read existing CLAUDE.md files
Leader: "Found 3 patterns. Here's what I propose to add to your user CLAUDE.md..."
Leader: "Do you approve these additions? [present changes]"
User: "Yes" / "No, change X"
Leader: [Makes approved edits]
```

## When to Use

- User asks to "learn from mistakes" or "improve CLAUDE.md"
- User wants to analyze past frustrations or corrections
- User asks what keeps going wrong in conversations
- User wants to see what's working well
- Proactively when noticing repeated patterns of correction or success

## Detection Terms

### Negative Signals (frustration, corrections)

**Strong frustration:**
- `fuck`, `fucking`, `ffs`, `wtf`, `shit`, `damn`, `crap`, `goddamn`
- `ugh`, `argh`, `smh`, `jfc`

**Corrections and negations:**
- `no,`, `no!`, `nope`, `wrong`, `incorrect`, `that's not`
- `I said`, `I meant`, `I already told you`, `I just said`
- `don't`, `stop`, `quit`, `never`, `not what I asked`

**Exasperation:**
- `again?`, `still?`, `why do you keep`, `how many times`
- `I've told you`, `we've been over this`, `for the nth time`
- `please just`, `can you just`, `just do`

**Disappointment:**
- `disappointing`, `frustrated`, `annoying`, `useless`
- `doesn't work`, `broken`, `failed`, `messed up`
- `you broke`, `you deleted`, `you removed`, `you changed`

### Positive Signals (praise, successful outcomes)

**Gratitude and approval:**
- `thanks`, `thank you`, `thx`, `ty`, `appreciated`
- `nice`, `great`, `awesome`, `perfect`, `excellent`
- `wow`, `amazing`, `impressive`, `love it`, `nailed it`
- `good job`, `well done`, `exactly`, `yes!`

**Successful completions:**
- `open pr`, `create pr`, `make pr`, `submit pr`
- `commit`, `push`, `merge`, `ship it`, `deploy`
- `lgtm`, `approved`, `looks good`

**Progress indicators:**
- `works`, `working`, `fixed`, `solved`, `done`
- `finally`, `got it`, `that's it`, `bingo`

## Search Commands

Use `memex search` to find patterns. Key options:

- `--role user` - filter to user messages only
- `--role assistant` - filter to assistant messages
- `--unique-session` - one result per session (dedup)
- `--top-n-per-session N` - limit N results per session
- `--limit N` - max total results
- `--project NAME` - filter by project
- `--source claude|codex` - filter by source
- `--since TIMESTAMP` - RFC3339 (2024-01-15T00:00:00Z) or unix seconds
- `--fields score,ts,session_id,snippet` - select output fields

Output is JSONL by default. Use `--json-array` for array format.

### Negative Searches

```bash
# Broad frustration sweep
memex search "fuck|shit|wtf|damn|wrong|no!" --role user --unique-session --limit 50

# Correction patterns
memex search "I said|I meant|I told you|that's not what" --role user --unique-session --limit 30

# Repetition complaints
memex search "again|still|keep doing|how many times" --role user --unique-session --limit 30

# Project-specific
memex search "wrong|no|stop" --project <project> --role user --limit 30

# Recent issues (use RFC3339 timestamp)
memex search "fuck|wrong|no" --since 2024-12-01T00:00:00Z --role user --unique-session --limit 30
```

### Positive Searches

```bash
# Praise and gratitude
memex search "thanks|awesome|perfect|great|nice" --role user --unique-session --limit 50

# Successful completions
memex search "open pr|commit|push|deploy|merge" --role user --unique-session --limit 30

# Approval signals
memex search "lgtm|looks good|exactly|yes!|nailed it" --role user --unique-session --limit 30

# Progress confirmations
memex search "works|working|fixed|solved|done" --role user --unique-session --limit 30

# Wow moments
memex search "wow|amazing|impressive|love it" --role user --unique-session --limit 20
```

## Project-Scoped Search Strategy

When the user selects **project-level** scope, you need to identify the current project name and filter searches accordingly.

### Finding the Project Name

The project name in memex corresponds to the directory path. To find it:

1. Check the current working directory
2. Use `memex search` with a broad query to see project names in results
3. Look for the project field in search output

```bash
# Find all projects with recent activity
memex search "the" --role user --limit 5 --fields project,session_id

# Search within a specific project (use the directory name)
memex search "wrong|no" --project khartoum-v2 --role user --limit 30
memex search "thanks|great" --project my-app --role user --limit 30
```

### Project-Specific Search Examples

```bash
# Frustrations in current project only
memex search "fuck|shit|wrong|no!" --project <PROJECT_NAME> --role user --unique-session --limit 50

# Corrections in current project
memex search "I said|I meant|that's not" --project <PROJECT_NAME> --role user --unique-session --limit 30

# Praise in current project
memex search "thanks|awesome|perfect" --project <PROJECT_NAME> --role user --unique-session --limit 50

# Stack-specific issues (e.g., for a Rust project)
memex search "cargo|rustc|borrow" --project <PROJECT_NAME> --role user --unique-session --limit 30
```

### Project vs User-Level Patterns

When analyzing project-level scope:
- Focus on patterns specific to this codebase (file structure, naming conventions)
- Look for stack-specific frustrations (language, framework, build tools)
- Identify project-specific workflows (deploy process, test commands)
- Find codebase-specific knowledge (where things are, how they connect)

When analyzing user-level scope:
- Search across ALL projects (omit `--project` flag)
- Look for behavioral patterns that repeat everywhere
- Identify universal tool preferences
- Find communication style issues

## Analysis Workflow

### Phase 1: Discovery (use Explore agents)

Launch parallel explore agents to:

1. **Search negative patterns** - frustration, corrections, complaints
2. **Search positive patterns** - praise, successful completions, approvals
3. **Read existing CLAUDE.md** - both user-level and project-level

**Important:** If user selected project-level scope, pass the project name to search agents so they use `--project <name>` in all searches.

Wait for all agents to complete before proceeding.

### Phase 2: Synthesis (leader)

1. **Review agent findings** - identify recurring themes
2. **Cross-reference with existing rules** - avoid duplicates
3. **Categorize by scope:**
   - User-level: general behaviors, universal preferences
   - Project-level: stack-specific, codebase-specific

### Phase 3: Proposal (leader -> user)

Present findings to user with:
- Summary of patterns found (positive and negative)
- Specific proposed additions for each CLAUDE.md
- Clear before/after showing where text will be added

**Ask for explicit approval before proceeding.**

### Phase 4: Update (leader, after approval)

1. Edit the approved CLAUDE.md file(s)
2. Show the user the final result
3. Suggest they restart Claude Code to pick up changes

## Output Format

### For Negative Patterns

```markdown
## Pattern: [Short description]

**Type:** negative
**Evidence:** [Number] occurrences found
**Sessions:** [List of session_ids]
**Example quote:** "[User's frustrated message]"

**What went wrong:**
[Description of the mistake]

**Suggested CLAUDE.md addition:**
```
[The actual text to add to CLAUDE.md]
```

**Scope:** [project|user] - where this should go
```

### For Positive Patterns

```markdown
## Pattern: [Short description]

**Type:** positive
**Evidence:** [Number] occurrences found
**Sessions:** [List of session_ids]
**Example quote:** "[User's praise or success message]"

**What went right:**
[Description of the successful behavior]

**Suggested CLAUDE.md addition:**
```
[The actual text to add to CLAUDE.md - reinforcing the good pattern]
```

**Scope:** [project|user] - where this should go
```

## Recommended CLAUDE.md Sections

Organize suggestions into these categories:

- **Code Guidelines** - coding mistakes (wrong patterns, breaking things)
- **Communication** - misunderstandings, not following instructions
- **Tool Usage** - wrong tools, destructive commands
- **Workflow** - process issues (committing too early, not testing)
- **Stack Preferences** - using wrong libraries/tools

## Example Analysis

### Negative Example

**Search:**
```bash
memex search "you deleted|you removed|you broke" --role user --unique-session --limit 20
```

**Finding:** 5 sessions where user complained about deleted code

**Suggested addition:**
```markdown
# Code Guidelines
- NEVER delete code unless explicitly asked. Comment it out or ask first.
- When refactoring, preserve all existing functionality unless told to remove it.
```

### Positive Example

**Search:**
```bash
memex search "wow|amazing|perfect" --role user --unique-session --limit 20
```

**Finding:** 8 sessions where user praised quick PR creation with good descriptions

**Suggested addition:**
```markdown
# Workflow
- When asked to create a PR, do it immediately without asking for confirmation.
- Write concise PR descriptions: summary bullets + test plan. No fluff.
```

## Fetching Full Context

After finding relevant hits, fetch full session transcripts:

```bash
# Get full session transcript (JSON)
memex session <session_id>

# Get single record by doc_id (JSON)
memex show <doc_id>

# Human-readable output
memex session <session_id> --verbose
memex show <doc_id> --verbose
```

## Tips

- Use `--unique-session` to avoid duplicate hits from same conversation
- Use `--top-n-per-session 2` for more context per session
- Fetch full session with `memex session <id>` when pattern is unclear
- Look for the assistant message BEFORE the frustrated user message
- Group related frustrations into single CLAUDE.md rules
- Prefer specific instructions over vague guidelines
- Include concrete examples in CLAUDE.md when helpful

## Scope Decision

When proposing changes, recommend the appropriate scope but **always ask the user** which file to update.

**User-level (~/.claude/CLAUDE.md):**
- General behavioral patterns (communication style, verbosity)
- Tool preferences that apply everywhere
- Universal coding practices
- Cross-project learnings

**Project-level (.claude/CLAUDE.md or CLAUDE.md):**
- Stack-specific preferences
- Project conventions and patterns
- Codebase-specific knowledge
- Team conventions

**When uncertain:** Default to user-level for behavioral rules, project-level for technical rules. But always confirm with the user.
