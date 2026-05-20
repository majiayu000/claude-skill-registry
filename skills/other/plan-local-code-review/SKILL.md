---
name: plan-local-code-review
description: This skill should be used when performing a code review on local changes on the current branch compared to the main branch. It uses multiple parallel agents to check for bugs, CLAUDE.md compliance, git history context, previous PR comments, and code comment adherence, then scores and filters findings by confidence level.
disable-model-invocation: false
---

Provide a code review for the local changes on the current branch compared to the main branch.

To do this, follow these steps precisely:

1. Use a Haiku agent to check the current git state:
   - Run `git branch --show-current` to get the current branch name
   - Run `git log main..HEAD --oneline` to see commits on this branch
   - Run `git diff main...HEAD --stat` to see changed files
   - If the current branch IS main, or there are no commits/changes compared to main, do not proceed.
2. Use another Haiku agent to give you a list of file paths to (but not the contents of) any relevant CLAUDE.md files from the codebase: the root CLAUDE.md file (if one exists), as well as any CLAUDE.md files in the directories whose files were modified on this branch
3. Use a Haiku agent to analyze the branch changes:
   - Run `git log main..HEAD --format="%s%n%b"` to get commit messages
   - Run `git diff main...HEAD` to get the full diff
   - Return a summary of the changes
4. Then, launch 5 parallel Sonnet agents to independently code review the change. The agents should do the following, then return a list of issues and the reason each issue was flagged (eg. CLAUDE.md adherence, bug, historical git context, etc.):
   a. Agent #1: Audit the changes to make sure they comply with the CLAUDE.md. Note that CLAUDE.md is guidance for Claude as it writes code, so not all instructions will be applicable during code review.
   b. Agent #2: Read the file changes (via `git diff main...HEAD`), then do a shallow scan for obvious bugs. Avoid reading extra context beyond the changes, focusing just on the changes themselves. Focus on large bugs, and avoid small issues and nitpicks. Ignore likely false positives.
   c. Agent #3: Read the git blame and history of the code modified, to identify any bugs in light of that historical context
   d. Agent #4: Read previous pull requests that touched these files, and check for any comments on those pull requests that may also apply to the current changes.
   e. Agent #5: Read code comments in the modified files, and make sure the changes comply with any guidance in the comments.
5. For each issue found in #4, launch a parallel Haiku agent that takes the diff, issue description, and list of CLAUDE.md files (from step 2), and returns a score to indicate the agent's level of confidence for whether the issue is real or false positive. To do that, the agent should score each issue on a scale from 0-100, indicating its level of confidence. For issues that were flagged due to CLAUDE.md instructions, the agent should double check that the CLAUDE.md actually calls out that issue specifically. The scale is (give this rubric to the agent verbatim):
   a. 0: Not confident at all. This is a false positive that doesn't stand up to light scrutiny, or is a pre-existing issue.
   b. 25: Somewhat confident. This might be a real issue, but may also be a false positive. The agent wasn't able to verify that it's a real issue. If the issue is stylistic, it is one that was not explicitly called out in the relevant CLAUDE.md.
   c. 50: Moderately confident. The agent was able to verify this is a real issue, but it might be a nitpick or not happen very often in practice. Relative to the rest of the changes, it's not very important.
   d. 75: Highly confident. The agent double checked the issue, and verified that it is very likely it is a real issue that will be hit in practice. The existing approach is insufficient. The issue is very important and will directly impact the code's functionality, or it is an issue that is directly mentioned in the relevant CLAUDE.md.
   e. 100: Absolutely certain. The agent double checked the issue, and confirmed that it is definitely a real issue, that will happen frequently in practice. The evidence directly confirms this.
6. Filter out any issues with a score less than 80.
7. Write the review to claude-review.md. When writing your review, keep in mind to:
   a. Keep your output brief
   b. Avoid emojis
   c. Reference relevant files and line numbers
8. Briefly summarize claude-review.md as direct output to the user

Examples of false positives, for steps 4 and 5:

- Pre-existing issues
- Something that looks like a bug but is not actually a bug
- Pedantic nitpicks that a senior engineer wouldn't call out
- Issues that a linter, typechecker, or compiler would catch (eg. missing or incorrect imports, type errors, broken tests, formatting issues, pedantic style issues like newlines). No need to run these build steps yourself -- it is safe to assume that they will be run separately as part of CI.
- General code quality issues (eg. lack of test coverage, general security issues, poor documentation), unless explicitly required in CLAUDE.md
- Issues that are called out in CLAUDE.md, but explicitly silenced in the code (eg. due to a lint ignore comment)
- Changes in functionality that are likely intentional or are directly related to the broader change
- Real issues, but on lines that were not modified in the current branch

Notes:

- Do not check build signal or attempt to build or typecheck the app. These will run separately, and are not relevant to your code review.
- Use git commands to analyze local changes (not `gh` commands for remote PRs)
- Make a todo list first
- You must cite each bug with file path and line number (eg. if referring to a CLAUDE.md, you must reference it)
- For your final output, follow the following format precisely (assuming for this example that you found 3 issues):

---

### Code review for branch `<branch-name>`

Reviewed X commits with changes to Y files.

Found 3 issues:

1. **<brief description of bug>** (CLAUDE.md says "<...>")
   - File: `path/to/file.ts:L10-L15`

2. **<brief description of bug>** (some/other/CLAUDE.md says "<...>")
   - File: `path/to/other-file.ts:L25-L30`

3. **<brief description of bug>** (bug due to <reasoning>)
   - File: `path/to/another-file.ts:L5-L8`

---

- Or, if you found no issues:

---

### Code review for branch `<branch-name>`

Reviewed X commits with changes to Y files.

No issues found. Checked for bugs and CLAUDE.md compliance.

---
