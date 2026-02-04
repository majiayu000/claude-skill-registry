---
name: judge-llm
description: Ultrathink LLM-as-Judge validation of completed work. Uses extended thinking by DEFAULT for thorough evaluation.
---

# /sw:judge-llm - Ultrathink LLM-as-Judge Validation

**ULTRATHINK BY DEFAULT** - Validate completed work using extended thinking and the LLM-as-Judge pattern.

## Implementation: Opus Model + Timeout Handling

**Model**: `opus` for deepest analysis
**Timeout**: 60 seconds default (configurable with `--timeout`)
**Progress Log**: `.specweave/logs/judge-llm.log`

Implementation in `src/core/skills/skill-judge.ts`:
- Uses Anthropic SDK with user's ANTHROPIC_API_KEY
- AbortController-based timeout to prevent stuck states
- Progress logging for visibility during evaluation
- Fallback to basic pattern matching if no API key

## CRITICAL: Extended Thinking is DEFAULT

This command ALWAYS uses **ultrathink (extended thinking)** for thorough LLM-as-Judge evaluation:

```
DEFAULT BEHAVIOR = ULTRATHINK MODE
- Extended thinking enabled
- Deep chain-of-thought reasoning
- Thorough multi-dimensional analysis
- ~60-90 seconds for comprehensive evaluation
- Uses Opus model for maximum quality
```

Use `--quick` only if you explicitly need faster (but less thorough) validation.

## Purpose

Use when you've completed work and want **maximum-quality AI validation**:
- Works on **any files** (not just SpecWeave increments)
- Uses **ultrathink extended thinking** for deepest analysis
- Returns **clear verdict** with detailed reasoning

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
/sw:judge-llm src/file.ts --timeout 120000   # 120 seconds
/sw:judge-llm src/file.ts --timeout 30000    # 30 seconds (faster cutoff)

# Additional options
/sw:judge-llm src/file.ts --strict   # Fail on any concern
/sw:judge-llm src/file.ts --fix      # Include fix suggestions
/sw:judge-llm src/file.ts --export   # Export report to markdown
/sw:judge-llm src/file.ts --verbose  # Show progress to console
```

## Visibility & Stuck Detection

Progress is **always logged** to `.specweave/logs/judge-llm.log`:

```
[2026-01-19T10:30:00.000Z] [0.0s] [INFO] Starting LLM Judge evaluation for domain: backend
[2026-01-19T10:30:00.001Z] [0.0s] [INFO] Task: Validate authentication implementation...
[2026-01-19T10:30:00.002Z] [0.0s] [INFO] Using model: opus
[2026-01-19T10:30:00.003Z] [0.0s] [INFO] Timeout: 60000ms
[2026-01-19T10:30:00.004Z] [0.0s] [PROGRESS] Sending request to Opus...
[2026-01-19T10:30:45.000Z] [45.0s] [PROGRESS] Response received, parsing...
```

**If evaluation gets stuck**:
1. Check `.specweave/logs/judge-llm.log` for last progress
2. Default timeout (60s) will abort if stuck
3. Increase timeout with `--timeout` if legitimately slow
4. Result will show `timedOut: true` if aborted

## How It Works

When you invoke `/sw:judge-llm`, Claude will:

### Step 1: Gather Input

Determine what to validate:
- If file paths provided → read those files
- If `--staged` → get staged git changes
- If `--last-commit` → get files from last commit
- If `--diff <branch>` → get diff against branch
- If no args → validate recent work in conversation context

### Step 2: ULTRATHINK Analysis (Default)

**MANDATORY**: Use extended thinking for deep LLM-as-Judge evaluation:

```
Claude MUST use ultrathink/extended thinking to:

1. **DEEP READ**: Thoroughly understand all code, context, and intent
2. **MULTI-DIMENSIONAL ANALYSIS**: Evaluate across ALL dimensions:
   - Correctness: Does it work exactly as intended?
   - Completeness: ALL edge cases handled? ALL requirements met?
   - Security: ANY vulnerabilities? OWASP Top 10 checked?
   - Performance: Algorithmic complexity? Memory usage? Bottlenecks?
   - Maintainability: Clean? Clear? Follows conventions?
   - Testability: Can it be tested? Are tests adequate?
   - Error handling: All failure modes covered?
3. **CRITICAL EVALUATION**: Weigh ALL findings by severity
4. **REASONED VERDICT**: Form verdict based on thorough analysis
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
🔴 CRITICAL: [title]
   [description]
   📍 [file:line]
   💡 [suggestion]

🟡 HIGH: [title]
   ...

🟢 LOW: [title]
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

## Validation Modes

