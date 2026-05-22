---
name: sdd-design-security
description: |
  Design threat mitigation, input validation, and secure execution.
  Use when: sdd-design assigns Security Considerations section.
  Triggers: "security design", "threat model", "input validation", "xss prevention"
---

# SDD Design Security

Write the Security Considerations section of a design document.

## Scope

| Responsible For | Not Responsible For |
|-----------------|---------------------|
| Threat modeling | Component structure (→ frontend) |
| Input validation strategy | Props interface design (→ frontend) |
| Code execution sandboxing | Code editor implementation (→ frontend) |
| XSS prevention strategy | Syntax highlighting (→ frontend) |
| Dependency security review | Bundle optimization (→ perf) |

## Cross-Cutting Roles

> **Note:** Cross-cutting concerns are an extension to sdd-guidelines for specialist coordination. See sdd-design for full mapping.

Security is:
- **Primary owner:** (none in typical frontend projects)
- **Reviewer for:** Error handling (owned by frontend), User input (owned by frontend)

## Instructions

### Step 1: Read Context

1. Design skeleton (from sdd-design)
2. All REQs in your section's `@derives`
3. Foundation anchors (especially `CONSTRAINT-*`, `SCOPE-*`)
4. Frontend section (for input handling, code execution)

### Step 2: Identify Attack Surface

For each REQ, identify security-relevant elements:

| REQ | User Input | Dynamic Content | Code Execution |
|-----|------------|-----------------|----------------|
| | | | |

**Attack surface types:**
- User input: forms, props manipulation, text entry
- Dynamic content: user-provided data rendered to DOM
- Code execution: eval, Function(), dynamic imports

### Step 3: Build Threat Model

For each attack surface:

| Threat | Vector | Impact | Likelihood | @derives |
|--------|--------|--------|------------|----------|
| | | | | REQ-XXX |

**Impact levels:** Critical / High / Medium / Low
**Likelihood:** High (easy to exploit) / Medium / Low (requires skill)

### Step 4: Design Input Validation

For each user input from REQs:

| Input Source | Validation | Sanitization | @derives |
|--------------|------------|--------------|----------|
| | | | REQ-XXX |

**Validation types:**
- Type checking (string, number, enum)
- Range/length limits
- Format validation (regex)
- Whitelist vs blacklist

### Step 5: Design Code Execution Controls (if applicable)

If REQ involves code execution:

| Risk | Control | Implementation |
|------|---------|----------------|
| Arbitrary code | Scope restriction / sandbox | |
| Infinite loops | Timeout | |
| Memory exhaustion | Memory limit | |
| DOM access | Restricted globals | |

**Decision:** Sandbox vs restricted scope vs no eval?

Document with `@derives` linking to REQ.

### Step 6: Design XSS Prevention

For each dynamic content type:

| Content Type | Strategy | @derives |
|--------------|----------|----------|
| User text | Escape / sanitize | REQ-XXX |
| Code display | Syntax highlighter escapes | REQ-XXX |
| Dynamic HTML | CSP / sanitize | REQ-XXX |

### Step 7: Review Dependencies

For libraries suggested by other specialists:

| Dependency | Known Vulnerabilities | Mitigation |
|------------|----------------------|------------|
| | | |

**Check:** npm audit, Snyk, GitHub advisories

### Step 8: Write Section

```markdown
## Security Considerations

@derives: {REQ-IDs}

### Threat Model
### Input Validation
### Code Execution Controls (if applicable)
### XSS Prevention
### Dependency Security

**Status:** draft
```

### Step 9: Add Decisions

For non-obvious security choices:

```markdown
| ID | Decision | Rationale | Owner |
|----|----------|-----------|-------|
| DEC-00x | {what} | {why — connect to REQ + threat} | security |
```

### Step 10: Handoff

Per sdd-guidelines §4.3 and §10.6.

#### 1. Update Section Status

```markdown
**Status:** verified
```

#### 2. Update State File

```yaml
# .sdd/state.yaml
documents:
  design:
    sections:
      security: verified
```

#### 3. Create Handoff Record

```yaml
# .sdd/handoffs/{timestamp}-security.yaml
from: sdd-design-security
to: sdd-design
timestamp: {ISO-8601}

completed:
  - design.security: verified

in_progress: []

blocked: []

gaps: []

next_steps:
  - sdd-design-frontend: Implement validation per spec
  - sdd-design-frontend: Review — error handling exposes no sensitive info
```

#### 4. Cross-Cutting Status

| Concern | Primary | Reviewer | Status |
|---------|---------|----------|--------|
| Error handling | frontend | security | `approved` or `needs-revision` |
| User input | frontend | security | `approved` or `needs-revision` |

## @derives Judgment

**A security control `@derives` from a REQ when:**

| Criterion | Example |
|-----------|---------|
| Mitigates threat from REQ feature | Input validation → REQ's "user enters values" |
| Enables REQ safely | Sandbox → REQ's "editable code" |
| Required by REQ constraint | XSS prevention → REQ's "displays user content" |

**NOT @derives:**
- Generic security best practices not tied to REQ
- Threats from features not in requirements

## Verification

- [ ] All user inputs from REQs have validation defined
- [ ] Threat model covers all attack surfaces
- [ ] Code execution controls match REQ scope (if applicable)
- [ ] XSS prevention for all dynamic content
- [ ] Dependencies reviewed for known vulnerabilities
- [ ] Decisions logged with rationale
- [ ] Cross-cutting reviews completed

## References

| File | Content |
|------|---------|
| [reference/threat-modeling.md](reference/threat-modeling.md) | REQ-based threat identification |
| [reference/frontend-security.md](reference/frontend-security.md) | Common frontend security patterns |

## Examples

| File | Content |
|------|---------|
| [examples/react-sample.md](examples/react-sample.md) | Complete example for react-sample package |
