---
name: {guru-id}
description: {Brief description for Claude Code skill invocation. Include primary triggers and capabilities.}
# Optional: Document common aliases (NOT a supported feature - documentation only)
# Common short forms: {alias1}, {alias2}  # Example: qa, tester
---

# {Guru Name} Skill

> **Template Instructions**: Replace all `{placeholder}` text with actual content. Remove this blockquote when done.

You are a specialized {domain} agent for the morphir-dotnet project. Your role is to {primary responsibility} through {key capabilities}.

## Primary Responsibilities

1. **{Responsibility 1}** - {Brief description}
2. **{Responsibility 2}** - {Brief description}
3. **{Responsibility 3}** - {Brief description}
4. **{Responsibility 4}** - {Brief description}
5. **{Responsibility 5}** - {Brief description}
6. **{Responsibility 6}** - {Brief description}

## Core Competencies

### {Competency 1}
When asked to {task related to competency 1}:
1. {Step 1}
2. {Step 2}
3. {Step 3}
4. {Step 4}
5. {Step 5}

**Example:**
```{language}
{Code example showing competency 1}
```

### {Competency 2}
When performing {task related to competency 2}:
1. {Step 1}
2. {Step 2}
3. {Step 3}
4. {Step 4}

**Key Principles:**
- {Principle 1}
- {Principle 2}
- {Principle 3}

### {Competency 3}
When {scenario for competency 3}:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Checklist:**
- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}
- [ ] {Check 4}

### {Competency 4}
{Description of competency 4}

**Process:**
```
{Visual representation of process}
```

**Common Patterns:**
- **{Pattern Name 1}**: {When to use} → {How to apply}
- **{Pattern Name 2}**: {When to use} → {How to apply}
- **{Pattern Name 3}**: {When to use} → {How to apply}

## Project-Specific Context

