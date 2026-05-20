---
name: open-pr
description: Create GitHub pull requests from conversation context with proper formatting and tag selection
---

# Open PR

This skill instructs AI agents on how to create GitHub pull requests from conversation context
with meaningful titles, proper formatting, and appropriate tag selection. The AI agent
should analyze the conversation, extract PR details, and confirm with the user before
creating the pull request.

## PR Format

GitHub pull requests created by this skill must follow this exact structure:

```markdown
# [tag][#issue-number] Brief description of what was achieved

## Summary

Provide a concise summary of what has been achieved in this PR. Focus on the
completed work and the value it delivers.

## Changes

Provide a detailed list of changes made in this PR:
- Modified `file_path:line_range` to implement X
- Added `new_file.py` for Y functionality
- Updated `config.json` to support Z
- Removed deprecated code from `old_file.py:line_range`

## Testing

Describe what was tested and how:
- Added `tests/test_feature.py` to verify behavior A
- Modified `tests/test_existing.py:line_range` to cover edge case B
- Manually tested scenario C with the following steps:
  1. Step 1
  2. Step 2
  3. Expected result

## Related Issue

Closes #issue-number

(Or "Part of #issue-number" if this PR partially addresses the issue)
```

## Tag Selection

A `git-msg-tags.md` file should appear in `{ROOT_PROJ}/docs/git-msg-tags.md` which
defines the tags related to the corresponding modules or modifications. The AI agent
**MUST** refer to this file to select the appropriate tag for the PR title.

If the file does not exist, reject the PR creation and ask the user to provide a
list of tags in `docs/git-msg-tags.md`.

### Tag Logic

The AI agent must determine which tag to use based on the PR type by reading
`docs/git-msg-tags.md` which contains the project's tag definitions.

**Selection guidelines:**
- Read `docs/git-msg-tags.md` to understand available tags and their meanings
- Choose the most specific tag that describes the primary change
- If multiple tags could apply, choose the one that best represents the core purpose
- If the tag is ambiguous, ask the user to select from 2-3 most relevant options

## Workflow for AI Agents

When this skill is invoked, the AI agent **MUST** follow these steps:

### 1. Context Analysis Phase

Review the entire conversation history and git changes to extract PR details:
- Identify what work was completed during the conversation
- Review git diff and git status to see actual changes made
- Extract key details: what was changed, why, which files were affected
- Determine the type of changes (feature, bugfix, refactor, etc.)
- Check if there's a related issue number mentioned in the conversation

Context signals for PR type:
- Feature signals: new functionality added, new files created, capabilities extended
- Bugfix signals: fixed error, resolved issue, corrected behavior
- Refactor signals: improved code structure, reorganized code, better patterns
- Documentation signals: updated README, added comments, wrote guides
- Test signals: added test coverage, modified test cases

### 2. Git Changes Review

**CRITICAL:** Before drafting the PR, the AI agent **MUST** review actual git changes:

```bash
# Check what files have changed
git status

# Review the actual changes
git diff

# Check commit history on current branch
git log origin/main..HEAD --oneline
```

This ensures the PR description accurately reflects the actual code changes.

### 3. Tag Selection Phase

- Read `docs/git-msg-tags.md` to understand available tags
- Analyze the changes and determine the primary purpose
- Apply the tag logic described above
- If multiple tags could apply, choose the most specific one
- If the tag is ambiguous, ask the user to choose from 2-3 most relevant options

### 4. Issue Number Extraction

**CRITICAL:** The PR title **MUST** include an issue number in the format `[tag][#N]`.

**How to find the issue number:**
1. Search conversation history for explicit issue references:
   - "for issue #42"
   - "closes #15"
   - "related to #23"
   - GitHub issue URLs containing issue numbers

2. If no issue number is found in conversation:
   - Check if there are recent issues that match this work:
     ```bash
     gh issue list --limit 10
     ```
   - Ask the user: "Which issue does this PR address? (Provide issue number)"

3. If user says there's no related issue:
   - **STOP** and inform the user:
     ```
     Cannot create PR without a related issue.
     Please create an issue first using the open-issue skill, or provide an existing issue number.
     ```

