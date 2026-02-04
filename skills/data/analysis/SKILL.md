---
name: analysis
description: Analyze feature requirements, dependencies, and security considerations. Use when starting feature implementation from GitHub issues to understand scope, technical feasibility, and risks.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__github-mcp__get_issue
  - mcp__github-mcp__get_issue_comments
  - mcp__github-mcp__search_issues
---

# Feature Analysis Skill

## Purpose

This skill provides systematic analysis of feature requirements from GitHub issues, evaluating technical feasibility, dependencies, security implications, and implementation scope.

## When to Use

- Starting feature implementation from a GitHub issue
- Need to understand requirements and acceptance criteria
- Evaluating technical approach and dependencies
- Identifying security considerations early
- Scoping effort and potential risks

## Analysis Workflow

### 1. Requirements Extraction

**From GitHub Issue:**
- Parse issue title, description, and acceptance criteria
- Extract functional and non-functional requirements
- Identify user stories and use cases
- Review issue comments for clarifications
- Check linked issues and dependencies

**Deliverable:** Structured requirements list with priorities

### 2. Technical Stack Evaluation

**Assess Technology Fit:**
- Review project's TECH-STACK.md for current technologies
- Identify required libraries/frameworks
- Check version compatibility
- Evaluate performance implications
- Consider maintenance burden

**Tools to Use:**
- Read TECH-STACK.md and relevant documentation
- Use `scripts/analyze_deps.py` for dependency analysis
- Grep codebase for similar patterns

**Deliverable:** Technology recommendations with rationale

### 3. Dependency Analysis

**Identify Dependencies:**
- External libraries (pip/npm/cargo packages)
- Internal modules and services
- Database schema changes
- API contracts
- Configuration requirements

**Check for Conflicts:**
```bash
# Use the analyze_deps script
python scripts/analyze_deps.py --feature <feature-name>
```

**Deliverable:** Dependency map with conflict analysis

### 4. Security Assessment

**Review Security Implications:**
- Authentication/authorization requirements
- Input validation needs
- Data sensitivity (PII, credentials, etc.)
- API security (rate limiting, CORS, etc.)
- Dependency vulnerabilities

**Use Checklist:**
Refer to `security-checklist.md` for systematic review

**Deliverable:** Security risk assessment and mitigation plan

### 5. Scope Definition

**Define Boundaries:**
- Core functionality (must-have)
- Extended functionality (should-have)
- Future enhancements (could-have)
- Out of scope (won't-have)

**Estimate Complexity:**
- Lines of code (rough estimate)
- Number of modules/files
- Test coverage requirements
- Documentation needs

**Deliverable:** Scope statement with effort estimate

## Output Format

Create an analysis report with:

```markdown
# Feature Analysis: [Feature Name]

## Requirements Summary
- [ ] Requirement 1
- [ ] Requirement 2
...

## Technical Approach
**Recommended Stack:** Python 3.9+, pytest, pydantic
**Key Libraries:** [list]
**Architecture Pattern:** [pattern]

## Dependencies
**External:**
- package-name==version (reason)

**Internal:**
- module.submodule (reason)

## Security Considerations
**Risk Level:** Low/Medium/High
**Key Concerns:**
- [concern 1]: [mitigation]

## Scope
**In Scope:**
- [feature 1]

**Out of Scope:**
- [deferred item]

**Effort Estimate:** [hours/days]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

## Best Practices

**Requirements Analysis:**
- Always check requirements-checklist.md for completeness
- Clarify ambiguous requirements before proceeding
- Document assumptions explicitly
- Consider edge cases and error scenarios

**Technical Evaluation:**
- Prefer existing project patterns over new approaches
- Consider maintainability over cleverness
- Check for similar existing implementations
- Evaluate performance implications early

**Security First:**
- Run security-checklist.md for all features
- Flag high-risk items for review
- Never skip input validation planning
- Consider data privacy implications

**Scope Management:**
- Be conservative with estimates
- Identify MVP vs. enhanced features
- Call out dependencies that block progress
- Document what's explicitly out of scope

## Supporting Resources

- **requirements-checklist.md**: Systematic requirements validation
- **security-checklist.md**: Security considerations framework
- **scripts/analyze_deps.py**: Automated dependency analysis

## Example Usage

```bash
# 1. Fetch issue details
Use mcp__github-mcp__get_issue to retrieve issue #<number>

# 2. Review requirements
Work through requirements-checklist.md systematically

# 3. Analyze dependencies
python scripts/analyze_deps.py --feature feature-name

# 4. Security review
Complete security-checklist.md

# 5. Generate analysis report
Create report in docs/implementation/feature-name-analysis.md
```

## Integration with Feature Implementation Flow

**Input:** GitHub issue number
**Process:** Systematic analysis using checklists and scripts
**Output:** Analysis report + recommendations
**Next Step:** Design skill for architecture planning
