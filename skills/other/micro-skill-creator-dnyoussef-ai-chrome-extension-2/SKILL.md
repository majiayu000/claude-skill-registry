---
name: micro-skill-creator
description: Rapidly creates atomic, focused skills optimized with evidence-based prompting, specialist agents, and systematic testing. Each micro-skill does one thing exceptionally well using self-consistency, program-of-thought, and plan-and-solve patterns. Enhanced with agent-creator principles and functionality-audit validation. Perfect for building composable workflow components.
tags: [skill-creation, atomic, modular, evidence-based, specialist-agents, tier-1]
version: 2.0.0
---

# Micro-Skill Creator (Enhanced)

## Overview
Creates small, focused skills that each spawn a specialist agent optimized for a specific task using evidence-based prompting techniques. This enhanced version integrates agent-creator principles, prompt-architect patterns, and systematic testing from functionality-audit.

## Philosophy: Atomic Excellence

**Unix Philosophy for AI**: Do one thing and do it well, with clean interfaces for composition.

**Evidence-Based Agents**: Every micro-skill spawns a specialist agent using research-validated techniques:
- **Self-consistency** for factual tasks
- **Program-of-thought** for analytical tasks
- **Plan-and-solve** for complex tasks
- **Neural training** integration for continuous improvement

**Key Principles**:
1. Single responsibility per skill
2. Specialist agent per domain
3. Clean input/output contracts
4. Systematic validation
5. Composability first

## When to Create Micro-Skills

✅ **Perfect For**:
- Tasks you perform repeatedly
- Operations needing specialist expertise
- Building blocks for cascades
- Capabilities for slash commands
- Domain-specific workflows

❌ **Don't Use For**:
- One-off exploratory tasks
- Tasks too simple for specialization
- Better handled by external tools

## Enhanced Creation Workflow

### Step 1: Define Single Responsibility

State in ONE sentence what this skill does:
- "Extract structured data from unstructured documents"
- "Validate API responses against OpenAPI schemas"
- "Refactor code to use dependency injection patterns"

**Trigger Pattern**: Define keywords for Claude Code discovery.

### Step 2: Design Specialist Agent (Enhanced)

Using **agent-creator** + **prompt-architect** principles:

#### A. Identity & Expertise
```markdown
I am a [domain] specialist with expertise in:
- [Core competency 1]
- [Core competency 2]
- [Edge case handling]
- [Output quality standards]
```

#### B. Evidence-Based Methodology

**For Factual Tasks (Self-Consistency)**:
```markdown
Methodology:
1. Extract information from multiple perspectives
2. Cross-reference findings for consistency
3. Flag any inconsistencies or ambiguities
4. Provide confidence scores
5. Return validated results
```

**For Analytical Tasks (Program-of-Thought)**:
```markdown
Methodology:
1. Decompose problem into logical components
2. Work through each component systematically
3. Show intermediate reasoning
4. Validate logical consistency
5. Synthesize final analysis
```

**For Complex Tasks (Plan-and-Solve)**:
```markdown
Methodology:
1. Create comprehensive plan with dependencies
2. Break into executable steps
3. Execute plan systematically
4. Validate completion at each step
5. Return complete solution
```

#### C. Output Specification
Precise format enables reliable composition:
```yaml
output:
  format: json | markdown | code
  structure:
    required_fields: [...]
    optional_fields: [...]
  validation_rules: [...]
  quality_standards: [...]
```

#### D. Failure Mode Awareness
```markdown
Common Failure Modes & Mitigations:
- [Failure type 1]: [How to detect and handle]
- [Failure type 2]: [How to detect and handle]
```

### Step 3: Create Skill Structure

**SKILL.md Template**:
```markdown
---
name: skill-name
description: [Specific trigger description]
tags: [domain, task-type, evidence-technique]
version: 1.0.0
---

# Skill Name

## Purpose
[Clear, single-sentence purpose]

## Specialist Agent
[Agent system prompt using evidence-based patterns]

## Input Contract
[Explicit input requirements]

## Output Contract
[Explicit output format and validation]

## Integration Points
- Cascades: [How it composes]
- Commands: [Slash command bindings]
- Other Skills: [Dependencies or companions]
```

### Step 4: Add Validation & Testing

**Systematic Testing** (from functionality-audit):
```markdown
Test Cases:
1. Normal operation with typical inputs
2. Boundary conditions
3. Error cases with invalid inputs
4. Edge cases
5. Performance stress tests
```

**Validation Checklist**:
- [ ] Skill triggers correctly
- [ ] Agent executes with domain expertise
- [ ] Output matches specifications
- [ ] Errors handled gracefully
- [ ] Composes with other skills
- [ ] Performance acceptable

### Step 5: Neural Training Integration

**Enable Learning** (from ruv-swarm):
```yaml
training:
  pattern: [cognitive pattern type]
  feedback_collection: true
  improvement_iteration: true
  success_tracking: true
```

## Micro-Skill Templates (Enhanced)

### 1. Data Extraction Micro-Skill

**Agent System Prompt**:
```markdown
I am an extraction specialist using self-consistency checking for accuracy.

Methodology (Self-Consistency Pattern):
1. Scan source from multiple angles
2. Extract candidate information
3. Cross-validate findings
4. Flag confidence levels and ambiguities
5. Return structured data with metadata

Failure Modes:
- Ambiguous source: Flag for human review
- Missing information: Explicitly note gaps
- Low confidence: Provide alternative interpretations
```

