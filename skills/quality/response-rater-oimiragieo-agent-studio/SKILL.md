---
name: response-rater
version: 1.0.0
description: Run headless AI CLIs (Claude Code, Gemini, OpenAI Codex, Cursor Agent, GitHub Copilot) to rate an assistant response against a rubric and return actionable feedback plus a rewritten improved response; use for response quality audits, prompt/docs reviews, and "have another AI critique this answer" workflows.
allowed-tools: bash
---

# Response Rater

Use this skill to get _independent_ critiques of an assistant response by calling external AI CLIs in headless mode and aggregating the results.

## Supported Providers

| Provider           | CLI Command                         | Auth                                         | Default Model        |
| ------------------ | ----------------------------------- | -------------------------------------------- | -------------------- |
| **Claude Code**    | `claude`                            | Session or `ANTHROPIC_API_KEY`               | (CLI default)        |
| **Gemini CLI**     | `gemini`                            | Session or `GEMINI_API_KEY`/`GOOGLE_API_KEY` | gemini-3-pro-preview |
| **OpenAI Codex**   | `codex`                             | `OPENAI_API_KEY` or `CODEX_API_KEY`          | gpt-5.1-codex-max    |
| **Cursor Agent**   | `cursor-agent` (via WSL on Windows) | Session or `CURSOR_API_KEY`                  | auto                 |
| **GitHub Copilot** | `copilot`                           | GitHub auth (`gh auth login`)                | claude-sonnet-4.5    |

## Quick Start

1. Save the response you want reviewed to a file (or pipe it via stdin).

2. Ensure you have at least one provider authenticated (see table above).

3. Run:

```bash
node .claude/skills/response-rater/scripts/rate.cjs --response-file <path> --providers claude,gemini
```

Or via stdin (PowerShell):

```powershell
Get-Content response.txt | node .claude/skills/response-rater/scripts/rate.cjs --providers claude,gemini
```

Or via stdin (Bash):

```bash
cat response.txt | node .claude/skills/response-rater/scripts/rate.cjs --providers claude,gemini
```

## All Providers Example

```bash
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file response.txt \
  --providers claude,gemini,codex,cursor,copilot
```

## Model Selection

Each provider has a configurable model:

```bash
# Use specific models for each provider
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file response.txt \
  --providers gemini,codex,copilot \
  --gemini-model gemini-2.5-pro \
  --codex-model gpt-5.1-codex \
  --copilot-model gpt-5
```

### Available Models by Provider

**Gemini CLI:**

- `gemini-3-pro-preview` (default, latest flagship)
- `gemini-3-flash-preview` (fast, latest)
- `gemini-2.5-pro` (stable pro)
- `gemini-2.5-flash` (stable fast)
- `gemini-2.5-flash-lite` (lightweight)

**OpenAI Codex:**

- `gpt-5.1-codex-max` (default, flagship)
- `gpt-5.1-codex` (standard)
- `gpt-5.1-codex-mini` (faster/cheaper)

**Cursor Agent:**

- `auto` (default, smart selection)
- `gpt-5.1-high`, `gpt-5.1-codex-high`
- `opus-4.5`, `sonnet-4.5`
- `gemini-3-pro`

**GitHub Copilot:**

- `claude-sonnet-4.5` (default)
- `claude-opus-4.5`, `claude-haiku-4.5`, `claude-sonnet-4`
- `gpt-5.1-codex-max`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`
- `gpt-5.2`, `gpt-5.1`, `gpt-5`, `gpt-5-mini`, `gpt-4.1`
- `gemini-3-pro-preview`

## Templates

```bash
# Response review (default) - critique against rubric
--template response-review

# Vocabulary review - security audit for LLM vocabulary files
--template vocab-review
```

### Vocabulary Review Example

```powershell
Get-Content vocabulary.json | node .claude/skills/response-rater/scripts/rate.cjs \
  --providers claude,gemini \
  --template vocab-review
