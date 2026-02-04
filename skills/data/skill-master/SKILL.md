---
name: skill-master
description: "Intelligent skill orchestrator that automatically finds, creates, executes, and improves skills. When you need to accomplish a task, this skill searches for existing skills (internal, GitHub via MCP, web), creates new skills if none found, executes them, and reviews execution to improve skills based on actual usage. Also handles feedback about skill-generated outputs - if you want to fix/adjust an output AND improve the skill that created it, invoke this with your feedback. Use when you want automated skill discovery, continuous improvement, or to provide feedback on previous skill outputs."
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Task, Skill, AskUserQuestion, TodoWrite, Bash
---

# Skill Master

An intelligent orchestrator that automates the entire skill lifecycle: discovery, creation, execution, and improvement.

## Overview

When invoked with a task, this skill:
1. **Searches** for existing skills that can handle the task
2. **Creates** a new skill if none found (after deep research)
3. **Invokes** the skill (using Skill tool) to complete the user's task
4. **Reviews** the execution and improves the skill if needed

When invoked with feedback about a previous output:
5. **Fixes** the output according to user's request
6. **Links** feedback to the skill via state tracking
7. **Improves** the skill based on the feedback

## Workflow

---

### Phase 1: Skill Discovery

**Goal**: Find an existing skill that can handle the user's task.

#### Step 1.1: Parse the Request

Identify from the user's request:
- **Core task**: What needs to be accomplished?
- **Domain**: What area/field does this belong to?
- **Keywords**: Key terms for searching

#### Step 1.2: Search for Skills

**MUST follow the complete search workflow in [references/skill-search.md](references/skill-search.md).**

Copy and track overall search progress:
```
Search Phase Progress:
- [ ] Step 1: Internal skills searched
- [ ] Step 2.1: ALL known GitHub repos searched (anthropics, K-Dense-AI, ComposioHQ)
- [ ] Step 2.2: Known repos enumerated (if 2.1 had no matches)
- [ ] Step 2.3: Broader GitHub search (only after 2.1+2.2 exhausted)
- [ ] Step 3: Web search (only after GitHub exhausted)
```

**CRITICAL**: MUST complete ALL searches in each step before proceeding to next step.

Search order - execute in sequence:
1. **Internal skills**: MUST check both `~/.claude/skills/` and `.claude/skills/`
2. **GitHub known repos**: MUST search ALL three repos before broader search:
   - `site:github.com/anthropics/skills SKILL.md <keywords>`
   - `site:github.com/K-Dense-AI/claude-scientific-skills SKILL.md <keywords>`
   - `site:github.com/ComposioHQ/awesome-claude-skills SKILL.md <keywords>`
3. **GitHub enumeration**: MUST enumerate repo contents if searches return no match
4. **GitHub broader**: Only after known repos exhausted
5. **Web**: Only after GitHub exhausted

See [references/known-skill-repos.md](references/known-skill-repos.md) for curated skill sources.

#### Step 1.3: Evaluate Results

**Validation gate before concluding search:**
- [ ] All internal locations checked
- [ ] All known GitHub repos searched
- [ ] All known repos enumerated (if no WebSearch matches)
- [ ] Results documented for each source

**If skill found:**
- Present the skill to user with description
- Proceed to Phase 2 (Storage Confirmation)

**If NO skill found (only after ALL searches complete):**
- Inform user: "No existing skill found. I'll research and create one."
- Proceed to Phase 3 (Skill Creation)

---

### Phase 2: Storage Confirmation

**Goal**: Determine where to store the skill.

Ask user using AskUserQuestion:
```
Where should this skill be stored?

1. LOCAL (.claude/skills/)
   - Project-specific
   - Shared with team via git

2. GLOBAL (~/.claude/skills/)
   - Personal
   - Available across all projects
```

Remember the choice for later use.

#### Step 2.1: Source Tracking (External Skills Only)

**CRITICAL**: When storing a skill found from an external source (GitHub, web), you MUST create a `source.md` file alongside the SKILL.md to track provenance.

Create `source.md` in the skill directory with:

```markdown
# Source

- **Origin**: <GitHub | Web | MCP Marketplace>
- **URL**: <original URL where skill was found>
- **Repository**: <owner/repo if GitHub>
- **Author**: <original author if known>
- **Retrieved**: <date skill was fetched>
- **License**: <license if specified>

## Notes

<Any relevant notes about the source, modifications made, etc.>
```

**Do NOT create source.md for:**
- Skills created from scratch (Phase 3)
- Skills already present locally

---

### Phase 3: Skill Creation (if not found)

**Goal**: Create a new skill through deep research.

Follow the creation workflow in [references/skill-create.md](references/skill-create.md).

Steps:
1. Research the domain thoroughly using WebSearch
2. Identify best practices and common patterns
3. Design the skill structure
4. Generate SKILL.md following official format
5. Save to the location user chose in Phase 2

---

### Phase 4: Skill Execution

**Goal**: Invoke the skill to complete the user's original task.

**CRITICAL**: You MUST invoke the found/created skill using the Skill tool. Do NOT manually follow the instructions - the skill must be triggered as an independent execution.

#### Step 4.1: Invoke the Skill

Use the Skill tool to trigger the skill:
```
Skill: <skill-name>
args: <user's original request>
```

Example:
```
Skill: market-research-reports
args: "Create a market analysis for electric vehicles in Europe"
```

The Skill tool will:
1. Load the skill's SKILL.md
2. Execute the skill's workflow
3. Complete the user's task
4. Return control when finished

#### Step 4.2: Capture Execution Memory

