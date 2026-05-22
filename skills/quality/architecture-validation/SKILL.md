---
name: architecture-validation
description: Dynamically validate codebase compliance with architectural decisions and constraints
audience: architects
workflow: architecture-review
---
# Architecture Validation Skill

Dynamically validate that the implemented codebase matches the architectural decisions, design patterns, and system constraints documented in ANY plan files found in the `plans/` directory.

## Purpose

This skill provides a **generic, adaptive framework** for architecture validation that:
- **Discovers** all plan files in `plans/` directory
- **Extracts** architectural requirements, decisions, and constraints dynamically
- **Validates** implementation compliance without hardcoded assumptions
- **Reports** gaps, drift, and violations with actionable recommendations

**Key Principle**: Be architecture-agnostic. Work with ANY project structure and ANY set of plans.

## When to Use This Skill

Use this skill when:
- Validating that implementation matches planning documents
- Checking for architecture drift after development
- Ensuring design decisions are being followed
- Identifying missing or incomplete implementations
- Auditing compliance with documented constraints
- Preparing for architecture reviews
- Verifying refactoring didn't break architectural boundaries

## Validation Dimensions

The skill validates across multiple dimensions, **dynamically discovered from plan files**:

### 1. **Component/Module Structure**
- Planned crates, packages, modules exist
- Directory organization matches plans
- Component boundaries are maintained

### 2. **Dependency Architecture**
- Dependency rules are followed
- No circular dependencies
- Proper abstraction layers
- No unwanted dependencies

### 3. **Data Models**
- Structs, enums, types match plans
- Required fields present
- Schemas implemented correctly

### 4. **APIs and Interfaces**
- Public APIs match planned signatures
- Required functions exist
- Traits/interfaces implemented

### 5. **Performance Architecture**
- Benchmarks exist for targets
- Performance requirements documented
- Resource limits implemented

### 6. **Security Architecture**
- Security measures implemented
- Attack surfaces addressed
- Input validation present
- No hardcoded secrets

### 7. **Testing Strategy**
- Test types match plan
- Coverage requirements met
- Test infrastructure present

### 8. **Integration Patterns**
- External integrations match design
- Communication patterns correct
- Protocol implementations compliant

## Validation Workflow

### Phase 1: Plan Discovery
```bash
# Find all plan files
ls -1 plans/*.md

# Read plan index
cat plans/README.md
```

**Output**: List of all plan files to analyze

### Phase 2: Architecture Extraction
```bash
# Extract components/crates
grep -rh "crate|component|module" plans/ | sort -u

# Extract dependencies
grep -rh "depend|flow|import" plans/ | sort -u

# Extract performance targets
grep -rh "target|metric|<.*ms|P[0-9]" plans/ | sort -u

# Extract security requirements
grep -rh "security|threat|attack" plans/ -i | sort -u

# Extract data models
grep -rh "struct|enum|type|schema" plans/ | sort -u
```

**Output**: Structured list of architectural elements

### Phase 3: Codebase Analysis
```bash
# Analyze project structure
find . -name "Cargo.toml" -not -path "*/target/*"
tree -L 2 -I target

# Analyze dependencies
cargo tree --depth 1
cargo tree --duplicates

# Analyze code
rg "pub (async )?fn|pub struct|pub enum" --type rust
```

**Output**: Actual implementation state

### Phase 4: Compliance Validation
For each discovered architectural element:
1. Check if it exists in codebase
2. Validate it matches specification
3. Assess compliance level
4. Document findings

**Output**: Compliance matrix

### Phase 5: Gap Analysis
Identify:
- **Missing**: Planned but not implemented
- **Drift**: Implemented differently than planned
- **Extra**: Implemented but not documented

**Output**: Gap report with priorities

### Phase 6: Report Generation
Generate comprehensive report with:
- Executive summary
- Detailed findings per dimension
- Specific recommendations
- Action items with priorities

## Extraction Patterns

### Components/Crates
Look for:
- "crate", "component", "module", "package"
- Directory tree structures in code blocks
- Architecture diagrams
- Component lists

### Dependencies
Look for:
- "depends on", "imports", "requires"
- "must not depend", "should not import"
- "flow:", "→", "-->", "⇒"
- Dependency rules and constraints