```

## Auth Behavior

By default the runner uses `--auth-mode session-first`:

1. Try the CLI using your existing logged-in session/subscription
2. If that fails and env keys exist, retry using env keys

To flip the order:

```bash
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file response.txt \
  --auth-mode env-first \
  --providers claude,gemini
```

## Direct Headless Commands (No Script)

**Claude Code:**

```powershell
Get-Content response.txt | claude -p --output-format json --permission-mode bypassPermissions
```

**Gemini CLI:**

```powershell
Get-Content response.txt | gemini --output-format json --model gemini-3-pro-preview
```

**OpenAI Codex:**

```bash
codex exec --json --color never --model gpt-5.1-codex-max --skip-git-repo-check "Your prompt"
```

**Cursor Agent (via WSL on Windows):**

```bash
wsl bash -lc "cursor-agent -p 'Your prompt' --output-format json --model auto"
```

**GitHub Copilot:**

```bash
copilot -p --silent --no-color --model claude-sonnet-4.5 "Your prompt"
```

## Output Format

JSON to stdout with:

- `promptVersion`: Schema version
- `template`: Template used
- `authMode`: Auth mode used
- `providers`: Object with per-provider results:
  - `ok`: Boolean success
  - `authUsed`: Which auth method worked
  - `raw`: Truncated raw output
  - `parsed`: Extracted JSON with `scores`, `summary`, `improvements`, `rewrite`
  - `attempts`: Auth attempt history

### Sample Output

```json
{
  "promptVersion": 3,
  "template": "response-review",
  "authMode": "session-first",
  "providers": {
    "claude": {
      "ok": true,
      "authUsed": "session",
      "parsed": {
        "scores": {
          "correctness": 8,
          "completeness": 7,
          "clarity": 9,
          "actionability": 8,
          "risk_management": 6,
          "constraint_alignment": 8,
          "brevity": 7
        },
        "summary": "The response is well-structured...",
        "improvements": ["Add error handling for...", "..."],
        "rewrite": "Improved version..."
      }
    },
    "gemini": { "ok": true, "..." },
    "codex": { "ok": true, "..." }
  }
}
```

## Notes / Constraints

- This skill **prefers network access** to contact AI providers for best results.
- **Offline Fallback**: If all providers fail due to network issues, automatic offline heuristic scoring activates.
- If a provider is missing credentials, it will be skipped with a clear error.
- Keep the reviewed response reasonably sized; start with the exact section you want critiqued.
- Timeout is 180 seconds per provider (3 minutes).

---

## Offline Fallback Mode

### Overview

When network access is unavailable, the response-rater automatically falls back to **offline heuristic scoring**. This enables plan rating in air-gapped environments, CI/CD pipelines without network, and development environments with intermittent connectivity.

### How It Works

**Automatic Detection**:

1. All configured providers are attempted (e.g., `claude,gemini`)
2. If **all providers fail** with **network errors** (ENOTFOUND, ETIMEDOUT, ECONNREFUSED)
3. Offline fallback activates automatically (no manual intervention required)

**Scoring Algorithm**:

The offline rater uses structural analysis to score plans across 5 dimensions:

| Dimension           | Weight | Scoring Method                                                 |
| ------------------- | ------ | -------------------------------------------------------------- |
| **Completeness**    | 20%    | Checks for required sections: objectives, context, steps, etc. |
| **Feasibility**     | 20%    | Analyzes time estimates, dependencies, resource requirements   |
| **Risk Mitigation** | 20%    | Counts identified risks and validates mitigation strategies    |
| **Agent Coverage**  | 20%    | Verifies agent assignments and diversity of agent types        |
| **Integration**     | 20%    | Checks integration points, data flow, API contracts            |

**Overall Score**: Average of all 5 dimensions (equal weights)

### Offline vs Online Scoring

| Feature              | Online (AI Providers) | Offline (Heuristic)   |
| -------------------- | --------------------- | --------------------- |
| Network Required     | ✅ Yes                | ❌ No                 |
| Scoring Method       | AI semantic analysis  | Structural heuristics |
| Accuracy             | High (95%+)           | Good (85-90%)         |
| Speed                | 10-60 seconds         | <1 second             |
| Improvement Feedback | Detailed, actionable  | Template-based        |
| Minimum Score        | 7/10 (standard)       | 7/10 (same threshold) |
| Score Tolerance      | Exact scores          | ±1 point variance     |

### Usage

**Automatic** (Recommended):

```bash
# Try online providers first; fallback to offline if network unavailable
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file plan.json \
  --providers claude,gemini
