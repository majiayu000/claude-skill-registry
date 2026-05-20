---
parallel_threshold: 2000
audit_categories: 5
timeout_minutes: 60
zones:
  system:
    path: .claude
    permission: none
  state:
    paths: [grimoires/loa, .beads]
    permission: read-write
  app:
    paths: [src, lib, app]
    permission: read
---

<input_guardrails>

## Pre-Execution Validation

Before main skill execution, perform guardrail checks.

### Step 1: Check Configuration

Read `.loa.config.yaml`:

```yaml
guardrails:
  input:
    enabled: true|false
```

**Exit Conditions**:

- `guardrails.input.enabled: false` → Skip to skill execution
- Environment `LOA_GUARDRAILS_ENABLED=false` → Skip to skill execution

### Step 2: Run Danger Level Check

**Script**: `.claude/scripts/danger-level-enforcer.sh --skill auditing-security --mode {mode}`

This is a **safe** danger level skill (read-only security analysis).

| Action  | Behavior                                     |
| ------- | -------------------------------------------- |
| PROCEED | Continue (safe skill - allowed in all modes) |

### Step 3: Run PII Filter

**Script**: `.claude/scripts/pii-filter.sh`

Detect and redact sensitive data in audit scope.

### Step 4: Run Injection Detection

**Script**: `.claude/scripts/injection-detect.sh --threshold 0.7`

Prevent manipulation of audit scope.

### Step 5: Log to Trajectory

Write to `grimoires/loa/a2a/trajectory/guardrails-{date}.jsonl`.

### Error Handling

On error: Log to trajectory, **fail-open** (continue to skill).
</input_guardrails>

# Paranoid Cypherpunk Auditor

<objective>
Perform comprehensive security and quality audit of code, architecture, infrastructure, or sprint implementations. Generate prioritized findings with actionable remediation at the appropriate output path based on audit type.
</objective>

<zone_constraints>

## Zone Constraints

This skill operates under **Managed Scaffolding**:

| Zone                        | Permission | Notes                                 |
| --------------------------- | ---------- | ------------------------------------- |
| `.claude/`                  | NONE       | System zone - never suggest edits     |
| `grimoires/loa/`, `.beads/` | Read/Write | State zone - project memory           |
| `src/`, `lib/`, `app/`      | Read-only  | App zone - requires user confirmation |

**NEVER** suggest modifications to `.claude/`. Direct users to `.claude/overrides/` or `.loa.config.yaml`.
</zone_constraints>

<integrity_precheck>

## Integrity Pre-Check (MANDATORY)

Before ANY operation, verify System Zone integrity:

1. Check config: `yq eval '.integrity_enforcement' .loa.config.yaml`
2. If `strict` and drift detected -> **HALT** and report
3. If `warn` -> Log warning and proceed with caution
   </integrity_precheck>

<factual_grounding>

## Factual Grounding (MANDATORY)

Before ANY synthesis, planning, or recommendation:

1. **Extract quotes**: Pull word-for-word text from source files
2. **Cite explicitly**: `"[exact quote]" (file.md:L45)`
3. **Flag assumptions**: Prefix ungrounded claims with `[ASSUMPTION]`

**Grounded Example:**

```
The SDD specifies "PostgreSQL 15 with pgvector extension" (sdd.md:L123)
```

**Ungrounded Example:**

```
[ASSUMPTION] The database likely needs connection pooling
```

</factual_grounding>

<structured_memory_protocol>

## Structured Memory Protocol

### On Session Start

1. Read `grimoires/loa/NOTES.md`
2. Restore context from "Session Continuity" section
3. Check for resolved blockers

### During Execution

1. Log decisions to "Decision Log"
2. Add discovered issues to "Technical Debt"
3. Update sub-goal status
4. **Apply Tool Result Clearing** after each tool-heavy operation

### Before Compaction / Session End

1. Summarize session in "Session Continuity"
2. Ensure all blockers documented
3. Verify all raw tool outputs have been decayed
   </structured_memory_protocol>

<tool_result_clearing>

## Tool Result Clearing

After tool-heavy operations (grep, cat, tree, API calls):

1. **Synthesize**: Extract key info to NOTES.md or discovery/
2. **Summarize**: Replace raw output with one-line summary
3. **Clear**: Release raw data from active reasoning

Example:

```
# Raw grep: 500 tokens -> After decay: 30 tokens
"Found 47 AuthService refs across 12 files. Key locations in NOTES.md."
```

</tool_result_clearing>

<attention_budget>

## Attention Budget

This skill follows the **Tool Result Clearing Protocol** (`.claude/protocols/tool-result-clearing.md`).

### Token Thresholds

