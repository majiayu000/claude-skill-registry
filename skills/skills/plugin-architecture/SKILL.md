---
name: plugin-architecture
description: Architecture principles, skill patterns, and design guidance for building goal-based Claude Code marketplace components
user-invocable: false
allowed-tools: Read
---

# Plugin Architecture Skill

**REFERENCE MODE**: This skill provides reference material. Load specific references on-demand based on current task. Do not load all references at once.

Pure reference skill providing architecture principles, skill patterns, and design guidance for building goal-based Claude Code marketplace components.

## What This Skill Provides

**Architecture Foundation**: Core principles for building marketplace components that follow Claude Skills best practices and goal-based organization.

**Skill Patterns**: 10 implementation patterns for building different types of skills (automation, analysis, validation, etc.).

**Design Guidance**: Workflow-focused skill design, thin orchestrator commands, and proper resource organization.

## Pattern Type

**Pattern 10: Reference Library** - Pure reference skill with no execution logic. Load references on-demand based on current task.

## When to Use This Skill

Activate when:
- **Creating new marketplace components** - Agents, commands, skills, or bundles
- **Refactoring existing components** - Migrating to goal-based architecture
- **Reviewing component design** - Ensuring architecture compliance
- **Learning marketplace architecture** - Understanding principles and patterns

## Core Concepts

### Goal-Based Organization

**Principle**: Organize by WHAT users want to accomplish (goals), not by WHAT component operates on (types).

**User Goals**:
- **CREATE** - Create new marketplace components
- **DIAGNOSE** - Find and understand issues
- **FIX** - Fix identified issues
- **MAINTAIN** - Keep marketplace healthy
- **LEARN** - Understand architecture and patterns

### Progressive Disclosure

**Principle**: Minimize initial context load, load details on-demand.

**Levels**:
1. **Frontmatter** - Minimal metadata (~3 lines)
2. **SKILL.md** - Full instructions (~400-800 lines)
3. **References** - Detailed content (thousands of lines, loaded when needed)

### Relative Path Pattern

**Principle**: All resource paths use relative paths from the skill directory for portability across installations.

**Examples**:
```
Read references/core-principles.md
bash scripts/analyzer.py
Load template: assets/template.html
```

When a skill is loaded, Claude knows its installation directory and resolves relative paths from there.

## Available References

Load references progressively based on current task. **Never load all references at once.**

### 1. Core Principles (NEW - Essential Foundation)
**File**: `references/core-principles.md`

**Load When**:
- Starting any marketplace component development
- Learning Claude Skills fundamentals
- Understanding relative path pattern
- Reviewing progressive disclosure strategy

**Contents**:
- Skills as prompt modifiers
- Relative path pattern for portability
- Progressive disclosure strategy
- Resource organization (scripts/, references/, assets/)
- Tool permissions scoping
- Imperative language guidelines
- Scripts for deterministic logic
- Anti-patterns to avoid

**Load Command**:
```
Read references/core-principles.md
```

### 2. Skill Patterns (NEW - Implementation Patterns)
**File**: `references/skill-patterns.md`

**Load When**:
- Designing a new skill
- Choosing implementation pattern
- Understanding skill composition
- Learning pattern combinations

**Contents**:
- Pattern 1: Script Automation
- Pattern 2: Read-Process-Write
- Pattern 3: Search-Analyze-Report
- Pattern 4: Command Chain Execution
- Pattern 5: Wizard-Style Workflow
- Pattern 6: Template-Based Generation
- Pattern 7: Iterative Refinement
- Pattern 8: Context Aggregation
- Pattern 9: Validation Pipeline
- Pattern 10: Reference Library
- Decision guide for choosing patterns
- Pattern combination strategies

**Load Command**:
```
Read references/skill-patterns.md
```

### 3. Goal-Based Organization (NEW - Architecture Paradigm)
**File**: `references/goal-based-organization.md`

**Load When**:
- Understanding goal-based vs component-centric
- Migrating from component-centric architecture
- Designing goal-based commands
- Learning context optimization strategies

**Contents**:
- Goal-centric vs component-centric comparison
- User goals: CREATE, DIAGNOSE, FIX, MAINTAIN, LEARN
- Benefits of goal-based structure
- Migration from component-centric
- Progressive disclosure in action
- Context reduction strategies

**Load Command**:
```
Read references/goal-based-organization.md
```

### 4. Architecture Rules (Core Requirements)
**File**: `references/architecture-rules.md`

