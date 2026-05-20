---
name: plan-w-team
description: >
  Break work into GitHub Issues with labels, dependencies, and acceptance criteria.
  Interviews Odin via Freya, wireframes via Luna (if UI), then files issues to the
  Project board and writes an epic dependency graph to tmp/epics/<N>.yml for
  /epic-manager to track. Use when the user says 'plan', 'plan with team',
  'break this into issues', or describes a feature/bug needing structured planning.
---

# Plan With Team

Break the user's request into GitHub Issues on Project #1. Each issue becomes a unit
of work that `/fire-next-up` picks up and runs through the agent chain. After filing,
write `tmp/epics/<root-N>.yml` so `/epic-manager` can track and dispatch the epic.

## Model

Use **Opus** for this skill — deep reasoning required for dependency analysis and
issue decomposition.

## Disallowed Tools

Do NOT use: `Task`, `EnterPlanMode`

## Variables

USER_PROMPT: $1
TEAM_MEMBERS:
  - Product Owner: `.claude/agents/freya.md` (subagent_type: freya-product-owner)
  - UX Designer: `.claude/agents/luna.md` (subagent_type: luna-ux-designer)
  - Builder: `.claude/agents/fireman-decko.md` (subagent_type: fireman-decko-principal-engineer)
  - Validator: `.claude/agents/loki.md` (subagent_type: loki-qa-tester)
  - Security: `.claude/agents/heimdall.md` (subagent_type: heimdall)

## Instructions

- **PLANNING ONLY**: Do NOT build, write code, or deploy agents. Your only output is GitHub Issues + the epic graph file.
- If no `USER_PROMPT` is provided, stop and ask the user to provide it.
- Think deeply about the best approach before breaking work into issues.
- Understand the codebase directly (no subagents) to understand existing patterns.
- Each issue must be small enough for a single agent chain to complete (1 branch, 1 PR).
- Break the work into as many issues as needed — no cap. Each issue must be small enough for a single agent chain.
- Issues must have correct type and priority labels so `/fire-next-up` routes them to the right agent chain.

## Workflow

### Step 1 — Analyze Requirements

Parse the USER_PROMPT. Determine:
- Work type: feature, bug, ux, security, test, chore
- Complexity: simple (1 issue), medium (2-5 issues), complex (6+ issues)
- Whether UI changes are involved (triggers Luna in Step 3)

### Step 2 — Freya Interviews Odin

Spawn Freya to clarify requirements with the user:

```
Agent({
  subagent_type: "freya-product-owner",
  prompt: "The user's name is Odin. He is the project owner and ultimate decision-maker
    for Fenrir Ledger. Address him as Odin.

    Interview Odin to clarify requirements for: <USER_PROMPT>

    Ask about:
    - Priorities and must-haves vs nice-to-haves
    - Edge cases and error scenarios
    - UX preferences (if UI work)
    - Acceptance criteria — what does 'done' look like?

    Use AskUserQuestion to conduct the interview.
    When done, summarize your findings as a structured brief with:
    - Problem statement
    - Requirements (numbered)
    - Acceptance criteria (checkboxes)
    - Priority recommendation (critical/high/normal/low)
    - Suggested issue breakdown (if multiple issues needed)"
})
```

Wait for Freya's summary before proceeding.

### Step 3 — Luna Wireframes (UI work only)

**Skip this step** if the work has no UI changes.

If the plan involves UI changes, spawn Luna:

```
Agent({
  subagent_type: "luna-ux-designer",
  prompt: "The user's name is Odin. Interview Odin about UX preferences using
    AskUserQuestion before producing wireframes.

    Create HTML5 wireframes (no theme styling — structure only) for:
    <UI components from Freya's brief>

    Write wireframes to ux/wireframes/<feature-slug>/.
    Questions to ask: layout preferences, interaction patterns, mobile behavior.

    When done, summarize:
    - Files created
    - Key layout decisions
    - Mobile behavior
    - Interaction patterns"
})
```

Wait for Luna's wireframes before proceeding. Reference them in issue bodies.

### Step 3b — Commit Design Artifacts

If Luna produced wireframes or if the orchestrator modified any design files (e.g., mermaid fixes),
commit them before filing issues. Implementers need these artifacts on `main`.

