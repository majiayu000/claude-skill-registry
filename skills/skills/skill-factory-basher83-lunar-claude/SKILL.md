---
name: skill-factory
description: >
  Research-backed skill creation workflow with automated firecrawl research gathering, multi-tier
  validation, and comprehensive auditing. Use when "create skills with research automation",
  "build research-backed skills", "validate skills end-to-end", "automate skill research and
  creation", needs 9-phase workflow from research through final audit, wants firecrawl-powered
  research combined with validation, or requires quality-assured skill creation following
  Anthropic specifications for Claude Code.
---

# Skill Factory

Comprehensive workflow orchestrator for creating high-quality Claude Code skills with automated research, content
review, and multi-tier validation.

## When to Use This Skill

Use skill-factory when:

- **Creating any new skill** - From initial idea to validated, production-ready skill
- **Research needed** - Automate gathering of documentation, examples, and best practices
- **Quality assurance required** - Ensure skills meet official specifications and best practices
- **Guided workflow preferred** - Step-by-step progression with clear checkpoints
- **Validation needed** - Runtime testing, integration checks, and comprehensive auditing

**Scope:** Creates skills for ANY purpose (not limited to meta-claude plugin):

- Infrastructure skills (terraform-best-practices, ansible-vault-security)
- Development skills (docker-compose-helper, git-workflow-automation)
- Domain-specific skills (brand-guidelines, conventional-git-commits)
- Any skill that extends Claude's capabilities

## Available Operations

The skill-factory provides 9 specialized commands for the create-review-validate lifecycle:

| Command | Purpose | Use When |
|---------|---------|----------|
| `/meta-claude:skill:research` | Gather domain knowledge using firecrawl API | Need automated web scraping for skill research |
| `/meta-claude:skill:format` | Clean and structure research materials | Have raw research needing markdown formatting |
| `/meta-claude:skill:create` | Initialize skill structure with references | Ready to scaffold skill directory from research |
| `/meta-claude:skill:write` | Synthesize references into SKILL.md content | Skill initialized but needs content written |
| `/meta-claude:skill:review-content` | Validate content quality and clarity | Need content review before compliance check |
| `/meta-claude:skill:review-compliance` | Run quick_validate.py on SKILL.md | Validate YAML frontmatter and naming conventions |
| `/meta-claude:skill:validate-runtime` | Test skill loading in Claude context | Verify skill loads without syntax errors |
| `/meta-claude:skill:validate-integration` | Check for conflicts with existing skills | Ensure no duplicate names or overlaps |
| `/meta-claude:skill:validate-audit` | Invoke claude-skill-auditor agent | Get comprehensive audit against Anthropic specs |

**Power user tip:** Commands work standalone or orchestrated. Use individual commands for targeted fixes,
or invoke the skill for full workflow automation.

**Visual learners:** See [workflows/visual-guide.md](workflows/visual-guide.md) for decision trees, state diagrams,
and workflow visualizations.

## Quick Decision Guide

### Full Workflow vs Individual Commands

**Creating new skill (full workflow):**

- With research → `skill-factory <skill-name> <research-path>`
- Without research → `skill-factory <skill-name>` (includes firecrawl research)
- From knowledge only → `skill-factory <skill-name>` → Select "Skip research"

**Using individual commands (power users):**

| Scenario | Command | Why |
|----------|---------|-----|
| Need web research for skill topic | `/meta-claude:skill:research <name> [sources]` | Automated firecrawl scraping |
| Have messy research files | `/meta-claude:skill:format <research-dir>` | Clean markdown formatting |
| Ready to scaffold skill directory | `/meta-claude:skill:create <name> <research-dir>` | Creates structure with references |
| Skill initialized, needs content | `/meta-claude:skill:write <skill-path>` | Synthesizes references into SKILL.md |
| Content unclear or incomplete | `/meta-claude:skill:review-content <skill-path>` | Quality gate before compliance |
| Check frontmatter syntax | `/meta-claude:skill:review-compliance <skill-path>` | Runs quick_validate.py |
| Skill won't load in Claude | `/meta-claude:skill:validate-runtime <skill-path>` | Tests actual loading |
| Worried about name conflicts | `/meta-claude:skill:validate-integration <skill-path>` | Checks existing skills |
| Want Anthropic spec audit | `/meta-claude:skill:validate-audit <skill-path>` | Runs claude-skill-auditor |