**Load When**:
- Validating component compliance
- Understanding self-containment requirements
- Learning reference pattern rules
- Implementing progressive disclosure

**Contents**:
- Rule 1: Skills must be self-contained
- Rule 2: Components must use skills (not direct file access)
- Rule 3: Reference categorization (internal, external, skill)
- Rule 4: Progressive disclosure requirement
- Rule 5: Goal-based organization requirement
- relative path pattern requirements
- Validation criteria

**Load Command**:
```
Read references/architecture-rules.md
```

### 5. Skill Design (Workflow-Focused)
**File**: `references/skill-design.md`

**Load When**:
- Designing skill workflows
- Creating multi-workflow skills
- Understanding workflow parameters
- Learning skill composition patterns

**Contents**:
- Workflow-focused design principles
- Multi-workflow vs single-workflow skills
- Workflow parameter design
- Conditional workflow selection
- Workflow composition patterns
- Quality standards for workflows

**Load Command**:
```
Read references/skill-design.md
```

### 6. Command Design (Thin Orchestrators)
**File**: `references/command-design.md`

**Load When**:
- Creating new commands
- Designing parameter parsing
- Routing to skill workflows
- Learning user interaction patterns

**Contents**:
- Thin orchestrator pattern
- Parameter parsing strategies
- Routing to skill workflows
- Goal-based command structure
- User interaction patterns
- Command quality standards

**Load Command**:
```
Read references/command-design.md
```

### 7. Token Optimization (Context Management)
**File**: `references/token-optimization.md`

**Load When**:
- Optimizing context usage
- Designing batch processing
- Implementing large-scale workflows
- Reducing token consumption

**Contents**:
- Pre-loading shared content
- Batched processing strategies
- Streamlined output formats
- Context budgeting
- Progressive disclosure for token reduction
- Pattern 7 (Iterative Refinement) for large codebases

**Load Command**:
```
Read references/token-optimization.md
```

### 8. Reference Patterns (relative paths Usage)
**File**: `references/reference-patterns.md`

**Load When**:
- Understanding allowed reference types
- Implementing relative path pattern
- Validating reference compliance
- Testing portability

**Contents**:
- Pattern 1: relative paths/references/ for documentation
- Pattern 2: relative paths/scripts/ for automation
- Pattern 3: relative paths/assets/ for templates
- Pattern 4: External URLs (allowed)
- Pattern 5: Skill dependencies (Skill:)
- Portability testing guidance
- Prohibited patterns

**Load Command**:
```
Read references/reference-patterns.md
```

### 9. Frontmatter Standards (Component Metadata)
**File**: `references/frontmatter-standards.md`

**Load When**:
- Creating component YAML frontmatter
- Validating frontmatter fields
- Understanding required vs optional fields

**Contents**:
- Required frontmatter fields
- Optional frontmatter fields
- Field format specifications
- Validation rules
- Examples for agents, commands, skills

**Load Command**:
```
Read references/frontmatter-standards.md
```

### 10. Script Standards (Executable Automation)
**File**: `references/script-standards.md`

**Load When**:
- Documenting scripts in SKILL.md
- Understanding script quality requirements
- Common issues and fixes

**Contents**:
- Script location (`{skill-dir}/scripts/`)
- Documentation requirements in SKILL.md
- Script quality checklist
- Common issues and fixes

**Related Skill**:
For Python implementation patterns, testing standards, and output contracts:
```
Skill: pm-plugin-development:plugin-script-architecture
```

**Load Command**:
```
Read references/script-standards.md
```

### 11. Execution Directive (Skill Execution Patterns)
**File**: `references/execution-directive.md`

**Load When**:
- Creating execution skills (Pattern 1-9)
- Ensuring Claude executes rather than explains
- Adding MANDATORY/CRITICAL markers
- Designing command handoff patterns
- Distinguishing EXECUTE vs READ vs REFERENCE modes

**Contents**:
- Execution Mode directive standard
- MANDATORY/CRITICAL marker usage
- Execution vs Reference clarity patterns
- Workflow decision tree patterns
- Command handoff pattern
- Imperative language guidelines
- Code-first pattern
- Validation checklist pattern
- Anti-patterns to avoid

**Load Command**:
```
Read references/execution-directive.md
```

### 12. Minimal Wrapper Pattern (Context Isolation Strategy)
**File**: `references/minimal-wrapper-pattern.md`

**Load When**:
- Designing agents or commands as thin orchestrators
- Solving context handling challenges
- Understanding agent-to-skill delegation
- Migrating from fat agents (> 150 lines)
- Implementing context isolation strategy
- Learning line budget guidelines for wrappers