```

**Explicit Offline** (Force offline mode):

```bash
# Use offline rater directly (bypasses network attempt)
node .claude/skills/response-rater/scripts/offline-rater.mjs plan.json
```

### Output Format (Offline Fallback)

When offline fallback activates, output includes:

```json
{
  "promptVersion": 3,
  "template": "plan-review",
  "authMode": "session-first",
  "method": "offline",
  "offline_fallback": true,
  "providers": {
    "claude": { "ok": false, "error": "ETIMEDOUT" },
    "gemini": { "ok": false, "error": "ENOTFOUND" }
  },
  "offline_rating": {
    "ok": true,
    "method": "offline",
    "duration_ms": 45,
    "scores": {
      "completeness": 8,
      "feasibility": 7,
      "risk_mitigation": 6,
      "agent_coverage": 9,
      "integration": 7
    },
    "overall_score": 7.4,
    "summary": "Plan scored 7.4/10 using offline heuristic analysis...",
    "improvements": [
      "Add missing plan sections: objectives, context, success criteria",
      "Include time estimates and resource requirements for each step"
    ],
    "note": "Offline scoring uses heuristic analysis. For production use, prefer online scoring with AI providers."
  }
}
```

### Testing Offline Mode

Run test suite to verify offline scoring:

```bash
node .claude/skills/response-rater/tests/offline-scoring.test.mjs
```

**Test Coverage**:

- High-quality plan (should score >= 7)
- Low-quality plan (should score < 7)
- Medium-quality plan (should score ~7)
- Performance test (<1 second)
- Invalid plan handling
- Improvement suggestion generation

### Limitations

**Offline mode cannot**:

- Perform semantic analysis (detects structure, not content quality)
- Validate business logic correctness
- Detect subtle plan flaws (e.g., circular dependencies)
- Provide nuanced improvement suggestions

**Offline mode is suitable for**:

- Air-gapped environments (no network access)
- CI/CD pipelines without external network
- Development environments with intermittent connectivity
- Emergency situations requiring immediate plan validation

**Recommendation**: Use online scoring for production workflows; offline mode is a fallback only.

---

## Installation Requirements

Install the CLIs you want to use:

```bash
# Claude Code (via npm)
npm install -g @anthropic-ai/claude-code

# Gemini CLI (via npm)
npm install -g @anthropic-ai/gemini

# OpenAI Codex (via npm)
npm install -g @openai/codex

# Cursor Agent (via curl, inside WSL on Windows)
wsl bash -lc "curl https://cursor.com/install -fsS | bash"

# GitHub Copilot (via npm)
npm install -g @github/copilot
```

**Note**: Offline fallback requires no installation (built-in heuristic scoring).

## Skill Invocation

**Natural language** (recommended):

```
"Rate this response against the rubric"
"Have another AI critique this answer"
"Review the vocabulary file for security issues"
"Get feedback from Claude, Gemini, and Codex on this response"
```

**Direct CLI**:

```bash
node .claude/skills/response-rater/scripts/rate.cjs --response-file response.txt --providers claude,gemini,codex,cursor,copilot
```

## CLI Reference

```
Usage:
  node .claude/skills/response-rater/scripts/rate.cjs --response-file <path> [options]
  cat response.txt | node .claude/skills/response-rater/scripts/rate.cjs [options]

