---
name: plan-feature
description: Plan a new feature from concept to approved implementation plan. Activates Product Council for strategic evaluation, then Feature Council for technical planning. Produces a documented decision and scoped task breakdown. Use when starting any new feature work.
user-invokable: true
---

# Feature Planning Workflow

Take a feature idea from concept to an approved implementation plan with lean scope, council consensus, and a documented decision record. This skill **challenges assumptions, asks hard questions, and pushes back** at every stage — before councils review, after councils vote, and before final approval. The goal is to arrive at the strongest possible plan, not to rubber-stamp the first idea.

> [!CAUTION]
> **Scope boundary**: This skill produces a _plan_, a decision record, GitHub issue(s), and integrates them into the [Product Roadmap]({PROJECT_BOARD_URL}) project with correct phase assignments. It does **NOT** write application code, create components, modify database schemas, run tests, create branches for implementation, or perform any build work. If the user asks to start building after the plan is approved, direct them to run `/build-feature <issue-number>` — do not begin implementation yourself.

## Step 1: Gather Feature Context

Ask the user to describe:

- **What** the feature does (user-facing behavior)
- **Who** it is for (target users)
- **Why** it matters (business or product value)
- **Constraints** (time, technical, budget, dependencies)

If the user provides a GitHub issue number, fetch the issue details:

```bash
gh issue view <number> --json title,body,labels,state,number
```

**Track the source issue number** — if planning was initiated from a GitHub issue, store the issue number for later updates in Steps 3, 5, and 7.

### Already-Planned Check

If the issue has the `build-ready` label, it has already been through `/plan-feature` and was deemed sufficiently planned. Warn the user before proceeding:

> [!WARNING]
> Issue #\<number\> already has the `build-ready` label, which means `/plan-feature` has been run on it before. Re-running will create a new decision record and may create duplicate implementation issues.

Ask the user whether to:

- **(a)** Continue anyway (re-plan from scratch, e.g., if requirements changed significantly)
- **(b)** Stop and use the existing plan (run `/build-feature <number>` instead)

Do not proceed past Step 1 without the user's explicit choice.

### Small-Scope Triage

After gathering context, assess whether the issue actually needs the full council workflow. Not every issue warrants a Product Council, Feature Council, decision record, and implementation issue. If **all** of the following are true, the issue is likely too small:

- **XS or S estimated size** (1-2 days of work)
- **Touches 3 or fewer files** with no architectural decisions
- **No frontend changes** (or trivial frontend changes)
- **No database schema changes**
- **No new API endpoints** (modifications to existing startup/config code are fine)
- **Clear, unambiguous implementation** — there is essentially one right way to do it

If the issue meets these criteria, recommend the small-scope bypass to the user:

> [!TIP]
> This issue looks small enough to skip the full `/plan-feature` council workflow. The scope is clear, the implementation is straightforward, and running two councils plus a decision record would add more overhead than value.
>
> **Recommended action**: Add the `build-ready` label directly and run `/build-feature <number>` or `/build-api <number>` to implement.

Ask the user whether to:

- **(a)** Apply `build-ready` and stop (they'll run `/build-feature` or `/build-api` separately)
- **(b)** Continue with the full `/plan-feature` workflow anyway (e.g., if they want council input for precedent or policy reasons)

If the user chooses **(a)**:

1. Add the `build-ready` label to the issue
2. Add a brief implementation context comment documenting any decisions made during triage (e.g., which approach to use, accepted values, files to modify)
3. Stop — do not proceed to Step 2 or beyond

If the user provides a brief description, that's sufficient — but do NOT simply accept it at face value. Proceed to Step 2.

## Step 2: Critical Analysis & Challenge

Before sending the feature to council, **act as a skeptical advisor**. Your job is to stress-test the idea and help the user arrive at the strongest possible version of their feature.

### Challenge Assumptions

Identify and question the implicit assumptions in the feature request:

- **Problem validity**: Is this solving the right problem? Could the user's stated problem be a symptom of a deeper issue?
- **Solution fit**: Is this the best solution, or is the user anchored on the first idea that came to mind? Present 1-2 alternative approaches if viable.
- **Scope creep risk**: Is the user asking for more than they need? What's the smallest thing that would validate the core hypothesis?
- **Timing**: Is this the right thing to build now, given the current state of the project? Are there prerequisites or dependencies that should come first?

### Ask Clarifying Questions

Ask 2-4 pointed questions that expose gaps or weak spots in the proposal. Examples:

- "What happens if [edge case]? Have you considered...?"
- "You mentioned X — but how does that interact with the existing Y?"
- "What's the user's current workaround? How painful is it really?"
- "What would you cut if this had to ship in half the time?"

### Make Recommendations

Based on your analysis, present:

- **What's strong** about the proposal (validate what works)
- **What concerns you** (risks, blind spots, over-engineering)
- **What you'd change** (concrete suggestions, not vague warnings)
- **Alternative framing** (if the problem could be solved differently)

### CHECKPOINT: Present your critical analysis and questions to the user. Wait for their responses and any scope adjustments before proceeding to the Product Council. Do NOT rubber-stamp — if the answers don't satisfy your concerns, push back again.

## Step 3: Activate the Product Council

Read the Product Council template from `.claude/councils/product-council.md` and evaluate the feature from all 6 member perspectives.

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

### Product Strategist (Lead)

- **User Value**: Does this solve a real user problem? Market fit?
- **Priority**: Is this the right thing to build now?
- **Recommendations**: Strategic considerations, positioning

### Lean Delivery Lead

- **Lean Scope**: What is the smallest version we can ship to get feedback?
- **Speed to Feedback**: How quickly can we get this in front of users?
- **Feature Flag Strategy**: Should this be prototyped behind a feature flag?
- **Recommendations**: How to ship faster and learn faster

### Design Lead — consult: ui-design

- **Design Quality**: Brand consistency? UX intuitiveness?
- **Accessibility**: WCAG compliance requirements?
- **Recommendations**: Design approach, component needs

### Business Operations Lead

- **Cost Analysis**: Budget required? Infrastructure costs?
- **ROI Potential**: Expected return on investment?
- **Recommendations**: Cost optimizations or budget concerns

### Principal Engineer — consult: full-stack-orchestration

- **Technical Feasibility**: Can we build this? Complexity level?
- **Architectural Fit**: Does this align with the current tech stack?
- **Recommendations**: Technical constraints or alternative approaches

### Frontend Specialist — consult: frontend-mobile-development

- **Implementation Assessment**: UX feasibility? Component complexity?
- **User Experience**: Implementation challenges?
- **Recommendations**: Frontend implementation approach

Present the full Product Council evaluation with all votes and recommendations.

### Post-Council Synthesis

After the council votes, **do not simply pass their results through**. Add your own analysis:

- **Where do you agree with the council?** Reinforce the strongest points.
- **Where do you disagree?** If a council member's assessment seems off, say so and explain why.
- **What did the council miss?** Identify blind spots — topics no member raised that matter.
- **Groupthink check**: If all members agree, play devil's advocate. What's the strongest argument against this feature?
- **Refined recommendation**: Based on both the council input and your own critical analysis from Step 2, give your honest recommendation — build as proposed, modify scope, defer, or reconsider entirely.

### CHECKPOINT: Present the Product Council results AND your synthesis to the user. If you have concerns the council didn't surface, raise them now. Wait for approval of scope and priority before proceeding to technical planning.

## Step 4: Define Lean Scope

Based on Product Council feedback, clearly define:

- **MVP Scope**: What ships in the first increment (1-2 weeks max). List specific user-facing capabilities.
- **Future Iterations**: What comes after MVP validation. List deferred capabilities.
- **Feature Flag Strategy**: Whether this should ship behind a flag, and the flag name.
- **Success Metrics**: How will we know this feature works? Define 2-3 measurable outcomes.

## Step 5: Activate the Feature Council

Read the Feature Council template from `.claude/councils/feature-council.md` and create the technical implementation plan.

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

### Principal Engineer (Lead) — consult: full-stack-orchestration

- **Architecture Fit**: Does this align with system design?
- **Complexity Assessment**: Is this appropriately scoped?
- **Recommendations**: Architectural considerations, patterns to follow

### Frontend Specialist — consult: frontend-mobile-development

- **UI/UX Approach**: Component structure, user interaction flow
- **Design Integration**: Tailwind/shadcn components needed? New or existing?
- **Recommendations**: Frontend implementation strategy

### Backend Specialist — consult: backend-development

- **API Design**: Endpoints, contracts, data flow
- **Database Changes**: Schema modifications needed?
- **Recommendations**: Backend implementation strategy

If the feature involves API work, invoke `/backend-development:api-design-principles` for detailed API design guidance.

### QA Lead

- **Testing Strategy**: Unit, integration, E2E approach
- **Edge Cases**: Scenarios to test, boundary conditions
- **Recommendations**: Quality gates and acceptance criteria

### Implementation Plan

Based on council input, produce a structured task breakdown:

**Frontend Tasks**: Component development, routing, state management, styling
**Backend Tasks**: API endpoints, services, business logic, validation
**Database Tasks**: Schema changes, migrations, seed data
**Testing Tasks**: Test creation, coverage goals, E2E scenarios
**Estimated Complexity**: Small / Medium / Large

**Size and Schedule Estimates**: For each task/issue that will be created, the council must provide:

- **Size**: XS (1 day), S (2 days), M (3 days), L (5 days), or XL (8 days) in business days
- **Dependencies**: Which other issues must complete before this one can start
- **Milestone**: Which phase (M1-M5) the issue belongs to
- **Schedule position**: Where in the milestone's serial queue this issue falls, considering dependencies and existing scheduled items

### Post-Council Synthesis

After the Feature Council votes, add your own technical analysis:

- **Implementation risks**: What's the hardest part of this plan? Where are teams most likely to get stuck or underestimate effort?
- **Sequencing concerns**: Is the task breakdown in the right order? Are there hidden dependencies between frontend and backend work?
- **Over-engineering check**: Is the council proposing more infrastructure than this feature needs? Could we do less and still validate the hypothesis?
- **Under-engineering check**: Is anything missing that will bite us later — error handling, migration rollback, accessibility, performance?
- **Honest assessment**: Given everything discussed, rate your confidence that this plan will succeed as written (High / Medium / Low) and explain why.

### CHECKPOINT: Present the Feature Council implementation plan AND your technical synthesis to the user. Flag any concerns about sequencing, risk, or scope. Wait for approval of the task breakdown before proceeding.

## Step 6: Generate Decision Record

Determine the next decision number by reading existing files in `docs/decisions/`.

Using the template from `docs/decisions/001-example-architecture-decision.md`, create a decision record that includes:

- **Date**: Today's date
- **Council**: Product Council + Feature Council
- **Status**: Approved (after user approval)
- **Question**: The feature being evaluated
- **Context**: Current situation, requirements, constraints
- **Council Votes**: All votes from both Product and Feature councils
- **Decision**: Approved scope (MVP + future)
- **Rationale Summary**: Synthesized perspectives from all council members
- **Action Items**: Task breakdown with clear owners (frontend, backend, testing)
- **Timeline**: Target dates based on complexity
- **Follow-up**: When to revisit, what to validate post-launch
- **References**: Related issues, documentation, prior decisions

### GFM Formatting Requirements

Decision records render in GitHub Flavored Markdown. Follow the GFM rules in `.claude/CLAUDE.md`:

- **Metadata blocks** must use bullet points (`- **Key**: value`), never consecutive bold lines.
- **Use GitHub alerts** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) for callouts instead of bold/italic emphasis.
- **Include a mermaid diagram** when the decision involves multiple components, services, or data flows. Place it in the Context or Rationale Summary section to visualize the architecture.
- **Use collapsible `<details>` sections** for lengthy council evaluations if the record would otherwise exceed ~150 lines of votes.
- **Use tables** for structured comparisons (e.g., options considered with trade-offs).

