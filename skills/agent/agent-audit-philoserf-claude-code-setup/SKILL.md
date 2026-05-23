---
name: agent-audit
description: Validates agent configurations for model selection, tool permissions, focus areas, and approach quality. Use when reviewing, auditing, improving agents, or learning agent best practices.
allowed-tools: [Read, Grep, Glob, Bash]
# model: inherit
---

## Reference Files

Advanced agent validation guidance:

- [model-selection.md](model-selection.md) - Model choice decision matrix, use cases, and appropriateness criteria
- [tool-restrictions.md](tool-restrictions.md) - Tool permission patterns, security implications, and restriction fit
- [focus-area-quality.md](focus-area-quality.md) - Focus area specificity assessment, quality scoring, and criteria
- [approach-methodology.md](approach-methodology.md) - Approach completeness, required components, and methodology patterns
- [resource-organization.md](resource-organization.md) - Resource directory validation and progressive disclosure
- [examples.md](examples.md) - Good vs poor agent comparisons and full audit reports
- [report-format.md](report-format.md) - Standardized audit report template and structure
- [common-issues.md](common-issues.md) - Frequent problems, fixes, and troubleshooting patterns

---

# Agent Auditor

Validates agent configurations for model selection, tool restrictions, focus areas, and approach methodology.

## Quick Start

**Basic audit workflow**:

1. Read agent file
2. Check model selection appropriateness
3. Validate tool restrictions
4. Assess focus area quality
5. Review approach methodology
6. Generate audit report

**Example usage**:

```text
User: "Audit my evaluator skill"
→ Reads skills/evaluator/SKILL.md
→ Validates model (Sonnet), tools, focus areas, approach
→ Generates report with findings and recommendations
```

## Agent Audit Checklist

### Critical Issues

Must be fixed for agent to function correctly:

- [ ] **Valid YAML frontmatter** - Proper syntax, required fields present
- [ ] **name field matches filename** - Name consistency
- [ ] **model field present and valid** - Sonnet, Haiku, or Opus only
- [ ] **At least 3 focus areas** - Minimum viable expertise definition
- [ ] **Tool restrictions present** - allowed_tools or allowed-patterns specified
- [ ] **No security vulnerabilities** - Tools don't expose dangerous capabilities

### Important Issues

Should be fixed for optimal agent performance:

- [ ] **Model matches complexity** - Haiku for simple, Sonnet default, Opus rare
- [ ] **5-15 focus areas** - Not too few (vague) or too many (unfocused)
- [ ] **Focus areas specific** - Concrete, not generic statements
- [ ] **Tools match usage** - No missing or excessive permissions
- [ ] **Approach section complete** - Methodology defined, output format specified
- [ ] **File size reasonable** - <500 lines or uses progressive disclosure

### Nice-to-Have Improvements

Polish for excellent agent quality:

- [ ] **Model choice justified** - Clear reason for non-default model
- [ ] **Focus areas have examples** - Technology/framework specificity
- [ ] **Approach has decision frameworks** - If/then logic for complex tasks
- [ ] **Tool restrictions documented** - Why specific tools are allowed/restricted
- [ ] **Resource organization** - Uses references/ when needed, proper structure
- [ ] **Context economy** - Concise without sacrificing clarity

## Audit Workflow

### Step 1: Read Agent File

Identify the agent file to audit:

```bash
# Single agent
Read skills/evaluator/SKILL.md

# Find all agents
Glob agents/*.md
```

### Step 2: Validate Model Selection

**Check model field**:

```yaml
model: sonnet  # Good - default choice
model: haiku   # Check: Is agent simple enough?
model: opus    # Check: Is complexity justified?
```

**Decision criteria**:

- **Haiku** (`haiku`): Simple read-only analysis, fast response needed, low cost priority
- **Sonnet** (`sonnet`): Default for most agents, balanced cost/capability
- **Opus** (`opus`): Complex reasoning required, highest capability needed

