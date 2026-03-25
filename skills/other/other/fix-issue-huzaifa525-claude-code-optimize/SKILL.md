---
name: fix-issue
description: Fetch a GitHub issue, understand requirements, implement the fix, write tests, and commit
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[issue-number]"
---

Fix GitHub issue **#$ARGUMENTS**.

## Steps

1. **Fetch the issue**
   ```
   gh issue view $ARGUMENTS
   ```

2. **Understand requirements** — read the issue title, description, labels, and comments

3. **Create a branch**
   ```
   git checkout -b fix/issue-$ARGUMENTS
   ```

4. **Find relevant code** — use Grep and Glob to locate files related to the issue

5. **Read the code** — understand the current behavior and why it's wrong

6. **Implement the fix** — make the minimum changes needed

7. **Write/update tests** — ensure the fix is tested

8. **Run tests** — verify nothing is broken
   ```
   [test command from CLAUDE.md or package.json]
   ```

9. **Commit** with conventional message:
   ```
   git add [specific files]
   git commit -m "fix: [description] (#$ARGUMENTS)"
   ```

10. **Show summary** — what was changed, why, and what tests cover it

## If issue doesn't exist

Tell the user the issue was not found.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
