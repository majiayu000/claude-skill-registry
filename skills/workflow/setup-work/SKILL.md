---
name: setup-work
description: Setup development environment from GitHub issue. Invoke when user says "init work on issue #X", "initialize issue #X", "setup issue #X", "prepare issue #X", "start fresh on issue #X", "start new work on issue #X", or provides a GitHub issue URL.
tools:
  - mcp__serena__*
  - mcp__github__*
  - mcp__linear__*
  - Bash:git *
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - LSP
---

# Issue Setup Skill

## Purpose
Transform a GitHub issue into a fully-prepared development environment with:
- Complete issue context and acceptance criteria
- Structured implementation plan (scratchpad)
- Feature branch ready for work
- Situational codebase awareness

## Context Prerequisites

Before beginning, load critical project context:

### Project Structure
Read the project's CLAUDE.md to understand:
- Module architecture
- Development philosophy
- Current sprint priorities
- Branch naming conventions

### Codebase Orientation
Get a high-level view of the repository structure to identify affected areas.

## Workflow Execution

### Phase 0: Check Existing Context (Self-Correction)

**Before proceeding with setup, check if work already initialized:**

1. **Detect existing scratchpad:**
   ```bash
   # Look for SCRATCHPAD_{issue_number}.md
   ls SCRATCHPAD_*.md 2>/dev/null
   ```

2. **If scratchpad exists:**
   ```
   ✓ Scratchpad already exists for this issue.

   Delegating to do-work skill...
   ```

   Then invoke:
   ```
   Skill: do-work
   args: "{issue_number}"
   ```

   **STOP here** - don't proceed with setup.

3. **If no scratchpad:**
   - Proceed to Phase 1 (normal setup flow)

### Phase 1: Gather Context (Parallel)

**Input:** Issue reference in format `owner/repo#number` or just `#number` (uses current repo)

**Examples:**
- `owner/repository#42`
- `#42` (assumes current repository)

**Execute these operations in parallel** for faster setup:

1. **Repository Context:**
   - Determine owner/repo from input or git remote
   - Read project's `CLAUDE.md` for conventions
   - Check current git status and branch

2. **Issue Details:**
   - Retrieve complete issue using GitHub tools:
     - Title, body (description), labels
     - State (open/closed), assignees
     - Milestone, project associations
     - All comments (especially implementation details)
     - Linked issues (mentions, closes, related)

3. **Generate branch name** (after issue fetched):
   - Format: `{issue-number}-{slugified-title}`
   - Example: `42-implement-fact-batching`
   - Sanitize title: lowercase, spaces→hyphens, remove special chars

4. **Build issue context map:**
   - Is this part of a milestone/project?
   - Are there dependent issues (blocks/blocked-by)?
   - What's the priority based on labels?
   - Are there linked PRs already?

### Phase 2: Analyze & Plan

**Goal:** Understand the issue deeply before writing any code.

**Analysis Steps:**

1. **Requirements Review:**
   - Parse issue body for requirements/acceptance criteria
   - Check for task lists (- [ ] items) in issue body
   - Identify ambiguities or missing information
   - Note any conflicting requirements in comments

2. **Codebase Investigation (Delegate to Scratchpad-Planner Agent):**

   For thorough codebase analysis, use the **scratchpad-planner agent**:

   ```
   Skill: scratchpad-planner
   args: "issue #{number}: {issue title}

          Summary: {brief issue summary}

          Key requirements:
          {extract key requirements from issue body}

          Affected areas (if known):
          {mention specific modules/components if issue indicates}

          Repository: {owner/repo}
          Project context: See CLAUDE.md for module structure and conventions"
   ```

   The scratchpad-planner agent will:
   - Read project's CLAUDE.md for conventions and structure
   - Search for relevant existing code patterns using Grep and LSP
   - Identify affected modules/components and integration points
   - Find similar implementations to learn from
   - Generate atomic task breakdown following project conventions
   - Ask clarifying questions for ambiguous requirements
   - Support resumable analysis for complex codebases

   The agent replaces generic exploration with specialized planning expertise,
   providing more structured analysis and implementation approach generation.