### Performance
Look for:
- "target:", "metric:", "goal:"
- "<Xms", "P95", "P99", "latency", "throughput"
- Performance requirements tables
- Benchmark specifications

### Security
Look for:
- "security", "threat", "attack", "vulnerability"
- "sanitize", "validate", "authenticate"
- Security requirement lists
- Attack surface descriptions

### Data Models
Look for:
- "struct", "enum", "type", "interface"
- "table", "schema", "field", "column"
- Data model diagrams
- Type definitions

### APIs
Look for:
- "pub fn", "public function", "API"
- "endpoint", "method", "operation"
- Function signatures
- Interface definitions

## Compliance Levels

### ✅ Compliant
- Architectural element fully implemented as planned
- No deviations
- All requirements met

### ⚠️ Partial
- Element exists but incomplete
- Some requirements met, others missing
- Functional but not fully compliant

### ❌ Non-Compliant
- Element missing entirely
- Significant violations
- Major architectural drift

## Report Format

```markdown
# Architecture Validation Report
**Date**: [Date]
**Project**: [Name]
**Plans**: [List of plan files]

## Executive Summary
- Overall Compliance: X%
- Critical Issues: N
- Warnings: M
- Info: K

## Plans Analyzed
1. plans/00-overview.md - Project overview
2. plans/01-understand.md - Requirements
...

## Architectural Elements Discovered
[Dynamic list based on plan extraction]

### Components
- Component A: ✅ Implemented
- Component B: ⚠️ Partial
- Component C: ❌ Missing

### Dependencies
- Rule 1: ✅ Compliant
- Rule 2: ❌ Violated

### Performance
- Target 1 (<100ms): ⚠️ Untested
- Target 2 (>1000 ops/s): ✅ Met

### Security
- Requirement 1: ✅ Implemented
- Requirement 2: ⚠️ Partial

## Detailed Findings

### ✅ Fully Compliant
[List compliant aspects]

### ⚠️ Partial Compliance
[List partial implementations with details]

### ❌ Non-Compliant
[List violations with:
- Plan reference (file:line)
- Expected vs Actual
- Impact assessment
- Priority
- Recommended action]

## Architecture Drift
[List intentional or unintentional deviations]

## Recommendations
### High Priority
[Critical items]

### Medium Priority
[Important items]

### Low Priority
[Nice to have items]

## Next Steps
[Actionable next steps]
```

## Example Usage

### Scenario 1: Initial Validation
```bash
# After reading all plan files
# Extract 50+ architectural elements
# Validate against codebase
# Generate report: 75% compliance, 5 critical issues
```

### Scenario 2: Post-Refactoring
```bash
# Re-validate after major changes
# Check for new violations
# Verify planned improvements implemented
# Generate diff report
```

### Scenario 3: Architecture Review Prep
```bash
# Comprehensive validation
# Document all drift
# Prepare justifications
# Generate presentation-ready report
```

## Integration with Agent

This skill is used by the `architecture-validator` agent to:
1. Provide validation patterns and utilities
2. Define report formats
3. Establish compliance criteria
4. Guide systematic validation process

## Validation Commands

### Discovery
```bash
# Find all plans
ls -1 plans/*.md | wc -l

# Check plan structure
head -20 plans/README.md
```

### Extraction
```bash
# Extract all architectural keywords
for file in plans/*.md; do
  echo "=== $file ==="
  grep -i "decision:|requirement:|target:|constraint:" "$file"
done
```

### Analysis
```bash
# Compare planned vs actual
echo "Planned crates:" && grep -rh "crate" plans/ | wc -l
echo "Actual crates:" && find . -name "Cargo.toml" | wc -l
```

### Validation
```bash
# Check specific requirement
grep -r "requirement X" plans/
rg "implementation of X" --type rust
```

## Best Practices

1. **Start with README**: Read `plans/README.md` first to understand structure
2. **Read all plans**: Don't skip any plan files
3. **Extract systematically**: Use consistent patterns across all files
4. **Be specific**: Always reference exact file and line numbers
5. **Assess impact**: Explain why violations matter
6. **Provide solutions**: Give clear remediation steps
7. **Track evolution**: Compare current vs previous validations

