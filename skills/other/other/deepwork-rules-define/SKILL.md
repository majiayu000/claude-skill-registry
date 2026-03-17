---
name: deepwork_rules.define
description: "Creates a rule file that triggers when specified files change. Use when setting up documentation sync, code review requirements, or automated commands."
user-invocable: false
---

# deepwork_rules.define

**Standalone skill** - can be run anytime

> Creates file-change rules that enforce guidelines during AI sessions. Use when automating documentation sync or code review triggers.


## Instructions

**Goal**: Creates a rule file that triggers when specified files change. Use when setting up documentation sync, code review requirements, or automated commands.

# Define Rule

## Objective

Create a new rule file in the `.deepwork/rules/` directory to enforce team guidelines, documentation requirements, or other constraints when specific files change.

## Task

Guide the user through defining a new rule by asking structured questions. **Do not create the rule without first understanding what they want to enforce.**

**Important**: Use the AskUserQuestion tool to ask structured questions when gathering information from the user. This provides a better user experience with clear options and guided choices.

### Step 1: Understand the Rule Purpose

Start by asking structured questions to understand what the user wants to enforce:

1. **What guideline or constraint should this rule enforce?**
   - What situation triggers the need for action?
   - What files or directories, when changed, should trigger this rule?
   - Examples: "When config files change", "When API code changes", "When database schema changes"

2. **What action should be taken?**
   - What should the agent do when the rule triggers?
   - Update documentation? Perform a security review? Update tests?
   - Is there a specific file or process that needs attention?

3. **Are there any "safety" conditions?**
   - Are there files that, if also changed, mean the rule doesn't need to fire?
   - For example: If config changes AND install_guide.md changes, assume docs are already updated
   - This prevents redundant prompts when the user has already done the right thing

### Step 2: Choose the Detection Mode

Help the user select the appropriate detection mode:

**Trigger/Safety Mode** (most common):
- Fires when trigger patterns match AND no safety patterns match
- Use for: "When X changes, check Y" rules
- Example: When config changes, verify install docs

**Set Mode** (bidirectional correspondence):
- Fires when files that should change together don't all change
- Use for: Source/test pairing, model/migration sync
- Example: `src/foo.py` and `tests/foo_test.py` should change together

**Pair Mode** (directional correspondence):
- Fires when a trigger file changes but expected files don't
- Changes to expected files alone do NOT trigger
- Use for: API code requires documentation updates (but docs can update independently)

### Step 3: Define the Patterns

Help the user define glob patterns for files.

**Common patterns:**
- `src/**/*.py` - All Python files in src directory (recursive)
- `app/config/**/*` - All files in app/config directory
- `*.md` - All markdown files in root
- `src/api/**/*` - All files in the API directory
- `migrations/**/*.sql` - All SQL migrations

**Variable patterns (for set/pair modes):**
- `src/{path}.py` - Captures path variable (e.g., `foo/bar` from `src/foo/bar.py`)
- `tests/{path}_test.py` - Uses same path variable in corresponding file
- `{name}` matches single segment, `{path}` matches multiple segments

**Pattern syntax:**
- `*` - Matches any characters within a single path segment
- `**` - Matches any characters across multiple path segments (recursive)
- `?` - Matches a single character

### Step 4: Choose the Comparison Mode (Optional)

The `compare_to` field controls what baseline is used when detecting "changed files":

**Options:**
- `base` (default) - Compares to the base of the current branch (merge-base with main/master). Best for feature branches.
- `default_tip` - Compares to the current tip of the default branch. Useful for seeing difference from production.
- `prompt` - Compares to the state at the start of each prompt. For rules about very recent changes.

Most rules should use the default (`base`) and don't need to specify `compare_to`.

### Step 5: Write the Instructions

Create clear, actionable instructions for what the agent should do when the rule fires.

**Good instructions include:**
- What to check or review
- What files might need updating
- Specific actions to take
- Quality criteria for completion

**Template variables available in instructions:**
- `{trigger_files}` - Files that triggered the rule
- `{expected_files}` - Expected corresponding files (for set/pair modes)

### Step 6: Create the Rule File

Create a new file in `.deepwork/rules/` with a kebab-case filename:

**File Location**: `.deepwork/rules/{rule-name}.md`

**Format for Trigger/Safety Mode:**
```markdown
---
name: Friendly Name for the Rule
trigger: "glob/pattern/**/*"  # or array: ["pattern1", "pattern2"]
safety: "optional/pattern"    # optional, or array
compare_to: base              # optional: "base" (default), "default_tip", or "prompt"
---
Instructions for the agent when this rule fires.

Multi-line markdown content is supported.
```

**Format for Set Mode (bidirectional):**
```markdown
---
name: Source/Test Pairing
set:
  - src/{path}.py
  - tests/{path}_test.py
---
Source and test files should change together.

Modified: {trigger_files}
Expected: {expected_files}
```

