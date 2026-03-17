---
name: git-commit-and-submit-pr
description: This skill should be used when creating conventional commits for current changes and then submitting the current branch as a pull request for code review. It combines the git:commit and git:submit-pr skills into a single workflow.
allowed-tools: ["Bash"]
---

1. Run /git-commit $ARGUMENTS
2. Run /git-submit-pr $ARGUMENTS
