---
name: save-rollback
description: When things go wrong, go back to the last working version.
---

# Rollback

When something breaks badly and fixing is too complex:
1. Git log to find last working commit
2. Revert to that commit
3. Tell user: "我退回到了上一个能正常运行的版本。刚才的改动撤销了，不用担心。"

Never say "git revert" or "git reset" to a beginner user. Just say "退回到上一个好的版本了。"

Only use rollback when:
- Fix would take longer than rebuilding
- Multiple things broke at once
- User explicitly asks to "退回去" or "回到之前的"
