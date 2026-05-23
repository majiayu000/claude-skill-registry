---
name: triage-workflow
description: SOC II triage workflow for creating Linear tickets, branches, OpenSpec proposals, commits, and PRs. Use when asked to triage an issue, create a triage ticket, or start SOC II workflow.
---

# SOC II Triage Workflow

> Orchestrates the complete triage process: Linear ticket → branch → OpenSpec proposal → implementation → commit → PR

## ⚠️ BEFORE YOU START

**This skill prevents 5 common errors and saves ~60% tokens by using subagents.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Setup Time | 30+ min | 5-10 min |
| Common Errors | 5+ | 0 |
| Token Usage | 50k+ | ~20k |

### Known Issues This Skill Prevents

1. Forgetting to create Linear ticket before starting work
2. Branch names not matching ticket identifiers
3. Commits missing ticket prefix (e.g., `ICE-1965:`)
4. OpenSpec proposals not validated before implementation
5. Context pollution from long-running workflows

## Workflow Overview

This skill guides you through a **7-step triage workflow**:

1. **Create Linear Ticket** - Use `linearis` CLI
2. **Create Git Branch** - Named after ticket identifier
3. **Create OpenSpec Proposal** - `/openspec:proposal`
4. **User Validates Proposal** - Review tasks and spec
5. **Apply OpenSpec Changes** - `/openspec:apply`
6. **Commit Changes** - `/git-commit` with ticket prefix
7. **Push & Create PR** - Optional, user decides

## Quick Start

### Step 1: Create Linear Ticket

```bash
# Run the helper script to create ticket
uv run scripts/create_linear_ticket.py "Issue title" --team TeamName --description "Details"
```

**Why this matters:** The ticket identifier (e.g., `ICE-1965`) becomes the prefix for branch names and commits.

### Step 2: Create Branch from Ticket

```bash
# Use the helper script (gets GitHub username automatically)
uv run scripts/create_branch.py ICE-1965 --push
# Creates: nodnarbnitram/ICE-1965
```

**Why this matters:** Branch format `username/identifier` enables traceability and ownership clarity.

### Step 3: Create OpenSpec Proposal

Use the slash command:
```
/openspec:proposal Add two-factor authentication
```

**Why this matters:** OpenSpec ensures alignment on requirements before implementation.

## Critical Rules

### ✅ Always Do

- ✅ Create Linear ticket FIRST before any code changes
- ✅ Use ticket identifier as branch name prefix
- ✅ Validate OpenSpec proposal with user before `/openspec:apply`
- ✅ Prefix all commits with ticket number (e.g., `ICE-1965: Fix bug`)
- ✅ Use subagents to keep main context clean

### ❌ Never Do

- ❌ Start coding without a Linear ticket
- ❌ Apply OpenSpec changes without user validation
- ❌ Commit without ticket prefix
- ❌ Push to main/master directly
- ❌ Skip the proposal validation step

### Common Mistakes

**❌ Wrong:**
```bash
git commit -m "Fix authentication bug"
```

**✅ Correct:**
```bash
git commit -m "ICE-1965: Fix authentication bug"
```

**Why:** SOC II compliance requires ticket traceability in all commits.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Missing ticket prefix | Forgot to extract identifier | Use `/git-commit` with prefix instruction |
| Branch name mismatch | Manual typing error | Use script to create branch from ticket |
| Proposal not validated | Rushed workflow | Always pause for user confirmation |
| Context bloat | Long workflows | Delegate to subagents for each step |

## Detailed Workflow Steps

### Phase 1: Ticket Creation

**Use subagent** to create Linear ticket:

```
> Create a Linear ticket for: [issue description]
```

The subagent will:
1. Run `linearis issues create` with appropriate parameters
2. Extract the ticket identifier from JSON response
3. Return the identifier (e.g., `ICE-1965`)

**Linearis command reference:**
```bash
linearis issues create "Title" \
  --team Backend \
  --description "Issue description" \
  --priority 2 \
  --labels "Bug,SOC-II"
```

### Phase 2: Branch Creation

After getting ticket identifier:

```bash
# Use helper script to create branch with GitHub username
uv run scripts/create_branch.py ICE-1965 --push
# Creates: nodnarbnitram/ICE-1965
```

### Phase 3: OpenSpec Proposal

Invoke the slash command:
```
/openspec:proposal [description of change]
```

This will:
1. Scaffold `openspec/changes/[change-id]/`
2. Create `proposal.md`, `tasks.md`, and delta specs
3. Return for user review

**CRITICAL: Wait for user validation before proceeding!**

### Phase 4: User Validation

Present the proposal to user and ask:
- Do the tasks in `tasks.md` make sense?
- Is the scope in `proposal.md` correct?
- Are the delta specs accurate?

Only proceed when user confirms.

### Phase 5: Apply OpenSpec Changes

After user validation:
```
/openspec:apply [change-name]
```

This implements the tasks defined in the proposal.

### Phase 6: Commit Changes

Use the git-commit command with ticket prefix:
```
/git-commit ICE-1965:
```

The commit helper will:
1. Analyze staged changes
2. Generate commit message
3. Prefix with ticket number

### Phase 7: Push & PR (Optional)

Ask user if they want to:
1. Push the branch
2. Create a pull request

If yes:
```bash
# Push
git push

# Create PR
gh pr create \
  --title "ICE-1965: [Description]" \
  --body "Fixes ICE-1965

## Summary
- [Change description]

## Test Plan
- [ ] Tests pass
- [ ] Manual verification"
```

## Bundled Resources

### Scripts

Located in `scripts/`:
- `create_linear_ticket.py` - Creates Linear ticket and returns identifier
- `create_branch.py` - Creates branch from ticket identifier
- `create_pr.py` - Creates PR with ticket reference

### References

Located in `references/`:
- [`linearis-reference.md`](references/linearis-reference.md) - Linearis CLI commands
- [`gh-cli-reference.md`](references/gh-cli-reference.md) - GitHub CLI commands
- [`openspec-reference.md`](references/openspec-reference.md) - OpenSpec workflow

> **Note:** For deep dives on specific tools, see the reference files above.

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| linearis | latest | Linear ticket management |
| gh | 2.x+ | GitHub CLI for PRs |
| openspec | 2.x+ | Spec-driven development |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| jq | 1.6+ | JSON parsing for scripts |

## Official Documentation

- [Linearis GitHub](https://github.com/czottmann/linearis)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec/)
- [GitHub CLI Manual](https://cli.github.com/manual/)

## Troubleshooting

### Linear ticket creation fails

**Symptoms:** `linearis` command returns error or empty response

**Solution:**
```bash
# Check authentication
echo $LINEAR_API_TOKEN
# Or check token file
cat ~/.linear_api_token

# Test with simple command
linearis issues list -l 1
```

### OpenSpec proposal not found

**Symptoms:** `/openspec:apply` can't find the change

**Solution:**
```bash
# List active changes
openspec list

# Validate the change
openspec validate [change-id]
```

### PR creation fails

**Symptoms:** `gh pr create` returns authentication error

**Solution:**
```bash
# Check GitHub auth
gh auth status

# Re-authenticate if needed
gh auth login
```

## Setup Checklist

Before using this skill, verify:

- [ ] `linearis` CLI installed and authenticated (`~/.linear_api_token` exists)
- [ ] `gh` CLI installed and authenticated (`gh auth status`)
- [ ] `openspec` installed (`npm install -g @fission-ai/openspec`)
- [ ] Git configured with user name and email
- [ ] Team name known for Linear tickets
