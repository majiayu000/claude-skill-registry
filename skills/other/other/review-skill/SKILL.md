---
name: review-skill
description: >
  Review a SKILL.md file or skill directory for quality, correctness, and
  alignment with Claude Code skill conventions. Use when you've written a new
  skill and want to check it before committing, or when evaluating an existing
  skill for improvements.
allowed-tools: Read, Glob, Grep, Edit, Write
argument-hint: <skill-dir>...
---

This skill reviews and fixes other skills — identifying issues and applying corrections with developer approval at each stage.

**Stop after each stage and have changes reviewed with the user.**

> **Note**: The agent checks skills against conventions and best practices, then proposes fixes. The developer approves before changes are applied. When uncertain about intent, ask — don't assume.

0. **Read and understand the skill** (agent proposes, developer confirms)
   - Read the target `SKILL.md` at `$ARGUMENTS` (and any supporting files in the directory)
   - Summarize: what does this skill do, when is it invoked, and what workflow does it follow?
   - Confirm understanding before proceeding to review

1. **Frontmatter review** (agent reviews, then fixes with developer approval)

   Check that frontmatter is well-formed and follows conventions:

   - Is `name` kebab-case and does it match the directory name?
   - Is `description` present, specific enough to trigger correctly, and does it include when-to-use context?
   - Are invocation control fields appropriate for the skill's purpose?
     - Side-effect workflows should use `disable-model-invocation: true`
     - Background knowledge should use `user-invocable: false`
   - Is `allowed-tools` set if the skill should restrict tool access?
   - Are `context`/`agent` set appropriately if the skill runs in isolation?
   - Are there unknown or misspelled frontmatter fields?

   Report findings as a checklist: pass / issue / suggestion. Then apply fixes for any issues, with developer approval.

2. **Prompt structure review** (agent reviews, then fixes with developer approval)

   Check the prompt body for structural quality:

   - Does it have a **stop-after-each-stage** instruction if it's a multi-stage workflow?
   - Is there a Stage 0 for understanding/confirmation before doing work?
   - Are agent vs developer responsibilities clear at each stage?
   - Does it use questions to guide analysis, not just imperatives?
   - Is the skill under 500 lines? Does it reference supporting files for detail rather than inlining everything?
   - Is the stage numbering consistent and logical?

   Report findings as a checklist: pass / issue / suggestion. Then apply fixes for any issues, with developer approval.

3. **Effectiveness review** (agent reviews, then fixes with developer approval)

   Check that the skill will work well in practice:

   - Are instructions unambiguous — will Claude interpret them correctly?
   - Is the scope right-sized? (Not trying to do too much in one skill)
   - Are `$ARGUMENTS`, `$0`, `$1` used correctly if present?
   - Is dynamic context (exclamation-mark backtick syntax) used correctly if present?
   - Are supporting files referenced from `SKILL.md`?
   - Check for anti-patterns:
     - Overly broad or narrow description
     - No review pauses in a multi-stage workflow
     - Unreferenced supporting files in the directory
     - Task instructions in a skill with no `context: fork` and no clear action

   Report findings as a checklist: pass / issue / suggestion. Then apply fixes for any issues, with developer approval.

4. **Alignment review** (agent reviews, then fixes with developer approval)

   If the skill is intended for this repo's skill library, check alignment with existing skills:

   - Consistent formatting with other skills in the repo?
     - Blockquotes for philosophy notes
     - Bold for stage titles
     - Tables for comparisons
   - Includes "When to use this vs other skills" if it overlaps with existing skills?
   - Follows the composition model (flesh-out -> review-steps -> strong-edit -> agent-optimize)?
   - Has a `responsibilities.md` if it's a multi-stage workflow with mixed agent/developer ownership?

   If the skill is standalone (not for this repo), skip repo-specific alignment checks and note this.

   Report findings as a checklist: pass / issue / suggestion. Then apply fixes for any issues, with developer approval.

5. **Summary and recommendations** (agent leads)

   Provide a final summary:

   - Overall quality assessment (ready to use / needs minor fixes / needs rework)
   - Top 3 issues to address (if any)
   - Top 3 strengths (what the skill does well)
   - Recommendation: publish / revise / rethink


## When to Use This vs Other Skills

| Goal | Use |
|------|-----|
| Review a **document** for polish | **review-steps** |
| Review a **document** for substantive critique | **strong-edit** |
| Review a **SKILL.md** for quality and conventions | **review-skill** |
| Create a new skill from scratch | Start with **_template**, then **review-skill** the result |
