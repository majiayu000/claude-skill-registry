---
name: Finishing a Development Branch
description: Use this when you have completed some feature implementation and have written passing tests, and you are ready to create a PR.
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Use the Task tool to verify tests by using the project's test suite.

```bash
# Run project's test suite
bb test / npm test / cargo test / pytest / go test ./...
```

**If tests fail:**

```
Tests failing (<N> failures). Must fix before creating PR:

[Show failures]

Cannot proceed until tests pass.
```

2. Confirm that there is some formatting/lint/typechecking in the project. If NONE of these exist, ask me if there was something that you missed.

3. Use the Task tool to run any formatters and fix issues in a subagent.

```bash
# Clojure 
bb fmt

# Node.js/JavaScript/TypeScript
ls package.json 2>/dev/null && jq -r '.scripts | keys[]' package.json | grep -E 'format|lint'

# Rust
ls rustfmt.toml .rustfmt.toml 2>/dev/null

# Python
ls .flake8 pyproject.toml setup.cfg 2>/dev/null

# Go
ls .golangci.yml .golangci.yaml 2>/dev/null
```

4. Use the Task tool to run any linters and fix issues in a subagent.

```bash
# Clojure
bb lint

# Node.js - check package.json scripts
npm run lint  # or: npm run lint:fix, npm run eslint

# Rust
cargo clippy --fix --allow-dirty --allow-staged

# Python
ruff check --fix .
# or: flake8 ., pylint .

# Go
golangci-lint run --fix
```

5. Use the Task tool to run type checking and fix issues in a subagent.

6. Use the code-reviewer subagent to do a self review. You do *NOT* have to follow the subagent's suggestions. This is merely a way to get a fresh pair of eyes on the code.

7. Confirm that you are not on the main branch. If you are, ask me before proceeding. NEVER push to main without permission.

8. Use `git add` to stage the changes to files you edited for this feature. Follow

    Commit message rules:
    - Never mention beads, bd issues in the commit message
    - Never use **bold** formatting
    - Never use emoji in the commit message
    - Never mention Claude/AI/LLMS/Coding Agents in the commit message
    - Do not list or mention files in the commit message (that is redundant, the commit itself has a list of files)
    - Do not include other redundant or obvious information
    - Use `git log -n 10` to look at past 10 commits, follow a similar commit message style (number of lines, casing etc)

8. Push and create a PR.

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary

<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

9. Make sure the PR branch CI succeeds. Skip if there are no checks/ci.

```bash
# Check if the PR CI succeeded
gh pr checks

# If it is still running, sleep and check again
sleep 60 && gh pr checks
```

If CI did not pass, examine why.
If the CI did not start, this is likely due to merge conflicts; merge main, fix conflicts, and try again.
<system-reminder>Do not move forward without a ci status unless you have checked for merge conflicts</system-reminder>

- Make changes as needed, push a new commit, and repeat the process.
<system-reminder> It is *critical* that you fix any ci issues, EVEN IF YOU DID NOT CAUSE THEM. </system-reminder>

9. Tell me: "I can automatically get review comments, just let me know when to do so."
</required>


