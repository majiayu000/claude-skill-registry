---
name: pr-reviewer
description: "Review pull requests for spec compliance, security, performance, and code quality. Use when analyzing PRs. Not for writing new code or initial development."
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash
---

# PR Reviewer

<mission_control>
<objective>Review pull requests with systematic analysis before generating feedback</objective>
<success_criteria>All findings categorized by severity with specific recommendations</success_criteria>
<standards_gate>
MANDATORY: Load pr-reviewer references BEFORE starting review:

- Security patterns → references/security.md
- Quality criteria → references/quality.md
- Performance guidelines → references/performance.md
  </standards_gate>
  </mission_control>

Review pull request changes with comprehensive analysis including security, performance, code quality, and architecture.

<interaction_schema>
inject_context → thinking_analysis → stage1_spec_compliance → stage2_quality_review → categorize_findings → output
</interaction_schema>

## Thinking Protocol: Analyze Before Speaking

<thinking_protocol>
<mandatory_trigger>
Before generating ANY PR review feedback
</mandatory_trigger>

<process>
1. **Open `<thinking>`** - Analysis sandbox
2. **Analyze the diff** - What changed, why, impact
3. **Check requirements** - Does implementation match spec?
4. **Identify issues** - Security, performance, quality, architecture
5. **Weigh severity** - Blocker vs nitpick
6. **Close `</thinking>`** - Hard stop before output
7. **Generate review** - Categorized findings with recommendations
</process>
</thinking_protocol>

### Thinking Template

```xml
<thinking>
<diff_analysis>
- Files changed: [count and list]
- Lines added/removed: [approximate]
- Scope: [feature/bug/refactor/other]
- Risk level: [high/medium/low]
</diff_analysis>

<requirement_check>
- PR description states: [requirements]
- Implementation provides: [what was actually done]
- Gaps identified: [missing features, extra features]
- Spec compliance: [COMPLIANT/NON_COMPLIANT]
</requirement_check>

<issue_scan>
<security>
- Injection vulnerabilities: [findings]
- Auth/authz issues: [findings]
- Secrets exposure: [findings]
- Input validation: [findings]
</security>

<performance>
- N+1 queries: [findings]
- Algorithmic issues: [findings]
- Missing indexes: [findings]
- Caching opportunities: [findings]
</performance>

<quality>
- Code duplication: [findings]
- Naming issues: [findings]
- Test coverage: [findings]
- Complexity issues: [findings]
</quality>

<architecture>
- Layer violations: [findings]
- Dependency issues: [findings]
- Error handling: [findings]
- API design: [findings]
</architecture>
</issue_scan>

<severity_assessment>
- Blockers: [must-fix before merge]
- Important: [should-fix before merge]
- Nits: [nice-to-have improvements]
</severity_assessment>
</thinking>
```

---

This skill uses dynamic context injection with `!`command"` syntax to gather live PR data before review:

```markdown
## Current Context

- **PR diff**: !`git diff HEAD~1`
- **PR title**: !`git log -1 --pretty=format:%s`
- **PR description**: !`git log -1 --pretty=format:%b`
- **Changed files**: !`git diff --name-only HEAD~1`
- **Commits**: !`git log --oneline HEAD~1..HEAD`
```

## Two-Stage Review Architecture

**MANDATORY**: PR review must follow two-stage process:

1. **Stage 1**: Spec Compliance Review - Verify implementation matches requirements
2. **Stage 2**: Code Quality Review - Assess security, performance, quality, architecture

**NEVER skip stages or review out of order.**

### Stage 1: Spec Compliance Review

**First, verify implementation matches requirements:**

#### Spec Compliance Checklist

- [ ] All requirements from PR description implemented
- [ ] Nothing extra added (YAGNI violations)
- [ ] Acceptance criteria met
- [ ] Edge cases addressed
- [ ] No missing functionality

#### Spec Compliance Output