### morphir-dotnet {Domain} Specifics
{Project-specific information relevant to this guru's domain}

**Key Areas:**
1. **{Area 1}** - {Description}
2. **{Area 2}** - {Description}
3. **{Area 3}** - {Description}

### Important Files and Directories
```
{Relevant file structure}
```

### Commands and Tools
```bash
# {Command purpose 1}
{command1}

# {Command purpose 2}
{command2}

# {Command purpose 3}
{command3}
```

## Decision Trees

### Decision Tree 1: "{When to make decision 1}"

```
{Question 1}?
  YES → {Action or next question}
    ├─ {Sub-question 1}?
    │  ├─ YES → {Action}
    │  └─ NO → {Action}
    └─ {Sub-question 2}?
       ├─ YES → {Action}
       └─ NO → {Action}
  
  NO → {Alternative question or action}
    └─ {Follow-up}
```

### Decision Tree 2: "{When to make decision 2}"

```
{Scenario description}?
  ├─ {Option A} → {Action A}
  ├─ {Option B} → {Action B}
  ├─ {Option C} → {Action C}
  └─ {Option D} → {Action D}

After decision:
  → {Follow-up step 1}
  → {Follow-up step 2}
```

### Decision Tree 3: "{When to make decision 3}"

```
1. {First check}
   A. {Condition A}
      → {Action for A}
   
   B. {Condition B}
      → {Action for B}
   
   C. {Condition C}
      → {Action for C}

2. After resolution:
   → {Follow-up}
   → {Validation}
```

## Playbooks

### Playbook 1: {Workflow Name}

**When to use:** {Scenario description}

**Prerequisites:**
- [ ] {Prerequisite 1}
- [ ] {Prerequisite 2}
- [ ] {Prerequisite 3}

**Steps:**

**Phase 1: {Phase Name}**
1. **{Step Name}**
   ```bash
   {command if applicable}
   ```
   - Expected result: {What you should see}
   - If fails: {Troubleshooting}

2. **{Step Name}**
   - {Action to take}
   - Validation: {How to verify success}

3. **{Step Name}**
   - {Action to take}
   - Note: {Important information}

**Phase 2: {Phase Name}**
4. **{Step Name}**
   ```bash
   {command if applicable}
   ```
   - {Important detail}

5. **{Step Name}**
   - {Action to take}
   - Why: {Rationale}

**Phase 3: {Phase Name}**
6. **{Step Name}**
   - {Action to take}
   - Verification: {Validation method}

7. **{Step Name}**
   - {Final action}
   - Success criteria: {What success looks like}

**Post-Workflow:**
- [ ] {Cleanup task 1}
- [ ] {Documentation task}
- [ ] {Feedback capture}

**Duration:** ~{X} minutes

### Playbook 2: {Workflow Name}

{Similar structure to Playbook 1}

### Playbook 3: {Workflow Name}

{Similar structure to Playbook 1}

## Review Capability

> **IMPORTANT**: Review capability is a core feature of every guru. This section defines proactive monitoring and quality assurance for your domain.

### Review Scope

This guru proactively reviews the {domain area} for:

1. **{Issue Category 1}** - {What to look for}
   - Example: {Specific pattern or anti-pattern}
   - Detection: {How to identify}
   - Impact: {Why this matters}

2. **{Issue Category 2}** - {What to look for}
   - Example: {Specific pattern or anti-pattern}
   - Detection: {How to identify}
   - Impact: {Why this matters}

3. **{Issue Category 3}** - {What to look for}
   - Example: {Specific pattern or anti-pattern}
   - Detection: {How to identify}
   - Impact: {Why this matters}

4. **{Issue Category 4}** - {What to look for}
   - Example: {Specific pattern or anti-pattern}
   - Detection: {How to identify}
   - Impact: {Why this matters}

### Review Triggers

**Continuous Review** (if applicable):
- Trigger: {When continuous review runs}
- Scope: {What gets reviewed}
- Output: {Where results go}

**Scheduled Review** (if applicable):
- Frequency: {How often} (e.g., quarterly, weekly)
- Trigger: {What initiates it}
- Scope: {What gets reviewed}
- Output: {Report format and location}

**Session-Based Review** (if applicable):
- Trigger: {After what workflow}
- Scope: {What gets reviewed}
- Output: {Integrated into workflow results}

**On-Demand Review** (if applicable):
- Trigger: Manual request (`@guru review`)
- Scope: Full domain scan
- Output: Comprehensive report

### Review Output Format

**Findings Structure:**
```markdown
# {Guru Name} Review Report
**Date:** {YYYY-MM-DD}
**Scope:** {What was reviewed}
**Duration:** {Review duration}

## Summary
- {Metric 1}: {Value}
- {Metric 2}: {Value}
- {Metric 3}: {Value}

## Findings

### Category: {Issue Category 1}
- **Finding 1:** {Issue description}
  - **Location:** {File/line/component}
  - **Severity:** {Critical/High/Medium/Low}
  - **Recommendation:** {Suggested fix}
  
- **Finding 2:** {Issue description}
  - **Location:** {File/line/component}
  - **Severity:** {Critical/High/Medium/Low}
  - **Recommendation:** {Suggested fix}

### Category: {Issue Category 2}
{Similar structure}

## Trends
- {Trend 1}: {Description and data}
- {Trend 2}: {Description and data}

## Recommendations
1. **Immediate:** {High-priority recommendations}
2. **Short-term:** {Next quarter priorities}
3. **Long-term:** {Future improvements}

## Automation Opportunities
- {Pattern 1}: Appears {N} times → {Suggested automation}
- {Pattern 2}: Appears {N} times → {Suggested automation}

## Next Review Focus
- {Area to monitor closely}
- {Threshold to watch}
```

### Integration with Retrospectives

Reviews and retrospectives work together for continuous improvement:

**Review (Proactive):**
- "I scanned {domain} and found these issues"
- Identifies patterns, trends, violations
- Feeds findings to retrospectives

**Retrospective (Reactive):**
- "That failure happened because of X"
- Root cause analysis
- Feeds prevention strategies to reviews

**Continuous Improvement Cycle:**
```
Review Findings
    ↓
Identify Root Causes (Retrospective)
    ↓
Implement Prevention
    ↓
Update Playbooks/Automation
    ↓
Update Review Criteria
    ↓
Next Review (with better focus)
```

**Example Integration:**
```
Q1 Review: Found {N} instances of {anti-pattern}
Q1 Retrospective: Analyzed why {anti-pattern} occurred
Q1 Action: Created {automation} to detect/prevent
Q2 Review: {Anti-pattern} instances reduced to 0
Q2 Outcome: Pattern successfully eliminated
```

### Review Automation Scripts

Location: `.claude/skills/{guru-id}/scripts/`

**{review-script-1}.fsx**
- Purpose: {What this review script does}
- Triggers: {When it runs}
- Output: {What it produces}
- Token Savings: ~{N} tokens (vs manual review)

**{review-script-2}.fsx**
- Purpose: {What this review script does}
- Triggers: {When it runs}
- Output: {What it produces}
- Token Savings: ~{N} tokens (vs manual review)

**Usage:**
```bash
# Run {review type 1}
dotnet fsi .claude/skills/{guru-id}/scripts/{review-script-1}.fsx

# Run {review type 2}
dotnet fsi .claude/skills/{guru-id}/scripts/{review-script-2}.fsx
```

### Review Checklist

Before completing a review:

- [ ] All defined scope areas covered
- [ ] Findings categorized by severity
- [ ] Recommendations provided for each finding
- [ ] Trends analyzed (vs previous review)
- [ ] Automation opportunities identified
- [ ] Report generated and saved
- [ ] Key stakeholders notified (if applicable)
- [ ] Next review criteria updated
- [ ] Learnings fed to playbooks/decision trees

## Pattern Catalog

> **Note**: This catalog grows over time. Start with 5-10 seed patterns, add more as discovered.

### Pattern 1: {Pattern Name}

**Category:** {Pattern category}  
**Frequency:** {How often seen}  
**Complexity:** {Low/Medium/High}

**Problem:**
{What problem does this pattern solve or represent?}

**Solution:**
```{language}
{Code example showing the pattern}
```

**When to Use:**
- {Scenario 1}
- {Scenario 2}
- {Scenario 3}

**When to Avoid:**
- {Anti-pattern scenario 1}
- {Anti-pattern scenario 2}

**Related Patterns:**
- {Related Pattern 1}
- {Related Pattern 2}

---

### Pattern 2: {Pattern Name}

{Similar structure to Pattern 1}

---

### Pattern 3: {Pattern Name}

{Similar structure to Pattern 1}

---

{Continue with more patterns...}

## Automation Scripts

Location: `.claude/skills/{guru-id}/scripts/`

### Script 1: {script-name-1}.fsx

**Purpose:** {What this script does}  
**Token Savings:** ~{N} tokens per use (vs {manual alternative})

**Usage:**
```bash
dotnet fsi .claude/skills/{guru-id}/scripts/{script-name-1}.fsx [args]
```

**Arguments:**
- `{arg1}` - {Description}
- `{arg2}` - {Description}
- `{arg3}` - {Description} (optional)

**Output:**
{Description of output format}

**Example:**
```bash
# {Example usage scenario}
dotnet fsi .claude/skills/{guru-id}/scripts/{script-name-1}.fsx --{arg1}=value
```

---

### Script 2: {script-name-2}.fsx

{Similar structure to Script 1}

---

### Script 3: {script-name-3}.fsx

{Similar structure to Script 1}

## Integration Points

### Coordination with Other Gurus

**{Other Guru 1}:**
- **Direction:** {to/from} this guru
- **Interaction:** {What gets passed}
- **Trigger:** {When this happens}
- **Protocol:** {How the hand-off works}

**{Other Guru 2}:**
- **Direction:** {to/from} this guru
- **Interaction:** {What gets passed}
- **Trigger:** {When this happens}
- **Protocol:** {How the hand-off works}

**{Other Guru 3}:**
- **Direction:** {to/from} this guru
- **Interaction:** {What gets passed}
- **Trigger:** {When this happens}
- **Protocol:** {How the hand-off works}

### Escalation Paths

**When to Escalate:**
1. {Scenario requiring human decision}
2. {Scenario beyond scope}
3. {Scenario with high uncertainty}

**How to Escalate:**
1. Document the decision point
2. Provide context and options
3. Tag appropriate maintainer: {maintainer-tag}
4. Label issue: `maintainer-attention`
5. Wait for guidance

**What NOT to Decide:**
- {Out-of-scope decision 1}
- {Out-of-scope decision 2}
- {Out-of-scope decision 3}

## Feedback Loop

### Feedback Capture

**Trigger Points:**
- {When feedback is captured - e.g., "After each {workflow}"}
- {When feedback is captured - e.g., "Every {N} {units}"}
- {When feedback is captured - e.g., "Quarterly review"}

**Capture Method:**
{How feedback is recorded - e.g., "Template section", "GitHub issue", "IMPLEMENTATION.md"}

**What to Capture:**
- Patterns discovered
- Decision points encountered
- Edge cases found
- Improvements identified
- Automation opportunities

### Quarterly Review Process

**Schedule:** {When reviews happen - e.g., "Q1, Q2, Q3, Q4"}

**Review Checklist:**
1. [ ] Collect all feedback from quarter
2. [ ] Analyze patterns and trends
3. [ ] Identify 2-3 key improvements
4. [ ] Update playbooks and decision trees
5. [ ] Add/update patterns in catalog
6. [ ] Evaluate automation opportunities
7. [ ] Document learnings
8. [ ] Bump version if user-facing changes
9. [ ] Notify team of improvements

**Improvement Triggers:**
- Pattern appears 3+ times → Consider automation
- New anti-pattern discovered → Update guidance
- Workflow changes → Update playbooks
- Tool updates → Validate scripts

## Cross-Agent Compatibility

### For Claude Code Users

**Invocation:**
```
@skill {guru-id}
{Your request}
```

**Triggers:** Keywords like "{keyword1}", "{keyword2}", "{keyword3}"

---

### For GitHub Copilot Users

**Access:**
- Read `.agents/{guru-id}.md` for equivalent guidance
- Run scripts directly: `dotnet fsi .claude/skills/{guru-id}/scripts/{script}.fsx`
- Follow decision trees and playbooks
- Reference pattern catalog

**Quick Start:**
```bash
# Run {common task}
dotnet fsi .claude/skills/{guru-id}/scripts/{script-name}.fsx
```

---

### For Other Agents (Cursor, Windsurf, Aider)

**Access:**
- Documentation: `.claude/skills/{guru-id}/skill.md` (this file)
- Quick reference: `.claude/skills/{guru-id}/README.md`
- Scripts: `.claude/skills/{guru-id}/scripts/`
- Templates: `.claude/skills/{guru-id}/templates/`

**Usage:**
1. Read skill.md for comprehensive guidance
2. Follow playbooks for complex workflows
3. Use decision trees for problem-solving
4. Run automation scripts for common tasks
5. Reference pattern catalog for examples

## Templates

Location: `.claude/skills/{guru-id}/templates/`

### Template 1: {template-name-1}.md

**Purpose:** {What this template is for}  
**When to Use:** {Scenarios for using this template}

**Usage:**
1. Copy template: `cp .claude/skills/{guru-id}/templates/{template-name-1}.md .`
2. Fill in {placeholder} values
3. Use for {intended purpose}

---

### Template 2: {template-name-2}.md

{Similar structure to Template 1}

## Related Resources

**Within This Project:**
- [README.md](./README.md) - Quick reference guide
- [MAINTENANCE.md](./MAINTENANCE.md) - Maintenance and evolution guide
- [metadata.yaml](./metadata.yaml) - Skill metadata and configuration
- [scripts/](./scripts/) - Automation scripts
- [templates/](./templates/) - Reusable templates
- [patterns/](./patterns/) - Detailed pattern documentation

**Project Guidance:**
- [AGENTS.md](../../../AGENTS.md) - Primary agent guidance
- [Guru Philosophy](../../../.agents/guru-philosophy.md) - Guru principles
- [Skills Reference](../../../.agents/skills-reference.md) - All available gurus
- [Skill Matrix](../../../.agents/skill-matrix.md) - Maturity tracking

**External Resources:**
- {External resource 1} - {Description}
- {External resource 2} - {Description}
- {External resource 3} - {Description}

---

**Last Updated:** {YYYY-MM-DD}  
**Version:** {Semantic version}  
**Status:** {alpha/beta/stable}  
**Maintainer:** {Maintainer name/GitHub handle}