**Format for Pair Mode (directional):**
```markdown
---
name: API Documentation
pair:
  trigger: api/{path}.py
  expects: docs/api/{path}.md
---
API code requires documentation updates.

Changed API: {trigger_files}
Update docs: {expected_files}
```

### Step 7: Verify the Rule

After creating the rule:

1. **Check the YAML frontmatter** - Ensure valid YAML formatting
2. **Test trigger patterns** - Verify patterns match intended files
3. **Review instructions** - Ensure they're clear and actionable
4. **Check for conflicts** - Ensure the rule doesn't conflict with existing ones

## Example Rules

### Update Documentation on Config Changes
`.deepwork/rules/config-docs.md`:
```markdown
---
name: Update Install Guide on Config Changes
trigger: app/config/**/*
safety: docs/install_guide.md
---
Configuration files have been modified. Please review docs/install_guide.md
and update it if any installation instructions need to change based on the
new configuration.
```

### Security Review for Auth Code
`.deepwork/rules/security-review.md`:
```markdown
---
name: Security Review for Authentication Changes
trigger:
  - src/auth/**/*
  - src/security/**/*
safety:
  - SECURITY.md
  - docs/security_audit.md
---
Authentication or security code has been changed. Please:

1. Review for hardcoded credentials or secrets
2. Check input validation on user inputs
3. Verify access control logic is correct
4. Update security documentation if needed
```

### Source/Test Pairing
`.deepwork/rules/source-test-pairing.md`:
```markdown
---
name: Source/Test Pairing
set:
  - src/{path}.py
  - tests/{path}_test.py
---
Source and test files should change together.

When modifying source code, ensure corresponding tests are updated.
When adding tests, ensure they test actual source code.

Modified: {trigger_files}
Expected: {expected_files}
```

### API Documentation Sync
`.deepwork/rules/api-docs.md`:
```markdown
---
name: API Documentation Update
pair:
  trigger: src/api/{path}.py
  expects: docs/api/{path}.md
---
API code has changed. Please verify that API documentation in docs/api/
is up to date with the code changes. Pay special attention to:

- New or changed endpoints
- Modified request/response schemas
- Updated authentication requirements

Changed API: {trigger_files}
Update: {expected_files}
```

## Output Format

### .deepwork/rules/{rule-name}.md
Create a new file with the rule definition using YAML frontmatter and markdown body.

## Quality Criteria

- Asked structured questions to understand user requirements
- Rule name is clear and descriptive (used in promise tags)
- Correct detection mode selected for the use case
- Patterns accurately match the intended files
- Safety patterns prevent unnecessary triggering (if applicable)
- Instructions are actionable and specific
- YAML frontmatter is valid

## Context

Rules are evaluated automatically when the agent finishes a task. The system:
1. Determines which files have changed based on each rule's `compare_to` setting
2. Evaluates rules based on their detection mode (trigger/safety, set, or pair)
3. Skips rules where the correspondence is satisfied (for set/pair) or safety matched
4. Prompts you with instructions for any triggered rules

You can mark a rule as addressed by including `<promise>Rule Name</promise>` in your response (replace Rule Name with the actual rule name from the `name` field). This tells the system you've already handled that rule's requirements.


### Job Context

Manages rules that automatically trigger when certain files change during an AI agent session.
Rules help ensure that code changes follow team guidelines, documentation is updated,
and architectural decisions are respected.

IMPORTANT: Rules are evaluated at the "Stop" hook, which fires when an agent finishes its turn.
This includes when sub-agents complete their work. Rules are NOT evaluated immediately after
each file edit - they batch up and run once at the end of the agent's response cycle.
- Command action rules: Execute their command (e.g., `uv sync`) when the agent stops
- Prompt action rules: Display instructions to the agent, blocking until addressed

Rules are stored as individual markdown files with YAML frontmatter in the `.deepwork/rules/`
directory. Each rule file specifies:
- Detection mode: trigger/safety, set (bidirectional), or pair (directional)
- Patterns: Glob patterns for matching files, with optional variable capture
- Action type: prompt (default) to show instructions, or command to run a shell command
- Instructions: Markdown content describing what the agent should do

Example use cases:
- Update installation docs when configuration files change
- Require security review when authentication code is modified
- Ensure API documentation stays in sync with API code
- Enforce source/test file pairing
- Auto-run `uv sync` when pyproject.toml changes (command action)


## Required Inputs

**User Parameters** - Gather from user before starting:
- **rule_purpose**: What guideline or constraint should this rule enforce?


## Work Branch

Use branch format: `deepwork/deepwork_rules-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/deepwork_rules-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `.deepwork/rules/{rule-name}.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "define complete, outputs: .deepwork/rules/{rule-name}.md"

This standalone skill can be re-run anytime.

---

**Reference files**: `.deepwork/jobs/deepwork_rules/job.yml`, `.deepwork/jobs/deepwork_rules/steps/define.md`