3. **Technical Breakdown:**
   - Break work into atomic, committable tasks
   - Identify integration points
   - Flag potential challenges
   - Estimate complexity/scope

4. **Dependency Check:**
   - Does this require other issues first? (check "depends on" mentions)
   - Will this block other work? (check "blocks" mentions)
   - Are there API contract implications?
   - Check milestone dependencies

### Phase 3: Create Scratchpad

**Generate:** `SCRATCHPAD_{issue_number}.md`

**Template Structure:**

```markdown
# {Issue Title} - #{issue_number}

## Issue Details
- **Repository:** {owner/repo}
- **GitHub URL:** {issue_url}
- **State:** {open/closed}
- **Labels:** {labels}
- **Milestone:** {milestone if exists}
- **Assignees:** {assignees}
- **Related Issues:** {linked issues if any}
  - Depends on: #{issue_numbers}
  - Blocks: #{issue_numbers}
  - Related: #{issue_numbers}

## Description
{full issue body from GitHub}

## Acceptance Criteria
{extract task list from issue body, or create from description}
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}

## Branch Strategy
- **Base branch:** main (or develop-ts/develop if exists)
- **Feature branch:** {issue_number}-{slugified-title}
- **Current branch:** {git branch --show-current}

## Implementation Checklist

### Setup
- [ ] Fetch latest from base branch
- [ ] Create and checkout feature branch

### Implementation Tasks
{Break down into atomic commits - each should be independently reviewable}

- [ ] {First atomic task with clear scope}
  - Files affected: {list}
  - Why: {brief rationale}
  
- [ ] {Second atomic task}
  - Files affected: {list}
  - Why: {brief rationale}

{Continue with granular breakdown...}

### Quality Checks
- [ ] Run linter/type checker
- [ ] Execute relevant tests
- [ ] Self-review for code quality
- [ ] Verify acceptance criteria met

### Documentation
- [ ] Update relevant README/docs (if applicable)
- [ ] Add inline comments for complex logic (if applicable)

## Technical Notes

### Architecture Considerations
{Any architectural decisions to consider}
{Module boundaries to respect}
{Integration points to handle}

### Implementation Approach
{High-level strategy for solving the problem}
{Why this approach vs alternatives}

### Potential Challenges
{Known complexity areas}
{Technical debt to navigate}
{Performance considerations}

## Questions/Blockers

### Clarifications Needed
{List any unclear requirements}
{Ambiguities in issue description}

### Blocked By
{List any dependencies not yet complete - reference issue numbers}

### Assumptions Made
{Document assumptions if requirements unclear}

### Decisions Made
{Populated during Phase 3.5 Interactive Q&A}
{Format: Q: question → A: decision (rationale)}

## Work Log

{This section fills in during execution via /start-work}
{Each work session adds dated entries}

---
**Generated:** {timestamp}
**By:** Issue Setup Skill
**Source:** {github_issue_url}
```

**Scratchpad Quality Guidelines:**

- **Atomic tasks:** Each checklist item should be one commit
- **Clear scope:** Reader should understand what each task does
- **Testable:** Acceptance criteria should be verifiable
- **Realistic:** Don't over-engineer or under-scope
- **Contextual:** Reference project-specific conventions

### Phase 3.5: Interactive Q&A (Resolve Clarifications)

**Goal:** Resolve any questions or ambiguities before starting implementation.

**Trigger:** If the scratchpad has items in the "Clarifications Needed" section.

**Process:**

1. **Check for Outstanding Questions:**
   - Review the Questions/Blockers section of the scratchpad
   - If "Clarifications Needed" is empty, skip to Phase 4
   - If questions exist, proceed with interactive resolution

