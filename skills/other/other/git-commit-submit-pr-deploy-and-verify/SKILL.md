---
name: git-commit-submit-pr-deploy-and-verify
description: This skill should be used when creating conventional commits for current changes and then submitting the current branch as a pull request for code review. And then verifying the pull request was approved. As well as making sure the resutling deploy succeeds.
allowed-tools: ["Bash"]
---

Run the /git-commit-submit-pr-and-verify with $ARGUMENTS. Once the merge is complete, follow the resulting deploy and fix anything that breaks with the deploy and then follow this process again with a new PR until the deploy succeeds.