## Edge Cases

- **No plans folder**: Report that validation cannot proceed
- **Empty plans**: Report insufficient documentation
- **Conflicting plans**: Flag conflicts for resolution
- **Outdated plans**: Note discrepancies and suggest updates
- **Ambiguous plans**: Request clarification
- **Multiple architectures**: Validate each separately

## Metrics

Track validation quality:
- **Plan Coverage**: % of plan files analyzed
- **Element Coverage**: % of architectural elements checked
- **Validation Depth**: How thoroughly each element validated
- **Finding Quality**: Specificity and actionability of findings
- **Report Completeness**: All sections filled out

## Self-Learning Framework

This skill enables **self-learning and continuous improvement** by learning from validation results.

### Learning Cycle

```
Validate → Identify Issues → Analyze Root Cause → Update Documentation → Re-validate
    ↑                                                                            ↓
    └────────────────────────── Feedback Loop ──────────────────────────────────┘
```

### Learning Triggers

**Trigger 1: Repeated Violations**
- Same violation appears 3+ times
- May indicate plan is outdated or unrealistic
- Action: Review and potentially update plan

**Trigger 2: False Positives**
- Validator reports violations for correct code
- Indicates validation logic needs refinement
- Action: Update agent/skill validation patterns

**Trigger 3: New Patterns Emerge**
- Implementation uses patterns not documented
- Patterns appear beneficial
- Action: Document new patterns in plans

**Trigger 4: Plan-Reality Mismatch**
- Consistent drift between plan and implementation
- Implementation is actually better
- Action: Update plan to reflect reality

### Self-Update Protocol

#### Phase 1: Detect Learning Opportunity
```bash
# After validation, analyze:
# - Number of violations by type
# - Pattern frequency
# - False positive rate
# - User feedback on findings

# If thresholds exceeded, trigger learning
```

#### Phase 2: Root Cause Analysis
```bash
# Determine root cause:
# - Is the plan outdated? → Update plan
# - Is validation incomplete? → Update agent/skill
# - Is implementation wrong? → Report to user
# - Is this a new valid pattern? → Document pattern
```

#### Phase 3: Update Documentation
```bash
# Update appropriate files:

# Option A: Update Plans
# - plans/00-overview.md: If project scope changed
# - plans/01-understand.md: If requirements changed
# - plans/02-plan.md: If architecture evolved
# - plans/03-execute.md: If implementation patterns changed
# - plans/04-review.md: If quality criteria changed
# - plans/05-secure.md: If security model changed
# - plans/06-feedback-loop.md: Document the learning

# Option B: Update Agent/Skill
# - .opencode/agent/architecture-validator.md: Update validation logic
# - .opencode/skills/architecture-validation.md: Update patterns

# Option C: Update Other OpenCode Files
# - Related skill files: If validation changes affect them
# - Agent coordination files: Update if dependencies change
```

#### Phase 4: Verification
```bash
# After updates:
# 1. Re-run validation
# 2. Confirm issue resolved
# 3. Check for new issues
# 4. Document learning
```

### Learning Examples

**Example 1: Outdated Dependency Rule**
```
Violation: "Core depends on storage implementation"
Frequency: 10 occurrences
Analysis: Dependency is intentional and beneficial
Learning: Rule too strict for current architecture
Action:
  1. Edit plans/02-plan.md: Update dependency rules
  2. Document rationale: "Direct dependency acceptable for X reason"
  3. Edit architecture-validator.md: Remove overly strict check
  4. Document in plans/06-feedback-loop.md
```

**Example 2: Missing Validation Pattern**
```
Issue: New async pattern not validated
Frequency: 5 instances found manually
Analysis: Validation extraction patterns incomplete
Learning: Need to check for async patterns
Action:
  1. Edit architecture-validator.md: Add async pattern checks
  2. Edit architecture-validation.md: Document async validation
  3. Re-run validation: Confirm new patterns detected
```

**Example 3: New Architecture Pattern**
```
Discovery: Code uses Circuit Breaker pattern
Status: Not documented in plans
Analysis: Pattern is beneficial, should be standard
Learning: Update plans to include pattern
Action:
  1. Edit plans/02-plan.md: Add Circuit Breaker section
  2. Edit plans/03-execute.md: Document implementation
  3. Edit architecture-validator.md: Validate circuit breakers
  4. Document in plans/06-feedback-loop.md
```

