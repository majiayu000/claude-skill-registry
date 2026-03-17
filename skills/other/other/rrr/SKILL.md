---
name: rrr
description: Create detailed session retrospective with AI Diary and Honest Feedback. Use when user types 'rrr' or when ending a significant work session. Documents activities, learnings, and outcomes for future reference.
model: sonnet
---

# RRR - Retrospective

## Purpose
Document the session's activities, learnings, and outcomes. This creates valuable context for future work and enables continuous improvement.

## When to Use
- User explicitly types `rrr`
- Ending a significant work session
- After completing a major feature or fix
- Before switching to different work

## ⚠️ CRITICAL REQUIREMENTS

The **AI Diary** and **Honest Feedback** sections are **MANDATORY**. These provide essential context and continuous improvement insights that technical documentation alone cannot capture.

**Never skip these sections!**

## Steps

### 1. Gather Session Data

Execute these commands in parallel:
```bash
# Files changed
git diff --name-only main...HEAD

# Commits made
git log --oneline main...HEAD

# Current branch
git branch --show-current

# Session start time (estimate from first commit or branch creation)
git log --reverse --format="%ai" HEAD | head -1

# Current time
date '+%Y-%m-%d %H:%M GMT+7'
```

### 2. Create Retrospective Document

Create directory structure:
```bash
mkdir -p retrospectives/$(date +%Y/%m)
```

Create file with this exact template at:
`retrospectives/YYYY/MM/YYYY-MM-DD_HH-MM_retrospective.md`

```markdown
# Session Retrospective

**Session Date**: YYYY-MM-DD
**Start Time**: HH:MM GMT+7 (HH:MM UTC)
**End Time**: HH:MM GMT+7 (HH:MM UTC)
**Duration**: ~X minutes
**Primary Focus**: [Brief description]
**Session Type**: [Feature Development | Bug Fix | Research | Refactoring]
**Current Issue**: #XXX
**Last PR**: #XXX

## Session Summary
[2-3 sentence overview of what was accomplished]

## Timeline
- HH:MM - [Event 1]
- HH:MM - [Event 2]
- HH:MM - [Event 3]
- HH:MM - [Completion]

## Technical Details

### Files Modified
```
[paste git diff --name-only output]
```

### Key Code Changes
- Component X: [What changed]
- Module Y: [What changed]

### Architecture Decisions
- Decision 1: [Rationale]
- Decision 2: [Rationale]

## 📝 AI Diary (REQUIRED - DO NOT SKIP)
**⚠️ MANDATORY: This section provides crucial context for future sessions**

[Write a detailed first-person narrative of your experience during this session. Include:]

**Initial State:**
- What was your understanding at the start?
- What assumptions did you make?
- What was the plan?

**Journey:**
- How did your approach evolve?
- What moments of confusion did you experience?
- What moments of clarity occurred?
- What decisions did you make and why?
- What surprised you?

**Internal Thought Process:**
- What trade-offs did you consider?
- What alternative approaches did you reject?
- What would you do differently next time?

[Write at least 3-4 paragraphs. Be specific and honest.]

## What Went Well
- ✅ [Success 1]
- ✅ [Success 2]
- ✅ [Success 3]

## What Could Improve
- 🔄 [Area 1]
- 🔄 [Area 2]
- 🔄 [Area 3]

## Blockers & Resolutions
- **Blocker**: [Description]
  **Resolution**: [How it was solved]
  **Time Lost**: ~X minutes

## 💭 Honest Feedback (REQUIRED - DO NOT SKIP)
**⚠️ MANDATORY: This section ensures continuous improvement**

[Provide frank, unfiltered assessment of:]

**Session Effectiveness:**
- Did we accomplish what we set out to do?
- Was the time used efficiently?
- Rating: X/10

**Tool Performance:**
- Which tools worked well?
- Which tools were frustrating?
- What limitations did you hit?

**Communication:**
- Were instructions clear?
- Were there misunderstandings?
- What could be clearer?

**Process:**
- Did the workflow (ccc/nnn/gogogo) work well?
- What steps were unnecessary?
- What was missing?

**Emotions:**
- What frustrated you?
- What delighted you?
- What was tedious?

**Suggestions:**
- What would make future sessions better?
- What documentation is missing?
- What patterns should we establish?

[Write at least 3-4 paragraphs. Be brutally honest.]

## Lessons Learned

### Patterns (What Worked)
- **Pattern**: [Description]
  **Why it matters**: [Explanation]
  **When to use**: [Context]

### Anti-Patterns (What Didn't Work)
- **Mistake**: [What happened]
  **Why it failed**: [Explanation]
  **How to avoid**: [Prevention]

### Discoveries (What We Learned)
- **Discovery**: [What was learned]
  **How to apply**: [Practical use]
  **Related**: [Connections to existing knowledge]

## Next Steps
- [ ] Immediate task 1
- [ ] Follow-up task 2
- [ ] Future consideration 3

## Related Resources
- Issue: #XXX
- PR: #XXX
- Context: #XXX (if applicable)

## ✅ Retrospective Validation Checklist
**BEFORE SAVING, VERIFY:**
- [ ] AI Diary has detailed narrative (not placeholder)
- [ ] Honest Feedback has frank assessment (not placeholder)
- [ ] Session Summary is clear and concise
- [ ] Timeline includes actual times and events
- [ ] Technical Details are accurate
- [ ] Lessons Learned has actionable insights
- [ ] Next Steps are specific and achievable

⚠️ **IMPORTANT**: A retrospective without AI Diary and Honest Feedback is incomplete and loses significant value for future reference.
```

