---
name: knowledge-extractor
description: Analyzes completed projects to identify generalizable patterns, common workflows, and reusable knowledge worth extracting into skills. Use after completing a project to review LOG.md, skill updates, and project artifacts. Generates extraction recommendations but does not modify skills directly (user decides whether to apply via skill-updater).
---

# Knowledge Extractor

## Overview

This skill analyzes completed projects to identify what should be extracted from project-specific context (CLAUDE.md, LOG.md) into general skills. It produces **recommendations** for extraction, which the user reviews and optionally applies using skill-updater.

**Critical principle**: This skill does NOT modify skills or invoke other skills. It only analyzes and recommends.

## When to Use This Skill

Use this skill when:
- Completing a project and want to extract learnings
- Multiple projects have used similar patterns
- LOG.md shows repeated skill updates worth generalizing
- Project developed domain knowledge worth preserving
- Want to identify what project-specific knowledge is actually general

**Typical trigger**: "Extract knowledge from this project" or "What should I add to my skills?"

## Workflow

### Step 1: Identify Project Scope

Determine what to analyze:

**Ask the user:**
- "Which project should I analyze for knowledge extraction?"
- "Where is the project's LOG.md file?"
- "Are there specific areas you think need extraction?"

**Default assumptions:**
- LOG.md location: `./.claude/LOG.md`
- CLAUDE.md location: `./.claude/CLAUDE.md`
- ERROR_LOG.md location: `./.claude/ERROR_LOG.md`
- Skills directory: `./.claude/skills/`

### Step 2: Read Project History

Gather extraction context:

**Read these files:**
1. **LOG.md**: All project history, decisions, and skill updates
2. **CLAUDE.md**: Project-specific conventions and context
3. **Skill update history**: Which skills were updated and why

**Look for:**
- Patterns that appeared multiple times
- Solutions to common problems
- Project-specific workflows that might be generalizable
- New techniques or approaches discovered
- Edge cases and their resolutions

### Step 3: Identify Extraction Candidates

Analyze for generalizable knowledge:

**Pattern recognition:**
- **Repeated patterns**: Same approach used 3+ times
- **Cross-project value**: "Would this help other projects?"
- **Domain knowledge**: Technical patterns, not project specifics
- **Skill gaps**: Functionality that should exist but doesn't

**Classification:**
```
For each candidate, determine:
1. Target: Which skill should receive this?
2. Type: Reference file, SKILL.md improvement, new skill?
3. Generality: How broadly applicable is this?
4. Value: How much does this improve the skill?
```

**Examples:**
- Discovered git workflow for monorepos → Add to git-workflow/references/
- Learned how to structure API docs → Add to project-context-generator template
- Found common log entry pattern → Add to project-logger examples
- Developed deployment checklist → Create new deployment-workflow skill

### Step 4: Check Skill Contracts

Verify each extraction is allowed:

**For each candidate:**
1. Identify target skill
2. Read skill's contract (SKILL.md or references/contract.md)
3. Classify update type (reference, SKILL.md, script, new skill)
4. Check against contract rules

**Contract compliance:**
- **Allowed without review**: Can recommend directly
- **Requires review**: Flag for user approval
- **Prohibited**: Suggest alternative (new skill, different target)

**If no contract exists:**
- Note: "Skill has no contract - suggest using skill-contract-generator first"

### Step 5: Generate Extraction Recommendations

Create structured recommendations file:

**Output file**: `EXTRACTIONS.md` in project root

**Format:**
```markdown
# Knowledge Extraction Recommendations
> Generated: YYYY-MM-DD HH:MM
> Project: [project name]
> Analyzed: LOG.md, CLAUDE.md, [other files]

## Summary

Total candidates identified: [N]
- High priority: [N]
- Medium priority: [N]
- Low priority: [N]
- Requires new skill: [N]

## High Priority Extractions

### [1] Add monorepo workflow to git-workflow

**What to extract:**
[Description of the pattern/knowledge]

**Where to add:**
- Target skill: `git-workflow`
- File: `references/monorepo-workflow.md`
- Update type: Add reference file

**Why generalizable:**
- Used across 3 different monorepo projects
- Not project-specific
- Common pain point

**Contract compliance:**
- Status: ✅ Allowed without review
- Rule: "Can add reference files documenting project patterns"

**Suggested content:**
```
[Actual content to add, formatted and ready]
```

**Next step:**
Invoke skill-updater to add this reference file.

---

### [2] Enhance project-logger with decision template

[Same structure as above]

## Medium Priority Extractions

[Same structure, lower priority items]

## Low Priority Extractions

[Same structure, nice-to-haves]

## New Skill Recommendations

### Create deployment-workflow skill

**Rationale:**
[Why this needs a new skill vs. updating existing]

**Scope:**
[What the new skill should cover]

**Next step:**
Use skill-creator to create this skill.

## Items NOT Recommended for Extraction

### Project-specific API client

**Why not extracted:**
- Specific to this project's API
- No cross-project value
- Should remain in project CLAUDE.md

[List other items considered but rejected]
```

### Step 6: Present Recommendations

Show recommendations to user:

**Summary message:**
```
I've analyzed the project and identified [N] extraction candidates:
- [N] high priority updates to existing skills
- [N] medium priority improvements
- [N] new skills to create
- [N] items NOT recommended for extraction

See EXTRACTIONS.md for full details.

Would you like me to:
1. Apply high priority extractions using skill-updater
2. Review specific recommendations
3. Create new skills identified
```

