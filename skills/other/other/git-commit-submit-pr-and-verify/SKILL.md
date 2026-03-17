---
name: git-commit-submit-pr-and-verify
description: This skill should be used when creating conventional commits for current changes and then submitting the current branch as a pull request for code review. And then verifying the pull request was approved.
allowed-tools: ["Bash"]
---

Run the /git-commit-and-submit-pr with $ARGUMENTS and set the PR to auto-merge. Fix any pre-commit or pre-push issues and then follow the pr, make sure all checks pass and comments are resolved or addressed. Fix anything that is broken and repeat.
