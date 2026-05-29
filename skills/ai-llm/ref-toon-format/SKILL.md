---
name: ref-toon-format
description: TOON format knowledge and usage patterns for agent communication and memory persistence in plan-marshall marketplace
user-invocable: false
allowed-tools: Read
---

# TOON Format Usage Skill

**REFERENCE MODE**: This skill provides TOON format reference material. Load specific references on-demand based on current task.

Pure reference skill providing TOON (Token-Oriented Object Notation) format specification and usage patterns for agent handoffs and memory persistence.

## What This Skill Provides

**TOON Specification**: Complete technical reference for TOON format syntax, semantics, and conversion patterns.

**Agent Patterns**: Usage patterns for agent handoffs, memory persistence, and inter-agent data exchange.

**Token Efficiency**: Guidance on when and how to use TOON for 30-60% token reduction.

## Pattern Type

**Pattern 10: Reference Library** - Pure reference skill with no execution logic. Load references on-demand based on current task.

## When to Use This Skill

Activate when:
- **Creating agent handoffs** - Need TOON format for inter-agent communication
- **Designing memory persistence** - Need structured data storage in memory layer
- **Converting JSON to TOON** - Need conversion examples and patterns
- **Optimizing token usage** - Need token-efficient data representation
- **Understanding TOON syntax** - Need technical reference for TOON format

## Core Concepts

### TOON Format Overview

TOON (Token-Oriented Object Notation) is a compact, human-readable encoding of the JSON data model that minimizes tokens.

**Key Features**:
- **30-60% token reduction** vs JSON for uniform arrays
- **Declared structure once**: Field headers defined upfront, not repeated
- **Tabular data**: CSV-style rows for uniform arrays
- **Explicit clarity**: `[N]` length and `{fields}` headers improve LLM parsing

**Best For**:
- Agent handoffs with uniform issue lists
- Coverage reports with tabular data
- Build failures with repeated structure
- Memory persistence with structured session data

**NOT For**:
- API interchange (use JSON)
- Configuration files (use YAML/JSON)
- Deeply nested structures (>3 levels)
- Non-uniform object shapes

### Agent Communication Scope

**TOON is ONLY for internal plan-marshall marketplace operations**:
- Agent-to-agent handoffs
- Memory persistence (memory layer)
- Inter-agent data exchange
- Test fixtures for agent workflows

**NOT for**:
- Application code or APIs
- General LLM integration
- External data interchange

## Available References

Load references progressively based on current task. **Never load all references at once.**

### 1. TOON Specification (Technical Reference)
**File**: `knowledge/toon-specification.md`

**Load When**:
- Learning TOON syntax and semantics
- Understanding conversion patterns
- Validating TOON structure
- Comparing with JSON/CSV/YAML