**Contents**:
- Problem: Context pollution with pure skill-based architecture
- Solution: Thin wrappers (< 150 lines) that delegate to skills
- Why agent→skill works but agent→agent doesn't
- Implementation patterns for commands and agents
- Line budget guidelines (150 line maximum)
- Skill invocation patterns (commands, agents, chained)
- Anti-patterns (fat wrappers, duplicate logic, agent-to-agent)
- Correct patterns (thin orchestration, single source of truth)
- Integration with goal-based organization
- Migration guide from fat agents to minimal wrappers
- Quality checklist for wrapper compliance
- Real-world before/after examples

**Load Command**:
```
Read references/minimal-wrapper-pattern.md
```

### 13. User-Facing Output (Display Standards)
**File**: `references/user-facing-output.md`

**Load When**:
- Designing skill/command output
- Filtering internal operations from user display
- Creating status messages and progress indicators
- Implementing phase transitions
- Reviewing output for anti-patterns

**Contents**:
- Core concept: Show status, not process
- Structured status output pattern
- Phase transition message format
- Configuration display pattern
- Progress tables pattern
- Issue detection output pattern
- Final metrics display pattern
- Anti-patterns: What NOT to display (step numbers, skill loading, tool execution, diffs)
- Output filtering rules (MUST/MUST NOT/MAY display)
- Output by component type (commands, skills, agents)
- Implementation checklist

**Load Command**:
```
Read references/user-facing-output.md
```

### 14. AskUserQuestion Patterns (User Interaction)
**File**: `references/askuserquestion-patterns.md`

**Load When**:
- Designing interactive workflows with user input
- Using AskUserQuestion tool in skills/commands
- Handling free-text input via "Other" option
- Avoiding common interaction anti-patterns

**Contents**:
- Tool characteristics and schema
- Pattern 1: Selection with free-text alternative
- Pattern 2: Confirmation with customization
- Pattern 3: Type selection
- Pattern 4: Multi-select features
- Anti-patterns (redundant options, follow-up questions, expecting customization)
- Best practices for question design
- Known limitations (fixed "Type something." label)
- Workarounds for UI constraints

**Load Command**:
```
Read references/askuserquestion-patterns.md
```

## Examples

### Example 1: Goal-Based Skill
**File**: `references/examples/goal-based-skill-example.md`

**Load When**:
- Learning goal-based skill structure
- Understanding workflow organization
- Seeing progressive disclosure in practice

**Shows**:
- plugin-diagnose skill structure
- 5 workflows for different diagnostic goals
- Progressive disclosure demonstration
- relative paths usage throughout
- Script contracts (JSON output)
- Reference loading patterns

**Load Command**:
```
Read references/examples/goal-based-skill-example.md
```

### Example 2: Thin Orchestrator Command
**File**: `references/examples/workflow-command-example.md`

**Load When**:
- Learning command design patterns
- Understanding parameter parsing
- Seeing skill invocation in practice

**Shows**:
- diagnose command structure
- Parameter parsing logic
- Scope determination
- Skill invocation with workflow selection
- User interaction patterns

**Load Command**:
```
Read references/examples/workflow-command-example.md
```

### Example 3: Pattern Usage
**File**: `references/examples/pattern-usage-examples.md`

**Load When**:
- Applying skill patterns to real scenarios
- Understanding pattern combinations
- Learning when to use which pattern

**Shows**:
- Each of 10 patterns applied to marketplace scenarios
- Pattern combinations (e.g., Pattern 5 + Pattern 6)
- When to use which pattern
- Anti-pattern examples

**Load Command**:
```
Read references/examples/pattern-usage-examples.md
```

## Usage Workflow

### Step 1: Identify Your Goal

Determine what you're trying to accomplish:
- **Creating component** → Load core-principles.md, skill-patterns.md
- **Understanding architecture** → Load goal-based-organization.md, architecture-rules.md
- **Designing skill** → Load skill-design.md, skill-patterns.md
- **Designing command** → Load command-design.md
- **Optimizing context** → Load token-optimization.md
- **Validating compliance** → Load architecture-rules.md, reference-patterns.md

### Step 2: Load Relevant References

**Never load all references** - Load only what's needed for current task.

**Example**:
```
# Creating a new skill
Read references/core-principles.md
Read references/skill-patterns.md
Read references/skill-design.md
```

### Step 3: Apply Principles