**Input/Output**:
```yaml
input:
  source_document: string | file_path
  target_schema: json_schema
  confidence_threshold: number (default: 0.8)

output:
  extracted_data: object (matches target_schema)
  confidence_scores: object (per field)
  ambiguities: array[string]
  metadata:
    extraction_quality: high | medium | low
    processing_time: number
```

### 2. Validation Micro-Skill

**Agent System Prompt**:
```markdown
I am a validation specialist using program-of-thought decomposition.

Methodology (Program-of-Thought Pattern):
1. Parse input systematically
2. Load specification/rules
3. Check each rule with clear reasoning
4. Show validation logic step-by-step
5. Categorize violations by severity

Failure Modes:
- Ambiguous rules: Request clarification
- Conflicting rules: Flag inconsistencies
- Edge cases: Apply conservative interpretation
```

**Input/Output**:
```yaml
input:
  data: object | array
  specification: schema | rules_file
  strictness: lenient | normal | strict

output:
  validation_result:
    status: pass | fail | warning
    violations: array[{rule, location, severity, message}]
    summary: {errors: number, warnings: number}
  suggested_fixes: array[{location, fix, confidence}]
```

### 3. Generation Micro-Skill

**Agent System Prompt**:
```markdown
I am a generation specialist using plan-and-solve framework.

Methodology (Plan-and-Solve Pattern):
1. Parse specification and understand requirements
2. Create comprehensive generation plan
3. Execute plan systematically
4. Validate output against requirements
5. Review for completeness and correctness

Failure Modes:
- Incomplete specification: Request missing details
- Ambiguous requirements: Provide multiple options
- Validation failures: Iterate with fixes
```

**Input/Output**:
```yaml
input:
  specification: object | markdown
  templates: array[template] (optional)
  config: object (generation parameters)

output:
  generated_artifact: string | object
  generation_metadata:
    decisions_made: array[{decision, rationale}]
    completeness_check: pass | partial | fail
    warnings: array[string]
```

### 4. Analysis Micro-Skill

**Agent System Prompt**:
```markdown
I am an analysis specialist combining program-of-thought and self-consistency.

Methodology:
1. Gather data systematically
2. Apply analytical framework (program-of-thought)
3. Identify patterns and anomalies
4. Validate conclusions (self-consistency)
5. Prioritize findings by importance

Failure Modes:
- Insufficient data: Flag and request more
- Conflicting indicators: Present both interpretations
- Uncertain conclusions: Provide confidence levels
```

**Input/Output**:
```yaml
input:
  data: object | array | file_path
  analysis_type: quality | security | performance | etc
  depth: shallow | normal | deep

output:
  analysis_report:
    key_findings: array[{finding, evidence, severity}]
    recommendations: array[{action, priority, rationale}]
    confidence_levels: object (per finding)
    supporting_data: object
```

## Integration with Cascade Workflows

**Composition Patterns**:
```yaml
# Sequential
extract-data → validate-data → transform-data → generate-report

# Parallel
input → [validate-schema + security-scan + quality-check] → merge-results

# Conditional
validate → (if pass: deploy) OR (if fail: generate-error-report)

# Map-Reduce
collection → map(analyze-item) → reduce(aggregate-results)

# Iterative
refactor → check-quality → (repeat if below threshold)
```

## Integration with Slash Commands

**Command Binding Example**:
```yaml
command:
  name: /validate-api
  binding:
    type: micro-skill
    target: validate-api-response
    parameter_mapping:
      file: ${file_path}
      schema: ${schema_path}
      strict: ${--strict flag}
```

## Best Practices (Enhanced)

### Skill Design
1. ✅ Truly atomic - one responsibility
2. ✅ Evidence-based agent methodology
3. ✅ Explicit input/output contracts
4. ✅ Comprehensive error handling
5. ✅ Systematic validation testing
6. ✅ Neural training enabled

### Agent Optimization
1. ✅ Use appropriate evidence technique
2. ✅ Include failure mode awareness
3. ✅ Specify exact output formats
4. ✅ Add self-validation steps
5. ✅ Enable continuous learning

### Composition
1. ✅ Clean interfaces for chaining
2. ✅ Standardized error formats
3. ✅ Idempotent when possible
4. ✅ Version interfaces carefully
5. ✅ Document dependencies

## Working with Micro-Skill Creator

**Invocation**:
"Create a micro-skill that [single responsibility] using [evidence technique] with [domain expertise]"

**The creator will**:
1. Guide you through agent design with evidence-based patterns
2. Generate skill structure with proper contracts
3. Create validation test cases
4. Set up neural training integration
5. Produce production-ready micro-skill

**Integration**:
- Works with **agent-creator** for agent design
- Works with **cascade-orchestrator** for workflow composition
- Works with **slash-command-encoder** for /command access
- Works with **functionality-audit** for validation
- Works with **ruv-swarm MCP** for neural training

---

**Version 2.0 Enhancements**:
- Evidence-based prompting patterns
- Systematic validation testing
- Neural training integration
- Enhanced agent design methodology
- Improved composition interfaces
