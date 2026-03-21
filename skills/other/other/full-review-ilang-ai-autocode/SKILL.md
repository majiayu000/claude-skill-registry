---
name: full-review
description: "[SAVE]=>[REVIEW:entire-project-from-beginning]=>[REPORT]=>[LEARN] MOST IMPORTANT. NEVER SKIP."
---
[PRIORITY:highest|trigger=every-save+commit+session-end]
[STEP1:save]
=>[GIT:commit|msg=human-readable]"Finished login feature"(not "feat: add auth")
=>[beginner:hide-git-commands|say="进度已保存。"]
[STEP2:review-from-beginning]
=>[READ:entire-codebase|from=first-file]
=>[CHECK:every-file]errors+inconsistencies+security+matches-requirements+earlier-code-needs-update
[STEP3:report|lang=plain]
completed+project-status+issues-found-fixed+whats-next
[STEP4:learn]
=>[RECORD:user-preferences+communication-style+mistakes+solutions]
=>[WRITE:.autocode/memory.md]
[RULE:NEVER-SKIP|NEVER-JUST-SAY="Saved."|ALWAYS-REVIEW-FROM-BEGINNING]
