---
version: 1.0.0
name: meta-merge-contributions
description: >
  Review and merge skill contribution branches into main. Lists pending
  contrib/ branches, shows diffs, and applies changes with version bumps
  and changelog updates. Use when the user says "merge contributions",
  "review contributions", "check for skill contributions", or after
  /meta-contribute-back has staged changes.
disable-model-invocation: true
user-invocable: true
argument-hint: "[--skill name | --all | --list]"
---

# Merge Contributions — Review & Apply Skill Improvements

Review contribution branches created by `/meta-contribute-back` from project
repos and merge approved improvements into skills with proper version bumps.

> This skill is designed for use in the agentic-workflow repo itself.

## Step 1: List Contribution Branches

1. List all `contrib/*` branches: `git branch --list 'contrib/*'`
2. Parse branch names to extract project and skill:
   - Pattern: `contrib/{project-name}/{skill-name}`
3. Group by skill name
4. If `--list` flag: show summary table and stop
5. If `--skill` flag: filter to that skill only

```
### Pending Contributions

| Branch | Project | Skill | Commits |
|--------|---------|-------|---------|
| contrib/my-project/dev-tdd-backend | my-project | dev-tdd-backend | 2 |
| contrib/my-project/dev-security-backend | my-project | dev-security-backend | 1 |
| contrib/other-project/dev-tdd-backend | other-project | dev-tdd-backend | 1 |
```

## Step 2: Review Each Contribution

6. For each branch (or filtered set):
   a. Show the branch log: `git log main..{branch} --oneline`
   b. Read contribution files on the branch:
      - Switch to branch (or use `git show {branch}:path`)
      - Read each file in `contributions/{skill-name}/`
   c. Read the current skill SKILL.md on main
   d. Present the proposed change:

```
### Contribution: Aspire Integration Tests

**Branch:** contrib/my-project/dev-tdd-backend
**From:** my-project
**Skill:** dev-tdd-backend (current: 1.0.0)
**Classification:** universal

**What changed:**
Added Phase 4 for Aspire integration tests using TestContainers.

**Proposed changes:**
[Content from the contribution file]

**Context:**
[Why this was needed]

Action? [merge / reject / defer]
```

## Step 3: Apply Merge

7. On **merge**:
   a. Read the contribution's proposed changes
   b. Apply the changes to the skill's SKILL.md on main
   c. Determine version bump:
      - Content addition (new section, new step) → **minor** bump
      - Wording fix, clarification → **patch** bump
      - Restructured workflow, removed steps → **major** bump (confirm with user)
   d. Update the skill's SKILL.md frontmatter `version` field
   e. Append entry to the skill's `CHANGELOG.md`:
      ```
      ## {new-version} — {YYYY-MM-DD}

      - {Description of change} (contributed from {project-name})
      ```
   f. Update `catalog.json`:
      - Set the skill's `version` to the new version
      - Update catalog `updated` date
   g. Remove the contribution file(s) for this skill from `contributions/`
   h. Commit on main: `feat({skill-name}): {description} [from {project}]`
   i. Delete the contribution branch: `git branch -d {branch}`
   j. Log to daily memory

## Step 4: Handle Reject / Defer

8. On **reject**:
   a. Ask for an optional reason
   b. Delete the contribution branch: `git branch -d {branch}`
   c. Log rejection in daily memory with reason

9. On **defer**:
   a. Leave the branch as-is
   b. Note in daily memory: "Deferred contribution: {skill} from {project}"

## Step 5: Report

10. After processing all contributions, show summary:

```
### Merge Results

| Skill | Action | New Version | Branch |
|-------|--------|-------------|--------|
| dev-tdd-backend | merged | 1.1.0 | deleted |
| dev-security-backend | rejected | — | deleted |
| dev-tdd-backend (other-project) | deferred | — | kept |

Merged skills can now be distributed via /meta-upgrade in target projects.
```

## Flags

| Flag | Behavior |
|------|----------|
| `--list` | Show pending contribution branches (read-only) |
| `--skill <name>` | Process only contributions for this skill |
| `--all` | Process all pending contributions |

## Safety Rules

- **Always review before merging** — show the full proposed change and get user approval
- **Single commit per skill** — each merged contribution gets its own commit
- **Never skip version bump** — every merge must bump the version
- **Never delete branches without confirmation** — for reject, always ask
- **Preserve contribution context** — the commit message should reference the source project
- **Clean up** — remove contribution files and branches after merge/reject