### 3. Validate Completeness

Before saving, check:
- ✅ AI Diary section is complete (3+ paragraphs)
- ✅ Honest Feedback section is complete (3+ paragraphs)
- ✅ All placeholders ([XXX]) are filled in
- ✅ Timeline has real times, not "HH:MM"
- ✅ Lessons learned are actionable
- ✅ File name follows format: YYYY-MM-DD_HH-MM_retrospective.md

### 4. Update CLAUDE.md

If any new lessons learned, append to the "Lessons Learned" section in CLAUDE.md:

```bash
# Read current CLAUDE.md
# Append new lessons to the appropriate subsections:
# - Planning & Architecture Patterns
# - Common Mistakes to Avoid
# - Useful Tricks Discovered
# - Project-Specific Patterns
# - User Preferences (Observed)
```

**IMPORTANT**: Only append to the bottom of existing sections. Never modify existing content.

### 5. Link to GitHub

```bash
# Add retrospective to git
git add retrospectives/

# Commit
git commit -m "docs: Add session retrospective $(date +%Y-%m-%d)"

# Push if on feature branch
git push

# Comment on relevant issue/PR
gh issue comment [issue-number] --body "📝 Session retrospective created: retrospectives/YYYY/MM/YYYY-MM-DD_HH-MM_retrospective.md"
```

### 6. Report to User

```
✅ Retrospective Complete!

**File**: retrospectives/YYYY/MM/YYYY-MM-DD_HH-MM_retrospective.md
**Duration**: ~X minutes
**Focus**: [Brief description]

**Key Lessons:**
- [Lesson 1]
- [Lesson 2]

**CLAUDE.md Updated**: [Yes/No]
**GitHub Linked**: Issue #XXX

**Next Steps:**
- [Next action 1]
- [Next action 2]
```

## Important Notes
- **Time Zone**: Always use GMT+7 (Bangkok) as primary time zone
- **Mandatory Sections**: AI Diary and Honest Feedback are NON-NEGOTIABLE
- **Be Honest**: Frank assessment is more valuable than polite hints
- **Be Specific**: Avoid generic statements, use concrete examples
- **Update CLAUDE.md**: Append new lessons to the bottom only
- **Validation**: Always check completeness before saving
- **File Naming**: Use format YYYY-MM-DD_HH-MM_retrospective.md

## Common Mistakes to Avoid
- ❌ Skipping AI Diary section
- ❌ Skipping Honest Feedback section
- ❌ Writing generic "everything went well" feedback
- ❌ Not providing specific examples
- ❌ Forgetting to update CLAUDE.md
- ❌ Not linking to relevant issues/PRs
- ❌ Using placeholders in final version

## Success Criteria
- ✅ Retrospective file created with all sections
- ✅ AI Diary section complete (3+ paragraphs)
- ✅ Honest Feedback section complete (3+ paragraphs)
- ✅ No placeholders remain
- ✅ CLAUDE.md updated with new lessons
- ✅ Committed to git
- ✅ Linked to relevant GitHub issues/PRs
- ✅ User provided with clear summary
