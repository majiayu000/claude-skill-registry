---
name: audit-coordinator
description: Orchestrates comprehensive audits of Claude Code customizations using specialized auditors. Use when auditing multiple components, asking about naming/organization best practices, or needing thorough validation before deployment.
allowed-tools: [Read, Glob, Grep, Bash, Skill, Task]
# model: inherit
---

## Reference Files

### Audit Orchestration

- [workflow-patterns.md](workflow-patterns.md) - Multi-auditor invocation patterns and decision matrix
- [report-compilation.md](report-compilation.md) - Unified report structure and priority reconciliation

### Evaluation Standards and Troubleshooting

- [evaluation-criteria.md](evaluation-criteria.md) - Comprehensive standards for each component type
- [common-issues.md](common-issues.md) - Frequent problems and specific fixes with examples
- [anti-patterns.md](anti-patterns.md) - Common mistakes to avoid when building customizations

### Shared References (Used by All Authoring Skills)

- [naming-conventions.md](../../references/naming-conventions.md) - Patterns for agents, commands, skills, hooks, and output-styles
- [frontmatter-requirements.md](../../references/frontmatter-requirements.md) - Complete YAML specification for each component type
- [when-to-use-what.md](../../references/when-to-use-what.md) - Decision guide for choosing agents vs skills vs commands vs output-styles
- [file-organization.md](../../references/file-organization.md) - Directory structure and layout best practices
- [hook-events.md](../../references/hook-events.md) - Hook event types and timing reference
- [customization-examples.md](../../references/customization-examples.md) - Real-world examples across all component types

---

# Audit Coordinator

Orchestrates comprehensive audits by coordinating multiple specialized auditors and compiling their findings into unified reports.

## Available Auditors

The audit ecosystem includes:

### evaluator (Agent)

**Purpose**: General correctness, clarity, and effectiveness validation
**Scope**: All customization types
**Focus**: YAML validation, required fields, structure, naming conventions, context economy
**Invocation**: Via Task tool with subagent_type='evaluator'

### audit-skill (Skill)

**Purpose**: Skill discoverability and triggering effectiveness
**Scope**: Skills only
**Focus**: Description quality, trigger phrase coverage, progressive disclosure, discovery score
**Invocation**: Via Skill tool or auto-triggers on skill-related queries

### audit-hook (Skill)

**Purpose**: Hook safety, correctness, and performance
**Scope**: Hooks only
**Focus**: JSON handling, exit codes, error handling, performance, settings.json registration
**Invocation**: Via Skill tool or auto-triggers on hook-related queries

### test-runner (Agent)

**Purpose**: Functional testing and execution validation
**Scope**: All customization types
**Focus**: Test generation, execution, edge cases, integration testing
**Invocation**: Via Task tool with subagent_type='test-runner'

### audit-agent (Skill)

**Purpose**: Agent-specific validation for model selection, tool restrictions, and focus areas
**Scope**: Agents only
**Focus**: Model appropriateness (Sonnet/Haiku/Opus), tool permissions, focus area quality, approach completeness
**Invocation**: Via Skill tool or auto-triggers on agent-related queries

### audit-command (Skill)

**Purpose**: Command delegation and simplicity validation
**Scope**: Commands only
**Focus**: Delegation clarity, simplicity enforcement (6-80 lines), argument handling, documentation proportionality
**Invocation**: Via Skill tool or auto-triggers on command-related queries

### audit-output-style (Skill)

**Purpose**: Output-style persona and behavior validation
**Scope**: Output-styles only
**Focus**: Persona definition clarity, behavior specification concreteness, keep-coding-instructions decision, scope alignment
**Invocation**: Via Skill tool or auto-triggers on output-style-related queries

## Orchestration Workflow

### Step 0: Determine Audit Scope

**FIRST**, determine the scope of the audit by analyzing the user's request for scope indicators:

**Local/Project Scope** (`.claude/` in current directory):

- **Keywords**: "local", "project", ".claude", "current directory"
- **Search Path**: `.claude/` only
- **Use Case**: Audit project-specific customizations before committing
- **Example**: "Audit my local setup", "Check the project's .claude directory"

**Personal/User Scope** (`~/.claude/` global configuration):

- **Keywords**: "personal", "user", "~/.claude", "global"
- **Search Path**: `~/.claude/` only
- **Use Case**: Validate personal global configuration independently
- **Example**: "Audit my personal setup", "Check my user-level configuration"

