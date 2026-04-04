---
name: ccs-delegation
description: >-
  Auto-activate CCS CLI delegation for deterministic tasks. Parses user input,
  auto-selects optimal profile (glm/kimi/custom) from ~/.ccs/config.json,
  enhances prompts with context, executes via `ccs {profile} -p "task"` or
  `ccs {profile}:continue`, and reports results. Triggers on "use ccs [task]"
  patterns, typo/test/refactor keywords. Excludes complex architecture,
  security-critical code, performance optimization, breaking changes.
version: 3.0.0
---

# CCS Delegation

Delegate deterministic tasks to cost-optimized models via CCS CLI.

## Core Concept

Execute tasks via alternative models using:
- **Initial delegation**: `ccs {profile} -p "task"`
- **Session continuation**: `ccs {profile}:continue -p "follow-up"`

**Profile Selection:**
- Auto-select from `~/.ccs/config.json` via task analysis
- Profiles: glm (cost-optimized), kimi (long-context/reasoning), custom profiles
- Override: `--{profile}` flag forces specific profile

## User Invocation Patterns

Users trigger delegation naturally:
- "use ccs [task]" - Auto-select best profile
- "use ccs --glm [task]" - Force GLM profile
- "use ccs --kimi [task]" - Force Kimi profile
- "use ccs:continue [task]" - Continue last session

**Examples:**
- "use ccs to fix typos in README.md"
- "use ccs to analyze the entire architecture"
- "use ccs --glm to add unit tests"
- "use ccs:continue to commit the changes"

## Agent Response Protocol

**For `/ccs [task]`:**

1. **Parse override flag**
   - Scan task for pattern: `--(\w+)`
   - If match: `profile = match[1]`, remove flag from task, skip to step 5
   - If no match: continue to step 2

2. **Discover profiles**
   - Read `~/.ccs/config.json` using Read tool
   - Extract `Object.keys(config.profiles)` → `availableProfiles[]`
   - If file missing → Error: "CCS not configured. Run: ccs doctor"
   - If empty → Error: "No profiles in config.json"

3. **Analyze task requirements**
   - Scan task for keywords:
     - `/(think|analyze|reason|debug|investigate|evaluate)/i` → `needsReasoning = true`
     - `/(architecture|entire|all files|codebase|analyze all)/i` → `needsLongContext = true`
     - `/(typo|test|refactor|update|fix)/i` → `preferCostOptimized = true`

4. **Select profile**
   - For each profile in `availableProfiles`: classify by name pattern (see Profile Characteristic Inference table)
   - If `needsReasoning`: filter profiles where `reasoning=true` → prefer kimi
   - Else if `needsLongContext`: filter profiles where `context=long` → prefer kimi
   - Else: filter profiles where `cost=low` → prefer glm
   - `selectedProfile = filteredProfiles[0]`
   - If `filteredProfiles.length === 0`: fallback to `glm` if exists, else first available
   - If no profiles: Error

5. **Enhance prompt**
   - If task mentions files: gather context using Read tool
   - Add: file paths, current implementation, expected behavior, success criteria
   - Preserve slash commands at task start (e.g., `/cook`, `/commit`)

6. **Execute delegation**
   - Run: `ccs {selectedProfile} -p "$enhancedPrompt"` via Bash tool

7. **Report results**
   - Log: "Selected {profile} (reason: {reasoning/long-context/cost-optimized})"
   - Report: Cost (USD), Duration (sec), Session ID, Exit code

**For `/ccs:continue [follow-up]`:**

1. **Detect profile**
   - Read `~/.ccs/delegation-sessions.json` using Read tool
   - Find most recent session (latest timestamp)
   - Extract profile name from session data
   - If no sessions → Error: "No previous delegation. Use /ccs first"

2. **Parse override flag**
   - Scan follow-up for pattern: `--(\w+)`
   - If match: `profile = match[1]`, remove flag from follow-up, log profile switch
   - If no match: use detected profile from step 1

3. **Enhance prompt**
   - Review previous work (check what was accomplished)
   - Add: previous context, incomplete tasks, validation criteria
   - Preserve slash commands at start

4. **Execute continuation**
   - Run: `ccs {profile}:continue -p "$enhancedPrompt"` via Bash tool

5. **Report results**
   - Report: Profile, Session #, Incremental cost, Total cost, Duration, Exit code

## Decision Framework

**Delegate when:**
- Simple refactoring, tests, typos, documentation
- Deterministic, well-defined scope
- No discussion/decisions needed

**Keep in main when:**
- Architecture/design decisions
- Security-critical code
- Complex debugging requiring investigation
- Performance optimization
- Breaking changes/migrations

## Profile Selection Logic

**Task Analysis Keywords** (scan task string with regex):

| Pattern | Variable | Example |
|---------|----------|---------|
| `/(think\|analyze\|reason\|debug\|investigate\|evaluate)/i` | `needsReasoning = true` | "think about caching" |
| `/(architecture\|entire\|all files\|codebase\|analyze all)/i` | `needsLongContext = true` | "analyze all files" |
| `/(typo\|test\|refactor\|update\|fix)/i` | `preferCostOptimized = true` | "fix typo in README" |

**Profile Characteristic Inference** (classify by name pattern):

| Profile Pattern | Cost | Context | Reasoning |
|----------------|------|---------|-----------|
| `/^glm/i` | low | standard | false |
| `/^kimi/i` | medium | long | true |
| `/^claude/i` | high | standard | false |
| others | low | standard | false |

**Selection Algorithm** (apply filters sequentially):

```
profiles = Object.keys(config.profiles)
classified = profiles.map(p => ({name: p, ...inferCharacteristics(p)}))

if (needsReasoning):
  filtered = classified.filter(p => p.reasoning === true).sort(['kimi'])
else if (needsLongContext):
  filtered = classified.filter(p => p.context === 'long').sort(['kimi'])
else:
  filtered = classified.filter(p => p.cost === 'low').sort(['glm', ...])

selected = filtered[0] || profiles.find(p => p === 'glm') || profiles[0]
if (!selected): throw Error("No profiles configured")

log("Selected {selected} (reason: {reasoning|long-context|cost-optimized})")
```

**Override Logic**:
- Parse task for `/--(\w+)/`. If match: `profile = match[1]`, remove from task, skip selection

## Example Delegation Tasks

**Good candidates:**
- "/ccs add unit tests for UserService using Jest"
  → Auto-selects: glm (simple task)
- "/ccs analyze entire architecture in src/"
  → Auto-selects: kimi (long-context)
- "/ccs think about the best database schema design"
  → Auto-selects: kimi (reasoning)
- "/ccs --glm refactor parseConfig to use destructuring"
  → Forces: glm (override)

**Bad candidates (keep in main):**
- "implement OAuth" (too complex, needs design)
- "improve performance" (requires profiling)
- "fix the bug" (needs investigation)

## Execution

**Commands:**
- `/ccs "task"` - Intelligent delegation (auto-select profile)
- `/ccs --{profile} "task"` - Force specific profile
- `/ccs:continue "follow-up"` - Continue last session (auto-detect profile)
- `/ccs:continue --{profile} "follow-up"` - Continue with profile switch

**Agent via Bash:**
- Auto: `ccs {auto-selected} -p "task"`
- Continue: `ccs {detected}:continue -p "follow-up"`

## References

Template: `CLAUDE.md.template` - Copy to user's CLAUDE.md for auto-delegation config
Troubleshooting: `references/troubleshooting.md`
