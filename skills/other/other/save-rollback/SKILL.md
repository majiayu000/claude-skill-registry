---
name: save-rollback
description: "[ROLLBACK:to-last-working]=>[SAY:plain-language|hide-git-commands]"
---
[TRIGGER:badly-broken+fix-too-complex]
[GIT:log]=>[FIND:last-working-commit]=>[REVERT]
[SAY:"我退回到了上一个能正常运行的版本。刚才的改动撤销了，不用担心。"]
[SAY:"git revert"|"git reset"|to-beginner=never]
[USE:only-when]fix>rebuild-time|multiple-breaks|user-says="退回去"