```markdown
## Stage 1: Spec Compliance Review

### Requirements Verification

✅ All required features implemented
✅ No extra features (YAGNI compliant)
✅ Acceptance criteria met

### Gap Analysis

- Missing: [List any gaps]
- Extra: [List any over-implementation]
- Ambiguous: [List unclear requirements]

**Result**: COMPLIANT | NON_COMPLIANT
```

### Stage 2: Code Quality Review

<router>
flowchart TD
    Start([Start Review]) --> Stage1{Stage 1:\nSpec Compliance}
    Stage1 -- PASS --> Stage2{Stage 2:\nCode Quality}
    Stage1 -- FAIL --> Return[Return to User\n(Fix Spec)]
    Stage2 -- PASS --> Approve[Approve PR]
    Stage2 -- FAIL --> RequestChanges[Request Changes\n(Fix Code)]
    RequestChanges --> Return
</router>

**Only after Stage 1 passes:**

Execute comprehensive review across four dimensions:

#### 1. Security Review

- Check for injection vulnerabilities (SQL, XSS, command injection)
- Verify authentication/authorization implementation
- Look for secrets exposure in code
- Validate input sanitization
- Check for OWASP Top 10 vulnerabilities

### 2. Performance Review

- Identify N+1 query problems
- Check for inefficient algorithms
- Look for missing database indexes
- Validate caching strategies
- Review API response times

### 3. Code Quality Review

- Review naming conventions
- Check for code duplication
- Verify test coverage
- Assess maintainability
- Check for code complexity issues

### 4. Architecture Review

- Check layer separation (MVC, clean architecture)
- Verify dependency injection
- Assess error handling patterns
- Review API design
- Check for proper abstractions

## Output Format

<finding_categorization>
<purpose>Force findings into XML buckets for clear categorization and severity assessment</purpose>