```bash
# Check for uncommitted design artifacts
git status --short -- ux/ product/

# If there are changes:
git checkout -b ux/<feature-slug>-wireframes
git add ux/ product/
git commit -m "feat(ux): add <feature> wireframes and interaction spec

Refs #<issue numbers if known>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push -u origin ux/<feature-slug>-wireframes
gh pr create --title "Add <feature> wireframes" --body "Luna wireframes for <feature>"
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

### Step 4 — Break Into Issues

Using Freya's brief (and Luna's wireframes if applicable), break the work into as many issues as the scope requires.

**Issue sizing rules:**
- Each issue = 1 branch + 1 PR + 1 agent chain
- A `ux` issue runs Luna -> FiremanDecko -> Loki (3-step chain)
- A `enhancement` or `bug` issue runs FiremanDecko -> Loki (2-step chain)
- A `security` issue runs Heimdall -> Loki (2-step chain)
- A test-only issue runs Loki only (1-step chain)
- If an issue needs both UX design AND implementation, label it `ux` — the chain handles both

**Dependency rules:**
- Issues that can be worked in parallel should have NO dependency references
- Issues that depend on others include `Blocked by #N` in their body
- `/fire-next-up` checks if blocking issues are still open before dispatching

**Label assignment:** See `quality/issue-template.md` for the full schema.
Each issue gets one type label (`bug`, `enhancement`, `ux`, `security`) and one
priority label (`critical`, `high`, `normal`, `low`).

### Step 5 — Create Issues via /file-issue

Create each issue sequentially (need the issue number from each to set dependencies on later ones).

**Title format:** Short and descriptive — no `[Type]` or `[Priority]` prefixes (labels carry that).

**Body template:** Use the template from `quality/issue-template.md`. Add an
`## Implementation Notes` section with key files, patterns, and wireframe paths.

**For each issue, invoke `/file-issue`** with the title, body, type, and priority.
`/file-issue` handles: issue creation, label assignment, project board placement,
and auto-dispatch prompt for bugs.

- For `bug` issues, `/file-issue` will prompt Odin to dispatch immediately — **decline
  the dispatch during planning** (issues should be dispatched via `/fire-next-up` after
  all issues are filed and dependencies are set).
- For all other types, `/file-issue` files and boards without prompting.

**After creating all issues:** If any issue references `Blocked by #N`, edit the earlier issue to add a note:

```bash
# Optional: add "Blocks #M" to the earlier issue for bidirectional tracking
gh issue comment <N> --body "Blocks #M — <one-line summary of dependent issue>"
```

### Step 5b — Create Epic Tracker Issue

After all work issues are filed, create a **tracker issue** that serves as the epic's
umbrella. This issue tracks the dependency graph, links all child issues, and
auto-closes when every child issue is closed (via a GitHub Actions workflow).

**Title format:** `[Epic] <epic title>`

**Body template:**

```markdown
## Epic: <title>

<one-sentence description>

### Dependency Graph

| Wave | Issue | Title | Depends On |
|------|-------|-------|------------|
| 0 | #A | ... | — |
| 0 | #B | ... | — |
| 1 | #C | ... | #A, #B |
| 2 | #D | ... | #C |

### Tracked Issues

<!-- GitHub renders these as a checklist that fills in as issues close -->
- [ ] #A
- [ ] #B
- [ ] #C
- [ ] #D

This issue will close automatically when all tracked issues above are closed.

---
Generated with [Claude Code](https://claude.com/claude-code)
```

**Labels:** `enhancement`, same priority as the highest-priority child issue.

**Create via `/file-issue`**, then add to board as `In Progress` (it stays open for
the duration of the epic):

```bash
SCRIPT_DIR="$(git rev-parse --show-toplevel)/.claude/skills/fire-next-up/scripts"
node "$SCRIPT_DIR/pack-status.mjs" --move <TRACKER_NUMBER> in-progress
```

The tracker issue number is the **epic number** used by `/epic-manager`.
The tracker issue body IS the dependency graph — no local YAML files needed.

### Step 5c — Link Sub-Issues (MANDATORY)

After creating the tracker issue, link every child issue as a **GitHub sub-issue**
of the tracker. This populates the "Sub-issues progress" column on the project board.