Invoke `/documentation-generation:architecture-decision-records` for ADR formatting guidance if the decision involves architectural choices.

### CHECKPOINT: Present the decision record to the user for final review before saving.

## Step 7: Create Branch and Save Artifacts

1. Create a feature branch from the latest `origin/main` following CONTRIBUTING.md conventions:

   ```bash
   git fetch origin main
   git checkout -b feature/<feature-slug> origin/main
   ```

2. Save the decision record:

   ```
   docs/decisions/NNN-<feature-slug>.md
   ```

3. Update the decisions index:

   Regenerate the **Decisions** table in `docs/decisions/INDEX.md` by scanning all decision files in the directory. For each file (excluding `INDEX.md` and `001-example-architecture-decision.md`):
   - Read the heading to extract the decision number and title
   - Read the metadata block to extract Date, Council, Status
   - Derive 2-5 Key Topics (lowercase, comma-separated) from the decision's Question and Context sections

   Rebuild the full table in reverse chronological order (newest first). Do not modify any other section of INDEX.md (the intro, How to Use, or Related Resources sections remain static).

4. Update the master documentation index:

   If any new documents were created in `docs/` (including the decision record), verify that `docs/INDEX.md` reflects them. Decision records are covered by the `decisions/INDEX.md` entry already present, so no per-decision update is needed. However, if a new documentation file was added to `docs/` outside of `decisions/` (e.g., a new science document), add a row to the appropriate table in `docs/INDEX.md`.