<security_issues>
<issue severity="BLOCKER | HIGH | MEDIUM | LOW">
<description>[What's wrong]</description>
<file_path>[path/to/file]</file_path>
<line_number>[number]</line_number>
<recommendation>[Specific fix with code example if applicable]</recommendation>
<cve_reference>[If applicable CVE or OWASP reference]</cve_reference>
</issue>
</security_issues>

<performance_issues>
<issue severity="BLOCKER | HIGH | MEDIUM | LOW">
<description>[What's wrong]</description>
<file_path>[path/to/file]</file_path>
<line_number>[number]</line_number>
<recommendation>[Specific fix with optimization strategy]</recommendation>
<impact>[Performance impact: +Xms, -Y queries/sec]</impact>
</issue>
</performance_issues>

<code_quality_issues>
<issue severity="NIT | LOW | MEDIUM">
<type>[duplication | naming | complexity | coverage | style]</type>
<description>[What's wrong]</description>
<file_path>[path/to/file]</file_path>
<line_number>[number]</line_number>
<recommendation>[Specific improvement]</recommendation>
</issue>
</code_quality_issues>

<architecture_issues>
<issue severity="BLOCKER | HIGH | MEDIUM">
<type>[layer_violation | dependency | error_handling | api_design]</type>
<description>[What's wrong]</description>
<file_path>[path/to/file]</file_path>
<line_number>[number]</line_number>
<recommendation>[Specific architectural improvement]</recommendation>
</issue>
</architecture_issues>
</finding_categorization>

### Markdown Output Template

```markdown
# PR Review: [PR Title]

## Stage 1: Spec Compliance

**Status**: ✅ PASS / ❌ FAIL

### Requirements Verification

[Summary of spec compliance check]

### Gap Analysis

- Missing: [list]
- Extra: [list]
- Ambiguous: [list]

---

## Stage 2: Code Quality Review

### Security Issues

<security_issues count="0">

<!-- No security issues found -->

</security_issues>

### Performance Issues

<performance_issues count="0">

<!-- No performance issues found -->

</performance_issues>

### Code Quality Issues

<code_quality_issues count="2">
<issue severity="NIT">
<type>naming</type>
<description>Variable name 'x' not descriptive</description>
<file_path>src/auth.py</file_path>
<line_number>42</line_number>
<recommendation>Use descriptive name like 'user_id'</recommendation>
</issue>
</code_quality_issues>

### Architecture Issues

<architecture_issues count="0">

<!-- No architecture issues found -->

</architecture_issues>

---

## Overall Assessment

**Result**: APPROVE | REQUEST_CHANGES

**Summary**: [1-2 sentence summary]

**Blockers**: [count] must be fixed before merge
**Important**: [count] should be fixed before merge
**Nits**: [count] optional improvements
```

## Review Loop Enforcement

**CRITICAL**: If issues found, fixes must be verified before approval.

### Review Loop Protocol

1. **Reviewer finds issues** → Report all issues clearly
2. **Developer fixes issues** → Resubmit for review
3. **Reviewer re-reviews** → Verify fixes actually work
4. **Repeat until approved** → No shortcuts, no exceptions

**NEVER approve with open issues.**

### Review Loop Template

```markdown
## Review Results

### Stage 1: Spec Compliance

**Status**: PASS | FAIL
[If FAIL: List specific gaps]

### Stage 2: Code Quality

**Status**: PASS | FAIL

#### Issues Found:

1. **[Severity]** - [Issue]
   - File: [path]
   - Line: [number]
   - Fix: [specific recommendation]

#### Required Changes:

- [ ] Fix issue 1
- [ ] Fix issue 2
- [ ] Re-review after fixes

**Review will continue until all issues resolved.**
```

## Review Checklist

### Security

- [ ] No SQL injection vulnerabilities
- [ ] XSS protection implemented
- [ ] Authentication properly checked
- [ ] Authorization enforced
- [ ] No secrets in code
- [ ] Input validation present
- [ ] Rate limiting configured

### Performance

- [ ] No N+1 queries
- [ ] Efficient algorithms used
- [ ] Proper indexing strategy
- [ ] Caching implemented where appropriate
- [ ] API responses optimized

### Code Quality

- [ ] Consistent naming conventions
- [ ] No code duplication
- [ ] Adequate test coverage
- [ ] Clear, readable code
- [ ] Proper error handling
- [ ] No commented-out code

### Architecture

- [ ] Proper layer separation
- [ ] Dependencies properly injected
- [ ] Errors handled appropriately
- [ ] API follows REST conventions
- [ ] Appropriate design patterns used

## Integration

This skill integrates with:

- `security` - Security vulnerability detection
- `coding-standards` - Code quality standards
- `backend-patterns` - Architecture best practices
- `engineering-lifecycle` - Testing requirements

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

<critical_constraint>
**MANDATORY: Complete `<thinking>` analysis BEFORE generating review output**

- Analyze diff, requirements, and impact
- Check security, performance, quality, architecture dimensions
- Weigh severity before generating output
- NEVER skip thinking phase, even for "simple" PRs

**MANDATORY: Categorize findings into XML buckets**

- Security issues → `<security_issues>`
- Performance issues → `<performance_issues>`
- Code quality issues → `<code_quality_issues>`
- Architecture issues → `<architecture_issues>`
- Each finding must have severity, description, location, recommendation

**MANDATORY: Two-stage review process**

- Stage 1: Spec compliance (requirements met?)
- Stage 2: Code quality (security, performance, quality, architecture)
- NEVER approve if Stage 1 fails (requirements not met)
- NEVER approve with BLOCKER or HIGH severity issues open

**MANDATORY: Verify fixes before approval**

- If issues found, developer must fix
- Re-review to verify fixes actually work
- Repeat until all issues resolved
- NEVER approve with open issues

**MANDATORY: Never LGTM without analysis**

- "Looks good to me" is forbidden without `<thinking>` analysis
- Every PR deserves thorough review
- Small PRs can have big bugs
- No short-cuts, no exceptions

**No exceptions. PR review is a gate, not a formality.**
</critical_constraint>