**Contents**:
- Core syntax (primitives, objects, arrays)
- Uniform arrays (TOON's sweet spot)
- Nested structures and mixing
- Advanced features (optional fields, escaping)
- Conversion examples (Sonar issues, coverage)
- Internal `toon_parser.py` module usage
- Best practices and optimization tips
- Performance characteristics and trade-offs

**Load Command**:
```
Read knowledge/toon-specification.md
```

### 2. Agent Patterns (Usage Patterns)
**File**: `knowledge/agent-patterns.md`

**Load When**:
- Creating agent handoff templates
- Designing memory persistence
- Converting JSON fixtures to TOON
- Understanding agent prompt patterns

**Contents**:
- Handoff template examples (minimal, standard, full)
- Memory persistence patterns
- Agent prompt patterns (receiving/generating TOON)
- Test fixture examples
- Token impact measurements
- Migration guidance

**Load Command**:
```
Read knowledge/agent-patterns.md
```

## Usage Workflow

### Step 1: Identify Your Goal

Determine what you're trying to accomplish:
- **Learning TOON syntax** → Load toon-specification.md
- **Creating agent handoff** → Load agent-patterns.md
- **Converting JSON to TOON** → Load both references
- **Understanding token savings** → Load toon-specification.md (performance section)

### Step 2: Load Relevant References

**Never load all references** - Load only what's needed for current task.

**Example**:
```
# Creating agent handoff
Read knowledge/agent-patterns.md

# Understanding TOON syntax
Read knowledge/toon-specification.md
```

### Step 3: Apply Patterns

Follow the guidance in loaded references:
- Use TOON for uniform array structures
- Follow tabular data format for repeated objects
- Include `[N]` length declarations
- Declare `{field1,field2}` headers explicitly
- Use proper CSV escaping for special characters

### Step 4: Validate Syntax

Ensure TOON follows format requirements:
- Length declaration matches row count
- Field count matches header declaration
- CSV escaping for commas in values
- Consistent indentation for nesting

## Quick Reference Guide

### When to Load What

**Learning TOON format**:
```
Read knowledge/toon-specification.md
```

**Creating agent handoffs**:
```
Read knowledge/agent-patterns.md
```

**Converting JSON to TOON**:
```
Read knowledge/toon-specification.md
Read knowledge/agent-patterns.md
```

### TOON Quick Syntax

**Uniform Array**:
```toon
issues[2]{file,line,severity}:
Example.java,42,BLOCKER
Service.java,89,MAJOR
```

**Nested Object**:
```toon
context:
  task: Fix issues
  files_analyzed: 15
```

**Mixed Structure**:
```toon
from_agent: quality
to_agent: fix

context:
  task: Fix code quality

issues[2]{file,line,severity}:
A.java,42,HIGH
B.java,89,MEDIUM
```

## Integration with Marketplace

### Agent Handoffs

**Purpose**: Token-efficient data exchange between agents in workflow chains.

**Example Workflows**:
- Quality → Implement → Test → Verify
- Sonar → Triage → Fix
- Coverage → Analysis → Report

**Token Savings**: 480 tokens (60%) for 4-agent chain vs JSON.

### Memory Persistence

**Purpose**: Structured session data storage in memory layer.

**Use Cases**:
- Task history tracking
- Incremental state management
- Multi-session context

### Test Fixtures

**Purpose**: Token-efficient test data for agent workflow tests.

**Examples**:
- sonar-issues.toon
- coverage-analysis.toon
- build-failure.toon

## Key Principles Summary

### 1. Token Efficiency
TOON provides 30-60% token reduction for uniform arrays vs JSON.

### 2. Structural Clarity
Explicit `[N]` and `{fields}` declarations improve LLM parsing accuracy.

### 3. Internal Use Only
TOON is for plan-marshall marketplace internal operations, not external APIs.

### 4. Progressive Loading
Load toon-specification.md and agent-patterns.md on-demand, not upfront.

### 5. Pattern-Driven Usage
Follow established patterns for handoffs, memory, and fixtures.

## Quality Verification

Components using this skill should demonstrate:
- [ ] TOON used for uniform array structures
- [ ] Length declarations `[N]` match actual row counts
- [ ] Field headers `{field1,field2}` match all rows
- [ ] CSV escaping for values with commas
- [ ] Proper indentation for nesting
- [ ] 30%+ token reduction vs equivalent JSON

## Resources

### External References
- TOON Specification: https://github.com/toon-format/spec
- TOON Main Repository: https://github.com/toon-format/toon
- TOON Playground: https://toon-format.github.io/playground
- Original Analysis: https://devtoolhub.com/toon-vs-json-token-efficient-ai-format/

### Related Skills
- pm-workflow:workflow-patterns - Agent handoff workflow patterns
- plan-marshall:manage-memories - Memory layer operations

### Internal References (Load On-Demand)
All references are in `knowledge/` directory:
- toon-specification.md - Complete TOON format technical reference
- agent-patterns.md - Agent handoff and memory patterns

---

## Non-Prompting Requirements

This skill is designed to run without user prompts. Required permissions:

**File Operations:**
- `Read(knowledge/**)` - Read reference documentation

**Ensuring Non-Prompting:**
- All file reads use `knowledge/` which resolves to skill's mounted path
- Pure reference skill with no writes or executions
- Only the Read tool is used (no prompting scenarios)

---

*This is a Pattern 10 (Reference Library) skill - pure documentation with no execution logic. All content is loaded progressively based on current needs.*