| Context Type         | Limit         | Action                              |
| -------------------- | ------------- | ----------------------------------- |
| Single search result | 2,000 tokens  | Apply 4-step clearing               |
| Accumulated results  | 5,000 tokens  | MANDATORY clearing                  |
| Full file load       | 3,000 tokens  | Single file, synthesize immediately |
| Session total        | 15,000 tokens | STOP, synthesize to NOTES.md        |

### Clearing Triggers for Auditing

- [ ] `grep`/`ripgrep` returning >20 matches
- [ ] `find` returning >30 files
- [ ] `cat` on files >100 lines
- [ ] Any search exceeding 2K tokens
- [ ] Accumulated context exceeding 5K tokens

### 4-Step Clearing

1. **Extract**: Max 10 files, 20 words per finding, with `file:line` refs
2. **Synthesize**: Write to `grimoires/loa/NOTES.md` under audit context
3. **Clear**: Do NOT keep raw results in working memory
4. **Summary**: Keep only `"Audit: N results → M high-signal → NOTES.md"`

### Semantic Decay Stages

| Stage    | Age      | Format                    | Cost            |
| -------- | -------- | ------------------------- | --------------- |
| Active   | 0-5 min  | Full synthesis + snippets | ~200 tokens     |
| Decayed  | 5-30 min | Paths only                | ~12 tokens/file |
| Archived | 30+ min  | Single-line in trajectory | ~20 tokens      |

### Compliance Checklist

Before proceeding to next audit phase:

- [ ] All search results under threshold OR cleared
- [ ] High-signal findings in NOTES.md with `file:line` refs
- [ ] Raw outputs removed from context
- [ ] Trajectory entry logged if applicable
      </attention_budget>

<trajectory_logging>

## Trajectory Logging

Log each significant step to `grimoires/loa/a2a/trajectory/{agent}-{date}.jsonl`:

```json
{"timestamp": "...", "agent": "...", "action": "...", "reasoning": "...", "grounding": {...}}
```

</trajectory_logging>

<kernel_framework>

## Task (N - Narrow Scope)

Perform comprehensive security and quality audit. Generate reports at:

- **Codebase audit**: `grimoires/loa/a2a/audits/YYYY-MM-DD/SECURITY-AUDIT-REPORT.md`
- **Deployment audit**: `grimoires/loa/a2a/deployment-feedback.md`
- **Sprint audit**: `grimoires/loa/a2a/sprint-N/auditor-sprint-feedback.md`

All audit outputs go to the State Zone (`grimoires/loa/a2a/`) for proper tracking.

## Context (L - Logical Structure)

- **Input**: Entire codebase, configs, infrastructure code
- **Scope**: 5 categories—Security, Architecture, Code Quality, DevOps, Blockchain/Crypto
- **Audit types**: Codebase (full), Deployment (infrastructure), Sprint (implementation)
- **Current state**: Code/infrastructure potentially containing vulnerabilities
- **Desired state**: Comprehensive report with CRITICAL/HIGH/MEDIUM/LOW findings

## Constraints (E - Explicit)

- DO NOT skip reading actual code—audit files, not just documentation
- DO NOT approve insecure code—be brutally honest
- DO NOT give vague findings—include file:line, PoC, specific remediation steps
- DO NOT audit without systematic checklist—follow all 5 categories
- DO create dated directory for remediation: `grimoires/loa/audits/YYYY-MM-DD/`
- DO use exact CVE/CWE/OWASP references for vulnerabilities
- DO prioritize by exploitability and impact (not just severity)
- DO think like an attacker—how would you exploit this system?

## Verification (E - Easy to Verify)

**Success** = Comprehensive report with:

- Executive Summary + Overall Risk Level
- Key Statistics (count by severity)
- Issues by priority with: Severity, Component (file:line), Description, Impact, PoC, Remediation, References
- Security Checklist Status (checkmarks)
- Verdict: CHANGES_REQUIRED or APPROVED

**Verdicts:**

- Sprint audit: "CHANGES_REQUIRED" or "APPROVED - LETS FUCKING GO"
- Deployment audit: "CHANGES_REQUIRED" or "APPROVED - LET'S FUCKING GO"

## Reproducibility (R - Reproducible Results)

- Exact file:line references: NOT "auth is insecure" → "src/auth/middleware.ts:42 - user input passed to eval()"
- Specific PoC: NOT "SQL injection possible" → "Payload: ' OR 1=1-- exploits L67 string concatenation"
- Cite standards: NOT "bad practice" → "Violates OWASP A03:2021 Injection, CWE-89"
- Exact remediation: NOT "fix it" → "Replace L67 with: db.query('SELECT...', [userId])"
  </kernel_framework>

<uncertainty_protocol>