**When to use full workflow:** Creating new skills from scratch
**When to use individual commands:** Fixing specific issues, power user iteration

For full workflow details, see Quick Start section below.

## Quick Start

### Path 1: Research Already Gathered

If you have research materials ready:

```bash
# Research exists at docs/research/skills/<skill-name>/
skill-factory <skill-name> docs/research/skills/<skill-name>/
```

The skill will:

1. Format research materials
2. Create skill structure (scaffold)
3. Write skill content (synthesize references)
4. Review content quality
5. Review technical compliance
6. Validate runtime loading
7. Validate integration
8. Run comprehensive audit
9. Present completion options

### Path 2: Research Needed

If starting from scratch:

```bash
# Let skill-factory handle research
skill-factory <skill-name>
```

The skill will ask about research sources and proceed through full workflow.

### Example Usage

```text
User: "Create a skill for CodeRabbit code review best practices"

skill-factory detects no research path provided, asks:

"Have you already gathered research for this skill?
[Yes - I have research at <path>]
[No - Help me gather research]
[Skip - I'll create from knowledge only]"

User: "No - Help me gather research"

skill-factory proceeds through Path 2:
1. Research skill domain
2. Format research materials
3. Create skill structure
... (continues through all phases)
```

## When This Skill Is Invoked

**Your role:** You are the skill-factory orchestrator. Your task is to guide the user through creating
a high-quality, validated skill using 9 primitive slash commands.

### Step 1: Entry Point Detection

Analyze the user's prompt to determine which workflow path to use:

**If research path is explicitly provided:**

```text
User: "skill-factory coderabbit docs/research/skills/coderabbit/"
→ Use Path 1 (skip research phase)
```

**If no research path is provided:**

Ask the user using AskUserQuestion:

```text
"Have you already gathered research for this skill?"

Options:
[Yes - I have research at a specific location]
[No - Help me gather research]
[Skip - I'll create from knowledge only]
```

**Based on user response:**

- **Yes** → Ask for research path, use Path 1
- **No** → Use Path 2 (include research phase)
- **Skip** → Use Path 1 without research (create from existing knowledge)

### Step 2: Initialize TodoWrite

Create a TodoWrite list based on the selected path:

**Path 2 (Full Workflow with Research):**

```javascript
TodoWrite([
  {"content": "Research skill domain", "status": "pending", "activeForm": "Researching skill domain"},
  {"content": "Format research materials", "status": "pending", "activeForm": "Formatting research materials"},
  {"content": "Create skill structure", "status": "pending", "activeForm": "Creating skill structure"},
  {"content": "Write skill content", "status": "pending", "activeForm": "Writing skill content"},
  {"content": "Review content quality", "status": "pending", "activeForm": "Reviewing content quality"},
  {"content": "Review technical compliance", "status": "pending", "activeForm": "Reviewing technical compliance"},
  {"content": "Validate runtime loading", "status": "pending", "activeForm": "Validating runtime loading"},
  {"content": "Validate integration", "status": "pending", "activeForm": "Validating integration"},
  {"content": "Run comprehensive audit", "status": "pending", "activeForm": "Running comprehensive audit"},
  {"content": "Complete workflow", "status": "pending", "activeForm": "Completing workflow"}
])
```

**Path 1 (Research Exists or Skipped):**

Omit the first "Research skill domain" task. Start with "Format research materials" or
"Create skill structure" depending on whether research exists.

### Step 3: Execute Workflow Sequentially

For each phase in the workflow, follow this pattern:

#### 1. Mark phase as in_progress

Update the corresponding TodoWrite item to `in_progress` status.

#### 2. Check dependencies

Before running a command, verify prior phases completed:

- Write requires create to complete (needs skill structure with references)
- Review-content requires write to complete (needs actual content to review)
- Review-compliance requires review-content to pass
- Validate-runtime requires review-compliance to pass
- Validate-integration requires validate-runtime to pass
- Validate-audit runs regardless (non-blocking feedback)

#### 3. Invoke command using SlashCommand tool

```text
/meta-claude:skill:research <skill-name> [sources]
/meta-claude:skill:format <research-dir>
/meta-claude:skill:create <skill-name> <research-dir>
/meta-claude:skill:write <skill-path>
/meta-claude:skill:review-content <skill-path>
/meta-claude:skill:review-compliance <skill-path>
/meta-claude:skill:validate-runtime <skill-path>
/meta-claude:skill:validate-integration <skill-path>
/meta-claude:skill:validate-audit <skill-path>
```

**IMPORTANT:** Wait for each command to complete before proceeding to the next phase.
Do not invoke multiple commands in parallel.

#### 4. Check command result

Each command returns success or failure with specific error details.

#### 5. Apply fix strategy if needed

The workflow uses a three-tier fix strategy:

- **Tier 1 (Simple):** Auto-fix formatting, frontmatter, markdown syntax
- **Tier 2 (Medium):** Guided fixes with user approval
- **Tier 3 (Complex):** Stop and report - requires manual fixes

**One-shot policy:** Each fix applied once, re-run once, then fail fast if still broken.

**For complete tier definitions, issue categorization, examples, and fix workflows:**
See [references/error-handling.md](references/error-handling.md)

#### 6. Mark phase completed

Update TodoWrite item to `completed` status.

#### 7. Continue to next phase

Proceed to the next workflow phase, or exit if fail-fast triggered.

### Step 4: Completion

When all phases pass successfully:

**Present completion summary:**

```text
✅ Skill created and validated successfully!

Location: <skill-output-path>/

Research materials: docs/research/skills/<skill-name>/
```

**Ask about artifact cleanup:**

```text
Keep research materials? [Keep/Remove] (default: Keep)
```

**Present next steps using AskUserQuestion:**

```text
Next steps - choose an option:
[Test in new session - Skills require session reload to be discoverable]
[Create PR - Submit skill to repository]
[Done - Exit workflow]
```

**Execute user's choice:**

- **Test in new session** → Skills load at session start. User must restart Claude Code to test.
- **Create PR** → Create git branch, commit, push, open PR
- **Done** → Clean exit

**Note:** Skills auto-discover based on directory structure - no plugin.json registration needed.

### Key Execution Principles

**Sequential Execution:** Do not run commands in parallel. Wait for each phase to complete before proceeding.

**Context Window Protection:** You are orchestrating commands, not sub-agents. Your context window is safe
because you're invoking slash commands sequentially, not spawning multiple agents.

**State Management:** TodoWrite provides real-time progress visibility. Update it at every phase
transition.

**Fail Fast:** When Tier 3 issues occur or user declines fixes, exit immediately with clear guidance.
Don't attempt complex recovery.

**Dependency Enforcement:** Never skip dependency checks. Review phases are sequential, validation
phases are tiered.

**One-shot Fixes:** Apply each fix once, re-run once, then fail if still broken. This prevents infinite loops.

**User Communication:** Report progress clearly. Show which phase is running, what the result was,
and what's happening next.

## Workflow Architecture

Two paths based on research availability: Path 1 (research exists) and Path 2 (research needed).
TodoWrite tracks progress through 8-10 phases. Entry point detection uses prompt analysis and AskUserQuestion.

**Details:** See [references/workflow-architecture.md](references/workflow-architecture.md)

## Workflow Execution

Sequential phase invocation pattern: mark in_progress → check dependencies → invoke command →
check result → apply fixes → mark completed → continue. Dependencies enforced (review sequential,
validation tiered). Commands invoked via SlashCommand tool with wait-for-completion pattern.

**Details:** See [references/workflow-execution.md](references/workflow-execution.md)

## Success Completion

When all phases pass successfully:

```text
✅ Skill created and validated successfully!

Location: <skill-output-path>/

Research materials: docs/research/skills/<skill-name>/
Keep research materials? [Keep/Remove] (default: Keep)
```