**User decision points:**
- Review and approve recommendations
- Decide which to apply
- Invoke skill-updater for approved items (user does this, not knowledge-extractor)

### Step 7: Document Extraction Session

Record the extraction process:

**Update LOG.md:**
```markdown
## YYYY-MM-DD HH:MM

### [MILESTONE] Knowledge extraction completed

**Context:** Completed [project name] and extracted learnings.

**What Changed:**
- Analyzed LOG.md and identified [N] extraction candidates
- Generated EXTRACTIONS.md with recommendations
- [List any extractions that were applied]

**Extraction summary:**
- High priority: [N] items
- Medium priority: [N] items
- New skills needed: [N]
- Items not extracted: [N] (project-specific)

**Next steps:**
- Review EXTRACTIONS.md
- Use skill-updater to apply approved extractions
- Use skill-creator for new skills identified

**Related:**
- Extraction file: `EXTRACTIONS.md`
- Project: [project name]
```

## Extraction Patterns

### Pattern 1: Workflow Addition

**Scenario:** Discovered project-specific workflow that's actually general

**Example:** Learned how to manage git in monorepo during project

**Action:**
```
1. Identify target skill (git-workflow)
2. Check contract: Can add reference files
3. Recommend: Add references/monorepo-workflow.md
4. User reviews → invokes skill-updater if approved
```

### Pattern 2: Edge Case Documentation

**Scenario:** Encountered and solved edge case not documented

**Example:** Found solution for git merge conflict in binary files

**Action:**
```
1. Identify target skill (git-workflow)
2. Check contract: Can add edge cases
3. Recommend: Add to references/edge-cases.md or update SKILL.md
4. User reviews → invokes skill-updater if approved
```

### Pattern 3: New Skill Creation

**Scenario:** Developed domain knowledge that needs own skill

**Example:** Built extensive deployment checklist during project

**Action:**
```
1. Determine: Too complex for existing skills
2. Recommend: Create new deployment-workflow skill
3. Draft skill structure and content
4. User reviews → invokes skill-creator if approved
```

### Pattern 4: Template Enhancement

**Scenario:** Improved a template during project usage

**Example:** Added security section to CLAUDE.md template

**Action:**
```
1. Identify target skill (project-context-generator)
2. Check contract: Template changes may require review
3. Recommend: Add optional security section to template
4. Flag: Requires review per contract
5. User reviews → invokes skill-updater if approved
```

## Decision Heuristics

### General vs. Project-Specific

**Extract to skill if:**
- Useful across 3+ projects (rule of three)
- No project-specific details embedded
- Generalizable pattern or technique
- Domain knowledge, not instance knowledge

**Keep in project if:**
- Specific to this codebase
- Includes project-specific APIs, schemas, or business logic
- One-off solution unlikely to recur
- Tied to project's unique context

**Examples:**
- ✅ Extract: "How to structure API documentation"
- ❌ Don't extract: "Our specific API endpoints"
- ✅ Extract: "Monorepo git workflow"
- ❌ Don't extract: "Our monorepo's specific structure"

### Update vs. New Skill

**Update existing skill when:**
- Natural extension of current scope
- Fills gap in existing coverage
- Same domain and use cases
- Skill would still be cohesive

**Create new skill when:**
- Different domain or purpose
- Would make existing skill too complex (>500 lines)
- Distinct user base or use cases
- Stands alone as independent capability

### Extraction Priority

**High priority:**
- Used frequently during project
- Solves common pain point
- Broadly applicable
- Allowed by contract without review

**Medium priority:**
- Used occasionally
- Moderately useful
- Somewhat general
- May require contract review

**Low priority:**
- Nice-to-have
- Niche use case
- Marginal value
- Uncertain generality

## Important Notes

### This Skill Does NOT Execute Updates

**Critical**: knowledge-extractor only analyzes and recommends.

**To apply recommendations:**
1. User reviews EXTRACTIONS.md
2. User decides which to apply
3. User invokes skill-updater (or Claude auto-triggers)
4. skill-updater executes the actual update

**Why this separation:**
- Follows "no skill-calling-skill" principle
- User maintains control over what gets extracted
- Clear separation: analysis vs. execution
- Respects that extraction is a manual, thoughtful process

### Relationship to Other Skills

**knowledge-extractor + skill-updater:**
- knowledge-extractor: Identifies WHAT to extract (brain)
- skill-updater: Executes HOW to extract (hands)
- User: Decides WHETHER to extract (judgment)
- No direct invocation between skills

**Analogous to:**
- skill-analyzer + skill-creator
- project-logger + git commit
- skill-contract-generator + skill-updater

### When NOT to Extract

**Don't extract if:**
- Only used once in one project
- Highly project-specific
- Would require significant abstraction
- Unclear if generalizable
- Would violate skill contract

**Document why NOT extracted:**
- Helps future decision-making
- Prevents re-analyzing same items
- Clarifies extraction criteria

## Resources

### references/extraction-checklist.md

Checklist for evaluating extraction candidates:
- Is it used 3+ times?
- Is it generalizable?
- Does it add value?
- Is it allowed by contract?
- Would it help other projects?

(To be created based on accumulated extraction experience)

## Skill Contract

**Stable:** 7-step workflow, decision heuristics (general vs. project-specific, update vs. new skill), recommendation format
**Mutable:** Extraction patterns, evaluation criteria, recommendation templates, checklist items
**Update rules:** See `references/contract.md` for detailed rules

> Full contract specification in `references/contract.md`