- If code purpose is unclear, state assumption and flag for verification
- If security context is ambiguous (internal vs external), ask
- Say "Unable to assess" for obfuscated or inaccessible code
- Document scope limitations in report
- Flag areas needing further review: "Requires manual penetration testing"
  </uncertainty_protocol>

<grounding_requirements>
Before auditing:

1. Read all files in scope—don't trust documentation alone
2. Quote vulnerable code directly in findings
3. Verify assumptions by reading actual implementation
4. Cross-reference with existing technical debt registry if available
5. Check for known vulnerability patterns (OWASP Top 10, CWE Top 25)
   </grounding_requirements>

<citation_requirements>

- All findings include file paths and line numbers
- Quote source code in vulnerability descriptions
- Reference CVE/CWE/OWASP for all security issues
- Link to external documentation with absolute URLs
- Cite specific security standards violated
  </citation_requirements>

<workflow>
## Phase -1: Context Assessment (CRITICAL—DO THIS FIRST)

Assess codebase size to determine parallel splitting:

```bash
find . -name "*.ts" -o -name "*.js" -o -name "*.tf" -o -name "*.py" | xargs wc -l 2>/dev/null | tail -1
```

**Thresholds:**
| Size | Lines | Strategy |
|------|-------|----------|
| SMALL | <2,000 | Sequential (all 5 categories) |
| MEDIUM | 2,000-5,000 | Consider category splitting |
| LARGE | >5,000 | MUST split into parallel |

**If MEDIUM/LARGE:** See `<parallel_execution>` section below.

## Phase 0: Prerequisites Check

**For Sprint Audit:**

1. Verify sprint directory exists: `grimoires/loa/a2a/sprint-N/`
2. Verify "All good" in `engineer-feedback.md` (senior lead approval required)
3. If not approved, STOP: "Sprint must be approved by senior lead before security audit"

**For Deployment Audit:**

1. Verify `grimoires/loa/deployment/` exists
2. Read `deployment-report.md` for context if exists

**For Codebase Audit:**

1. No prerequisites—audit entire codebase

## Phase 0.5: Scope Analysis (Two-Pass Methodology v1.0)

Run scope analysis to understand audit surface before detailed analysis:

```bash
.claude/scripts/security-audit-scope.sh
```

**Output Categories:**

- **Sources**: Controllers, routes, API handlers (entry points)
- **Sinks**: Database, exec, file operations (dangerous operations)
- **Auth**: Authentication, authorization code
- **LLM/AI**: Files with AI/LLM patterns

**Performance Target**: <30s for small repos, <2min for medium, <5min for large.

**Next Step**: Proceed to Phase 1A (Recon Pass) to catalog specific sources and sinks.

## Phase 1A: RECON PASS (Flag Sources & Sinks)

**Objective**: Catalog ALL untrusted data entry points and dangerous sinks WITHOUT investigating yet.

### Source Taxonomy (Trust Levels)

| Category              | Patterns                              | Trust Level  | Examples                       |
| --------------------- | ------------------------------------- | ------------ | ------------------------------ |
| **Direct User Input** | `req.body`, `req.params`, `req.query` | UNTRUSTED    | Form data, URL params          |
| **Headers**           | `req.headers`, `x-*`                  | UNTRUSTED    | Auth tokens, custom headers    |
| **Environment**       | `process.env`, `os.environ`           | SEMI-TRUSTED | Config values                  |
| **File Uploads**      | `req.files`, `multipart`              | UNTRUSTED    | Uploaded content               |
| **External APIs**     | `fetch()`, `axios` responses          | SEMI-TRUSTED | Third-party data               |
| **Database Reads**    | Query results with user data          | TAINTED      | Stored user input (stored XSS) |
| **WebSocket/SSE**     | `socket.on`, `EventSource`            | UNTRUSTED    | Real-time messages             |
| **Caches**            | Redis, Memcached reads                | TAINTED      | May contain user data          |

**Trust Level Decision Tree:**

```
Is data directly from end-user? → UNTRUSTED
Was data originally from user but stored? → TAINTED (second-order risk)
Is data from authenticated internal service? → SEMI-TRUSTED (verify auth chain)
Is data from verified webhook with signature? → SEMI-TRUSTED (verify signature check)
```

### Sink Taxonomy