```bash
PARENT_ID=$(gh issue view <TRACKER_NUMBER> --repo declanshanaghy/fenrir-ledger --json id -q .id)
for N in <issue1> <issue2> <issue3> ...; do
  CHILD_ID=$(gh issue view $N --repo declanshanaghy/fenrir-ledger --json id -q .id)
  gh api graphql -f query="mutation { addSubIssue(input: { issueId: \"$PARENT_ID\", subIssueId: \"$CHILD_ID\" }) { subIssue { number } } }"
done
```

**This step is not optional.** Without it, the "Sub-issues progress" column on the
project board shows empty. The markdown checklist in the body is for visual tracking
only — GitHub's native sub-issues feature is what drives the progress column.

### Step 5d — Set Up Auto-Close Workflow

Check if `.github/workflows/close-epic-tracker.yml` already exists. If not, create it.
This workflow closes the tracker issue when all its linked child issues are closed.

```yaml
# .github/workflows/close-epic-tracker.yml
name: Close Epic Tracker
on:
  issues:
    types: [closed]

jobs:
  check-epic:
    runs-on: ubuntu-latest
    steps:
      - name: Check and close parent epic tracker
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            // Find open issues with [Epic] prefix that reference the closed issue
            const closedNumber = context.payload.issue.number;
            const { data: epics } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              labels: 'enhancement',
              per_page: 100,
            });

            for (const epic of epics) {
              if (!epic.title.startsWith('[Epic]')) continue;
              if (!epic.body) continue;

              // Extract all issue numbers from "- [ ] #N" and "- [x] #N" lines
              const checklistPattern = /^- \[[ x]\] #(\d+)/gm;
              const issueNumbers = [];
              let match;
              while ((match = checklistPattern.exec(epic.body)) !== null) {
                issueNumbers.push(parseInt(match[1], 10));
              }

              if (issueNumbers.length === 0) continue;
              if (!issueNumbers.includes(closedNumber)) continue;

              // Check if ALL referenced issues are now closed
              let allClosed = true;
              for (const num of issueNumbers) {
                const { data: issue } = await github.rest.issues.get({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: num,
                });
                if (issue.state !== 'closed') {
                  allClosed = false;
                  break;
                }
              }

              if (allClosed) {
                await github.rest.issues.update({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: epic.number,
                  state: 'closed',
                  state_reason: 'completed',
                });
                await github.rest.issues.createComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: epic.number,
                  body: `All tracked issues are closed. Epic complete! 🐺`,
                });
                console.log(`Closed epic tracker #${epic.number}`);
              }
            }
```

This workflow is **created once** and covers all future epics. If the file already
exists, skip this step entirely.

### Step 6 — Report

After all issues are created and the tracker is filed, report:

```
## Plan Filed

**Topic:** <brief description>
**Tracker issue:** #T — [Epic] <title>
**Issues created:** N (+ 1 tracker)

| # | Title | Type | Priority | Chain | Wave | Depends On |
|---|-------|------|----------|-------|------|------------|
| #N | ... | enhancement | normal | Decko -> Loki | 0 | — |
| #M | ... | ux | high | Luna -> Decko -> Loki | 1 | #N |

**Wireframes:** <path or "none">
**Auto-close:** When all tracked issues close, #T closes automatically.

To start execution:
- `/epic-manager <T>` — dashboard + next dispatch recommendation
- `/epic-manager <T> --dispatch` — dashboard + ready dispatch commands
- `/fire-next-up` — pick the top unblocked issue from the board
```

## Rules

1. **No issue cap** — create as many issues as the scope requires; each must be self-contained (one branch, one PR, one agent chain)
2. **Each issue must be self-contained** — one branch, one PR, one agent chain; split anything larger
3. **Labels are mandatory** — every issue gets one type label and one priority label
4. **Use `/file-issue`** — every issue is created via `/file-issue`, which handles labels, board placement, and auto-dispatch prompts
5. **Sequential creation** — create issues one at a time to capture numbers for dependencies
6. **No spec files** — the issues ARE the spec. Do not write to `specs/`
7. **No code** — planning only. Agents do the building via `/fire-next-up`
8. **Freya always interviews** — never skip the product owner interview
9. **Luna only for UI** — skip wireframes for pure backend/infra/test work
10. **Use the issue template** — all required sections must be present for agents to work from
11. **GitHub is the source of truth** — the tracker issue body IS the dependency graph. No local YAML files. `/epic-manager` reads the tracker issue directly from GitHub.
