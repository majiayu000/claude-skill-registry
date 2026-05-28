---
name: plugin-maintain
description: Comprehensive maintenance skill for marketplace components - update components, manage knowledge, maintain READMEs, restructure, and apply orchestration compliance
tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Skill
---

# Plugin Maintain Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the appropriate workflow based on the task type parameter.

Comprehensive maintenance automation for marketplace bundles. Consolidates update, knowledge management, README maintenance, refactoring, and orchestration compliance into a single skill with progressive disclosure.

## Overview

This skill provides 5 maintenance workflows:

1. **update-component** - Update existing agents or commands with improvements
2. **add-knowledge** - Add external knowledge to skills with duplication prevention
3. **update-readme** - Synchronize README files with current marketplace state
4. **refactor-structure** - Restructure components for better organization
5. **apply-orchestration** - Apply bundle-by-bundle orchestration compliance patterns

## Progressive Disclosure Strategy

**Context Reduction**: Load only what's needed per workflow.

| Workflow | Reference Loaded | Lines |
|----------|------------------|-------|
| update-component | component-update-guide.md | ~650 |
| add-knowledge | knowledge-management-guide.md | ~600 |
| update-readme | readme-maintenance-guide.md | ~550 |
| refactor-structure | refactoring-strategies-guide.md | ~600 |
| apply-orchestration | orchestration-compliance.md | ~600 |

**Total Context Per Workflow**: ~1,400 lines (SKILL.md + reference)
**vs Loading Everything**: ~3,800 lines (75% reduction)

## Scripts

Script: `pm-plugin-development:plugin-maintain` → `maintain.py`

| Subcommand | Purpose |
|------------|---------|
| `analyze` | Analyze component for quality and improvement opportunities |
| `check-duplication` | Check for duplicate knowledge when adding content |
| `update` | Apply updates to a component file |
| `readme` | Generate README content from bundle inventory |

All scripts are stdlib-only with JSON output.

## Assets Available

| Asset | Purpose |
|-------|---------|
| `readme-template.md` | Template for README generation (`assets/readme-template.md`) |

## Workflow 1: update-component

**Goal**: Update existing agent or command with improvements.

**Parameters**:
- `component_path` (required): Path to component file
- `improvements` (required): Description of improvements to apply
- `verify` (optional): Run diagnosis after update (default: true)

### Steps

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Reference Guide

```
Read: references/component-update-guide.md
```

#### Step 2: Analyze Current State

Run component analysis:

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-maintain:maintain analyze --component {component_path}
```

Parse JSON output to understand:
- Current quality score
- Existing issues
- Section structure
- Line count

#### Step 3: Validate Improvements

Check that proposed improvements:
- Apply to this component's purpose
- Are specific enough to implement
- Follow anti-bloat rules (target 0 to -10% line change)
- Don't duplicate existing content

#### Step 4: Apply Updates

Use `maintain.py update` or Edit tool to apply changes:

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-maintain:maintain update --component {component_path} --updates '{"updates": [...]}'
```

Or use Edit tool for precise modifications.

#### Step 5: Verify Update

If `verify=true`:
- Re-run analyze-component.py
- Compare quality scores
- Check for new issues introduced

Report results including:
- Lines added/removed
- Quality score change
- Any warnings

## Workflow 2: add-knowledge

**Goal**: Add external knowledge to skill with duplication prevention.

**Parameters**:
- `skill_path` (required): Path to skill directory
- `source` (required): URL or file path to knowledge source
- `topic` (required): Topic/category for the knowledge
- `load_type` (optional): How to load - on-demand, conditional, always (default: on-demand)

### Steps

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Reference Guide

```
Read: references/knowledge-management-guide.md
```

#### Step 2: Validate Skill

Verify skill directory exists and has:
- SKILL.md file
- references/ or standards/ directory (create if missing)

#### Step 3: Fetch Source Content

If URL: Use WebFetch to retrieve content
If file: Read the file

#### Step 4: Check for Duplication

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-maintain:maintain check-duplication --skill-path {skill_path} --content-file {content_file}
```

Parse JSON output:
- `duplication_detected`: Boolean
- `duplication_percentage`: 0-100
- `recommendation`: proceed, consolidate, or skip

#### Step 5: Handle Duplication

If duplication found:
- Present findings to user
- Ask: Proceed anyway, Consolidate, or Skip

Use AskUserQuestion for confirmation.

#### Step 6: Create Knowledge Document

Create reference file in skill/references/:
- Add source attribution header
- Convert content to Markdown if needed
- Preserve all code examples

#### Step 7: Update SKILL.md

Add reference based on load_type:
- on-demand: Add to optional loading section
- conditional: Add with condition
- always: Add to main loading section

## Workflow 3: update-readme

**Goal**: Synchronize README with current marketplace state.

**Parameters**:
- `bundle_path` (optional): Path to bundle (default: all bundles)
- `force` (optional): Overwrite even if manual edits detected (default: false)

### Steps

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Reference Guide

```
Read: references/readme-maintenance-guide.md
```

#### Step 2: Generate README Content

For each bundle:

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-maintain:maintain readme --bundle-path {bundle_path}
```