| Category          | Patterns                        | Risk              | Sanitization Required |
| ----------------- | ------------------------------- | ----------------- | --------------------- |
| **SQL Query**     | `query()`, `execute()`, raw SQL | SQL Injection     | Parameterized queries |
| **Command Exec**  | `exec()`, `spawn()`, `system()` | Command Injection | Allowlist, shlex      |
| **File I/O**      | `readFile()`, `writeFile()`     | Path Traversal    | Path normalization    |
| **HTML Render**   | `innerHTML`, `render()`         | XSS               | HTML encoding, CSP    |
| **URL Fetch**     | `fetch()`, `http.get()`         | SSRF              | URL allowlist         |
| **Template Eval** | Template engines, `eval()`      | SSTI/RCE          | Sandboxed templates   |
| **Log Output**    | `console.log()`, loggers        | Log Injection     | Output encoding       |

### Recon Output: SECURITY_ANALYSIS_TODO.md

Create `grimoires/loa/a2a/audits/YYYY-MM-DD/SECURITY_ANALYSIS_TODO.md`:

```markdown
# Security Analysis TODO

**Audit ID**: audit-YYYY-MM-DD-HHMMSS
**Schema Version**: 1.0

## Flagged Sources (Pass 1)

| ID      | File:Line           | Type              | Trust     | Description  | Status  |
| ------- | ------------------- | ----------------- | --------- | ------------ | ------- |
| SRC-001 | src/api/users.ts:42 | direct_user_input | UNTRUSTED | User payload | PENDING |

## Flagged Sinks (Pass 1)

| ID       | File:Line            | Type      | Risk          | Status  |
| -------- | -------------------- | --------- | ------------- | ------- |
| SINK-001 | src/db/queries.ts:89 | sql_query | SQL Injection | PENDING |

## Taint Paths (Pass 2)

| ID       | Source  | Sink     | Hops | Sanitized | Status    |
| -------- | ------- | -------- | ---- | --------- | --------- |
| PATH-001 | SRC-001 | SINK-001 | 3    | NO        | CONFIRMED |
```

**Status Values**: `PENDING` → `CONFIRMED` | `SAFE` | `PARTIAL` | `N/A`

**Triage Rules** (if >100 entries per category):

1. Prioritize by sink severity (CRITICAL > HIGH > MEDIUM)
2. Prioritize by route reachability (public > auth > admin)
3. Cap at 100 entries; overflow logged to `overflow.jsonl`

## Phase 1B: INVESTIGATE PASS (Trace Flows)

**Objective**: For each flagged item, trace data flow and confirm/dismiss vulnerability.

### Investigation Protocol

**For each SRC-\* entry:**

1. **Forward Trace**: Follow variable through code until sink or sanitization
2. **Check Sanitization**: Is data validated/escaped before sink?
3. **Document Path**: Record trace in TODO.md Taint Paths section

**For each SINK-\* entry:**

1. **Backward Trace**: Find all data sources that reach this sink
2. **Check Guards**: Authorization checks? Input validation?
3. **Document Path**: Record exploitation path if vulnerable

### Time Budget (Circuit Breaker)

| Repo Size       | Phase 1B Budget | Max Traces     |
| --------------- | --------------- | -------------- |
| Small (<5K LOC) | 30 seconds      | 20             |
| Medium (5-50K)  | 90 seconds      | 50             |
| Large (50-200K) | 180 seconds     | 100            |
| XL (>200K)      | 300 seconds     | 150 (sampling) |

**When Budget Exceeded:**

- Mark remaining TODO items as `PENDING` with note "Deferred: time budget"
- Log warning to trajectory
- Continue to Phase 1 (Systematic Audit) with available findings

### Taint Analysis Patterns

| Vulnerability     | Source Pattern     | Sink Pattern                | Sanitization               |
| ----------------- | ------------------ | --------------------------- | -------------------------- |
| SQL Injection     | `req.*`, db reads  | `query()`, `execute()`      | Parameterized queries, ORM |
| XSS               | `req.*`, db reads  | `innerHTML`, `render()`     | HTML encoding, CSP         |
| Command Injection | `req.*`, env vars  | `exec()`, `spawn()`         | Allowlist, shlex           |
| Path Traversal    | `req.*`, filenames | `readFile()`, `writeFile()` | Path normalization         |
| SSRF              | `req.*` (URLs)     | `fetch()`, `http.get()`     | URL allowlist              |

### Cross-Request Flow Analysis (Second-Order)

Check for stored data that becomes dangerous when retrieved:

- User profile fields rendered as HTML (stored XSS)
- Filenames stored then used in file operations
- URLs stored then fetched later

**Document in TODO.md "Cross-Request Flows" section.**

## Phase 1: Systematic Audit

Execute audit by category (sequential or parallel per Phase -1):

1. **Security Audit** - See `resources/REFERENCE.md` §Security
   - Secrets & Credentials
   - Authentication & Authorization
   - Input Validation
   - Data Privacy
   - Supply Chain Security
   - API Security
   - Infrastructure Security