**Never create a PR without an issue number.**

### 5. PR Draft Construction

Build the PR following the format specification:

**Title:**
- Format: `[tag][#issue-number] Brief description`
- The description should be in past tense (what was achieved)
- Keep description concise (max 80 characters for the description portion)
- Example: `[feat][#42] Add TypeScript SDK template support`
- Example: `[bugfix][#15] Fix pre-commit hook test execution`

**Summary section:**
- Describe what has been achieved (past tense)
- Focus on the value and purpose of the changes
- Keep it concise but meaningful

**Changes section:**
- List specific files modified, added, or deleted
- Include line ranges when relevant (e.g., `file.py:12-34`)
- Describe what each change does
- Order changes logically (not just alphabetically)
- **DO NOT** include actual code snippets to save context length

**Testing section:**
- Describe what was tested
- List new test files added with what they test
- List modified test files with what new coverage was added
- Include manual testing steps if applicable
- Be specific about test scenarios and expected outcomes

**Related Issue section:**
- Use `Closes #N` if this PR fully resolves the issue
- Use `Part of #N` if this PR partially addresses the issue
- Use `Fixes #N` for bugfix PRs
- GitHub will automatically link and close the issue when PR is merged

### 6. User Confirmation Phase

**CRITICAL:** The AI agent **MUST** display the complete PR draft to the user
and wait for explicit confirmation before creating the PR.

Present the draft in a clear format:
```
I've prepared this pull request:

---
[Full PR content here]
---

Should I create this PR?
```

- Wait for explicit "yes", "confirm", "create it", or similar affirmative response
- If the user requests modifications, update the draft and present again
- If the user declines, abort PR creation gracefully

### 6.5. Remote Branch Verification

**CRITICAL:** Before creating the PR, verify the current branch exists on the remote repository.

Check if the current branch is tracking a remote branch:

```bash
# Check if current branch has an upstream branch
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

**If the command fails (no upstream branch):**
1. Get the current branch name:
   ```bash
   git branch --show-current
   ```
2. Push the branch with tracking:
   ```bash
   git push -u origin <branch-name>
   ```
3. Confirm to user: "Pushed branch to remote: origin/<branch-name>"

**If the command succeeds (upstream branch exists):**
1. Check if local is ahead of remote:
   ```bash
   git status --porcelain --branch
   ```
2. If output contains `[ahead N]`, push changes:
   ```bash
   git push
   ```
3. If up-to-date, continue to PR creation

**Error handling:**
- If push fails due to authentication:
  ```
  Git push failed. Please check your Git credentials.
  ```
- If push fails due to conflicts:
  ```
  Cannot push: your branch has diverged from remote.
  Please resolve conflicts manually with:
    git pull --rebase origin <branch-name>
  ```
- For other push failures: Display the error and abort PR creation

### 7. GitHub PR Creation

Once confirmed and the branch is on remote, create the PR using the GitHub CLI:

```bash
gh pr create --title "TITLE_HERE" --body "$(cat <<'EOF'
BODY_CONTENT_HERE
EOF
)"
```

**Important:**
- Use heredoc (`<<'EOF' ... EOF`) to preserve markdown formatting
- The body should include all sections from Summary onwards (not the title)
- The PR will be created against the default branch (usually main/master)
- After successful creation, display the PR URL to the user
- Confirm: "Pull request created successfully: [URL]"

**Optional flags:**
- Add `--draft` if the user wants to create a draft PR
- Add `--base BRANCH` if targeting a different base branch

### 8. Error Handling

Handle common error scenarios gracefully:

**Missing git-msg-tags.md:**
```
Cannot create PR: docs/git-msg-tags.md not found.
Please create this file with your project's tag definitions.
```

**No issue number found:**
```
Cannot create PR: No related issue number found.

Please either:
1. Provide the issue number this PR addresses
2. Create an issue first using the open-issue skill
```

**No git changes:**
```
Cannot create PR: No changes detected in the working directory.
Please make and commit your changes first.
```

**GitHub CLI not authenticated:**
```
GitHub CLI is not authenticated. Please run:
  gh auth login
