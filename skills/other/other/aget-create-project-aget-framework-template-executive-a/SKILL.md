---
name: aget-create-project
description: Create research projects with context-aware scaffolding. Reads AGET identity, searches prior work, pre-populates Due Diligence. Use when starting any formal AGET project.
disable-model-invocation: true
---

# /aget-create-project

Create a new AGET project with research-informed scaffolding per PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md.

## Input

$ARGUMENTS

## Mode Detection

| Input Pattern | Mode | Behavior |
|---------------|------|----------|
| Empty or blank | **Interactive** | Prompt for type and name |
| `<type> <name>` | **Explicit** | Create project of specified type |
| `<topic>` only | **Inference** | Infer type from topic and AGET domain |

## Supported Project Types

| Type | Template | Output Location |
|------|----------|-----------------|
| `research` | `templates/poc/RESEARCH_PROJECT_PLAN.template.md` | `planning/PROJECT_PLAN_<NAME>.md` |
| `poc` | `templates/poc/PROPOSAL.template.md` | `planning/poc-proposals/POC-XXX-<name>.md` |

## Project Creation Process

### Step 1: Input Analysis

Parse $ARGUMENTS to determine:
- Project type (research, poc, or infer from topic)
- Project name
- If empty in interactive mode, prompt user

**Headless mode**: If no arguments and headless, return error:
```
Error: Project type and name required in headless mode.
Usage: /aget-create-project <type> <name>
Types: research, poc
```

### Step 2: Conflict Check

Check for existing project:
```bash
ls planning/ | grep -qi "<name>"
```

If project exists, WARN and ask for confirmation before proceeding.

### Step 3: Research Phase (KEY DIFFERENTIATOR)

Before scaffolding, gather AGET context:

#### 3.1 Read AGET Identity
```bash
cat .aget/identity.json
```
Extract:
- `north_star`: Agent's purpose
- `domain`: Research focus areas
- `archetype`: Agent type

#### 3.2 Search Relevant L-docs
```bash
grep -l "<topic_keywords>" .aget/evolution/*.md
```
For each found L-doc, extract:
- L-doc ID and title
- Key lesson
- Application to this project

#### 3.3 Search Prior Sessions
```bash
grep -l "<topic_keywords>" sessions/*.md
```
Note related sessions for Traceability.

#### 3.4 Search Similar Projects
```bash
grep -l "<topic_keywords>" planning/PROJECT_PLAN_*.md
```
If similar project exists, WARN about potential duplication.

#### 3.5 Extract Vocabulary Terms
```bash
grep -B2 -A5 "<topic_keywords>" specs/CLI_VOCABULARY.md
```
Identify vocabulary terms for Traceability section.

### Step 4: Template Selection

Verify template exists:
```bash
test -f templates/poc/RESEARCH_PROJECT_PLAN.template.md
```

If template missing, STOP with error:
```
Error: Template not found: templates/poc/RESEARCH_PROJECT_PLAN.template.md
Cannot create project without template.
```

### Step 5: Scaffold Generation

Read template and populate:

#### 5.1 Header
```markdown
**Version**: 1.0.0
**Status**: Phase -1 (Due Diligence)
**Created**: <today's date>
**Author**: <AGET name from identity.json>
**Template**: `templates/poc/RESEARCH_PROJECT_PLAN.template.md`
```

#### 5.2 Hypothesis
Generate hypothesis ID: `H-<PREFIX>-000` where PREFIX is derived from project name.

#### 5.3 Phase -1 (Pre-populated)
Fill L-doc Review table with results from Step 3.2:
```markdown
| L-doc | Title | Key Lesson | Application |
|-------|-------|------------|-------------|
| <from research> | <from research> | <from research> | <from research> |
```

#### 5.4 Traceability
Include:
- Template reference
- Vocabulary terms from Step 3.5
- Related L-docs from Step 3.2
- Related sessions from Step 3.3
- Identity reference

### Step 6: Write Output

Write to appropriate location:
- Research: `planning/PROJECT_PLAN_<NAME>.md`
- POC: `planning/poc-proposals/POC-XXX-<name>.md`

### Step 7: Report

Output summary:
```markdown
## Project Created: <name>

**Type**: <type>
**Location**: <output path>

**Research Summary**:
- Identity: <north_star excerpt>
- Related L-docs: <count> found
- Related sessions: <count> found
- Similar projects: <count> found (warnings if any)

**Pre-populated**:
- Phase -1: L-doc Review table filled
- Traceability: Vocabulary and L-doc links added

**Next Steps**:
1. Review generated project plan
2. Refine hypothesis statement
3. Execute Phase -1 due diligence checklist
```

## Output Format

```markdown
## Project Created: <name>

**Type**: research
**Location**: planning/PROJECT_PLAN_<NAME>.md

**Research Summary**:
- Identity: CLI agent subsystem research
- Related L-docs: 5 found
- Related sessions: 2 found
- Similar projects: 0 found

**Pre-populated**:
- Phase -1: L-doc Review table filled with 5 entries
- Traceability: 3 vocabulary terms, 5 L-doc links

**Next Steps**:
1. Review generated project plan
2. Refine hypothesis statement
3. Execute Phase -1 due diligence checklist
```

## Constraints

These are INVIOLABLE - you MUST NOT violate these constraints:

1. **NEVER** create project without valid template
2. **NEVER** overwrite existing project without explicit confirmation
3. **NEVER** modify specs/, governance/, or .aget/ directly
4. **NEVER** skip the Research Phase (Step 3)
5. **NEVER** create project in headless mode without explicit type and name
6. **DO** read .aget/identity.json before scaffolding
7. **DO** search for relevant L-docs and include in Phase -1
8. **DO** warn about similar existing projects
9. **DO** include Traceability section with vocabulary links
10. **DO** use prohibitive form for constraints per L561

## Rationale

Per AGET theoretical grounding:
- **Stigmergy** (Grasse): Project artifacts enable cross-session coordination
- **Extended Mind** (Clark/Chalmers): Research phase extends agent's project-creation capability with prior knowledge
- **Evidence-First Design** (L289): Research before scaffolding
- **Ontology-Driven Creation** (L481): Vocabulary terms inform project structure

This skill implements the "research-informed project creation" pattern per PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md.

## Traceability

| Link | Reference |
|------|-----------|
| Vocabulary | Project, Agent_Skill, AGET_Skill (CLI_VOCABULARY.md) |
| Requirements | R-SKILL-006-001 through R-SKILL-006-021 |
| Skill Spec | SKILL-006 |
| SOP | SOP_SKILL_DEVELOPMENT.md |
| Template | templates/poc/RESEARCH_PROJECT_PLAN.template.md |
| L-docs | L474, L561, L567, L582, L584 |
| Project | PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md |
| Hypotheses | H-ACP-000 through H-ACP-006 |