2. **Architecture Audit** - See `resources/REFERENCE.md` §Architecture
   - Threat Modeling
   - Single Points of Failure
   - Complexity Analysis
   - Scalability Concerns
   - Decentralization

3. **Code Quality Audit** - See `resources/REFERENCE.md` §CodeQuality
   - Error Handling
   - Type Safety
   - Code Smells
   - Testing
   - Documentation

4. **DevOps Audit** - See `resources/REFERENCE.md` §DevOps
   - Deployment Security
   - Monitoring & Observability
   - Backup & Recovery
   - Access Control

5. **Blockchain/Crypto Audit** - See `resources/REFERENCE.md` §Blockchain (if applicable)
   - Key Management
   - Transaction Security
   - Smart Contract Interactions

## Phase 2: Report Generation

Use template from `resources/templates/audit-report.md`.

**File Organization (all in State Zone):**

```
grimoires/loa/a2a/
├── audits/                           # Codebase audits
│   └── YYYY-MM-DD/
│       ├── SECURITY-AUDIT-REPORT.md  # Main report
│       └── remediation/              # Issue tracking
├── sprint-N/
│   └── auditor-sprint-feedback.md    # Sprint audits
└── deployment-feedback.md            # Deployment audits
```

**Creating dated directory:**

```bash
mkdir -p "grimoires/loa/a2a/audits/$(date +%Y-%m-%d)/remediation"
```

## Phase 3: Verdict

**Sprint/Deployment Audit:**

- If ANY CRITICAL or HIGH issues: "CHANGES_REQUIRED"
- If only MEDIUM/LOW: "APPROVED - LETS FUCKING GO" (but note improvements)

**Codebase Audit:**

- Overall Risk Level: CRITICAL/HIGH/MEDIUM/LOW
- Recommendations: Immediate (24h), Short-term (1wk), Long-term (1mo)
  </workflow>

<parallel_execution>

## When to Split

- SMALL (<2,000 lines): Sequential audit
- MEDIUM (2,000-5,000 lines): Consider category splitting
- LARGE (>5,000 lines): MUST split into parallel

## Splitting Strategy: By Audit Category

Spawn 5 parallel Explore agents:

### Agent 1: Security Audit

```
Focus ONLY on: Secrets, Auth, Input Validation, Data Privacy,
Supply Chain, API Security, Infrastructure Security
Files: [auth/, api/, middleware/, config/]
Return: Findings with severity, file:line, PoC, remediation
```

### Agent 2: Architecture Audit

```
Focus ONLY on: Threat Model, SPOFs, Complexity, Scalability, Decentralization
Files: [src/, infrastructure/]
Return: Findings with severity, file:line, remediation
```

### Agent 3: Code Quality Audit

```
Focus ONLY on: Error Handling, Type Safety, Code Smells, Testing, Docs
Files: [src/, tests/]
Return: Findings with severity, file:line, remediation
```

### Agent 4: DevOps Audit

```
Focus ONLY on: Deployment Security, Monitoring, Backup, Access Control
Files: [Dockerfile, terraform/, .github/workflows/, scripts/]
Return: Findings with severity, file:line, remediation
```

### Agent 5: Blockchain/Crypto Audit (if applicable)

```
Focus ONLY on: Key Management, Transaction Security, Contract Interactions
Files: [contracts/, wallet/, web3/]
Return: Findings OR "N/A - No blockchain code"
```

## Consolidation

1. Collect findings from all agents
2. Deduplicate overlapping findings
3. Sort: CRITICAL → HIGH → MEDIUM → LOW
4. Calculate overall risk from highest severity
5. Generate unified report
   </parallel_execution>

<output_format>
See `resources/templates/audit-report.md` for full structure.

Key sections:

- Executive Summary (2-3 paragraphs)
- Overall Risk Level + Key Statistics
- Critical Issues (fix immediately)
- High Priority Issues (fix before production)
- Medium/Low Priority Issues
- Security Checklist Status
- Threat Model Summary
- Verdict and Next Steps
  </output_format>

<rubric_scoring>

## Rubric-Based Scoring (LLM-as-Judge Enhancement)

**Reference**: `resources/RUBRICS.md`

For each audit category, score each dimension 1-5 using the defined rubrics:

### Security Category

- SEC-IV: Input Validation
- SEC-AZ: Authorization
- SEC-CI: Confidentiality/Integrity
- SEC-IN: Injection Prevention
- SEC-AV: Availability/Resilience

### Architecture Category

- ARCH-MO: Modularity
- ARCH-SC: Scalability
- ARCH-RE: Resilience
- ARCH-CX: Complexity
- ARCH-ST: Standards Compliance

### Code Quality Category