### Default Mode (ULTRATHINK) - RECOMMENDED
- **Extended thinking ENABLED by default**
- Most thorough validation (~60-90 seconds)
- Deep multi-dimensional analysis
- Best for any completed work
- Cost: ~$0.10-0.25

### Quick Mode (`--quick`)
- Fast validation (~10-15 seconds)
- Standard reasoning (no extended thinking)
- Good for quick sanity checks during development
- Cost: ~$0.02-0.05

### Strict Mode (`--strict`)
- Any concern results in REJECTED
- Use for critical paths, security code, or CI gates
- Combines with ultrathink by default

## Examples

### Example 1: Default ultrathink validation

```
User: /sw:judge-llm src/core/auth/login.ts

Claude: [Uses extended thinking for deep analysis]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JUDGE-LLM VERDICT: APPROVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: ULTRATHINK (extended thinking)
Confidence: 0.91
Files Analyzed: 1

REASONING:
After thorough analysis with extended thinking:

The login implementation demonstrates excellent security practices:
- Password hashing uses bcrypt with cost factor 12 (appropriate)
- Rate limiting implemented correctly (5 attempts, 15 min exponential backoff)
- Input validation prevents SQL injection and XSS
- Error messages are generic (don't leak user existence)
- Session tokens use cryptographically secure random generation
- CSRF protection properly implemented

Edge cases handled:
- Empty input validation ✓
- Unicode normalization for usernames ✓
- Timing attack mitigation via constant-time comparison ✓

No security, performance, or maintainability issues found.

VERDICT: Production-ready implementation with excellent security posture.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example 2: Validate staged changes

```
User: /sw:judge-llm --staged

Claude: [Uses extended thinking]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JUDGE-LLM VERDICT: CONCERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: ULTRATHINK (extended thinking)
Confidence: 0.84
Files Analyzed: 3

REASONING:
Extended thinking analysis of staged changes reveals:

Positive aspects:
- New API endpoint follows existing patterns
- TypeScript types are correct
- Error handling present

However, thorough analysis found issues:

🟡 HIGH: Missing Input Validation
   User input passed to database without sanitization
   📍 src/api/users.ts:45
   💡 Add Zod schema validation:
   ```typescript
   const schema = z.object({ userId: z.string().uuid() });
   const { userId } = schema.parse(req.body);
   ```

🟡 HIGH: Information Disclosure Risk
   Stack traces exposed in error responses
   📍 src/api/users.ts:62
   💡 Use production error handler that sanitizes output

🟢 LOW: Missing rate limiting
   New endpoint has no rate limiting
   📍 src/api/users.ts:30
   💡 Add rate limiter middleware

VERDICT: Address HIGH issues before merging. LOW can be follow-up.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example 3: Quick validation (when needed)

```
User: /sw:judge-llm src/utils/format.ts --quick

Claude: [Standard reasoning, no extended thinking]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JUDGE-LLM VERDICT: APPROVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: QUICK (standard reasoning)
Confidence: 0.75
Files Analyzed: 1

REASONING:
Utility formatting functions look correct. No obvious issues.

VERDICT: Looks good for a utility file.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Simplest Usage

Just say in your prompt:
```
"judge-llm my work"
"use judge-llm"
"judge-llm this"
```

Claude will:
1. Automatically gather context from the conversation
2. Use ULTRATHINK extended thinking by default
3. Apply thorough LLM-as-Judge evaluation

## Difference from /sw:qa

| Aspect | `/sw:qa` | `/sw:judge-llm` |
|--------|-----------------|------------------------|
| **Scope** | Increments only | Any files |
| **Input** | Increment ID | Files, git diff, context |
| **Default Mode** | Standard | **ULTRATHINK** |
| **Pattern** | 7-dimension scoring | Judge LLM reasoning |
| **Focus** | Spec quality, risks | Code correctness |
| **When** | Before increment close | After any work |

## Best Practices

1. **Use by default**: Ultrathink is worth the extra time for quality
2. **Use `--staged`**: Validate before committing
3. **Use `--strict` for critical code**: Payment, auth, security
4. **Fix CRITICAL issues immediately**: Never ignore these
5. **Trust the ultrathink analysis**: Extended thinking catches subtle issues

## Limitations

- ❌ Doesn't execute tests (use test runners)
- ❌ Doesn't auto-apply fixes (only suggests)
- ❌ May miss domain-specific issues
- ❌ Not a replacement for human review

## Related

- `/sw:qa` - Increment-bound quality assessment
- `/sw:validate` - Rule-based increment validation
- `ado-sync-judge` agent - Uses judge pattern for sync validation
