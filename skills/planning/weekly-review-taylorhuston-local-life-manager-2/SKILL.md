---
name: weekly-review
description: Weekly review and planning session. Use at end of week or weekend to review progress, plan next week, and set priorities. Triggers on "weekly review", "plan my week", "what did I do this week", "Sunday planning".
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Bash(gh:*, date:*)
---

Run a weekly review and planning session. Keep it conversational - one section at a time.

## Step 0: Get Week Info

```bash
date +%Y-%m-%d        # Today
date +%Y-W%V          # Current ISO week
date -d "last sunday" +%Y-%m-%d  # Week start (for lookback)
```

## Step 1: Weekly Note Setup

1. Check if this week's note exists: `my-vault/02 Calendar/YYYY-Www.md`
2. If not, create from `09 System/Templates/Weekly Template.md`
   - Replace Templater placeholders with actual dates
   - The week note format is `YYYY-[W]ww` (e.g., `2026-W03`)

## Step 2: Journal Completeness Check

**Critical**: Verify all 7 days have journal entries and content.

```bash
# List last 7 days' journal files
for i in {0..6}; do
  d=$(date -d "$i days ago" +%Y-%m-%d)
  f="my-vault/02 Calendar/$d.md"
  if [[ -f "$f" ]]; then
    lines=$(wc -l < "$f")
    echo "$d: EXISTS ($lines lines)"
  else
    echo "$d: MISSING"
  fi
done
```

For each existing entry, check if sections are filled in:
- "# What Did I Do?" - should have content
- "# What Did I Work On?" - should have content
- "# What Did I Study?" - optional but note if empty

**Report gaps**: "These days are missing entries: ..." or "These entries look empty: ..."
**Offer to fill in**: "Want me to check GitHub for commits on those days to help fill them in?"

## Step 3: Review the Week

### GitHub Activity (all week)
```bash
gh search commits --author=TaylorHuston --committer-date=YYYY-MM-DD..YYYY-MM-DD --limit=50
```
Summarize by project/repo.

### Journal Highlights
Read each day's journal and extract:
- **Personal**: From "What Did I Do?"
- **Technical**: From "What Did I Work On?"
- **Learning**: From "What Did I Study?"

Present as a brief week summary, not raw dump.

### Learning Progress
1. Check `.claude/learning-sessions/learning-plan.json` if exists
2. Note topics covered, sessions completed

### Project Progress
1. Scan `ideas/*/issues/` for any WORKLOG.md updates this week
2. Note completed tasks, status changes

## Step 4: Fill In Weekly Note

Update the weekly note (`my-vault/02 Calendar/YYYY-Www.md`) sections:
- **What Went Well**: Ask Taylor
- **What Didn't Go Well**: Ask Taylor
- **Key Accomplishments**: Summarize from review
- **Lessons Learned**: Ask Taylor

## Step 5: Plan Next Week

Ask Taylor (one at a time):
1. "Any interviews or job search priorities this week?"
2. "What's the one thing that would make next week a success?"
3. "Any personal commitments to work around?"

Fill in "Next Week's Focus" section with their answers.

## Step 6: Memory Capture

Review conversation for memory-worthy items:
- Job search updates
- New preferences or workflow changes
- Project decisions
- Personal context changes

Update `.claude/memories/about-taylor.md` if job status or major context changed.

## Conversational Flow

Don't dump everything at once. Flow should be:
1. "Let me check your journal entries for this week..." → Report gaps
2. "Here's what I found from your week..." → Brief summary
3. "What went well this week?" → Capture response
4. "What didn't go well?" → Capture response
5. "Any lessons learned?" → Capture response
6. "Looking ahead - any job search priorities?" → Plan next week
7. "What would make next week a success?" → Set focus
8. "I've updated your weekly note. Anything else?"
