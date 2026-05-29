---
name: session-intelligence-harvester
description: This skill should be used after productive sessions to extract learnings and route them to appropriate Reusable Intelligence Infrastructure (RII) components. Use when corrections were made, format drift was fixed, new patterns emerged, or the user explicitly asks to "harvest learnings" or "capture session intelligence". Transforms one-time fixes into permanent organizational knowledge by implementing updates across multiple files.
---

# Session Intelligence Harvester

## Overview

Transform session learnings into permanent organizational intelligence by implementing updates across RII components. After productive sessions involving corrections, discoveries, or pattern identification, systematically extract what was learned, route it to the correct component, and apply the changes.

**Why this matters**: One-time fixes that aren't encoded into RII components will recur. The Chapter N skill format drift happened because no check existed to prevent it. After harvesting, that failure mode is encoded in 4 files—future sessions automatically benefit.

## When to Use This Skill

**Automatic Triggers** (proactively suggest harvesting):
- Session corrected format drift (wrong file structure, YAML, invocation)
- Session added missing checks to orchestration files
- Session identified failure mode worth preventing
- Session touched 3+ files with similar pattern corrections
- PHR was created documenting significant learning

**Manual Triggers** (user requests):
- "Harvest learnings from this session"
- "Capture session intelligence"
- "What should we encode from this work?"
- "Update RII with what we learned"

## Workflow

**Default to action**: Implement all updates rather than only proposing them. Read target files, make edits, and commit changes. Only propose without implementing if explicitly asked.

### Step 1: Session Analysis

Analyze the session by answering these questions. Write your analysis to track progress:

```
1. CORRECTIONS MADE
   - What errors/drift were corrected?
   - What was wrong vs what is now correct?
   - Why did the error occur? (missing check, format drift, etc.)

   WHY THIS MATTERS: Understanding root cause determines which RII
   component prevents recurrence. Format drift → agent convergence
   pattern. Missing context → CLAUDE.md protocol step.

2. PATTERNS IDENTIFIED
   - What recurring patterns emerged?
   - What canonical sources were referenced?
   - What validation would have caught this earlier?

   WHY THIS MATTERS: Patterns that recur across sessions deserve
   encoding. If you referenced a canonical source, other sessions
   will need that same reference.

3. LEARNING CLASSIFICATION
   - Context-gathering gap? (CLAUDE.md)
   - Pedagogical/teaching issue? (Constitution)
   - Agent convergence pattern? (Agents)
   - Reusable workflow? (Skills)
   - Missing orchestration check? (Commands)

   WHY THIS MATTERS: Wrong routing means learnings don't trigger at
   the right time. A convergence pattern in CLAUDE.md won't help
   chapter-planner catch it during planning.
```

### Step 2: Route to RII Components

Use this routing table. Route learnings to the component where they will be discovered at the right time:

| Learning Type | Target Component | Location | What to Add | When It Triggers |
|---------------|------------------|----------|-------------|------------------|
| Context-gathering gaps | CLAUDE.md | Section I | New step in context protocol | Before ANY platform work |
| Failure mode example | CLAUDE.md | Failure modes | Named example with correction | When similar situation detected |
| Pedagogical framework | Constitution | Section IIa | Teaching method update | During lesson design |
| Agent convergence pattern | Agent file | Convergence Patterns | Pattern + why + correction | During agent execution |
| Agent self-monitoring | Agent file | Self-Monitoring Checklist | New checklist item | Before agent finalizes output |
| Canonical source lookup | Multiple agents | Analysis Questions | Cross-reference check | During planning phase |
| Reusable workflow | New skill | .claude/skills/ | New SKILL.md | When user invokes skill |
| Orchestration check | Command file | Phase 0 or relevant phase | New validation step | During workflow execution |
| Format specification | Canonical source chapter | Lesson content | Authoritative format | When teaching that pattern |

**WHY ROUTING MATTERS**: Learnings placed in the wrong component don't prevent recurrence. A check in `content-implementer.md` won't help if the error happens during `chapter-planner` execution.

### Step 3: Read Target Files and Generate Updates

For each identified learning:

1. **Read the target file** to understand current structure and find exact placement
2. **Generate the update** with surrounding context for precise placement
3. **Track progress** as you work through multiple files

```markdown
## Learning: [Brief Title]

**Type**: [Context gap | Failure mode | Convergence pattern | etc.]

**Target**: [File path]

**Current State** (after reading file):
[What's missing or incorrect - quote existing content if helpful]

**Exact Placement**:
[Which section, after which content - be specific enough to Edit]

**Content to Add**:
[Exact content, matching the file's style and format]

**Rationale**:
[Why this prevents recurrence - what will trigger this check]

**Canonical Source** (if applicable):
[Which chapter/lesson defines the authoritative format]
```

### Step 4: Implement Updates

**Take action**: Edit each target file. Use the Edit tool to make changes.

For each update:
1. Read the target file (if not already read)
2. Locate the exact insertion point
3. Apply the edit using Edit tool
4. Verify the edit was applied correctly

Track completion:
```
Updates Progress:
- [x] CLAUDE.md - Added failure mode section
- [x] chapter-planner.md - Added convergence pattern 6
- [ ] sp.loopflow.v2.md - Adding Phase 0 check (in progress)
- [ ] content-implementer.md - Pending
```