**Full Scope** (both `.claude/` and `~/.claude/`):

- **Keywords**: "full", "both", "everything", "complete", "all", or no scope specified
- **Search Paths**: Both `.claude/` and `~/.claude/`
- **Use Case**: Comprehensive audit including conflict detection
- **Example**: "Audit my entire setup", "Check everything", or just "/audit-setup"
- **Default**: If no scope indicators found, use Full scope

**Scope Detection Logic**:

1. Parse user request for scope keywords
2. If "local" or "project" found → Local scope
3. If "personal" or "user" or "global" found → Personal scope
4. If "full" or "both" or "everything" found → Full scope
5. Otherwise → Full scope (default)

**Report Scope Section**: Include scope information in report header:

```markdown
# Comprehensive Audit Report

**Scope**: Local Project | Personal/User | Full Setup
**Project Path**: .claude/ {or "N/A - not in scope"}
**Personal Path**: ~/.claude/ {or "N/A - not in scope"}
**Date**: {timestamp}

{If full scope and both exist, add:}
**Conflicts**: {count} name(s) exist in both scopes (project takes precedence)
```

### Step 1: Identify Target Type

Determine what needs auditing **within the selected scope**:

**Single File**:

- Agent file (\*.md in agents/)
- Skill (SKILL.md in skills/\*/SKILL.md)
- Hook (_.sh or_.py in hooks/)
- Command (\*.md in commands/)
- Output-style (\*.md in output-styles/)

**Multiple Files**:

- All skills
- All hooks
- All agents
- Entire setup

**Context Clues**:

- File path mentioned
- Type specified ("audit my hook", "check this skill")
- General request ("audit my setup", "review everything")

**Path Filtering by Scope**:

- **Local scope**: Only search in `.claude/` directory
- **Personal scope**: Only search in `~/.claude/` directory
- **Full scope**: Search both, noting which files come from which scope

### Step 2: Determine Appropriate Auditors

Use decision matrix based on target type:

**Agent**:

- Primary: audit-agent (model, tools, focus areas, approach)
- Secondary: evaluator (structure)
- Optional: test-runner (if testing requested)

**Skill**:

- Primary: audit-skill (discoverability)
- Secondary: evaluator (structure)
- Optional: test-runner (functionality)

**Hook**:

- Primary: audit-hook (safety and correctness)
- Secondary: evaluator (structure)

**Command**:

- Primary: audit-command (delegation, simplicity, arguments)
- Secondary: evaluator (structure)

**Output-Style**:

- Primary: audit-output-style (persona, behaviors, coding-instructions)
- Secondary: evaluator (structure)
- Optional: test-runner (effectiveness)

**Setup (All)**:

- audit-agent (all agents)
- audit-skill (all skills)
- audit-hook (all hooks)
- audit-command (all commands)
- audit-output-style (all output-styles)
- evaluator (comprehensive)
- Can run in parallel

### Step 3: Invoke Auditors

Execute auditors in appropriate sequence, passing scope information:

**Sequential** (when results depend on each other):

```text
audit-skill → evaluator → test-runner
```

**Parallel** (when independent):

```text
audit-skill (all skills) || audit-hook (all hooks) || evaluator (agents/commands)
```

**Single** (when only one needed):

```text
audit-hook → done
```

**Scope Filtering During Invocation**:

- When invoking auditors, only pass files from the selected scope
- For **local scope**: Only pass paths starting with `.claude/`
- For **personal scope**: Only pass paths starting with `~/.claude/` or `/Users/.../.claude/`
- For **full scope**: Pass all paths, but note scope origin in reports

### Step 4: Compile Reports

Collect findings from all auditors and create unified report with scope information.

**Scope-Aware Report Compilation**:

- Group findings by scope (local vs personal) when in full scope mode
- Note which scope each component belongs to
- Identify conflicts (same name in both scopes)
- Remember: project-local files take precedence over personal files

### Step 5: Generate Unified Summary

Consolidate recommendations by priority and provide next steps.

**Scope-Specific Guidance**:

- **Local scope**: Focus on project-specific best practices, pre-commit validation
- **Personal scope**: Focus on global configuration consistency, tool compatibility
- **Full scope**: Include conflict resolution recommendations

## Target-Specific Patterns

### Pattern: Single Skill Audit

**User Query**: "Audit my hook-audit skill"

**Workflow**:

1. Invoke audit-skill for discoverability analysis
2. Invoke evaluator for structure validation
3. Compile reports
4. Generate unified recommendations

**Output**:

- Discovery score
- Structure assessment
- Progressive disclosure status
- Consolidated recommendations

### Pattern: Single Hook Audit

**User Query**: "Check my validate-config.py hook"

**Workflow**:

1. Invoke audit-hook for safety and correctness
2. Optionally invoke evaluator for structure
3. Compile reports
4. Generate unified recommendations

**Output**:

- Safety compliance status
- Exit code correctness
- Error handling assessment
- Performance analysis
- Consolidated recommendations

### Pattern: Setup-Wide Audit

**User Query**: "Audit my entire Claude Code setup"

**Workflow**:

1. Invoke evaluator for comprehensive setup analysis
2. Invoke audit-skill for all skills
3. Invoke audit-hook for all hooks
4. Run in parallel when possible
5. Compile all reports
6. Generate prioritized recommendations

**Output**:

- Setup summary (counts, sizes, context usage)
- Component-specific findings
- Cross-cutting issues
- Prioritized action items

### Pattern: Multiple Component Types

**User Query**: "Audit all my skills and hooks"

**Workflow**:

1. Invoke audit-skill for all skills (can run in parallel)
2. Invoke audit-hook for all hooks (can run in parallel)
3. Compile reports
4. Generate unified summary

**Output**:

- Skills: Discovery scores, structure
- Hooks: Safety compliance, performance
- Consolidated recommendations

## Report Compilation

When multiple auditors run, compile findings:

### Consolidation Strategy

1. **Collect all findings** from each auditor
2. **Group by severity**: Critical → Important → Nice-to-Have
3. **Deduplicate** similar issues across auditors
4. **Reconcile priorities** when auditors disagree
5. **Generate unified recommendations**

### Priority Reconciliation

When different auditors assign different priorities:

**Rule 1**: Critical from any auditor → Critical overall
**Rule 2**: Important + Important → Critical
**Rule 3**: Important + Nice-to-Have → Important
**Rule 4**: Nice-to-Have + Nice-to-Have → Nice-to-Have

### Unified Report Structure

```markdown
# Comprehensive Audit Report

**Target**: {what was audited}
**Date**: {YYYY-MM-DD HH:MM}
**Auditors**: {list of auditors invoked}

## Executive Summary

{1-2 sentence overview of findings}

## Overall Status

**Health Score**: {composite score}

- {Auditor 1}: {status}
- {Auditor 2}: {status}
- {Auditor 3}: {status}

## Critical Issues

{Must-fix issues from any auditor}

## Important Issues

{Should-fix issues}

## Nice-to-Have Improvements

{Polish items}

## Detailed Findings by Component

### {Component 1}

{Findings from relevant auditors}

### {Component 2}

{Findings from relevant auditors}

## Prioritized Action Items

1. **Critical**: {consolidated must-fix items}
2. **Important**: {consolidated should-fix items}
3. **Nice-to-Have**: {consolidated polish items}

## Next Steps

{Specific, actionable next steps}
```

## Quick Usage Examples

**Audit a skill**:

```text
User: "Audit my hook-audit skill"
Assistant: [Invokes audit-skill, evaluator; compiles report]
```

**Audit a hook**:

```text
User: "Check my validate-config.py hook"
Assistant: [Invokes audit-hook; generates report]
```

**Audit entire setup** (full scope - default):

```text
User: "Audit my complete Claude Code setup"
Assistant: [Invokes evaluator, audit-skill, audit-hook in parallel; compiles comprehensive report]
```

**Audit local project setup**:

```text
User: "Audit my local .claude configuration"
User: "/audit-setup local"
Assistant: [Determines scope: local; audits only .claude/ directory; generates project-specific report]
```

**Audit personal global setup**:

```text
User: "Audit my personal Claude setup"
User: "/audit-setup personal"
Assistant: [Determines scope: personal; audits only ~/.claude/ directory; generates user-level report]
```

**Audit with conflict detection**:

```text
User: "Audit everything and show me any conflicts"
User: "/audit-setup full"
Assistant: [Determines scope: full; audits both scopes; identifies conflicting names; generates comprehensive report]
```

**Audit multiple skills**:

```text
User: "Check all my skills for discoverability"
Assistant: [Invokes audit-skill for each skill; generates consolidated report]
```

## Integration with Other Auditors

### With audit-skill

**When to use together**:

- Comprehensive skill analysis
- Combining discoverability + structure validation

**Sequence**: audit-skill → evaluator
**Output**: Discovery score + structure assessment

### With audit-hook

**When to use together**:

- Complete hook validation
- Safety + structure analysis

**Sequence**: audit-hook → evaluator (optional)
**Output**: Safety compliance + structure validation

### With evaluator

**When to use together**:

- Always, for structural validation
- Complements specialized auditors

**Sequence**: Specialized auditor first, then evaluator
**Output**: Specialized analysis + general validation

### With test-runner

**When to use together**:

- Functional validation requested
- After structure/discovery validation

**Sequence**: Other auditors → test-runner
**Output**: Design validation + functional testing

## Decision Matrix

Quick reference for which auditors to invoke:

| Target       | Primary Auditor    | Secondary | Optional    | Sequence   |
| ------------ | ------------------ | --------- | ----------- | ---------- |
| Skill        | audit-skill        | evaluator | test-runner | Sequential |
| Hook         | audit-hook         | evaluator | -           | Sequential |
| Agent        | audit-agent        | evaluator | test-runner | Sequential |
| Command      | audit-command      | evaluator | -           | Sequential |
| Output-Style | audit-output-style | evaluator | test-runner | Sequential |
| All Skills   | audit-skill        | evaluator | -           | Parallel   |
| All Hooks    | audit-hook         | evaluator | -           | Parallel   |
| All Agents   | audit-agent        | evaluator | -           | Parallel   |
| All Commands | audit-command      | evaluator | -           | Parallel   |
| Setup        | all specialized    | evaluator | test-runner | Parallel   |

## Summary

**Audit Coordinator Benefits**:

1. **Automatic auditor selection** - Chooses right auditors for target
2. **Parallel execution** - Runs independent audits concurrently
3. **Unified reporting** - Compiles findings from multiple sources
4. **Priority reconciliation** - Consolidates conflicting priorities
5. **Comprehensive coverage** - Ensures all relevant checks performed

**Best for**: Multi-component audits, setup-wide analysis, coordinated validation

For detailed orchestration patterns, see [workflow-patterns.md](workflow-patterns.md).
For report compilation guidance, see [report-compilation.md](report-compilation.md).

## Guidance Workflows

Beyond orchestrating audits, this skill provides guidance on Claude Code customization standards and best practices.

### Pattern: Naming Guidance

**User Query**: "What should I name my new agent that reviews security?"

**Workflow**:

1. Identify component type (agent, skill, command, hook, output-style)
2. Reference naming conventions (see shared reference: naming-conventions.md)
3. Provide specific name suggestions with rationale
4. Offer examples of similar components
5. Explain naming pattern (e.g., {domain}-{role} for agents)

**Output**: Concrete name suggestions + pattern explanation

### Pattern: Organization Guidance

**User Query**: "How should I organize my skill's reference files?"

**Workflow**:

1. Assess current structure
2. Reference file organization standards (see shared reference: file-organization.md)
3. Apply progressive disclosure principles
4. Recommend structure improvements
5. Provide migration guidance if restructuring needed

**Output**: Recommended directory structure + migration steps

### Pattern: Pre-Deployment Validation

**User Query**: "Does this new skill look good?" (while editing SKILL.md)

**Workflow**:

1. Read target file
2. Invoke appropriate auditor (audit-skill, audit-agent, etc.)
3. Check against evaluation criteria (see references/evaluation-criteria.md)
4. Flag blocking issues (missing fields, invalid YAML, critical violations)
5. Provide quick validation summary

**Output**: Go/No-Go decision + critical fixes needed

### Pattern: Troubleshooting Guidance

**User Query**: "Why isn't my skill being discovered?"

**Workflow**:

1. Identify symptom (not discovered, not triggering, errors, etc.)
2. Reference common issues guide (see references/common-issues.md)
3. Reference anti-patterns (see references/anti-patterns.md)
4. Provide specific diagnosis and fix
5. Offer to run diagnostic audit if needed

**Output**: Diagnosis + specific fix + optional follow-up audit

### Pattern: Best Practices Consultation

**User Query**: "What are best practices for agents?"

**Workflow**:

1. Identify component type
2. Reference evaluation criteria (see references/evaluation-criteria.md)
3. Provide component-specific best practices
4. Give concrete examples of good patterns
5. Point to anti-patterns to avoid

**Output**: Best practices summary + examples + anti-patterns