### Files to Update

**Plans (plans/)**:
- Update when architecture evolves
- Document new patterns
- Revise constraints
- Add learnings to 06-feedback-loop.md

**Agent (.opencode/agent/architecture-validator.md)**:
- Update validation logic
- Add new extraction patterns
- Refine reporting
- Document self-learning improvements

**Skill (.opencode/skills/architecture-validation.md)**:
- Update validation dimensions
- Add new patterns
- Refine workflows
- Document examples

**Other OpenCode Files (.opencode/)**:
- Related skills: Update if validation changes affect them
- Agent coordination files: Update if dependencies change

### Learning Metrics

Track learning effectiveness:
- **Learning Rate**: Updates per week
- **False Positive Reduction**: % decrease over time
- **Coverage Improvement**: New patterns detected
- **Plan Accuracy**: Plan-reality alignment
- **Validation Quality**: User satisfaction with findings

### Learning History Format

In `plans/06-feedback-loop.md`:
```markdown
## Architecture Validator Learnings

### [Date]: Dependency Rule Refinement
**Issue**: Core-Storage dependency flagged incorrectly
**Analysis**: Rule too strict, dependency is intentional
**Action**: Updated plans/02-plan.md lines 45-50
**Result**: False positives reduced from 10 to 0
**Status**: ✅ Verified

### [Date]: New Pattern Recognition
**Issue**: Circuit Breaker pattern not validated
**Analysis**: Pattern is widely used, should validate
**Action**: Updated architecture-validator.md, added extraction
**Result**: Now detects 5 instances of pattern
**Status**: ✅ Verified
```

### Continuous Improvement

**Weekly Review**:
- Review validation results
- Identify improvement opportunities
- Update documentation
- Refine validation logic

**Monthly Retrospective**:
- Assess learning metrics
- Major architecture changes
- Plan substantial updates
- Validate learning effectiveness

**Quarterly Audit**:
- Comprehensive review of plans
- Major agent/skill updates
- Architecture evolution assessment
- Long-term pattern analysis

## Updates and Versioning

**Version 2.0.0 Changes**:
- Made validation fully generic and plan-driven
- Removed hardcoded architectural assumptions
- Added dynamic element extraction
- Enhanced pattern matching capabilities
- Improved report generation
- Added comprehensive edge case handling
- **Added self-learning and adaptation framework**
- **Integrated feedback loop for continuous improvement**
- **Enabled automatic plan and agent updates**

## Related Skills

- `plan-gap-analysis`: Analyzes gaps between plans and implementation
- `rust-code-quality`: Validates Rust-specific code quality
- `code-reviewer`: Reviews code changes for quality
- `episode-complete`: For recording validation learnings in memory system
- `github-release-best-practices`: For release architecture validation and quality gates

## GitHub Release Integration

This skill provides architecture validation capabilities for release preparation workflows:

### Pre-Release Architecture Review
When preparing releases, use this skill to validate:
- **Architectural Consistency**: Ensure changes align with overall system design
- **Module Dependencies**: Verify new features don't break existing architectural patterns
- **Performance Impact**: Assess architectural implications of changes on system performance
- **Security Architecture**: Validate security considerations in release changes

### Release Quality Gates
Integrate architecture validation into release workflows:
1. **Pre-Implementation**: Baseline architecture assessment
2. **During Development**: Ongoing architecture compliance checks
3. **Pre-Release**: Comprehensive architecture validation
4. **Post-Release**: Architecture impact assessment

### Coordination with Release Best Practices
- **github-release-best-practices**: Incorporates architecture validation in quality gates
- **goap-agent**: Uses architecture validation for complex release planning
- **code-reviewer**: Combines code quality with architectural compliance assessment

This integration ensures releases maintain architectural integrity while following 2025 GitHub release best practices.

## Resources

- Agent: `.opencode/agent/architecture-validator.md`
- Plans: `plans/*.md`
- Project guidelines: `AGENTS.md`
- Learning history: `plans/06-feedback-loop.md`