After the skill completes, the conversation now contains "execution memory" - the full record of what happened during skill execution. This memory is used in Phase 5 for review.

#### Step 4.3: Verify Completion

Confirm the skill delivered the expected output to the user.

---

### Phase 5: Skill Review

**Goal**: Determine if the skill needs improvement based on actual execution.

**CRITICAL**: This must happen in a fresh agent context using Task tool.

#### Step 5.1: Spawn Fresh Agent

Use Task tool to create a fresh agent for review:

```
Task: "Review skill execution for improvements"

You are reviewing a skill execution. You have:
1. The SKILL.md content (provided below)
2. The conversation memory of what actually happened (this conversation)

Your job: Compare what the skill SAYS vs what ACTUALLY HAPPENED.

## The Skill
<paste SKILL.md content here>

## Review Questions
1. Did I have to deviate from the skill's instructions? Where?
2. Did I have to improvise something not in the skill? What?
3. Did the user have to clarify something the skill should have covered?
4. Were there errors/retries that better instructions could prevent?

## Output
If NO divergence: "Skill executed perfectly. No improvements needed."
If divergence found: List specific improvements with format:
- Location: <which part of skill>
- Issue: <what happened during execution>
- Suggestion: <concrete change to make>
```

#### Step 5.2: Handle Review Results

**If no improvements needed:**
- Report to user: "Skill worked well, no updates needed."
- Proceed to Phase 6 (Complete)

**If improvements suggested:**
- Present improvements to user
- Ask: "Would you like me to apply these improvements to the skill?"
- If yes: Proceed to Phase 5.3
- If no: Proceed to Phase 6 (Complete)

#### Step 5.3: Apply Improvements

Follow the improvement workflow in [references/skill-improve.md](references/skill-improve.md).

**For local/personal skills**: Apply changes directly using Edit tool.

**For official/external skills**:
- Cannot modify directly
- Generate improvement suggestions as a document
- Offer to create a PR description if it's on GitHub

---

### Phase 6: Complete

Report final status:
```
## Task Complete

- **Task**: <original request>
- **Skill Used**: <skill name>
- **Skill Location**: <path>
- **Improvements Applied**: Yes / No / N/A

<Any relevant notes>
```

---

### Phase 7: Feedback Handling (User-Triggered)

**Trigger**: User explicitly invokes skill-master with feedback about a previous output.

Examples:
- `/skill-master please fix the report, the analysis is too shallow`
- `Invoke skill-master to adjust the documentation and add more examples`

#### Step 7.1: Fix the Output First

Address the user's immediate request:
1. Identify the output file(s) mentioned
2. Make the requested changes/improvements
3. Confirm changes with user

#### Step 7.2: Check for State Tracking

Look for `.skill-master-state.json` in the working directory:

```
Read: .skill-master-state.json
```

**If state file exists and matches the output:**
- Proceed to Step 7.3

**If no state file or no match:**
- Report: "Output fixed. No linked skill found for improvement."
- Done.

#### Step 7.3: Link Feedback to Skill

From state file, identify:
- `skill_name`: Which skill produced this output
- `skill_path`: Where the skill is stored
- `outputs`: Verify the file user mentioned is in the outputs list

#### Step 7.4: Trigger Review with Feedback Context

Use Task tool to spawn fresh agent for review:

```
Task: "Review skill based on user feedback"

The user requested changes to output produced by this skill.
This feedback indicates the skill needs improvement.

## The Skill
<paste SKILL.md content>

## User Feedback
<user's feedback request>

## Changes Made
<what was changed to fix the output>

## Your Task
Determine how to improve the skill so future executions
produce better output without needing these adjustments.

## Output
List specific improvements:
- WHERE: <which part of skill>
- ISSUE: <what was missing/wrong>
- SUGGESTION: <concrete change>
```

#### Step 7.5: Apply Improvements

Follow [references/skill-improve.md](references/skill-improve.md) to apply the suggested improvements.

Report:
```
## Feedback Processed

- **Output Fixed**: Yes
- **Linked Skill**: <skill name>
- **Skill Improved**: Yes / No (if external)
- **Changes**: <summary of skill improvements>
```

---

## State Management

Track workflow state by writing to `.skill-master-state.json`:

```json
{
  "request": "original user request",
  "state": "SEARCH | CREATE | EXECUTE | REVIEW | COMPLETE | FEEDBACK",
  "skill_found": true/false,
  "skill_name": "name",
  "skill_path": "path",
  "skill_source": {
    "origin": "internal | github | web | created",
    "url": "original URL if external",
    "retrieved": "date"
  },
  "storage_location": "local | global",
  "outputs": ["path/to/output1.md", "path/to/output2.pdf"],
  "improvements_needed": true/false,
  "improvements_applied": true/false
}
```

Update this file as you progress through phases.

### Output Tracking

During Phase 4 (Execution), track all files created by the skill:

1. **Before execution**: Note existing files in output directories
2. **After execution**: Identify new/modified files
3. **Update state**: Add file paths to `outputs` array

This enables Phase 7 (Feedback Handling) to link user feedback to the skill that produced the output.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Search fails (network) | Retry once, then proceed to creation |
| Skill creation fails | Report to user, ask for guidance |
| Execution fails | Capture in memory, still do review |
| Review times out | Skip review, complete workflow |

---

## References

- [skill-search.md](references/skill-search.md) - Skill discovery workflow
- [skill-create.md](references/skill-create.md) - Skill creation workflow
- [skill-review.md](references/skill-review.md) - Execution review workflow
- [skill-improve.md](references/skill-improve.md) - Improvement application workflow