5. Commit with:

   ```
   docs(council): document feature plan for <feature-name>
   ```

6. Run Prettier on all new/modified files before pushing:

   ```bash
   pnpm exec prettier --write <files>
   ```

   Stage and commit any formatting fixes separately:

   ```
   style: fix Prettier formatting in decision record and skill
   ```

7. Push the branch and create a PR for the decision record:

   ```bash
   git push -u origin feature/<feature-slug>

   gh pr create \
     --title "docs(council): add Decision NNN — <feature-name>" \
     --body "## Summary\n\n- Adds Decision NNN documenting the council-approved plan for <feature-name>\n- Product Council (<tally>) and Feature Council (<tally>) both approved\n- Implementation issues: #N, #N, ...\n\n## Test plan\n\n- [ ] Decision record renders correctly in GitHub markdown\n- [ ] Mermaid diagrams render (if any)\n- [ ] All cross-references to existing issues and docs are valid links\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
   ```

8. Watch CI until all checks pass:

   ```bash
   gh pr checks <pr-number> --watch
   ```

   If checks fail, read the failure logs, fix the issue, commit, push, and re-watch. Do not proceed to issue creation until CI is green.

   > [!IMPORTANT]
   > Every `/plan-feature` run that produces a decision record must submit a PR to get the record merged to main. The PR must pass CI before the planning step is considered complete. The decision record branch is also the feature branch that `/build-feature` will use for implementation.

### Update Source GitHub Issue

If planning was initiated from a GitHub issue (tracked in Step 1), update the source issue with the council findings. This keeps the issue as a living document that reflects the planning outcome.

Add a comment to the source issue summarizing the council results:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Council Planning Complete

### Product Council — <Vote tally> (Approve-Concern-Block)
<2-3 sentence summary of key Product Council decisions>

### Feature Council — <Vote tally> (Approve-Concern-Block)
<2-3 sentence summary of key technical decisions>

### Key Decisions
- <Decision 1>
- <Decision 2>
- <Decision 3>

### Artifacts
- **Decision Record**: [Decision NNN](docs/decisions/NNN-slug.md) _(link becomes active after the planning PR merges to main)_
- **Feature Branch**: `feature/<slug>`
- **Implementation Issue**: #<new-issue-number> (created in Step 9)

