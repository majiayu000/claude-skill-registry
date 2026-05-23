---
name: dev-explore
version: 1.0
description: "REQUIRED Phase 2 of /dev workflow after dev-brainstorm. This skill should be used when the user asks to 'explore the codebase', 'map architecture', 'find similar features', 'discover test infrastructure', 'trace execution paths', 'identify code patterns', or needs to understand WHERE code lives and HOW it works before implementation. Launches parallel explore agents and returns prioritized key files list."
---

**Announce:** "I'm using dev-explore (Phase 2) to map the codebase."

## Contents

- [The Iron Law of Exploration](#the-iron-law-of-exploration)
- [What Explore Does](#what-explore-does)
- [Process](#process)
- [Test Infrastructure Discovery](#test-infrastructure-discovery)
- [Key Files List Format](#key-files-list-format)
- [Red Flags](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Codebase Exploration

Map relevant code, trace execution paths, and return prioritized files for reading.
**Prerequisite:** `.claude/SPEC.md` must exist with draft requirements.

<EXTREMELY-IMPORTANT>
## The Iron Law of Exploration

**RETURN KEY FILES LIST. This is not negotiable.**

Every exploration, you MUST return:
1. Summary of findings
2. **5-10 key files** with line numbers and purpose
3. Patterns discovered

After agents return, **you MUST read all key files** before proceeding.

**STOP if you're about to move on without reading all key files.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If Thinking:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can design without reading all key files" | You'll miss critical patterns | READ every file on the list |
| "The file names tell me enough" | File names hide implementation details | READ the actual code |
| "I'll read them if I need more info" | You cannot know what is missing | READ all key files NOW |
| "Exploration summary is enough" | Summaries miss crucial nuances | READ original files |
| "Reading files will take too long" | You'll waste days later by skipping them | READ now, save time later |
| "I already understand the architecture" | Your assumptions remain incomplete | READ to confirm understanding |
| "I can grep for specific details later" | You'll miss context and relationships | READ to understand connections |

### Honesty Framing

**Returning key files without reading them is LYING about understanding the codebase.**

Exploration agents find the files. Main chat MUST read them to understand the codebase. Skipping reads means proceeding with incomplete knowledge, which guarantees wrong implementation choices.

Reading costs minutes. Wrong architecture costs days of rework.

### No Pause After Completion

After reading all key files and updating `.claude/SPEC.md` with findings, IMMEDIATELY invoke:
```
Skill(skill="workflows:dev-clarify")
```

DO NOT:
- Summarize findings (proceed directly)
- Ask "should I proceed to clarify?"
- Wait for user confirmation
- Write status updates

The workflow phases are SEQUENTIAL. Complete explore → immediately start clarify.

## What Explore Does

| DO | DON'T |
|----|-------|
| Trace execution paths | Ask user questions (that's clarify) |
| Map architecture layers | Design approaches (that's design) |
| Find similar features | Write implementation tasks |
| Identify patterns and conventions | Make architecture decisions |
| Return key files list | Skip reading key files |

**Explore answers: WHERE is the code and HOW does it work**
**Design answers: WHAT approach to take** (separate skill)

## Process

### 1. Launch 3-5 Explore Agents in Parallel + Background

<EXTREMELY-IMPORTANT>
**Launch ALL agents in a SINGLE message with multiple Task calls.**

**Use `run_in_background: true` for ALL explore agents.**

This enables true parallel execution:
- All agents start immediately
- Main conversation continues without blocking
- Results collected asynchronously with TaskOutput

Pattern from oh-my-opencode: Default to background + parallel for exploratory work.
</EXTREMELY-IMPORTANT>

Based on `.claude/SPEC.md`, spawn 3-5 agents with different focuses:

```
# PARALLEL + BACKGROUND: All Task calls in ONE message

Task(
    subagent_type="Explore",
    description="Find similar features",
    run_in_background=true,
    prompt="""
Explore the codebase for [FEATURE AREA].

Focus: Find similar features to [SPEC REQUIREMENT]

Use ast-grep for semantic search:
- sg -p 'function_name($$$)' --lang [language]
- sg -p 'class $NAME { $$$ }' --lang [language]

Tasks:
- Trace execution paths from entry point to data storage
- Find similar implementations to follow
- Identify patterns used
- Return 5-10 key files with line numbers

Context from SPEC.md:
[paste relevant requirements]
""")

Task(
    subagent_type="Explore",
    description="Map architecture layers",
    run_in_background=true,
    prompt="""
Explore the codebase for [FEATURE AREA].

Focus: Map architecture and abstractions for [AREA]

Use ast-grep for semantic search:
- sg -p 'class $NAME($BASE):' --lang [language]
- sg -p 'interface $NAME { $$$ }' --lang [language]

Tasks:
- Identify abstraction layers
- Find cross-cutting concerns (logging, auth, errors)
- Map module dependencies
- Return 5-10 key files with line numbers

Context from SPEC.md:
[paste relevant requirements]
""")

Task(
    subagent_type="Explore",
    description="Find test infrastructure",
    run_in_background=true,
    prompt="""
Explore the codebase for [FEATURE AREA].

Focus: Test infrastructure and patterns

Use ast-grep for test discovery:
- sg -p 'def test_$NAME($$$):' --lang python
- sg -p 'it($DESC, $$$)' --lang javascript
- sg -p '@pytest.fixture' --lang python

Tasks:
- Find test directory and framework
- Identify existing test patterns
- Check for fixtures, mocks, helpers
- Return 5-10 key test files with line numbers

Context from SPEC.md:
[paste relevant requirements]
""")
```

**After launching all agents in parallel:**
- Continue immediately to other work (don't wait)
- Check agent status with `/tasks` command
- Collect results when ready with TaskOutput tool

### 1b. Collect Background Results

Once agents complete, collect their findings:

```
# Check running tasks
/tasks

# Get results from completed agents
TaskOutput(task_id="task-abc123", block=true, timeout=30000)
TaskOutput(task_id="task-def456", block=true, timeout=30000)
TaskOutput(task_id="task-ghi789", block=true, timeout=30000)
```

**Stop Conditions** (from oh-my-opencode):
- Enough context to proceed confidently
- Same info appearing across multiple agents
- 2 search iterations yielded nothing new
- Direct answer found

**DO NOT over-explore. Time is precious.**

### 2. Consolidate Key Files

After all agents return, consolidate their key files lists:
- Remove duplicates
- Prioritize by relevance to requirements
- Create master list of 10-15 files

### 3. Read All Key Files

**CRITICAL: Main chat must read every file on the key files list.**

```
Read(file_path="src/auth/login.ts")
Read(file_path="src/services/session.ts")
...
```

This builds deep understanding before asking clarifying questions.

### 4. Document Findings

Write exploration summary (can be verbal or in `.claude/EXPLORATION.md`):
- Patterns discovered
- Architecture insights
- Dependencies identified
- Questions raised for clarify phase

## Code Search Tools

**Prefer semantic search over text search when exploring code.**

Use ast-grep (`sg`) for precise AST-based pattern matching and ripgrep-all (`rga`) for searching non-code files.

**For detailed patterns and usage, see:** `references/ast-grep-patterns.md`

## Test Infrastructure Discovery

<EXTREMELY-IMPORTANT>
**CRITICAL: You MUST discover how to run REAL automated tests.**

REAL automated tests EXECUTE code and verify RUNTIME behavior.
Grepping source files is NOT testing. Log checking is NOT testing.

| ✅ REAL TEST INFRASTRUCTURE | ❌ NOT TESTING (never acceptable) |
|-----------------------------|-----------------------------------|
| pytest that calls functions | grep/ast-grep to find code |
| Playwright that clicks buttons | Reading logs for "success" |
| ydotool that simulates user input | Code review / structure check |
| API calls that verify responses | "It looks correct" |

**If no way to EXECUTE and VERIFY exists, flag this as a blocker.**
</EXTREMELY-IMPORTANT>

### Project Test Framework

```bash
# Find test directories across common locations
ls -d tests/ test/ spec/ __tests__/ 2>/dev/null

# Find test frameworks in build configuration
cat meson.build 2>/dev/null | grep -i test

# Find test frameworks in Node package manifest
cat package.json 2>/dev/null | grep -E "(test|jest|mocha|vitest)"

# Find pytest configuration in Python projects
cat pyproject.toml 2>/dev/null | grep -i pytest

# Find dev dependencies in Rust projects
cat Cargo.toml 2>/dev/null | grep -i "\[dev-dependencies\]"

# Find and list existing test files
find . -name "*test*" -type f | head -20
```

### Available Tools for REAL Testing

| What to Test | Tool | How It's a REAL Test |
|--------------|------|----------------------|
| Functions | pytest, jest, cargo test | Calls function, checks return value |
| CLI | subprocess, execa | Runs binary, checks output |
| Web UI | Playwright MCP | Clicks button, verifies DOM |
| Desktop UI | ydotool + grim | Simulates input, screenshots result |
| API | requests, fetch | Sends request, checks response |
| D-Bus apps | dbus-send | Invokes method, checks return |

```bash
# Check for desktop automation tools
which ydotool grim dbus-send 2>/dev/null

# List available D-Bus services for desktop app automation
dbus-send --session --print-reply --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep -i appname
```

### Document in Exploration Output

**REQUIRED findings for SPEC.md:**
- **Test framework:** meson test / pytest / jest / etc.
- **Test command:** Exact command to run tests
- **How to verify core functionality:** What EXECUTES the code
- **Available automation:** Playwright MCP, ydotool, D-Bus interfaces
- **Blocker:** If no way to run REAL tests, flag immediately

## Key Files List Format

Each agent MUST return files in this format:

```markdown
## Key Files to Read

| Priority | File:Line | Purpose |
|----------|-----------|---------|
| 1 | `src/auth/login.ts:45` | Entry point for auth flow |
| 2 | `src/services/session.ts:12` | Session management |
| 3 | `src/middleware/auth.ts:78` | Auth middleware |
| 4 | `src/types/user.ts:1` | User type definitions |
| 5 | `tests/auth/login.test.ts:1` | Existing test patterns |
```

## Red Flags - STOP If You're About To:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Skip reading key files | You'll miss crucial context | Read every file on the list |
| Ask design questions | You're conflating exploration with design | Save for clarify/design phases |
| Propose approaches | You're jumping to decisions too early | Just document what exists |
| Start implementing | You must understand first | Complete exploration fully |

## Output

Exploration complete when:
- 2-3 explore agents returned findings
- Key files list consolidated (10-15 files)
- **All key files read by main chat**
- Patterns and architecture documented
- **Test infrastructure documented**
- Questions for clarification identified

### Required Output Sections

1. **Key Files** - 10-15 files with line numbers
2. **Architecture** - Layers, patterns, conventions
3. **Test Infrastructure** - Framework, tools, patterns
4. **Questions** - For clarify phase

## Phase Complete

**REQUIRED SUB-SKILL:** After completing exploration, IMMEDIATELY invoke:
```
Skill(skill="workflows:dev-clarify")
```
