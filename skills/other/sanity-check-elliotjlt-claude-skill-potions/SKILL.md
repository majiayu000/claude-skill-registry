---
name: sanity-check
description: |
  Before building on assumptions, validates them first. Activates when making
  claims about how code works, what exists, or why something happens. Prevents
  assumption cascades where one wrong guess leads to a completely wrong solution.
allowed-tools: |
  bash: grep, find, test
  file: read
---

# Sanity Check

<purpose>
Claude confidently builds on assumptions that turn out to be wrong. "The auth
middleware probably checks X" becomes a 50-line solution for a problem that
doesn't exist. This skill forces verification of key assumptions before
building on them.
</purpose>

## When To Activate

<triggers>
- Using words like "probably", "likely", "I assume", "should be"
- Explaining how code works without reading it
- Diagnosing a bug without reproducing it
- Making claims about what exists or doesn't exist
- Building a solution based on inferred behavior
- User asks "why is X happening?" and you're about to guess
</triggers>

## Instructions

### Identify Your Assumptions

Before proposing a solution, list what you're assuming:

```markdown
## Assumptions

1. [The function X exists and does Y]
2. [The error is caused by Z]
3. [This file is imported by W]
4. [The config value is set to V]
```

### Verify Before Building

<verify>
For each assumption, verify it:

| Assumption | Verification | Status |
|------------|--------------|--------|
| Function X does Y | Read the function | Verified / Wrong |
| Error caused by Z | Check error logs | Verified / Wrong |
| File imported by W | Grep for imports | Verified / Wrong |

**Stop if any key assumption is wrong.** Don't patch - reassess.
</verify>

### Types of Assumptions

**Existence assumptions:**
- "There's probably a config file for this"
- "The API endpoint likely exists"
- Verify: `find`, `grep`, `ls`

**Behavior assumptions:**
- "This function probably validates input"
- "The middleware likely checks auth"
- Verify: Read the actual code

**Causation assumptions:**
- "The error is probably from X"
- "This is likely failing because Y"
- Verify: Reproduce, check logs, trace execution

**State assumptions:**
- "The database probably has this column"
- "The env var is likely set"
- Verify: Check schema, check actual values

### The Assumption Cascade

```
Wrong assumption: "Auth is handled by middleware"
    ↓
Build solution: "Just call the protected endpoint"
    ↓
Solution fails: "Auth not working"
    ↓
Wrong diagnosis: "Middleware must be misconfigured"
    ↓
Deeper hole: "Let me fix the middleware..."
    ↓
Reality: Auth was in the route handler all along
```

Break the cascade early. Verify before building.

## Output Format

When working on non-trivial problems:

```markdown
## Sanity Check

**Key assumptions:**
1. [assumption] → Verified by [how]
2. [assumption] → Verified by [how]
3. [assumption] → ⚠️ NOT verified, checking...

**Proceeding with:** [list verified assumptions]
```

## NEVER

- Say "probably" or "likely" without then verifying
- Diagnose bugs without reproducing or checking logs
- Build multi-step solutions on unverified assumptions
- Explain code behavior without reading the code
- Assume error messages are accurate (verify root cause)

## ALWAYS

- List assumptions explicitly before building on them
- Verify existence before assuming something exists
- Read code before explaining what it does
- Reproduce issues before diagnosing them
- Stop and reassess when an assumption proves wrong

## Example

**User:** "The user signup isn't sending confirmation emails"

**Bad approach (assumption cascade):**
> "The email service probably isn't configured correctly. Let me check
> the SMTP settings... Actually, the email template might be wrong...
> Let me also check if the queue is processing..."

**Good approach (sanity check):**

```markdown
## Sanity Check

**Assumptions to verify:**
1. Signup actually triggers email sending
2. Email sending code exists and is called
3. Email service is configured
4. No errors in logs

**Verifying #1:**
Reading signup handler... Found: `sendConfirmationEmail(user)` on line 45.
Verified: signup does call email function.

**Verifying #2:**
Reading sendConfirmationEmail... Found: it calls `emailService.send()`.
But wait - there's a `if (config.emailEnabled)` check on line 12.

**Verifying #3:**
Checking config... `emailEnabled: false` in development.

**Root cause found:** Emails disabled in config, not a bug.
```

No assumption cascade. Verified each step. Found real cause.
