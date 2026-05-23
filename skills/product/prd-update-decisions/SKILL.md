---
name: prd-update-decisions
description: Update PRD based on design decisions and strategic changes made during conversations
category: project-management
---

# PRD Update Decisions Slash Command

## Instructions

You are updating a PRD based on design decisions, strategic changes, and architectural choices made during conversations. This command captures conceptual changes that may not yet be reflected in code but affect requirements, approach, or scope.

## Process Overview

1. **Identify Target PRD** - Determine which PRD to update
2. **Analyze Conversation Context** - Review discussions for design decisions and strategic changes
3. **Identify Decision Points** - Find architecture, workflow, requirement, or scope changes
4. **Map to PRD Sections** - Determine which parts of the PRD need updates
5. **Propose Updates** - Suggest changes to requirements, approaches, and constraints
6. **Update Decision Log** - Record new decisions with rationale and impact

## Step 1: PRD Analysis

Ask the user which PRD to update, then:
- Read the PRD file from `prds/[issue-id]-[feature-name].md`
- Understand current requirements, approach, and constraints
- Identify areas most likely to be affected by design decisions

## Step 2: Conversation Analysis

Review the conversation context for decision-making patterns:

### Design Decision Indicators
Look for conversation elements that suggest strategic changes:
- **Workflow changes**: "Let's simplify this to..." "What if we instead..."
- **Architecture decisions**: "I think we should use..." "The better approach would be..."
- **Requirement modifications**: "Actually, we don't need..." "We should also include..."
- **Scope adjustments**: "Let's defer this..." "This is more complex than we thought..."
- **User experience pivots**: "Users would prefer..." "This workflow makes more sense..."

### Specific Decision Types
- **Technical Architecture**: Framework choices, design patterns, data structures
- **User Experience**: Workflow changes, interface decisions, interaction models
- **Requirements**: New requirements, modified requirements, removed requirements
- **Scope Management**: Features added, deferred, or eliminated
- **Implementation Strategy**: Phasing changes, priority adjustments, approach modifications

## Step 3: Decision Impact Assessment

For each identified decision, assess:

### Impact Categories
- **Requirements Impact**: What requirements need to be added, modified, or removed?
- **Scope Impact**: Does this expand or contract the project scope?
- **Timeline Impact**: Does this affect project phases or delivery dates?
- **Architecture Impact**: Does this change technical constraints or approaches?
- **Code Example Impact**: Which examples, interfaces, or snippets become outdated?
- **Risk Impact**: Does this introduce new risks or mitigate existing ones?

### Decision Documentation Format
For each decision, record:
- **Decision**: What was decided
- **Date**: When the decision was made
- **Rationale**: Why this approach was chosen
- **Impact**: How this affects the PRD requirements, scope, or approach
- **Code Impact**: Which code examples, interfaces, or snippets need updating
- **Owner**: Who made or approved the decision

## Step 4: PRD Updates

Update the appropriate PRD sections:

### Decision Log Updates
- Add new resolved decisions with date and rationale
- Mark open questions as resolved if decisions were made
- Update decision impact on requirements and scope

### Requirements Updates
- Modify functional requirements based on design changes
- Update non-functional requirements if performance/quality criteria changed
- Adjust success criteria if measurements or targets changed

### Implementation Approach Updates
- Update phases if sequencing or priorities changed
- Modify architecture decisions if technical approach evolved
- Adjust scope management if features were added, deferred, or removed

### Code Example Validation and Updates
- **Identify Outdated Examples**: Scan PRD for code snippets that may be affected by design decisions
- **Interface Changes**: Update examples when function signatures, parameter types, or return values change
- **API Modifications**: Revise examples when method names, class structures, or data formats evolve
- **Workflow Updates**: Update process examples when user interaction patterns or step sequences change
- **Mark for Verification**: Flag code examples that need manual testing to ensure they still work

### Risk and Dependency Updates
- Add new risks introduced by design decisions
- Update mitigation strategies if approach changed
- Modify dependencies if architectural changes affect integrations