2. **Present Questions via AskUserQuestion:**
   For each clarification needed, use the `AskUserQuestion` tool to get user input:

   ```
   AskUserQuestion:
     question: "{The specific clarification question}"
     header: "Clarify"
     options:
       - label: "{Option A}"
         description: "{What this choice means}"
       - label: "{Option B}"
         description: "{What this choice means}"
       - label: "{Option C}" (if applicable)
         description: "{What this choice means}"
     multiSelect: false (or true if multiple answers valid)
   ```

   **Guidelines for presenting questions:**
   - Frame questions clearly with context
   - Provide 2-4 concrete options when possible
   - Include descriptions explaining implications of each choice
   - User can always select "Other" for custom input
   - Group related questions if they have dependencies

3. **Update Scratchpad with Decisions:**
   After collecting all answers, update the scratchpad:

   a) **Add "Decisions Made" section** (if not present) under Questions/Blockers:
   ```markdown
   ### Decisions Made
   {Timestamp}

   **Q: {Original question}**
   **A:** {User's answer/decision}
   **Rationale:** {Brief explanation of why, if provided}
   ```

   b) **Remove resolved items** from "Clarifications Needed"

   c) **Update relevant sections** if decisions affect:
      - Implementation tasks (add/remove/modify based on decisions)
      - Technical approach
      - Assumptions (convert to confirmed decisions)

4. **Confirm Resolution:**
   Display summary of decisions made:
   ```
   ✓ Resolved {N} clarifications:

   1. {Question summary} → {Decision}
   2. {Question summary} → {Decision}
   ...

   📋 SCRATCHPAD updated with decisions.
   ```

**Example Interaction:**

```
📋 SCRATCHPAD_42.md has 3 clarifications that need resolution before proceeding.

[AskUserQuestion 1/3]
Question: "Should we keep commands as aliases during the transition to skills?"
Header: "Migration"
Options:
  - "Keep as thin wrappers" - Commands remain but delegate to skills
  - "Remove immediately" - Clean break, skills only
  - "Decide per-command" - Evaluate each command individually

[User selects: "Keep as thin wrappers"]

[AskUserQuestion 2/3]
Question: "How should prime-session be handled?"
Header: "Behavior"
Options:
  - "Convert to auto-invoke skill" - Activates when entering new repo
  - "Keep as explicit command" - User must invoke manually
  - "Remove entirely" - Claude reads CLAUDE.md automatically anyway

[User selects: "Keep as explicit command"]

...

✓ Resolved 3 clarifications:

1. Migration strategy → Keep commands as thin wrappers
2. prime-session behavior → Keep as explicit command
3. ...

📋 SCRATCHPAD_42.md updated with decisions.
Proceeding to branch creation...
```

**Skip Conditions:**
- No items in "Clarifications Needed" → Skip directly to Phase 4
- User explicitly requests to skip → Note unresolved questions, proceed with assumptions

### Phase 4: Prepare Workspace

**Branch Creation:**

1. **Detect base branch:**
   ```bash
   # Check what branches exist
   git fetch origin
   
   # Prefer in this order:
   # 1. develop-ts (if exists)
   # 2. develop (if exists)
   # 3. main (default)
   git branch -r | grep -E 'origin/(develop-ts|develop|main)'
   ```

2. **Create feature branch:**
   ```bash
   # Generate branch name from issue
   # Format: {issue_number}-{slugified-title}
   # Example: 42-implement-fact-batching
   
   git branch {issue-number}-{slugified-title} origin/{base-branch}
   # Don't checkout yet - let operator decide when to switch
   ```

3. **Confirm creation:**
   ```bash
   git branch --list {branch-name}
   ```

**Final Output:**

Display concise summary:
```
✓ Issue #{issue_number} analyzed and prepared

📋 SCRATCHPAD_{issue_number}.md created with:
   - {X} implementation tasks
   - {Y} quality checks
   - {Z} decisions made (via Q&A)

🌿 Branch '{issue-number}-{slugified-title}' created from {base-branch}

🔗 GitHub Issue: {issue_url}

🚀 Ready to begin work:
   git checkout {branch-name}
   # Then start implementation
```