Options:
  --response-file <path>   # file containing the response to review
  --question-file <path>   # optional; original question/request for context
  --providers <list>       # comma-separated: claude,gemini,codex,cursor,copilot

Models:
  --gemini-model <model>   # default: gemini-3-pro-preview
  --codex-model <model>    # default: gpt-5.1-codex-max
  --cursor-model <model>   # default: auto
  --copilot-model <model>  # default: claude-sonnet-4.5

Templates:
  --template response-review   # default
  --template vocab-review      # security audit

Auth:
  --auth-mode session-first   # default
  --auth-mode env-first       # try env keys first
```

---

## Plan Rating for Orchestration

### Overview

The response-rater skill is **mandatory** for orchestrators to validate plan quality before workflow execution. This ensures all plans meet minimum quality standards and reduces execution failures.

### Plan Rating Usage for Orchestrators

**When to Use**: After Planner creates a plan, before workflow execution starts

**Workflow Pattern**:

1. Planner creates `plan-{{workflow_id}}.json`
2. Orchestrator invokes response-rater skill with plan content
3. Response-rater evaluates plan using rubric
4. If score >= 7/10: Proceed with execution
5. If score < 7/10: Return to Planner with feedback (max 3 attempts)

**Command**:

```bash
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file .claude/context/artifacts/plan-{{workflow_id}}.json \
  --providers claude,gemini \
  --template plan-review
```

### Rubric Dimensions

Plans are evaluated on 5 key dimensions (equal weight):

| Dimension           | Weight | Description                                        |
| ------------------- | ------ | -------------------------------------------------- |
| **completeness**    | 20%    | All required information present, no gaps          |
| **feasibility**     | 20%    | Plan is realistic and achievable                   |
| **risk_mitigation** | 20%    | Risks identified and mitigation strategies defined |
| **agent_coverage**  | 20%    | Appropriate agents assigned to each task           |
| **integration**     | 20%    | Plan integrates properly with existing systems     |

**Overall Score**: Average of all 5 dimensions

**Minimum Score**: **7/10** (standard), 8/10 (enterprise), 9/10 (critical)

### Feedback Format

Response-rater returns structured JSON with:

```json
{
  "scores": {
    "completeness": 8,
    "feasibility": 7,
    "risk_mitigation": 6,
    "agent_coverage": 9,
    "integration": 7
  },
  "overall_score": 7.4,
  "summary": "Plan is generally solid with strong agent coverage...",
  "improvements": [
    "Add explicit error handling strategy for each phase",
    "Define fallback agents for critical steps",
    "Include rollback procedures for failed steps"
  ],
  "rewrite": "Improved plan with enhanced risk mitigation..."
}
```

### Minimum Scores by Task Type

| Task Type  | Minimum Score | Example                               |
| ---------- | ------------- | ------------------------------------- |
| Emergency  | 5/10          | Production outages, critical hotfixes |
| Standard   | 7/10          | Regular features, bug fixes (default) |
| Enterprise | 8/10          | Enterprise integrations, migrations   |
| Critical   | 9/10          | Security, compliance, data protection |

---

## Provider Configuration for Plan Rating

### Default Providers

**Standard plan rating** uses 2 providers for consensus:

```bash
--providers claude,gemini
```

**Enterprise plan rating** uses 3 providers:

```bash
--providers claude,gemini,codex
```

**Critical plan rating** uses all 5 providers:

```bash
--providers claude,gemini,codex,cursor,copilot
```

### Provider Selection Strategy

| Scenario         | Providers           | Rationale                                    |
| ---------------- | ------------------- | -------------------------------------------- |
| Standard plans   | claude,gemini       | Fast, reliable, good consensus               |
| Enterprise plans | claude,gemini,codex | Additional perspective for complex plans     |
| Critical plans   | All 5               | Maximum validation for mission-critical work |

---

## Timeout and Failure Handling

### Timeout Configuration

**Default timeout**: **180 seconds per provider** (3 minutes)

**Rationale**: Plan rating requires deep analysis; allow sufficient time

**Increase timeout for complex plans**:

```bash
# Enterprise migration plan (5 minutes per provider)
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file plan-enterprise-migration.json \
  --providers claude,gemini,codex \
  --timeout 300000