```

**Not on a feature branch:**
```
Warning: You're on the main/master branch.
PRs should typically be created from feature branches.

Create a new branch with:
  git checkout -b feature/your-feature-name

Or confirm you want to create a PR from the current branch.
```

**No conversation context:**
```
I don't have enough context to create a PR. Could you please provide:
- What changes were made?
- What issue does this PR address?
- What was tested?
```

**PR creation failed:**
```
Failed to create pull request: [error message]
Please check your GitHub CLI configuration and try again.
```

## Ownership

The AI agent **SHALL NOT** claim authorship or co-authorship of the pull request.
The PR is created on behalf of the user, who is **FULLY** responsible for its content.

Do not add any "Created by AI" or similar attributions to the PR body unless
explicitly requested by the user.

## Examples

**Note:** The following examples use tags like `[feat]`, `[bugfix]`, `[agent.skill]` etc.
These are illustrative only - actual tags must come from your project's `docs/git-msg-tags.md`.

### Example 1: Feature PR

**Context:** User implemented TypeScript SDK template support to close issue #42.

**PR:**
```markdown
# [feat][#42] Add TypeScript SDK template support

## Summary

Added support for generating TypeScript SDK templates in the agentize project.
Developers can now bootstrap TypeScript-based agent SDKs alongside existing
Python templates.

## Changes

- Created `templates/typescript/` directory structure with standard layout
- Added `templates/typescript/package.json` with default dependencies (typescript, @types/node)
- Created `templates/typescript/tsconfig.json` with recommended compiler settings
- Added `templates/typescript/src/index.ts` as the SDK entry point
- Updated `claude/skills/sdk-init/SKILL.md` to include TypeScript as a language option
- Modified `sdk-init` skill logic to handle TypeScript template generation

## Testing

- Added `tests/test_typescript_template.py` to verify:
  - Template directory creation
  - All required files are generated correctly
  - package.json has correct dependencies
  - tsconfig.json has proper compiler options
- Manually tested TypeScript template generation:
  1. Ran sdk-init skill and selected TypeScript
  2. Verified generated files compile without errors
  3. Confirmed npm install works correctly
  4. Built sample TypeScript SDK successfully

## Related Issue

Closes #42
```

### Example 2: Bugfix PR

**Context:** User fixed pre-commit hook not running tests (issue #15).

**PR:**
```markdown
# [bugfix][#15] Fix pre-commit hook test execution

## Summary

Fixed the pre-commit hook to properly execute the test suite before allowing commits.
The hook was not running tests due to incorrect path resolution.

## Changes

- Modified `.git/hooks/pre-commit:8-12` to use absolute path for test script
- Updated hook to check exit code and block commit on test failure
- Added error message output when tests fail

## Testing

- Modified `tests/test_hooks.py:23-45` to verify pre-commit hook behavior
- Manually tested the fix:
  1. Made changes to a Python file in `claude/skills/`
  2. Ran `git add .` and `git commit -m "test"`
  3. Confirmed tests executed and commit was blocked when tests failed
  4. Fixed the test failure
  5. Confirmed commit succeeded after tests passed

## Related Issue

Fixes #15
```

### Example 3: Agent Skill PR

**Context:** User created the open-pr skill (issue #67).

**PR:**
```markdown
# [agent.skill][#67] Add open-pr skill for creating pull requests

## Summary

Added the open-pr skill that guides AI agents through creating well-formatted
GitHub pull requests with proper tag selection and mandatory issue references.

## Changes

- Created `claude/skills/open-pr/` directory
- Added `claude/skills/open-pr/SKILL.md` with complete PR creation workflow
- Skill enforces issue number requirement in PR titles
- Includes comprehensive examples and error handling guidelines

## Testing

- Added `tests/test_open_pr_skill.py` to verify:
  - Skill file structure and format
  - Tag selection logic correctness
  - Issue number extraction from various formats
- Manually tested skill workflow:
  1. Invoked open-pr skill in conversation
  2. Verified it correctly extracted issue number from context
  3. Confirmed it generated proper PR format
  4. Tested error handling for missing issue numbers

## Related Issue

Closes #67
```