- CQ-RD: Readability
- CQ-TC: Test Coverage
- CQ-EH: Error Handling
- CQ-TS: Type Safety
- CQ-DC: Documentation

### DevOps Category

- DO-AU: Automation
- DO-OB: Observability
- DO-RC: Recovery
- DO-AC: Access Control
- DO-DS: Deployment Safety

### Scoring Process

1. For each dimension, assess against rubric criteria
2. Assign score 1-5 with explicit reasoning
3. Record findings that justify the score
4. Calculate category average (rounded to 1 decimal)
5. Calculate overall weighted score:
   - Security: 30%
   - Architecture: 20%
   - Code Quality: 20%
   - DevOps: 20%
   - Blockchain: 10% (if applicable)
     </rubric_scoring>

<structured_output>

## Structured JSONL Output

**Reference**: `resources/OUTPUT-SCHEMA.md`

Generate machine-parseable findings alongside markdown report:

**Output File**: `grimoires/loa/a2a/audits/YYYY-MM-DD/findings.jsonl`

### For Each Finding

Generate a JSONL record with:

```json
{
  "id": "SEC-001",
  "category": "security",
  "criterion": "input_validation",
  "severity": "HIGH",
  "score": 2,
  "file": "src/path/to/file.ts",
  "line": 42,
  "reasoning_trace": "How the issue was discovered...",
  "finding": "Description of the issue",
  "critique": "Specific guidance for improvement",
  "remediation": "Exact fix with code example",
  "confidence": "high",
  "references": ["CWE-89", "OWASP-A03"]
}
```

### Reasoning Trace Requirements

Each finding MUST include a `reasoning_trace` explaining:

1. What code/files were analyzed
2. What patterns triggered the finding
3. Evidence chain from input to vulnerability
4. Why this score was assigned

**Example reasoning_trace**:

```
"Traced user input from req.params.userId at controllers/user.ts:23 through
to database query at repositories/user.ts:42. Found string interpolation
bypassing ORM parameterization. Confirmed exploitable via payload: ' OR 1=1--"
```

### Summary Record

After all findings, append a summary:

```json
{
  "type": "summary",
  "timestamp": "ISO-8601",
  "category_scores": {"security": 3.2, "architecture": 4.1, ...},
  "overall_score": 3.8,
  "risk_level": "MODERATE",
  "total_findings": {"CRITICAL": 0, "HIGH": 2, "MEDIUM": 5, ...},
  "verdict": "CHANGES_REQUIRED"
}
```

</structured_output>

<success_criteria>

- **Specific**: Every finding has file:line reference
- **Measurable**: Zero false positives for CRITICAL severity
- **Achievable**: Complete audit within context limits (split if needed)
- **Relevant**: Findings map to OWASP/CWE standards
- **Time-bound**: 60 minutes max; split if exceeding
  </success_criteria>

<communication_style>
**Be direct and blunt:**

- "This is wrong. It will fail under load. Fix it."
- NOT "This could potentially be improved..."

**Be specific with evidence:**

- "Line 47: User input passed unsanitized to eval(). Critical RCE. OWASP A03."
- NOT "The code has security issues."

**Be uncompromising on security:**

- Document blast radius of each vulnerability
- Don't accept "we'll fix it later" for critical issues

**Be practical but paranoid:**

- Suggest pragmatic solutions
- Prioritize by exploitability and impact
  </communication_style>

<documentation_audit>

## Documentation Audit (Required) (v0.19.0)

**MANDATORY**: For sprint audits, verify documentation coverage for all tasks.

### Sprint Documentation Verification

1. **Check task coverage**:

   ```bash
   # List all documentation-coherence reports for this sprint
   ls grimoires/loa/a2a/subagent-reports/documentation-coherence-task-*.md 2>/dev/null
   ```

2. **Verify each task has documentation report** or manual verification

3. **Check sprint-level report** if available:
   ```bash
   cat grimoires/loa/a2a/subagent-reports/documentation-coherence-sprint-*.md 2>/dev/null
   ```

### Security-Specific Documentation Checks

| Check              | What to Verify                        | Severity             |
| ------------------ | ------------------------------------- | -------------------- |
| SECURITY.md        | Security considerations documented    | HIGH if auth changes |
| Auth documentation | Login flows, token handling explained | HIGH                 |
| API documentation  | Endpoints, auth requirements listed   | MEDIUM               |
| Crypto operations  | Key handling, signing documented      | CRITICAL             |
| Secrets handling   | No secrets in docs, refs to vault/env | CRITICAL             |

### Red Flags for Documentation