**Common issues**:

- Opus overuse: Using expensive model when Sonnet sufficient
- Haiku underperformance: Too simple for task complexity
- Missing model: No model field specified (defaults to Sonnet)

See [model-selection.md](model-selection.md) for detailed decision matrix.

### Step 3: Validate Tool Restrictions

**Check allowed_tools or allowed-patterns**:

```yaml
allowed_tools:
  - Read
  - Grep
  - Glob
  - Bash
```

**Validation checklist**:

1. **Tools specified**: Has allowed_tools field (not unrestricted)
2. **Tools match usage**: All mentioned tools are allowed
3. **No missing tools**: All needed tools are included
4. **No excessive tools**: No unnecessary permissions
5. **Security implications**: No dangerous tool combinations

**Common patterns**:

- **Read-only analyzer**: [Read, Grep, Glob, Bash (read commands)]
- **Code generator**: [Read, Write, Edit, Grep, Glob, Bash]
- **Orchestrator**: [Task, Skill, Read, AskUserQuestion]

See [tool-restrictions.md](tool-restrictions.md) for security analysis.

### Step 4: Assess Focus Area Quality

**Target**: 5-15 focus areas that are specific, concrete, and comprehensive

**Quality criteria**:

**Specific vs Generic**:

- ✗ Generic: "Python programming"
- ✓ Specific: "FastAPI REST APIs with SQLAlchemy ORM"

**Concrete vs Vague**:

- ✗ Vague: "Best practices"
- ✓ Concrete: "Defensive programming with strict error handling"

**Coverage**:

- Too few (<5): Expertise unclear or overly narrow
- Sweet spot (5-15): Comprehensive, focused expertise
- Too many (>15): Unfocused, trying to do everything

**Example analysis**:

```markdown
## Focus Areas

- Defensive programming with strict error handling ✓
- POSIX compliance and cross-platform portability ✓
- Safe argument parsing and input validation ✓
- Robust file operations and temporary resource management ✓
- Production-grade logging and error reporting ✓
```

**Score**: 5/5 areas, all specific and concrete → GOOD

See [focus-area-quality.md](focus-area-quality.md) for scoring methodology.

### Step 5: Review Approach Methodology

**Check approach section completeness**:

Required elements:

- [ ] **Methodology defined** - Step-by-step process
- [ ] **Decision frameworks** - How to handle different scenarios
- [ ] **Output format** - What the agent produces
- [ ] **Integration with focus** - How approach uses expertise

**Example complete approach**:

```markdown
## Approach

1. Analyze requirements and constraints
2. Design solution using defensive programming principles
3. Implement with POSIX compliance
4. Add comprehensive error handling
5. Test on multiple platforms
6. Document with inline comments

Output: Production-ready Bash script with full error handling
```

**Incomplete approach** (missing steps, no output format):

```markdown
## Approach

Write good Bash scripts following best practices.
```

See [approach-methodology.md](approach-methodology.md) for templates.

### Step 6: Validate Resource Organization

**Check for progressive disclosure**:

**Single file agents**:

1. Count lines in agent file
2. If <500 lines: No references needed, mark as N/A
3. If >500 lines: Should use references/, flag for refactoring

**Directory-based agents**:

1. Check for references/ subdirectory
2. Count files in references/
3. Verify all references linked from main file
4. Check for orphaned files
5. Verify flat structure (no nested directories)

**Targets**:

- **Main file**: <500 lines (300-400 ideal)
- **References**: 2-6 focused files in references/ directory
- **Navigation**: Clear "Reference Files" section with descriptive links
- **Structure**: Flat (no subdirectories within references/)

**Scoring**:

- EXCELLENT (9-10): Well-organized with clear navigation
- GOOD (7-8): Reasonable organization, minor issues
- NEEDS IMPROVEMENT (4-6): Size issues or poor organization
- POOR (1-3): >800 lines single file or bad structure
- N/A: Simple agent <300 lines, no references needed

