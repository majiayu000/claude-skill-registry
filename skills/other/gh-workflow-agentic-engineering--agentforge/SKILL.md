---
name: gh-workflow
description: GitHub workflow using the gh CLI for PRs, issues, CI checks, and code review. Use this instead of the GitHub MCP — covers creating PRs with spec references, monitoring CI runs, and reviewing PR comments.
argument-hint: "[pr|issue|ci|review]"
---

Use the `gh` CLI for all GitHub operations in AgentForge.

---

## PR Workflow

**List open PRs:**
```bash
gh pr list
```

**View PR details:**
```bash
gh pr view [number]
```

**Check CI status for a PR:**
```bash
gh pr checks [number]
```

**Create a PR** (always use a HEREDOC for the body):
```bash
gh pr create --title "SPEC-NNN: Short description" --body "$(cat <<'EOF'
## Summary
- What this PR does

## Test plan
- [ ] pnpm test — all green
- [ ] tsc --noEmit — 0 errors
- [ ] pnpm audit — 0 high/critical
- [ ] Manual: agentforge start / chat / status
- [ ] Related spec: SPEC-NNN

🤖 Generated with Claude Code
EOF
)"
```

**Merge a PR:**
```bash
gh pr merge [number] --squash --delete-branch
```

---

## Issue Workflow

**List issues:**
```bash
gh issue list
gh issue list --label "bug"
```

**View an issue:**
```bash
gh issue view [number]
```

**Create an issue linked to a spec:**
```bash
gh issue create --title "SPEC-NNN: Short description" \
  --body "Implements specs/active/SPEC-NNN-<title>.md"
```

**Close an issue:**
```bash
gh issue close [number]
```

---

## CI / Actions Workflow

**List recent runs:**
```bash
gh run list --limit 5
```

**Watch a run live:**
```bash
gh run watch
```

**View failed run logs:**
```bash
gh run view [run-id] --log-failed
```

---

## Code Review

**View PR with all comments:**
```bash
gh pr view [number] --comments
```

**Add a review comment:**
```bash
gh pr review [number] --comment -b "Your comment here"
```

**Approve or request changes:**
```bash
gh pr review [number] --approve
gh pr review [number] --request-changes -b "Please fix X before merging"
```

---

## AgentForge PR Guidelines

- Title must reference the related spec: `SPEC-NNN: description`
- Body must include test plan: `pnpm test`, `tsc --noEmit`, `pnpm audit`, manual CLI test
- Link to the spec file in `specs/active/`
- Never force-push to `main`