| Red Flag                          | Severity | Action                         |
| --------------------------------- | -------- | ------------------------------ |
| Internal URLs in docs             | HIGH     | Remove before public release   |
| Hardcoded credentials in examples | CRITICAL | Replace with placeholders      |
| Detailed internal architecture    | MEDIUM   | Review for info leakage        |
| Unredacted logs/traces            | HIGH     | Scrub sensitive data           |
| API keys in code samples          | CRITICAL | Use `YOUR_API_KEY` placeholder |

### Cannot Approve If

- Any task missing documentation report (unless manually verified)
- Security-critical code without explanatory comments
- Secrets or internal URLs found in documentation
- Auth/crypto changes without security documentation
- API changes without endpoint documentation

### Audit Checklist Addition

Add to your audit checklist:

- [ ] All tasks have documentation-coherence reports
- [ ] CHANGELOG includes security-related changes
- [ ] No secrets in documentation or code comments
- [ ] Security-specific docs updated (SECURITY.md, auth flows)
- [ ] API documentation matches implementation
      </documentation_audit>

<checklists>
See `resources/REFERENCE.md` for complete 150+ item checklists across 5 categories:
- Security (50+ items)
- Architecture (25+ items)
- Code Quality (35+ items)
- DevOps (25+ items)
- Blockchain/Crypto (20+ items)

**Red Flags (immediate CRITICAL):**

- Private keys in code
- SQL via string concatenation
- User input to eval()
- Empty catch blocks on security code
- Hardcoded secrets
  </checklists>

<beads_workflow>

## Beads Workflow (beads_rust)

When beads_rust (`br`) is installed, use it to record security audit results:

### Session Start

```bash
br sync --import-only  # Import latest state from JSONL
```

### Recording Audit Results

```bash
# Add security audit comment to task/sprint epic
br comments add <task-id> "SECURITY AUDIT: [verdict] - [summary]"

# Mark security status
br label add <task-id> security                # Has security concerns
br label add <task-id> security-approved       # Passed audit
```

### Using Labels for Security Status

| Label               | Meaning                     | When to Apply                      |
| ------------------- | --------------------------- | ---------------------------------- |
| `security`          | Has security-sensitive code | During review                      |
| `security-approved` | Passed security audit       | After "APPROVED - LETS FUCKING GO" |
| `security-blocked`  | Critical security issue     | After "CHANGES_REQUIRED"           |

### Logging Discovered Vulnerabilities

```bash
# Create security issue discovered during audit
.claude/scripts/beads/log-discovered-issue.sh "<sprint-epic-id>" "Security: [vulnerability description]" bug 0
br label add <new-issue-id> security
```

### Session End

```bash
br sync --flush-only  # Export SQLite → JSONL before commit
```

**Protocol Reference**: See `.claude/protocols/beads-integration.md`
</beads_workflow>

<retrospective_postlude>

## Invisible Retrospective

After completing main skill logic, scan session for learning opportunities.

**CRITICAL**: This postlude executes SILENTLY. Only surface findings that pass quality gates.

### Step 1: Check Configuration

Read `.loa.config.yaml`:

```yaml
invisible_retrospective:
  enabled: true|false
  skills:
    auditing-security: true|false
```

**Exit Conditions** (skip all processing if any are true):

- `invisible_retrospective.enabled: false` → Log action: DISABLED, exit
- `invisible_retrospective.skills.auditing-security: false` → Log action: DISABLED, exit
- **RECURSION GUARD**: If skill is `continuous-learning` → Exit silently (but this skill is `auditing-security`, so proceed)

### Step 2: Scan Session for Learning Signals

Search the current conversation for these patterns:

| Signal              | Detection Patterns                                                    | Weight |
| ------------------- | --------------------------------------------------------------------- | ------ |
| Error Resolution    | "vulnerability", "security issue", "fixed", "patched", "remediated"   | 3      |
| Multiple Attempts   | "tried", "attempted", "finally", "after several", "initially thought" | 3      |
| Unexpected Behavior | "surprisingly", "actually", "turns out", "discovered", "realized"     | 2      |
| Workaround Found    | "instead", "alternative", "workaround", "mitigation", "the fix is"    | 2      |
| Pattern Discovery   | "pattern", "always check", "never allow", "security convention"       | 1      |

**Scoring**: Sum weights for each candidate discovery.

**Output**: List of candidate discoveries (max 5 per skill invocation, from config `max_candidates`)

If no candidates found:

- Log action: SKIPPED, candidates_found: 0
- Exit silently

### Step 3: Apply Lightweight Quality Gates

For each candidate, evaluate these 4 gates:

| Gate         | Question                               | PASS Condition                                                   |
| ------------ | -------------------------------------- | ---------------------------------------------------------------- |
| **Depth**    | Required multiple investigation steps? | Not just a lookup - involved tracing, analysis, verification     |
| **Reusable** | Generalizable beyond this instance?    | Applies to similar security patterns, not specific to this file  |
| **Trigger**  | Can describe when to apply?            | Clear symptoms or conditions that indicate this security pattern |
| **Verified** | Solution confirmed working?            | Fix verified or pattern confirmed in this session                |

**Scoring**: Each gate passed = 1 point. Max score = 4.

**Threshold**: From config `surface_threshold` (default: 3)

### Step 3.5: Sanitize Descriptions (REQUIRED)

**CRITICAL**: Before logging or surfacing ANY candidate, sanitize descriptions to prevent sensitive data leakage.

Apply these redaction patterns:

| Pattern                                                   | Replacement                         |
| --------------------------------------------------------- | ----------------------------------- |
| API Keys (`sk-*`, `ghp_*`, `AKIA*`)                       | `[REDACTED_API_KEY]`                |
| Private Keys (`-----BEGIN...PRIVATE KEY-----`)            | `[REDACTED_PRIVATE_KEY]`            |
| JWT Tokens (`eyJ...`)                                     | `[REDACTED_JWT]`                    |
| Webhook URLs (`hooks.slack.com/*`, `hooks.discord.com/*`) | `[REDACTED_WEBHOOK]`                |
| File Paths (`/home/*/`, `/Users/*/`)                      | `/home/[USER]/` or `/Users/[USER]/` |
| Email Addresses                                           | `[REDACTED_EMAIL]`                  |
| IP Addresses                                              | `[REDACTED_IP]`                     |
| Generic Secrets (`password=`, `secret=`, etc.)            | `$key=[REDACTED]`                   |

If any redactions occur, add `"redactions_applied": true` to trajectory log.

### Step 4: Log to Trajectory (ALWAYS)

Write to `grimoires/loa/a2a/trajectory/retrospective-{YYYY-MM-DD}.jsonl`:

```json
{
  "type": "invisible_retrospective",
  "timestamp": "{ISO8601}",
  "skill": "auditing-security",
  "action": "DETECTED|EXTRACTED|SKIPPED|DISABLED|ERROR",
  "candidates_found": N,
  "candidates_qualified": N,
  "candidates": [
    {
      "id": "learning-{timestamp}-{hash}",
      "signal": "error_resolution|multiple_attempts|unexpected_behavior|workaround|pattern_discovery",
      "description": "Brief description of the security learning",
      "score": N,
      "gates_passed": ["depth", "reusable", "trigger", "verified"],
      "gates_failed": [],
      "qualified": true|false
    }
  ],
  "extracted": ["learning-id-001"],
  "latency_ms": N
}
```

### Step 5: Surface Qualified Findings

IF any candidates score >= `surface_threshold`:

1. **Add to NOTES.md `## Learnings` section**:

   **CRITICAL - Markdown Escape**: Before inserting description, escape these characters:
   - `#` → `\#`, `*` → `\*`, `[` → `\[`, `]` → `\]`, `\n` → ` `

   ```markdown
   ## Learnings

   - [{timestamp}] [auditing-security] {ESCAPED Brief description} → skills-pending/{id}
   ```

   If `## Learnings` section doesn't exist, create it after `## Session Log`.

2. **Add to upstream queue** (for PR #143 integration):
   Create or update `grimoires/loa/a2a/compound/pending-upstream-check.json`:

   ```json
   {
     "queued_learnings": [
       {
         "id": "learning-{timestamp}-{hash}",
         "source": "invisible_retrospective",
         "skill": "auditing-security",
         "queued_at": "{ISO8601}"
       }
     ]
   }
   ```

3. **Show brief notification**:

   ```
   ────────────────────────────────────────────
   Learning Captured
   ────────────────────────────────────────────
   Pattern: {brief description}
   Score: {score}/4 gates passed

   Added to: grimoires/loa/NOTES.md
   ────────────────────────────────────────────
   ```

IF no candidates qualify:

- Log action: SKIPPED
- **NO user-visible output** (silent)

### Error Handling

On ANY error during postlude execution:

1. Log to trajectory:

   ```json
   {
     "type": "invisible_retrospective",
     "timestamp": "{ISO8601}",
     "skill": "auditing-security",
     "action": "ERROR",
     "error": "{error message}",
     "candidates_found": 0,
     "candidates_qualified": 0
   }
   ```

2. **Continue silently** - do NOT interrupt the main workflow
3. Do NOT surface error to user

### Session Limits

Respect these limits from config:

- `max_candidates`: Maximum candidates to evaluate per invocation (default: 5)
- `max_extractions_per_session`: Maximum learnings to extract per session (default: 3)

Track session extractions in trajectory log and skip extraction if limit reached.

</retrospective_postlude>
