/*============================================================================*/
/* WHEN-REVIEWING-CODE-COMPREHENSIVELY-USE-CODE-REVIEW-ASSISTANT SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-reviewing-code-comprehensively-use-code-review-assistant
version: 1.0.0
description: |
  [assert|neutral] Comprehensive PR review with multi-agent swarm specialization for security, performance, style, tests, and documentation [ground:given] [conf:0.95] [state:confirmed]
category: testing-quality
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-reviewing-code-comprehensively-use-code-review-assistant workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic testing-quality processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-reviewing-code-comprehensively-use-code-review-assistant",
  category: "testing-quality",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-reviewing-code-comprehensively-use-code-review-assistant", "testing-quality", "workflow"],
  context: "user needs when-reviewing-code-comprehensively-use-code-review-assistant capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Comprehensive Code Review Assistant

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose

Orchestrate multi-agent swarm review of pull requests with specialized reviewers for security, performance, style, test coverage, and documentation. Provides detailed feedback with auto-fix suggestions and merge readiness assessment.

## Core Principles

- **Multi-Agent Specialization**: Dedicated agents for each review dimension
- **Parallel Analysis**: Concurrent review across all quality vectors
- **Evidence-Based**: Measurable quality metrics and validation gates
- **Auto-Fix Capability**: Automated corrections where possible
- **Merge Readiness**: Clear approval/rejection criteria

## MCP Requirements

This skill requires the following MCP servers for optimal functionality:

### focused-changes (1.8k tokens - TIER 1: Code Quality)

**Purpose**: Track PR changes, validate focused scope, and build error trees from review findings.

**Tools Used**:
- `start_tracking`: Track original files before review
- `analyze_changes`: Ensure PR changes are focused and cohesive
- `root_cause_analysis`: Build error trees from test failures and code issues

**Activation** (PowerShell):
```powershell
# Check if already active
claude mcp list

# Add if not present
claude mcp add focused-changes node C:/Users/17175/Documents/Cline/MCP/focused-changes-server/build/index.js
```

**Usage Example**:
```javascript
// Track changes across all review phases
mcp__focused_changes__start_tracking({
  filepath: 'src/auth/middleware.js',
  content: originalCode
});

// Validate changes are focused (not mixing features)
mcp__focused_changes__analyze_changes({
  newContent: prChanges
});

// Build error tree from test failures
mcp__focused_changes__root_cause_analysis({
  testResults: failedTestResults
});
```

**Token Cost**: 1.8k tokens (0.9% of 200k context)
**When to Load**: When performing comprehensive code reviews with change tracking

## Phase 1: Security Review

### Objective
Identify and report security vulnerabilities, OWASP violations, and authentication/authorization issues.

### Agent Configuration
```yaml
agent: security-manager
specialization: security-audit
validation: OWASP-Top-10
```

### Execution Steps

**1. Initialize Security Scan**
```bash
# Pre-task setup
npx claude-flow@alpha hooks pre-task \
  --agent-id "security-manager" \
  --description "Security vulnerability scanning" \
  --task-type "security-audit"

# Restore session context
npx claude-flow@alpha hooks session-restore \
  --session-id "code-review-swarm-${PR_ID}" \
  --agent-id "security-manager"
```

**2. OWASP Top 10 Scan**
```bash
# Scan for OWASP vulnerabilities
npx eslint . --format json --config .eslintrc-security.json > security-report.json

# Check for dependency vulnerabilities
npm audit --json > npm-audit.json

# Scan for secrets and credentials
npx gitleaks detect --source . --report-path gitleaks-report.json
```

**3. Authentication/Authorization Review**
```javascript
// Analyze authentication patterns
const authPatterns = {
  jwt_validation: /jwt\.verify\(/g,
  password_hashing: /bcrypt|argon2|scrypt/g,
  sql_injection: /\$\{.*\}/g,
  xss_prevention: /sanitize|escape|DOMPurify/g,
  csrf_protection: /csrf|csurf/g
};

// Validate security controls
const securityChecks = {
  has_jwt_validation: false,
  has_password_hashing: false,
  has_sql_parameterization: false,
  has_xss_prevention: false,
  has_csrf_protection: false
};
```

**4. Store Security Findings**
```bash
# Store results in memory
npx claude-flow@alpha hooks post-edit \
  --file "security-report.json" \
  --memory-key "swarm/security-manager/findings" \
  --metadata "{\"critical\": ${CRITICAL_COUNT}, \"high\": ${HIGH_COUNT}}"
```

**5. Generate Security Report**
```markdown
## Security Review Results

### Critical Issues (Blocking)
- [ ] SQL injection vulnerability in user.controller.js:45
- [ ] Hardcoded API key in config/production.js:12

### High Priority Issues
-

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/testing-quality/when-reviewing-code-comprehensively-use-code-review-assistant/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-reviewing-code-comprehensively-use-code-review-assistant-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>WHEN_REVIEWING_CODE_COMPREHENSIVELY_USE_CODE_REVIEW_ASSISTANT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