### Step 5: Validation

Before finalizing, verify each of these (check the box as you confirm):

```
- [ ] Read each target file before editing (no speculation about structure)
- [ ] Verified each learning routes to the component where it triggers at the right time
- [ ] Confirmed updates include exact placement context (not vague locations)
- [ ] Checked canonical sources exist for format-related learnings
- [ ] Searched target files to confirm no duplicate information exists
- [ ] Used imperative form for agent files, appropriate style for others
- [ ] Added cross-references where pattern appears in multiple files
- [ ] All edits applied successfully (no pending changes)
```

### Step 6: Create PHR and Commit

1. **Create PHR** documenting:
   - What was learned
   - Where it was encoded (list all files)
   - Why this improves future work

2. **Commit changes** with descriptive message:
   ```
   feat(intelligence): Harvest session learnings into RII

   Updates:
   - [File 1]: [What was added]
   - [File 2]: [What was added]

   Prevents: [What failure mode this prevents]
   ```

## RII Component Reference

### CLAUDE.md Structure

```
Section I: Context Gathering Protocol
  - Step 1-N: Sequential context steps
  - Each step has WHAT to do and WHY it matters
  - "Find canonical source" step for pattern teaching

Failure Modes (between Section I and II):
  - Named failure examples: "FAILURE MODE: [Name] Example"
  - "What I did wrong" list
  - "What I should have done" numbered steps
  - "Result" showing what was prevented
```

### Agent File Structure

```
Analysis Questions (Section III):
  - Numbered questions with "Why this matters" explanation
  - Self-check prompt at end

Principles (Section IV):
  - Named principles with Framework + What this means + Application guidance
  - Self-check prompt

Convergence Patterns (Section VI):
  - "Generic pattern" description
  - "Why this is convergence" explanation
  - "Correction" with specific steps

Self-Monitoring Checklist (Section VIII):
  - Numbered checklist with checkmark emoji prefix
  - Each item is a verification question
```

### Command File Structure

```
Phase 0: Foundation checks
  - Constitutional reading
  - Canonical source checks (for educational content)
  - Each step explains WHY

Convergence Patterns:
  - Symptom description
  - Detection method
  - Correction steps
```

## Output Format

After completing harvest, provide summary:

```markdown
## Session Intelligence Harvest Summary

**Session**: [Brief description]
**Date**: [ISO date]
**Status**: COMPLETE

### Learnings Extracted: [N]

| # | Learning | Type | Target | Status |
|---|----------|------|--------|--------|
| 1 | [Title] | [Type] | [File] | Applied |
| 2 | [Title] | [Type] | [File] | Applied |

### Updates Applied

1. **[File]**: [What was added] (lines X-Y)
2. **[File]**: [What was added] (lines X-Y)

### PHR Created
- Path: [PHR path]
- Stage: [Stage]

### Canonical Sources Referenced
- [Pattern]: [Chapter X Lesson Y]

### Commit
- Hash: [commit hash]
- Message: [commit message summary]
```

## Examples

### Example 1: Format Drift Correction (Multi-File)

**Session**: Fixed skill format to use domain-based structure

**Analysis**:
```
CORRECTIONS MADE:
- Wrong: .claude/skills/section-writer.md (flat file, no domain)
- Correct: .claude/skills/authoring/section-writer/SKILL.md (domain + directory structure)
- Root cause: No domain organization for skills/agents

PATTERNS IDENTIFIED:
- Skills must be in authoring/ or engineering/ domain folders
- Agents must be in authoring/ or engineering/ domain folders
- Multiple files referenced old flat structure

CLASSIFICATION:
- Failure mode → CLAUDE.md
- Convergence pattern → chapter-planner.md, content-implementer.md
- Skill structure → skill-creator, session-intelligence-harvester
```

**Updates Applied**:
1. CLAUDE.md: Updated agent architecture section
2. skill-creator: Added domain organization requirement
3. session-intelligence-harvester: Updated routing table with domain paths
4. Moved all skills to authoring/ or engineering/
5. Moved all agents to authoring/ or engineering/
6. Generals Skills are at .claude/skills/
### Example 2: Missing Validation (Single File)

**Session**: Discovered lessons weren't checking chapter-index.md for prerequisites

**Analysis**:
```
CORRECTIONS MADE:
- Wrong: Started chapter work without reading chapter-index.md
- Correct: MUST read chapter-index.md first to get Part, proficiency, prerequisites
- Root cause: No mandatory step in context protocol

CLASSIFICATION:
- Context-gathering gap → CLAUDE.md Section I
```

**Updates Applied**:
1. CLAUDE.md: Added Step 1 to read chapter-index.md with specific extraction requirements

## Self-Monitoring

Before marking harvest complete, verify you have:

- [ ] Analyzed session to identify all corrections and patterns
- [ ] Classified each learning to determine correct routing
- [ ] Read each target file before editing (no speculation)
- [ ] Applied all edits using Edit tool (not just proposed)
- [ ] Verified edits match target file's style and structure
- [ ] Added cross-references where patterns appear in multiple files
- [ ] Created PHR documenting the harvest
- [ ] Committed changes with descriptive message
- [ ] Generated summary showing all updates applied