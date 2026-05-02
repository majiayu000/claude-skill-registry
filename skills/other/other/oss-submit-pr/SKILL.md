---
name: oss-submit-pr
description: |
  Submit a pull request following the repo's contribution guidelines. Reviews the diff,
  checks for common rejection reasons, and helps the user write their own PR description.
  The LLM reviews - the user writes. Use when implementation is complete and tests pass.
---

# Submit PR

Get your PR right the first time. This skill checks your work against the repo's rules, catches common rejection reasons, and helps you write a PR description that maintainers actually want to read. You write the description - the LLM reviews it.

## Purpose

A clean PR gets reviewed and merged. A sloppy PR gets ignored or closed. Most new contributors get rejected not because their code is bad, but because they didn't follow the process - wrong branch, missing tests, unclear description, scope creep. This skill catches all of that before you hit submit.

## Prerequisites

- Implementation complete (from `oss-contribute`)
- Tests pass locally
- Lint/formatting passes locally
- User can explain what they changed and why (verified in `oss-contribute` step 6)

## Process

### 1. Re-read contribution requirements

Even if `oss-prep-to-contribute` already read these, read them again - specifically for PR submission rules:

```bash
# Fetch latest CONTRIBUTING.md
gh api repos/{owner}/{repo}/contents/CONTRIBUTING.md --jq '.content' | base64 -d 2>/dev/null

# Check for PR template - all standard locations
for path in \
  ".github/PULL_REQUEST_TEMPLATE.md" \
  ".github/pull_request_template.md" \
  "PULL_REQUEST_TEMPLATE.md" \
  "pull_request_template.md" \
  "docs/PULL_REQUEST_TEMPLATE.md" \
  "docs/pull_request_template.md"; do
  if content=$(gh api "repos/{owner}/{repo}/contents/$path" --jq '.content' 2>/dev/null); then
    printf '%s' "$content" | base64 -d 2>/dev/null
    break
  fi
done

# Check for multiple PR templates (directory-based)
gh api "repos/{owner}/{repo}/contents/.github/PULL_REQUEST_TEMPLATE" \
  --jq '.[] | .name' 2>/dev/null
```

**If a single template is found**: use it. The PR description must follow its structure exactly.

**If a template directory exists with multiple templates**: present each template name to the user and ask which one matches their contribution type (bug fix, feature, docs, etc.). Fetch the selected template and use it.

**If no template is found**: no template required - follow the general PR description guidance below.

Extract PR-specific requirements:
- PR template (must follow if present - check ALL locations above)
- Branch naming convention
- Commit message format (conventional commits? sign-off required? DCO?)
- Squash policy (squash before merge? maintainer squashes?)
- Linked issue format ("Fixes #123" vs "Closes #123" vs "Resolves #123")
- Required reviewers or labels
- CI checks that must pass

### 2. Pre-flight checks

Run every check the CI will run - locally, before pushing:

```bash
# Rebase on latest upstream
git fetch upstream
git rebase upstream/main

# Run tests
# {repo-specific test command}

# Run linting/formatting
# {repo-specific lint command}

# Check the diff is focused
git diff upstream/main...HEAD --stat
```

### 3. Review the diff

Go through the entire diff and flag issues:

```bash
git diff upstream/main...HEAD
```

Check for:

| Check | What to look for |
|-------|-----------------|
| **Scope creep** | Changes to files unrelated to the issue |
| **Debug leftovers** | console.log, print(), debugger, TODO comments |
| **Style drift** | Naming that doesn't match repo conventions |
| **Missing tests** | Code changes without corresponding test changes |
| **Commented-out code** | Dead code that shouldn't be committed |
| **Unrelated formatting** | Whitespace-only changes to lines you didn't modify |
| **Hardcoded values** | Magic numbers, hardcoded strings that should be constants |
| **Error handling** | New code paths without error handling (if repo expects it) |

For each issue found, present it to the user with the exact location:

> "Found a potential issue at `src/foo.ts:42` - you left a `console.log` from debugging. Remove it before submitting."

Don't auto-fix. Tell the user what and where.

### 4. Verify commit conventions

```bash
# Check commit messages against repo conventions
git log upstream/main..HEAD --oneline
```

If the repo uses conventional commits and the user's messages don't conform, explain the format and ask them to amend. If sign-off is required:

```bash
# Check for sign-off
git log upstream/main..HEAD --format='%B' | grep -c 'Signed-off-by'
```

### 5. Thinking gate - user writes the PR description

**The user writes the PR description, not the LLM.**

Tell the user:

> "Write your PR description. Start with one sentence: what does this PR do?
>
> Then add:
> 1. Link to the issue ('Fixes #number')
> 2. Why this approach - remember the trade-offs from /oss-contribute? Mention the key one
> 3. How you tested it - what did you run, what passed?
>
> Keep it short. If the repo has a PR template, follow it. Write in your own words - I'll review it after."

Wait for the user to write it.

### 6. Review the PR description

Once the user has written their description, review it for **conciseness and clarity**:

- Does it link the issue? ("Fixes #{number}")
- Does it follow the repo's PR template structure? (If a template was found in step 1, every section from the template must be addressed)
- Is it **short and direct**? Maintainers review dozens of PRs - they skim
- Does it explain non-obvious decisions **without over-explaining obvious ones**?
- Does it mention how the change was tested?

**Writing rules for PR descriptions:**
- Lead with what changed, not why you're writing
- One sentence per point. No paragraphs where a bullet works
- No filler: "This PR addresses the issue where..." → "Fixes null check in auth handler"
- No AI jargon: "comprehensive", "robust", "leverages", "utilizing" - cut all of it
- No self-narration: "I noticed that..." / "After investigating..." - just state the facts
- Technical terms are fine. Buzzwords are not
- If the PR template asks for something, answer it. Don't add extra sections

Give specific feedback:

> "Your description is good, but trim the first paragraph - the reviewer doesn't need the backstory. Lead with what changed."

Don't rewrite it - give feedback and let the user revise.

### 7. Submit

Once the description passes review:

```bash
# Push the branch
git push origin {branch-name}

# Create the PR
gh pr create \
  --repo {owner}/{repo} \
  --title "{title following repo convention}" \
  --body "$(cat <<'EOF'
{user's PR description}
EOF
)"
```

### 8. Post-submission verification

```bash
# Check CI status
gh pr checks {pr-number} -R {owner}/{repo} --watch
```

If CI fails:
- Explain WHAT failed (test name, lint rule, build error)
- Point to the relevant code
- Don't fix it - tell the user what needs to change

## Common rejection reasons (educate the user)

Present these before submission as a final checklist:

1. **Scope creep** - PR touches files unrelated to the issue
2. **No tests** - code changes without test changes in a repo that expects tests
3. **CI failure** - tests or lint fail (never submit with red CI)
4. **Poor description** - maintainer can't understand what the PR does from the description alone
5. **Wrong base branch** - PR targets wrong branch (check repo conventions)
6. **Style violations** - code doesn't match repo's formatting/naming conventions
7. **Breaking changes without discussion** - changes public API without prior maintainer approval

## Related Skills

- **Previous step**: ← `oss-contribute` - the implementation work
- **Next step**: → `oss-post-pr` - handle review feedback after submission
- **If CI fails**: Fix locally and push again (don't invoke another skill, just fix and push)

## Anti-patterns

- **DO NOT** write the PR description for the user - review and give feedback on theirs
- **DO NOT** auto-fix diff issues - tell the user what and where, they fix it
- **DO NOT** submit with failing CI - ever
- **DO NOT** skip the pre-flight checks - "it works on my machine" is not enough
- **DO NOT** include "AI-generated" boilerplate in the PR unless the repo's CODE_OF_CONDUCT requires disclosure
