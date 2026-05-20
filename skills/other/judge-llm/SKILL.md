---
description: Ultrathink LLM-as-Judge validation of completed work. Uses extended thinking and Opus model for thorough, independent evaluation. Use when saying "judge my code", "judge-llm", "deep validate", or as part of /sw:done closure.
allowed-tools: Read, Grep, Glob, Bash
---

# Ultrathink LLM-as-Judge Validation

**ULTRATHINK BY DEFAULT** - Validate completed work using extended thinking and the LLM-as-Judge pattern. Provides an independent second opinion separate from `/sw:grill`.

## How It Differs from /sw:grill

| Aspect | `/sw:grill` | `/sw:judge-llm` |
|--------|-------------|-----------------|
| Execution | In-session (same context) | **Separate Opus API call** |
| Context | Shares conversation context | **Fresh context (no bias)** |
| Thinking | Standard reasoning | **Extended thinking / ultrathink** |
| Output | Confidence-scored findings | Structured verdict + score |
| Domain | Generic code review | **Built-in domain criteria** |

**Key value**: Independent perspective with fresh model context catches issues that in-session review may miss.

## Implementation

**TypeScript**: `src/core/skills/skill-judge.ts`
- Uses Anthropic SDK with user's `ANTHROPIC_API_KEY`
- AbortController-based timeout to prevent stuck states (default: 60s)
- Progress logging to `.specweave/logs/judge-llm.log`
- Fallback to basic pattern matching if no API key
- Domain-specific evaluation criteria (frontend, backend, mobile, infrastructure, testing, ML)

## Usage

```bash
# DEFAULT: Ultrathink validation (recommended)
/sw:judge-llm src/file.ts
/sw:judge-llm "src/**/*.ts"

# Validate git changes (ultrathink by default)
/sw:judge-llm --staged           # Staged changes
/sw:judge-llm --last-commit      # Last commit
/sw:judge-llm --diff main        # Diff vs branch

# Quick mode (ONLY if you need speed over thoroughness)
/sw:judge-llm src/file.ts --quick

# Timeout control (default: 60s)
/sw:judge-llm src/file.ts --timeout 120000

# Additional options
/sw:judge-llm src/file.ts --strict   # Fail on any concern
/sw:judge-llm src/file.ts --fix      # Include fix suggestions
/sw:judge-llm src/file.ts --export   # Export report to markdown
/sw:judge-llm src/file.ts --verbose  # Show progress to console
```

## External API Cost Consent (MANDATORY)

**This skill uses the Anthropic API directly (NOT your Claude Code subscription).** Each evaluation costs approximately $0.01-0.05 depending on code size.

**Before invoking the Anthropic API, you MUST check consent:**

1. Read `.specweave/config.json` → check `externalModels.consent` field
2. If `"always-allow"` → proceed silently
3. If `"never"` → skip API call, use in-session ultrathink evaluation instead
4. If `"ask"` (default):
   - Check if `"anthropic"` is in `externalModels.allowedProviders`
   - If YES → proceed silently (standing permission)
   - If NO → **ASK USER**: "Judge-LLM will call the Anthropic API using your ANTHROPIC_API_KEY. This costs ~$0.01-0.05 per evaluation. Proceed? (yes/no/always)"
     - "yes" → proceed this time only
     - "no" → skip API call, use in-session ultrathink instead
     - "always" → run: `grantStandingConsent('anthropic', projectRoot)` from `src/core/llm/consent.ts`, then proceed
5. No `ANTHROPIC_API_KEY` set → falls back to pattern matching automatically (no cost, no consent needed)

## Workflow

### Step 1: Gather Input

Determine what to validate:
- If file paths provided: read those files
- If `--staged`: get staged git changes
- If `--last-commit`: get files from last commit
- If `--diff <branch>`: get diff against branch
- If no args: validate recent work in conversation context

### Step 2: Ultrathink Analysis (Default)

Use extended thinking for deep LLM-as-Judge evaluation via the Opus model:

```
Claude MUST use ultrathink/extended thinking to:

1. DEEP READ: Thoroughly understand all code, context, and intent
2. MULTI-DIMENSIONAL ANALYSIS: Evaluate across ALL dimensions:
   - Correctness: Does it work exactly as intended?
   - Completeness: ALL edge cases handled? ALL requirements met?
   - Security: ANY vulnerabilities? OWASP Top 10 checked?
   - Performance: Algorithmic complexity? Memory usage? Bottlenecks?
   - Maintainability: Clean? Clear? Follows conventions?
   - Testability: Can it be tested? Are tests adequate?
   - Error handling: All failure modes covered?
3. CRITICAL EVALUATION: Weigh ALL findings by severity
4. REASONED VERDICT: Form verdict based on thorough analysis
```

### Step 3: Return Verdict

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JUDGE-LLM VERDICT: APPROVED | CONCERNS | REJECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: ULTRATHINK (extended thinking)
Confidence: 0.XX
Files Analyzed: N

REASONING:
[Detailed chain-of-thought from extended thinking]

ISSUES (if any):
  CRITICAL: [title]
   [description]
   [file:line]
   [suggestion]

  HIGH: [title]
   ...

  LOW: [title]
   ...

VERDICT: [summary sentence]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Verdict Meanings

| Verdict | Meaning | Action |
|---------|---------|--------|
| **APPROVED** | Work is solid, no significant issues | Safe to proceed |
| **CONCERNS** | Issues found worth addressing | Review and fix recommended |
| **REJECTED** | Critical issues found | MUST fix before proceeding |

## Visibility & Stuck Detection

Progress is **always logged** to `.specweave/logs/judge-llm.log`.

**If evaluation gets stuck**:
1. Check `.specweave/logs/judge-llm.log` for last progress
2. Default timeout (60s) will abort if stuck
3. Increase timeout with `--timeout` if legitimately slow
4. Result will show `timedOut: true` if aborted

## Related

- `/sw:grill` - Confidence-scored pre-ship quality gate (in-session)
- `/sw:validate` - Rule-based increment validation
- `/sw:done` - Increment closure (runs both grill and judge-llm)