**Note:** If clarifications were resolved in Phase 3.5, the scratchpad now contains
confirmed decisions rather than open questions. All ambiguities should be resolved
before reaching this point.

## Project-Specific Adaptations

### For UI/Frontend Projects:

**Component Context:**
- Which components affected?
- State management implications?
- API contract dependencies?

### For API/Backend Projects:

**Contract Context:**
- API endpoints added/modified?
- Breaking changes?
- Database migrations needed?

## Error Handling

### Issue Not Found
If GitHub issue doesn't exist:
- Verify issue number and repository
- Check if issue is in different repo
- Offer to search issues by title/keyword
- Confirm you have access to private repos (if applicable)

### Insufficient Information
If issue lacks description or clear scope:
- Note this prominently in Questions/Blockers
- Suggest adding task list to issue before starting work
- Don't guess - make assumptions explicit
- Consider commenting on issue to request clarification

### Branch Already Exists
If feature branch already exists:
- Check if work in progress (git log)
- Offer to resume vs. create new branch
- Warn about potential conflicts
- Suggest reviewing existing commits

### Repository Access Issues
If can't access repository:
- Verify GitHub authentication (gh auth status)
- Check repository exists (might be private)
- Confirm repository name spelling
- Ensure gh CLI is installed and configured

## Integration with Other Skills

**Flows to:**
- `/start-work {issue_number}` - Begin execution from scratchpad
- `/commit` - Make atomic commits as checklist progresses

**Receives context from:**
- Project CLAUDE.md - Architecture and conventions
- `/prime-session` - Current development priorities

## Best Practices

### ✅ DO:
- Read acceptance criteria carefully
- Break work into truly atomic commits
- Flag ambiguities early
- Research codebase before planning
- Make scratchpad detailed but scannable
- Document assumptions explicitly

### ❌ DON'T:
- Start coding before scratchpad approved
- Guess at unclear requirements
- Create tasks too large to review
- Skip codebase investigation
- Over-engineer the plan
- Hide complexity in vague task descriptions

## Operator Interaction Points

**Before Scratchpad Creation:**
If issue is complex or ambiguous, ask:
- "This issue affects multiple modules. Should we break it into sub-issues?"
- "Acceptance criteria unclear on X. Should we clarify before planning?"

**After Scratchpad Created:**
Present for review:
- "I've created SCRATCHPAD_42.md. Please review the implementation plan."
- "I flagged 2 questions in the Blockers section - need clarification?"

**Before Branch Creation:**
Confirm readiness:
- "Base branch develop-ts is 5 commits behind origin. Pull first?"
- "Ready to create feature branch?"

## Success Criteria

A successful issue setup produces:

✓ **Complete context:** All issue details captured
✓ **Clear plan:** Implementation steps are atomic and logical
✓ **Identified risks:** Challenges flagged upfront
✓ **Ready workspace:** Branch created, scratchpad prepared
✓ **Operator confidence:** Developer knows exactly what to build

The scratchpad should be so clear that another developer could pick it up and execute it.

### Complex Implementation Detection

If the issue analysis reveals a complex implementation, suggest entering plan mode:

**Triggers for EnterPlanMode:**
- Implementation affects more than 3-4 files
- Multiple valid architectural approaches exist
- Significant refactoring required
- New patterns or abstractions needed
- Breaking changes to existing APIs

**Suggestion:**
```
This issue appears complex ({reason}). Would you like me to enter
plan mode to design the implementation approach before we proceed?
```

---

**Version:** 1.1.0
**Last Updated:** 2025-12-31
**Maintained By:** Escapement
**Changelog:**
- v1.1.0: Added Task delegation to Explore agent, parallel execution, LSP integration, EnterPlanMode triggers