Follow the guidance in loaded references:
- Use relative paths for all resource paths
- Implement progressive disclosure
- Choose appropriate skill pattern
- Follow architecture rules
- Optimize token usage

### Step 4: Validate Compliance

Ensure component follows architecture requirements:
- Self-contained (no external file references)
- Uses relative path pattern
- Implements progressive disclosure
- Follows chosen skill pattern
- Meets quality standards

## Integration with Other Skills

### Plugin-Create Skill
When creating components, this skill provides:
- Architecture principles for templates
- Frontmatter standards
- Validation rules

### Plugin-Diagnose Skill
When analyzing components, this skill provides:
- Quality standards for validation
- Architecture rules for compliance checking
- Reference patterns for validation

### Plugin-Fix Skill
When fixing components, this skill provides:
- Architecture rules for fix guidance
- Reference patterns for corrections
- Compliance criteria

## Quick Reference Guide

### When to Load What

**Starting any work**:
```
Read references/core-principles.md
```

**Creating skill**:
```
Read references/skill-patterns.md
Read references/skill-design.md
```

**Creating command**:
```
Read references/command-design.md
```

**Understanding architecture**:
```
Read references/goal-based-organization.md
Read references/architecture-rules.md
```

**Optimizing performance**:
```
Read references/token-optimization.md
```

**Validating compliance**:
```
Read references/architecture-rules.md
Read references/reference-patterns.md
```

**Ensuring execution (not explanation)**:
```
Read references/execution-directive.md
```

**Creating scripts**:
```
Read references/script-standards.md
```

**Designing thin wrappers**:
```
Read references/minimal-wrapper-pattern.md
```

**Designing user output**:
```
Read references/user-facing-output.md
```

**Designing user interactions**:
```
Read references/askuserquestion-patterns.md
```

**Learning by example**:
```
Read references/examples/goal-based-skill-example.md
Read references/examples/workflow-command-example.md
```

## Key Principles Summary

### 1. Goal-Based Organization
Organize by user goals (CREATE, DIAGNOSE, FIX, MAINTAIN, LEARN), not component types.

### 2. Progressive Disclosure
Minimize upfront information, load details on-demand.

### 3. relative paths Pattern
Always use `relative paths` for resource paths - never hardcode paths.

### 4. Self-Containment
Skills contain all content within their directory structure.

### 5. Pattern-Driven Design
Choose from 10 patterns based on skill purpose and complexity.

### 6. Workflow-Focused
Skills provide workflows, not monolithic operations.

### 7. Thin Orchestrators
Commands parse parameters and route to skill workflows.

### 8. Token Optimization
Pre-load shared content, use batching, streamline output.

### 9. Quality Standards
Follow architecture rules, validate compliance.

### 10. Composition
Build complex capabilities from simple, focused skills.

## Quality Verification

Components using this skill should demonstrate:
- [ ] Self-contained (no external file references)
- [ ] relative path pattern used throughout
- [ ] Progressive disclosure implemented
- [ ] Appropriate skill pattern chosen
- [ ] Goal-based organization followed
- [ ] Architecture rules compliance
- [ ] Token optimization applied
- [ ] Quality standards met

## References

### Source Materials
- Claude Skills Deep Dive: https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- Claude Code Plugin Documentation: https://docs.claude.com/en/docs/claude-code/plugins

### Related Skills
- plan-marshall:ref-development-standards - Core development principles
- plan-marshall:ref-development-standards - Tool usage patterns
- pm-plugin-development:plugin-script-architecture - Python implementation, testing, output contracts

### Internal References (Load On-Demand)
All references are in `references/` directory:
- core-principles.md
- skill-patterns.md
- goal-based-organization.md
- architecture-rules.md
- skill-design.md
- command-design.md
- token-optimization.md
- reference-patterns.md
- frontmatter-standards.md
- script-standards.md
- execution-directive.md
- minimal-wrapper-pattern.md
- user-facing-output.md
- askuserquestion-patterns.md
- examples/goal-based-skill-example.md
- examples/workflow-command-example.md
- examples/pattern-usage-examples.md

---

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**File Operations:**
- `Read(relative paths/references/**)` - Read reference documentation

**Ensuring Non-Prompting:**
- All file reads use `relative paths/references/` which resolves to skill's mounted path
- Pure reference skill with no writes or executions
- Only the Read tool is used (no prompting scenarios)

---

*This is a Pattern 10 (Reference Library) skill - pure documentation with no execution logic. All content is loaded progressively based on current needs.*