**Artifact Cleanup:**

Ask user about research materials:

- **Keep** (default): Preserves research for future iterations, builds knowledge base
- **Remove**: Cleans up workspace, research can be re-gathered if needed

**Next Steps:**

Present options to user:

```text
Next steps - choose an option:
  [1] Test in new session - Skills require session reload to be discoverable
  [2] Create PR - Submit skill to repository
  [3] Done - Exit workflow

What would you like to do?
```

**User Actions:**

1. **Test in new session** → Skills load at session start. User must restart Claude Code to test.
2. **Create PR** → Create git branch, commit, push, open PR
3. **Done** → Clean exit

**Note:** Skills auto-discover based on directory structure - no plugin.json registration needed.

Execute the user's choice, then exit cleanly.

## Examples

The skill-factory workflow supports various scenarios:

1. **Path 2 (Full Workflow):** Creating skills from scratch with automated research gathering
2. **Path 1 (Existing Research):** Creating skills when research materials already exist
3. **Guided Fix Workflow:** Applying Tier 2 fixes with user approval
4. **Fail-Fast Pattern:** Handling Tier 3 complex issues with immediate exit

**Detailed Examples:** See [references/workflow-examples.md](references/workflow-examples.md) for complete walkthrough
scenarios showing TodoWrite state transitions, command invocations, error handling, and success paths.

## Design Principles

Six core principles: (1) Primitives First (slash commands foundation), (2) KISS State Management (TodoWrite only),
(3) Fail Fast (no complex recovery), (4) Context-Aware Entry (prompt analysis), (5) Composable & Testable
(standalone or orchestrated), (6) Quality Gates (sequential dependencies).

**Details:** See [references/design-principles.md](references/design-principles.md)

## Implementation Notes

### Command-Based Architecture

skill-factory orchestrates 9 primitive slash commands through a sequential workflow:

**Creation Phase:**

- `/meta-claude:skill:research` → Gather domain knowledge via firecrawl
- `/meta-claude:skill:format` → Clean and structure research materials
- `/meta-claude:skill:create` → Scaffold skill directory with references (runs init_skill.py)
- `/meta-claude:skill:write` → Synthesize references into SKILL.md content

**Validation Phase:**

- `/meta-claude:skill:review-content` → Quality gate for clarity and completeness
- `/meta-claude:skill:review-compliance` → Technical validation via quick_validate.py
- `/meta-claude:skill:validate-runtime` → Test actual skill loading
- `/meta-claude:skill:validate-integration` → Check for naming conflicts
- `/meta-claude:skill:validate-audit` → Comprehensive audit via claude-skill-auditor agent

Each command is standalone and testable. skill-factory provides orchestration, not abstraction.

### Progressive Disclosure

This skill provides:

1. **Quick Start** - Fast path for common use cases
2. **Workflow Architecture** - Understanding the orchestration model
3. **Detailed Phase Documentation** - Deep dive into each phase
4. **Error Handling** - Comprehensive fix strategies
5. **Examples** - Real-world scenarios

Load sections as needed for your use case.

## Troubleshooting

Common issues: research phase failures (check FIRECRAWL_API_KEY), content review loops (Tier 3 issues need
redesign), compliance validation (run quick_validate.py manually), integration conflicts (check duplicate names).

**Details:** See [references/troubleshooting.md](references/troubleshooting.md)

## Success Metrics

You know skill-factory succeeds when:

1. **Time to create skill:** Reduced from hours to minutes
2. **Skill quality:** 100% compliance with official specs on first validation
3. **User satisfaction:** Beginners create high-quality skills without deep knowledge
4. **Maintainability:** Primitives are independently testable and reusable
5. **Workflow clarity:** Users understand current phase and next steps at all times

## Related Resources

- **multi-agent-composition skill** - Architectural patterns and composition rules
- **Primitive commands** - Individual slash commands under `/meta-claude:skill:*` namespace
- **quick_validate.py** - Compliance validation script
- **skill-audit-agent** - Comprehensive skill audit agent