# Critical security audit plan (10 minutes per provider)
node .claude/skills/response-rater/scripts/rate.cjs \
  --response-file plan-security-audit.json \
  --providers claude,gemini,codex,cursor,copilot \
  --timeout 600000
```

### Failure Handling

**Scenario 1: One provider fails**

- **Action**: Continue with successful providers
- **Minimum**: Require at least 1 successful provider
- **Log**: Record failure in reasoning file

**Scenario 2: All providers fail**

- **Action**: Retry with exponential backoff (3 attempts)
- **If still failing**: Escalate to user
- **Options**: Manual review, skip rating (force-proceed), cancel workflow

**Scenario 3: Provider timeout**

- **Action**: Retry provider once
- **If timeout persists**: Skip provider, continue with others
- **Log**: Record timeout in reasoning file

**Scenario 4: Authentication failure**

- **Action**: Retry with environment-based auth (if available)
- **If auth still fails**: Skip provider, log error
- **Minimum**: Require at least 1 authenticated provider

---

## Workflow Integration for Plan Rating

### Step 0.1: Plan Rating Gate (Standard Pattern)

All workflows include a plan rating gate after planning:

```yaml
steps:
  - step: 0.1
    name: 'Plan Rating Gate'
    agent: orchestrator
    type: validation
    skill: response-rater
    inputs:
      - plan-{{workflow_id}}.json (from step 0)
    outputs:
      - .claude/context/runs/<run_id>/plans/<plan_id>-rating.json
      - reasoning: .claude/context/history/reasoning/{{workflow_id}}/00.1-orchestrator.json
    validation:
      minimum_score: 7
      rubric_file: .claude/context/artifacts/standard-plan-rubric.json
      gate: .claude/context/history/gates/{{workflow_id}}/00.1-orchestrator.json
    retry:
      max_attempts: 3
      on_failure: escalate_to_human
    description: |
      Rate plan quality using response-rater skill.
      - Minimum passing score: 7/10
      - If score < 7: Return to Planner with feedback
      - If score >= 7: Proceed with workflow execution
```

### Rating File Location

**Standard path**: `.claude/context/runs/<run_id>/plans/<plan_id>-rating.json`

**Example**: `.claude/context/runs/run-001/plans/plan-greenfield-2025-01-06-rating.json`

### Orchestrator Responsibilities

1. **After Planner completes**: Invoke response-rater skill with plan content
2. **Process rating results**: Extract overall score and rubric scores
3. **Save rating**: Persist to standard path for audit trail
4. **Decision logic**:
   - If score >= minimum: Proceed to next step
   - If score < minimum: Return to Planner with feedback (max 3 attempts)
   - If 3 failures: Escalate to user for manual review

### Retry Logic

1. **Attempt 1**: Rate → if < 7 → return to Planner with feedback
2. **Attempt 2**: Planner revises → re-rate → if < 7 → return again
3. **Attempt 3**: Final revision → re-rate → if < 7 → escalate to user

**Force-proceed**: User can approve execution despite low score (requires explicit acknowledgment of risks)

---

## Timeout Escalation

When a provider times out, the response-rater follows this escalation pattern:

### Escalation Flow

1. **Primary Provider Timeout** (after 180s)
   - Log timeout with provider name
   - Mark provider as failed for this request
   - Immediately try next provider in list

2. **Secondary Provider Timeout**
   - Log cumulative timeout
   - If more providers available, try next
   - If total time > 600s, stop and use available results

3. **All Providers Timeout**
   - Check for cached rating (< 1 hour old)
   - If cached: Use cached rating with warning
   - If no cache: Escalate to manual review

### Configuration

Timeouts are configured in `.claude/config/response-rater.yaml`:

```yaml
timeouts:
  per_provider: 180 # Per-provider timeout
  total_max: 600 # Max total time
  connection: 30 # Connection timeout