Planning completed via `/plan-feature`.
EOF
)"
```

Add the `build-ready` label to the source issue (it has now been fully planned):

```bash
gh label list | grep -q "build-ready" || gh label create "build-ready" --description "Planned by /plan-feature and ready for /build-feature" --color "0E8A16"
gh issue edit <number> --add-label "build-ready"
```

### Ensure Source Issue is on Project Board

After labeling the source issue, verify it is tracked on the [Product Roadmap]({PROJECT_BOARD_URL}) project board. An issue with `build-ready` that is not on the board becomes an orphaned work item that `/build-feature` auto-pick cannot discover.

```bash
# Check if the issue is already on the project board
# --limit 200 covers the current board size; increase if the project grows beyond 200 items
EXISTING=$(gh project item-list {PROJECT_NUMBER} --owner {OWNER} --format json --limit 200 \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('items', []):
    # <number> must be an integer literal, e.g., == 42, not == '42'
    if item.get('content', {}).get('number') == <number>:
        print(item['id'])
        break
")

# If not on the board, add it and set fields
if [ -z "$EXISTING" ]; then
  ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "https://github.com/{OWNER}/{REPO}/issues/<number>" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
  # Set phase and milestone fields to match the implementation issues that will be created in the Issue Creation step
  gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {PHASE_FIELD_ID} --single-select-option-id <phase-option-id>
  echo "Added issue #<number> to the project board and set phase."
fi
```

> [!NOTE]
> The source issue retains its original content as context. The comment provides a clear audit trail of what the councils decided and links to the detailed decision record. After the implementation issue is created in the Issue Creation step (Step 9), come back and edit this comment to include the implementation issue number.

## Step 8: Pre-Issue Validation

Before creating GitHub issue(s), validate the planning artifacts:

1. **Decision record completeness**: Verify the decision record file exists and contains all required sections (Question, Context, Council Votes, Decision, Rationale Summary, Action Items, Timeline). If any section is missing, stop and add it before proceeding.

2. **Council consensus**: Scan both council vote sections for any "Block" votes. If a Block vote exists:

   > [!WARNING]
   > A council member voted to Block this feature. Creating an implementation issue with unresolved Block votes is unusual. Consider addressing the concern before proceeding.

   Ask the user whether to proceed or resolve the concern first.

3. **Task breakdown present**: Verify the Action Items section contains at least one task (checkbox line). If empty, stop and ask the user to define the implementation tasks.

4. **Approval status**: Verify the Decision section shows `Status: Approved`. If not approved, warn the user before proceeding.

5. **Duplicate issue detection**: Search existing open issues for potential duplicates or substantially overlapping work:

   ```bash
   gh issue list --state open --limit 200 --json number,title,labels
   ```

   Compare the planned issue title(s) and scope against existing issues. If a potential duplicate is found:

   > [!WARNING]
   > Potential duplicate detected: issue #N has a similar title/scope. Review the existing issue before creating a new one.

   Present the potential duplicate(s) to the user and ask whether to:
   - **(a)** Update the existing issue instead (add the planning context as a comment)
   - **(b)** Create a new issue anyway (if scope is genuinely different — explain why)
   - **(c)** Adjust the plan to avoid overlap

   Do NOT create issues that substantially duplicate existing work items.

## Step 9: Create GitHub Issue(s)

> [!IMPORTANT]
> GitHub issues are **actionable work items** derived from the decision record — they do NOT replace it. The decision record (Step 6) remains the authoritative project-level record of council evaluations, rationale, and architectural context. Issues reference the decision record and provide a task-oriented view for `/build-feature` to consume.

Create GitHub issue(s) containing the full implementation plan so that `/build-feature` can be run from an issue at any time — immediately or days later.

### Ensure Label Exists

```bash
gh label list | grep -q "feature-implementation" || gh label create "feature-implementation" --description "Implementation plan from /plan-feature" --color "1D76DB"
gh label list | grep -q "security-audit" || gh label create "security-audit" --description "Phase security audit checkpoint" --color "D93F0B"
```

### Assemble Issue Body

Build the issue body following the template at `.github/ISSUE_TEMPLATE/feature-implementation.yml`. Include these sections:

**Problem Statement**: From the decision record's Question and Context sections. Explain what is being solved and why.

**Council Decisions**: Summarize both councils:

- Product Council vote tally and key decisions
- Feature Council vote tally and architecture decisions
- Any dissenting opinions or conditions

Use a collapsible `<details>` section for full council votes if they exceed ~30 lines.

**Implementation Plan**: The Action Items from the decision record, organized by layer (Frontend, Backend, Database, Testing) with checkboxes. This is the primary content that `/build-feature` will consume.

**Success Metrics**: The measurable outcomes from the lean scope definition (Step 4).

**Technical Context**: Key technical decisions — architecture patterns, API contracts, schema changes, component structure.

**Decision Record Reference**: Link to the decision record file: `[Decision NNN](docs/decisions/NNN-slug.md)`

**Feature Branch**: The branch name created in Step 7.

**Feature Flag**: Flag name and strategy, if applicable.

**Estimated Complexity**: Small / Medium / Large from the Feature Council assessment.

### Multi-Issue Option

If the implementation plan has multiple distinct phases, ask the user:

> The implementation plan has N phases. Would you like:
>
> 1. A single issue with all phases as task groups
> 2. Separate issues per phase (cross-referenced)

If separate issues, create them in sequence with "Part X of N" and links to sibling issues. Each issue must be assigned to the correct project phase (see Phase & Project Mapping below).

When creating multiple phase issues, also **create a parent issue** and set up sub-issue relationships per the "Parent Issues and Sub-Issues" section in `AGENTS.md`:

1. Create the parent issue first (high-level feature description, no implementation details)
2. Create child issues for each phase
3. Link children to parent via the sub-issues API:
   ```bash
   CHILD_ID=$(gh api repos/{OWNER}/{REPO}/issues/<child-number> --jq '.id')
   gh api repos/{OWNER}/{REPO}/issues/<parent-number>/sub_issues -X POST -F sub_issue_id=$CHILD_ID
   ```
4. Set the parent issue's dates to span all children (earliest Start to latest Target)
5. **If children span multiple milestones**: Remove the parent from any milestone (`gh api repos/{OWNER}/{REPO}/issues/<number> -X PATCH -F milestone=null`) and clear its project phase field via GraphQL (`clearProjectV2ItemFieldValue`). The parent is a tracking container; children carry milestone and phase assignments. If a source issue was used as the parent and already had a milestone, remove it.

### Phase & Project Mapping

Before presenting issues for confirmation, determine the correct project phase and size for each issue:

1. **Review existing phases** on the [{PROJECT_BOARD_NAME}]({PROJECT_BOARD_URL}): <!-- TODO: Replace {PROJECT_BOARD_NAME} with your project board's display name -->

   ```bash
   gh project field-list 6 --owner {OWNER} --format json
   ```

2. **Map each issue to a phase** based on the milestone breakdown in `docs/PRODUCT.md` and the nature of the work. Consider where the issue fits in the existing roadmap progression.

3. **Recommend new phases** if the planned work doesn't fit any existing phase. New phase recommendations must include a rationale and where they sit relative to existing phases (e.g., "between M2 and M3").

### CHECKPOINT: Present the full issue plan for user confirmation.

Present a table summarizing **all** issues that will be created or modified, their project phase assignments, and any project changes:

**Issues to create/update:**

| Action | Issue | Title     | Phase     | Size            | Milestone | Start        | Target       |
| ------ | ----- | --------- | --------- | --------------- | --------- | ------------ | ------------ |
| Create | NEW   | `<title>` | `<phase>` | `<XS/S/M/L/XL>` | `<M1-M5>` | `YYYY-MM-DD` | `YYYY-MM-DD` |
| Update | #N    | `<title>` | `<phase>` | `<size>`        | `<M1-M5>` | `YYYY-MM-DD` | `YYYY-MM-DD` |

If new phases are recommended:

| New Phase      | Position     | Rationale                |
| -------------- | ------------ | ------------------------ |
| `M_N_: <Name>` | After `M_N_` | Why this phase is needed |

If GTM review issues or security audit issues need to be created or updated for affected phases (see GTM Review Gate and Security Audit Gate below), include them in the summary.

**Wait for explicit user approval before creating any issues or modifying the project.**

### Issue Creation & Project Assignment

Ensure required labels exist:

```bash
gh label list | grep -q "feature-implementation" || gh label create "feature-implementation" --description "Implementation plan from /plan-feature" --color "1D76DB"
gh label list | grep -q "build-ready" || gh label create "build-ready" --description "Planned by /plan-feature and ready for /build-feature" --color "0E8A16"
gh label list | grep -q "gtm-review" || gh label create "gtm-review" --description "Go to Market & Business Review checkpoint" --color "0E8A16"
gh label list | grep -q "security-audit" || gh label create "security-audit" --description "Phase security audit checkpoint" --color "D93F0B"
```

### Selective `build-ready` Labeling

For each issue being created, decide whether it is **sufficiently planned** to go straight to `/build-feature`:

- **Add `build-ready`** if the issue has a concrete task breakdown, clear acceptance criteria, and no significant open questions. This is the common case for single-issue plans and for well-scoped child issues in multi-issue plans.
- **Do NOT add `build-ready`** if the issue is broad, has open architectural questions, or would benefit from its own `/plan-feature` pass to refine scope and get council input. This is common for large child issues in multi-issue plans where only the high-level direction was established.

For each approved issue, create it and assign it to the project with the correct phase, size, milestone, and dates:

```bash
# Create the issue (add --label "build-ready" if the issue is fully planned)
ISSUE_URL=$(gh issue create \
  --title "<title>" \
  --body "<body>" \
  --label "enhancement" \
  --label "feature-implementation" \
  --milestone "<milestone-name>" | tail -1)

# Extract issue number from URL
ISSUE_NUM=$(echo "$ISSUE_URL" | grep -o '[0-9]*$')

# Add to project and set phase + size fields
ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "$ISSUE_URL" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {PHASE_FIELD_ID} --single-select-option-id <phase-option-id>
gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {SIZE_FIELD_ID} --single-select-option-id <size-option-id>

# Set Start and Target dates (computed from size estimate and schedule position)
gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {START_FIELD_ID} --date <start-date>
gh project item-edit --project-id {PROJECT_ID} --id "$ITEM_ID" --field-id {TARGET_FIELD_ID} --date <target-date>
```

> [!NOTE]
> **Project field IDs** — Refresh from `gh project field-list 6 --owner {OWNER} --format json` if the project structure changes.
>
> - **Phase field**: `{PHASE_FIELD_ID}` — Options: M0 (`5d1aaeb2`), M1 (`4cfa6c51`), M2 (`27c0efa8`), M3 (`ed327f33`), M4 (`df98aad8`), M5 (`0604582f`)
> - **Size field**: `{SIZE_FIELD_ID}` — Options: XS (`88044618`), S (`27e6800e`), M (`c4753411`), L (`cde643b6`), XL (`286a9b9c`)
> - **Milestone numbers**: M0=1, M1=2, M2=3, M3=4, M4=5, M5=6
> - **Start field**: `{START_FIELD_ID}`
> - **Target field**: `{TARGET_FIELD_ID}`

### Schedule Date Computation

When creating issues, compute Start and Target dates following the scheduling rules in `AGENTS.md`:

1. **Check the existing schedule** in the target milestone:

   ```bash
   gh project item-list {PROJECT_NUMBER} --owner {OWNER} --format json --limit 200
   ```

   Find the latest Target date of any **non-gate** item in the milestone. Gate items are issues labeled `gtm-review` or `security-audit` — exclude them when determining the insertion point.

2. **Compute the new issue's dates** using the size-to-days table (XS=1, S=2, M=3, L=5, XL=8 business days). The Start date is the next business day after the latest non-gate item's Target (or after the dependency's Target, whichever is later). Skip weekends.

3. **Cascade all subsequent items.** After inserting the new issue, recompute the Start and Target dates of **every issue that follows it** in the milestone. Each subsequent issue's Start = next business day after the previous issue's Target. There must be no gaps or overlaps between consecutive issues — Start and Target dates determine the order of operations.

4. **Shift gate items forward.** Every milestone must end with exactly two gate items in this fixed order: GTM review (second-to-last), then security audit (last). After all non-gate items are positioned, recompute the gate items' dates so the GTM review starts the next business day after the last non-gate item's Target, and the security audit starts the next business day after the GTM review's Target. Update both gate items' Start and Target dates on the project board.

5. **Update the milestone due date** if the security audit's new Target extends it:

   ```bash
   gh api repos/{OWNER}/{REPO}/milestones/<number> -X PATCH -f due_on="<new-target>T00:00:00Z"
   ```

   > [!IMPORTANT]
   > No issue of any kind (feature, bug fix, chore, test, etc.) may ever be scheduled after the GTM review and security audit gate items. These two items are always the final items in every milestone, and their order (GTM → security audit) is an invariant that must be preserved on every project update.

6. **Update all affected items on the project board** using the Start and Target field IDs. Only recompute the **current milestone being developed**. Later milestones will be adjusted when the current milestone ends.

If multiple issues were requested, create each in sequence and capture the issue numbers for cross-referencing.

Report the created issue number(s), URL(s), project phase assignment(s), milestone(s), and scheduled dates.

### GTM Review Gate

Every project phase must end with a comprehensive **Go to Market & Business Review** issue. After creating or assigning feature issues, verify GTM coverage for every affected phase:

1. **Check for existing GTM review issues** in affected phases:

   ```bash
   gh issue list --state open --label "gtm-review" --json number,title
   ```

2. **For phases missing a GTM review issue**, create one:

   ```bash
   gh issue create \
     --title "gtm: Go to Market & Business Review — <Phase Name>" \
     --body "<body>" \
     --label "enhancement" \
     --label "marketing" \
     --label "gtm-review"
   ```

   The GTM review issue body must include:
   - **Phase Summary**: Features and changes included in this phase
   - **Marketing Page Audit**: Checklist to verify landing pages, feature descriptions, screenshots, and CTAs reflect the phase's changes
   - **Content Consistency**: Blog posts, help docs, and in-app copy alignment with new capabilities
   - **GTM Recommendations**: Positioning, messaging, launch tactics, and channel strategy
   - **Business Review**: Revenue impact, pricing implications, competitive positioning updates
   - **Success Metrics**: How to measure GTM effectiveness for this phase

   > [!IMPORTANT]
   > All user-facing copy produced during GTM work (landing pages, blog posts, in-app text, marketing content) must follow the **User-Facing Content Style** rules in `AGENTS.md`. No em dashes, no AI-slop vocabulary, no promotional inflation.

   Add the GTM review issue to the project with the correct phase, size, milestone, and **dates**:

   ```bash
   GTM_URL=<created-issue-url>
   GTM_NUM=$(echo "$GTM_URL" | grep -o '[0-9]*$')

   # Add to project and set fields
   GTM_ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "$GTM_URL" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
   gh project item-edit --project-id {PROJECT_ID} --id "$GTM_ITEM_ID" --field-id {PHASE_FIELD_ID} --single-select-option-id <phase-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$GTM_ITEM_ID" --field-id {SIZE_FIELD_ID} --single-select-option-id <size-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$GTM_ITEM_ID" --field-id {START_FIELD_ID} --date <start-date>
   gh project item-edit --project-id {PROJECT_ID} --id "$GTM_ITEM_ID" --field-id {TARGET_FIELD_ID} --date <target-date>
   ```

   The GTM issue is **S** (2 business days). Its Start date is the next business day after the last feature issue's Target in the phase. Compute dates using the same schedule logic as feature issues (see Schedule Date Computation above).

3. **For phases that already have a GTM review issue**, check whether the newly planned work is covered. If the phase scope has expanded significantly, add a comment to the existing GTM issue noting the new items that need review.

> [!IMPORTANT]
> GTM review issues ensure that every shippable phase includes a business review checkpoint. They are not optional — every phase must have one before the phase is considered complete. **Exemption**: Phases that are purely bug fixes or continuous delivery/maintenance (e.g., dependency upgrades, security patches, CI improvements) are exempt.

### Security Audit Gate

Every project phase must end with a comprehensive **Security Audit** issue as its final work item — after the GTM review. This ensures that any code changes introduced during the GTM review are also covered by the audit. After verifying GTM coverage, verify security audit coverage for every affected phase:

1. **Check for existing security audit issues** in affected phases:

   ```bash
   gh issue list --state open --label "security-audit" --json number,title
   ```

2. **For phases missing a security audit issue**, create one:

   ```bash
   gh issue create \
     --title "security: Comprehensive Security Audit — <Phase Name>" \
     --body "<body>" \
     --label "enhancement" \
     --label "security-audit"
   ```

   The security audit issue body must include:
   - **Phase Summary**: Features, services, and changes included in this phase that require security review
   - **Audit Scope**: Which areas of the codebase are affected (API endpoints, authentication flows, data models, third-party integrations, etc.)
   - **SAST Scanning**: Run automated static analysis on all code changes in the phase
   - **STRIDE Threat Modeling**: Apply STRIDE methodology to new or modified features
   - **Attack Tree Analysis**: Build attack trees for the top 3 risks identified in threat modeling
   - **Dependency Audit**: Review new or updated dependencies for known vulnerabilities
   - **Remediation Plan**: Prioritized list of findings with severity ratings and fix recommendations

   Add the security audit issue to the project with the correct phase, size, milestone, and **dates**:

   ```bash
   SEC_URL=<created-issue-url>
   SEC_NUM=$(echo "$SEC_URL" | grep -o '[0-9]*$')

   # Add to project and set fields
   SEC_ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "$SEC_URL" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
   gh project item-edit --project-id {PROJECT_ID} --id "$SEC_ITEM_ID" --field-id {PHASE_FIELD_ID} --single-select-option-id <phase-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$SEC_ITEM_ID" --field-id {SIZE_FIELD_ID} --single-select-option-id <size-option-id>
   gh project item-edit --project-id {PROJECT_ID} --id "$SEC_ITEM_ID" --field-id {START_FIELD_ID} --date <start-date>
   gh project item-edit --project-id {PROJECT_ID} --id "$SEC_ITEM_ID" --field-id {TARGET_FIELD_ID} --date <target-date>
   ```

   The security audit issue is **M** (3 business days). Its Start date is the next business day after the GTM issue's Target in the same phase. The security audit is always the **last** issue in a phase. Compute dates using the same schedule logic as feature issues (see Schedule Date Computation above).

3. **For phases that already have a security audit issue**, check whether the newly planned work is covered. If the phase scope has expanded significantly, add a comment to the existing security audit issue noting the new items that need review.

> [!IMPORTANT]
> Security audit issues ensure that every shippable phase includes a security checkpoint before release. They are not optional — every phase must have one before the phase is considered complete. The security audit is always the **last** issue in a phase, running after the GTM review. Run it using `/security-audit`. **Exemption**: Phases that are purely bug fixes or continuous delivery/maintenance (e.g., dependency upgrades, security patches, CI improvements) are exempt — same as the GTM review exemption.

## Step 10: Output Summary

Present a clear summary:

- **Approved Scope**: MVP capabilities and deferred items
- **Task Breakdown**: Frontend, backend, database, and testing tasks
- **Feature Flag**: Name and strategy (if applicable)
- **Success Metrics**: How we'll measure outcomes
- **Branch**: Feature branch name ready for implementation
- **Decision Record**: File path for reference
- **GitHub Issue(s)**: Issue number(s) and URL(s) for the implementation plan
- **Project Phase(s)**: Which phase(s) on the [Product Roadmap]({PROJECT_BOARD_URL}) each issue is assigned to
- **GTM Coverage**: GTM review issue(s) for affected phase(s) — created, updated, or verified
- **Security Audit Coverage**: Security audit issue(s) for affected phase(s) — created, updated, or verified

**Next step**: Run `/build-feature <issue-number>` for full-stack implementation, or `/build-api` for backend-only work.