See [resource-organization.md](resource-organization.md) for detailed validation criteria.

### Step 7: Check Context Economy

**File size assessment**:

```bash
# Count lines
wc -l skills/evaluator/SKILL.md
```

**Targets**:

- **<300 lines**: Excellent - concise and focused
- **300-500 lines**: Good - comprehensive without bloat
- **500-800 lines**: Consider progressive disclosure
- **>800 lines**: Should use references/ directory

**If oversized**:

1. Extract detailed content to references/ files
2. Keep main file focused on core workflow
3. Link to references from main file
4. Maintain one-level-deep structure

### Step 8: Generate Audit Report

Compile findings into standardized report format. See [report-format.md](report-format.md) for the complete template.

## Agent-Specific Validation

For detailed validation criteria in each area, see the reference files:

- **Model Selection**: See [model-selection.md](model-selection.md) for appropriateness criteria, use cases, and red flags
- **Tool Restrictions**: See [tool-restrictions.md](tool-restrictions.md) for security implications and restriction fit analysis
- **Focus Area Quality**: See [focus-area-quality.md](focus-area-quality.md) for specificity assessment and scoring methodology
- **Approach Completeness**: See [approach-methodology.md](approach-methodology.md) for required components and impact analysis
- **Resource Organization**: See [resource-organization.md](resource-organization.md) for progressive disclosure patterns and validation

## Common Issues

For detailed troubleshooting guidance, see [common-issues.md](common-issues.md).

Common patterns include:

- **Opus overuse**: Expensive model for simple tasks
- **Generic focus areas**: Lack of specificity and concrete examples
- **Missing tool restrictions**: Unrestricted access creates security risks
- **Overly restrictive tools**: Missing tools the agent needs
- **Incomplete approach**: Vague methodology without clear steps

## Report Format

Use the standardized template in [report-format.md](report-format.md) for all agent audit reports.

## Integration with audit-coordinator

**Invocation pattern**:

```text
User: "Audit my agent"
→ audit-coordinator invokes audit-agent
→ audit-agent performs specialized validation
→ Results returned to audit-coordinator
→ Consolidated with evaluator findings
```

**Sequence**:

1. audit-agent (primary) - Agent-specific validation
2. evaluator (secondary) - General structure validation
3. test-runner (optional) - Functional testing

**Report compilation**:

- audit-agent findings (model, tools, focus, approach)
- evaluator findings (YAML, markdown, structure)
- Unified report with reconciled priorities

## Related Audit Skills

This skill is part of the audit skill family:

- **audit-agent** (this skill) - Validates agent configurations
- **audit-skill** - Validates skill configurations
- **audit-command** - Validates command configurations
- **audit-hook** - Validates hook configurations
- **audit-output-style** - Validates output-style configurations
- **audit-coordinator** - Orchestrates multi-faceted audits

For comprehensive audits, use audit-coordinator which will invoke the appropriate specialists.

## Examples

### Example 1: Good Agent (evaluator)

**Status**: PASS

**Strengths**:

- Model: Sonnet (appropriate for analysis tasks)
- Tools: Read, Grep, Glob, Bash (read-only pattern, secure)
- Focus: 12 specific areas covering evaluation expertise
- Approach: Complete methodology with output format

**Score**: 9/10 - Excellent agent design

### Example 2: Agent Needs Work

**Status**: NEEDS WORK

**Issues**:

- Model: Opus (expensive, Sonnet sufficient for task)
- Tools: No allowed_tools (unrestricted access)
- Focus: 3 generic areas ("best practices", "code quality")
- Approach: Missing (no methodology defined)

**Critical fixes**:

1. Add allowed_tools field
2. Change model to Sonnet
3. Expand focus areas to 5-10 specific items
4. Add complete approach section

**Score**: 4/10 - Requires significant improvement

See [examples.md](examples.md) for complete audit reports.

---

For detailed guidance on each validation area, consult the reference files linked at the top of this document.