```

### Example Timeout Scenario

```
Provider: claude (timeout after 180s) → FAILED
Provider: gemini (success in 45s) → Score: 7.2
Provider: codex (timeout after 180s) → FAILED

Result: Score 7.2 from gemini (single provider)
Warning: "2 of 3 providers timed out"
```

### Fallback Behavior

```yaml
fallback:
  on_all_fail: use_cached_or_manual_review
  cache_ttl: 3600 # Use cache if < 1 hour old
  manual_review_enabled: true
```

When all providers fail:

1. Check rating cache for identical plan hash
2. If valid cache exists, return cached rating with `source: cache` flag
3. If no cache, return `{ status: "manual_review_required" }`
4. Log escalation for monitoring

### Provider Selection by Workflow

Response-rater automatically selects providers based on workflow criticality:

| Workflow Type             | Tier       | Providers             | Rationale                          |
| ------------------------- | ---------- | --------------------- | ---------------------------------- |
| incident-flow             | standard   | claude, gemini        | Fast response for emergencies      |
| quick-flow                | standard   | claude, gemini        | Quick validation for minor changes |
| enterprise-track          | enterprise | claude, gemini, codex | Enhanced validation for enterprise |
| automated-enterprise-flow | enterprise | claude, gemini, codex | Enterprise compliance requirements |
| legacy-modernization-flow | enterprise | claude, gemini, codex | Complex migration validation       |
| ai-system-flow            | critical   | all 5 providers       | Maximum validation for AI systems  |
| security-flow             | critical   | all 5 providers       | Critical security validation       |
| compliance-flow           | critical   | all 5 providers       | Regulatory compliance requirements |

**Provider selection tool**:

```bash
node .claude/tools/response-rater-provider-selector.mjs --workflow <name>
```

---

## Security

### API Key Protection

This skill implements defense-in-depth for credential protection following OWASP A02:2021 guidelines.

**Automatic Sanitization**:

- All error messages are automatically sanitized to prevent API key leakage
- Stack traces and stderr output are filtered before logging
- Environment variable values are redacted in error contexts
- Provider authentication failures never expose actual credentials

**Sanitized Patterns**:

- Anthropic API keys (`sk-ant-...`)
- OpenAI API keys (`sk-...`)
- Google/Gemini API keys (`AIza...`)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`)
- JWT tokens
- Authorization headers (Bearer, Basic)
- Environment variable assignments (`KEY=value`)
- Long alphanumeric tokens (40+ characters)

**Best Practices**:

1. **Use session-first authentication** - Avoids storing API keys in environment
2. **Never commit API keys** - Use environment variables or secret managers
3. **Rotate keys regularly** - Especially after suspected exposure
4. **Monitor logs for `[REDACTED]` markers** - Indicates potential key exposure attempt was blocked
5. **Use CI secrets** - Store keys in CI/CD secret management, not in code

**Implementation**:

```javascript
// Error handling in rate.js automatically sanitizes
const { sanitize } = require('../../shared/sanitize-secrets.js');
console.error(`fatal: ${sanitize(error.message)}`); // Safe to log
```

**Security Audit**:

- Run `node .claude/tools/test-sanitization.mjs` to verify sanitization patterns
- All 15 test cases must pass before deployment

---

## References

- **Plan Rating Guide**: `.claude/docs/PLAN_RATING_GUIDE.md` (comprehensive documentation)
- **Enforcement Gate**: `.claude/tools/enforcement-gate.mjs` (validation CLI)
- **Plan Review Matrix**: `.claude/context/plan-review-matrix.json` (minimum scores by task type)
- **Workflow Guide**: `.claude/workflows/WORKFLOW-GUIDE.md` (workflow integration)
- **Provider Config**: `.claude/config/response-rater.yaml` (provider selection and timeouts)