Parse JSON output for:
- Bundle name
- Commands, agents, skills with descriptions
- Generated README content

#### Step 3: Compare with Existing

Read current README.md if exists:
- Identify manual edits (content not matching generated)
- Check for outdated component listings
- Detect missing or obsolete components

#### Step 4: Handle Manual Edits

If manual edits detected and not `force`:
- Display differences
- Ask user: Update, Skip, or Force

#### Step 5: Write Updated README

Use Write tool to update README.md.

Report:
- Components added
- Components removed
- Descriptions updated

## Workflow 4: refactor-structure

**Goal**: Restructure components for better organization.

**Parameters**:
- `scope` (required): What to refactor - component, bundle, or marketplace
- `strategy` (required): Refactoring strategy to apply

### Steps

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Reference Guide

```
Read: references/refactoring-strategies-guide.md
```

#### Step 2: Analyze Current Structure

For each component in scope:

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-maintain:maintain analyze --component {component_path}
```

Identify:
- Bloated components (>500 lines)
- Missing sections
- Quality issues
- Duplication across components

#### Step 3: Generate Refactoring Plan

Based on strategy:
- **consolidate**: Merge related components
- **split**: Break large components into smaller ones
- **extract**: Move shared content to skill
- **reorganize**: Restructure directory layout

#### Step 4: Apply Refactoring

Execute refactoring plan:
- Rename/move files
- Update cross-references
- Modify plugin.json entries
- Run verification

#### Step 5: Verify Results

Run plugin-diagnose on affected components.
Report any issues introduced.

## Workflow 5: apply-orchestration

**Goal**: Apply bundle-by-bundle orchestration compliance patterns.

**Parameters**:
- `command_path` (required): Path to diagnose command to update
- `verify` (optional): Verify compliance after update (default: true)

### Steps

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Reference Guide

```
Read: references/orchestration-compliance.md
```

This contains:
- Bundle-by-bundle processing rules
- Mandatory completion checklists
- Anti-skip protections
- Post-fix verification requirements

#### Step 2: Validate Command

Verify command is a diagnose command:
- Check name contains "diagnose"
- Verify it processes bundles

#### Step 3: Analyze Current Implementation

Read command file and check for:
- Bundle iteration pattern
- Completion checklist
- Stop points
- Verification gates

#### Step 4: Apply Compliance Patterns

Using Edit tool, add or update:
- Bundle-by-bundle iteration (Step 5)
- Anti-skip protections for steps 5e-5i
- Mandatory completion checklist (10 items)
- Post-fix verification with git status

#### Step 5: Verify Compliance

If `verify=true`:
- Check all required patterns present
- Validate checklist completeness
- Test command with sample bundle

## Critical Rules

### Anti-Bloat

- **TARGET 0 to -10% line change** when updating components
- **PREFER consolidation** over addition
- **PREFER skill references** over duplicating content
- **EXTRACT to skill** if content appears in 3+ components

### Quality Verification

- **ALWAYS analyze** before and after updates
- **VERIFY quality score** doesn't decrease significantly
- **RUN diagnosis** after structural changes
- **CHECK for new issues** introduced by changes

### Backup and Safety

- **CREATE backups** before modifications (scripts do this automatically)
- **RESTORE on failure** (scripts handle rollback)
- **GIT provides version control** - no manual backup files needed
- **PROMPT user** for risky changes (duplication found, manual edits detected)

### Knowledge Management

- **CHECK duplication** before adding knowledge
- **CONSOLIDATE** when overlap detected (>40%)
- **SKIP** when high duplication (>70%)
- **REFERENCE existing** instead of duplicating

## Error Handling

Each workflow handles errors:
1. Log error details
2. Restore from backup if applicable
3. Continue with next item if batch processing
4. Report all errors in summary

## Related Resources

- **plugin-diagnose skill** - Diagnose issues in components
- **plugin-fix skill** - Apply fixes to diagnosed issues
- **plugin-create skill** - Create new components

