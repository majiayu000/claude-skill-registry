---
name: audit-coordinator
description: Orchestrates comprehensive audits across multiple specialized auditors
  for Claude Code customizations. Use when user wants complete evaluation of agents,
  skills, hooks, commands, output-styles, entire
---

---
name: audit-coordinator
description: Orchestrates comprehensive audits across multiple specialized auditors for Claude Code customizations and provides guidance on naming, organization, best practices, and troubleshooting. Use when: (1) Auditing - wants complete evaluation, multi-faceted analysis, coordinated audit reports, thorough validation, or asks to audit multiple components; (2) Guidance - asks "what should I name...", "how should I organize...", "best practices for...", troubleshooting issues, understanding evaluation criteria, or needs pre-deployment validation. Automatically determines which auditors to invoke (agent-audit, skill-audit, hook-audit, command-audit, output-style-audit, evaluator, test-runner) based on target type and compiles unified reports with consolidated recommendations.
allowed-tools: [Read, Glob, Grep, Bash, Skill, Task]
model: sonnet
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

### claude-code-evaluator (Agent)

**Purpose**: General correctness, clarity, and effectiveness validation
**Scope**: All customization types
**Focus**: YAML validation, required fields, structure, naming conventions, context economy
**Invocation**: Via Task tool with subagent_type='claude-code-evaluator'

### skill-audit (Skill)

**Purpose**: Skill discoverability and triggering effectiveness
**Scope**: Skills only
**Focus**: Description quality, trigger phrase coverage, progressive disclosure, discovery score
**Invocation**: Via Skill tool or auto-triggers on skill-related queries

### hook-audit (Skill)

**Purpose**: Hook safety, correctness, and performance
**Scope**: Hooks only
**Focus**: JSON handling, exit codes, error handling, performance, settings.json registration
**Invocation**: Via Skill tool or auto-triggers on hook-related queries

### claude-code-test-runner (Agent)

**Purpose**: Functional testing and execution validation
**Scope**: All customization types
**Focus**: Test generation, execution, edge cases, integration testing
**Invocation**: Via Task tool with subagent_type='claude-code-test-runner'

### agent-audit (Skill)

**Purpose**: Agent-specific validation for model selection, tool restrictions, and focus areas
**Scope**: Agents only
**Focus**: Model appropriateness (Sonnet/Haiku/Opus), tool permissions, focus area quality, approach completeness
**Invocation**: Via Skill tool or auto-triggers on agent-related queries

### command-audit (Skill)

**Purpose**: Command delegation and simplicity validation
**Scope**: Commands only
**Focus**: Delegation clarity, simplicity enforcement (6-80 lines), argument handling, documentation proportionality
**Invocation**: Via Skill tool or auto-triggers on command-related queries

### output-style-audit (Skill)

**Purpose**: Output-style persona and behavior validation
**Scope**: Output-styles only
**Focus**: Persona definition clarity, behavior specification concreteness, keep-coding-instructions decision, scope alignment
**Invocation**: Via Skill tool or auto-triggers on output-style-related queries

## Orchestration Workflow

### Step 1: Identify Target Type

Determine what needs auditing:

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

### Step 2: Determine Appropriate Auditors

Use decision matrix based on target type:

**Agent**:

- Primary: agent-audit (model, tools, focus areas, approach)
- Secondary: claude-code-evaluator (structure)
- Optional: claude-code-test-runner (if testing requested)

**Skill**:

- Primary: skill-audit (discoverability)
- Secondary: claude-code-evaluator (structure)
- Optional: claude-code-test-runner (functionality)

**Hook**:

- Primary: hook-audit (safety and correctness)
- Secondary: claude-code-evaluator (structure)

**Command**:

- Primary: command-audit (delegation, simplicity, arguments)
- Secondary: claude-code-evaluator (structure)

**Output-Style**:

- Primary: output-style-audit (persona, behaviors, coding-instructions)
- Secondary: claude-code-evaluator (structure)
- Optional: claude-code-test-runner (effectiveness)

**Setup (All)**:

- agent-audit (all agents)
- skill-audit (all skills)
- hook-audit (all hooks)
- command-audit (all commands)
- output-style-audit (all output-styles)
- claude-code-evaluator (comprehensive)
- Can run in parallel

### Step 3: Invoke Auditors

Execute auditors in appropriate sequence:

**Sequential** (when results depend on each other):

```text
skill-audit → claude-code-evaluator → test-runner
```

**Parallel** (when independent):

```text
skill-audit (all skills) || hook-audit (all hooks) || evaluator (agents/commands)
```

**Single** (when only one needed):

```text
hook-audit → done
```

### Step 4: Compile Reports

Collect findings from all auditors and create unified report.

### Step 5: Generate Unified Summary

Consolidate recommendations by priority and provide next steps.

## Target-Specific Patterns

### Pattern: Single Skill Audit

**User Query**: "Audit my bash-audit skill"

**Workflow**:

1. Invoke skill-audit for discoverability analysis
2. Invoke claude-code-evaluator for structure validation
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

1. Invoke hook-audit for safety and correctness
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

1. Invoke claude-code-evaluator for comprehensive setup analysis
2. Invoke skill-audit for all skills
3. Invoke hook-audit for all hooks
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

1. Invoke skill-audit for all skills (can run in parallel)
2. Invoke hook-audit for all hooks (can run in parallel)
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
User: "Audit my bash-audit skill"
Assistant: [Invokes skill-audit, evaluator; compiles report]
```

**Audit a hook**:

```text
User: "Check my validate-config.py hook"
Assistant: [Invokes hook-audit; generates report]
```

**Audit entire setup**:

```text
User: "Audit my complete Claude Code setup"
Assistant: [Invokes evaluator, skill-audit, hook-audit in parallel; compiles comprehensive report]
```

**Audit multiple skills**:

```text
User: "Check all my skills for discoverability"
Assistant: [Invokes skill-audit for each skill; generates consolidated report]
```

## Integration with Other Auditors

### With skill-audit

**When to use together**:

- Comprehensive skill analysis
- Combining discoverability + structure validation

**Sequence**: skill-audit → evaluator
**Output**: Discovery score + structure assessment

### With hook-audit

**When to use together**:

- Complete hook validation
- Safety + structure analysis

**Sequence**: hook-audit → evaluator (optional)
**Output**: Safety compliance + structure validation

### With claude-code-evaluator

**When to use together**:

- Always, for structural validation
- Complements specialized auditors

**Sequence**: Specialized auditor first, then evaluator
**Output**: Specialized analysis + general validation

### With claude-code-test-runner

**When to use together**:

- Functional validation requested
- After structure/discovery validation

**Sequence**: Other auditors → test-runner
**Output**: Design validation + functional testing

## Decision Matrix

Quick reference for which auditors to invoke:

| Target       | Primary Auditor    | Secondary | Optional    | Sequence   |
| ------------ | ------------------ | --------- | ----------- | ---------- |
| Skill        | skill-audit        | evaluator | test-runner | Sequential |
| Hook         | hook-audit         | evaluator | -           | Sequential |
| Agent        | agent-audit        | evaluator | test-runner | Sequential |
| Command      | command-audit      | evaluator | -           | Sequential |
| Output-Style | output-style-audit | evaluator | test-runner | Sequential |
| All Skills   | skill-audit        | evaluator | -           | Parallel   |
| All Hooks    | hook-audit         | evaluator | -           | Parallel   |
| All Agents   | agent-audit        | evaluator | -           | Parallel   |
| All Commands | command-audit      | evaluator | -           | Parallel   |
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
2. Invoke appropriate auditor (skill-audit, agent-audit, etc.)
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
