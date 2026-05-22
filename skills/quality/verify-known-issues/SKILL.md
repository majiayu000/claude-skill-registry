---
name: verify-known-issues
description: Verify claims about known issues in libraries or tools. Use when about to state something is a "known issue", "known bug", or "known limitation".
version: 1.0.0
---

# Verify Known Issues

## Trigger

This skill activates when Claude is about to say ANY of these patterns:

- "This is a known issue with..."
- "This is a known bug in..."
- "This is a known limitation of..."
- "This is a known problem with..."
- "There's a known issue..."
- "This is a documented issue..."
- "This is a common issue with..."
- "This is a recognized bug..."

## Why This Exists

Claude may hallucinate "known issues" that don't exist. Claims about external software bugs, library limitations, or platform issues MUST be verified before stating them as fact.

## Required Workflow

### Step 1: STOP Before Claiming

Do NOT write "This is a known issue" until verification is complete.

### Step 2: Web Search Verification

Use WebSearch to find evidence:

```
Search queries to try:
- "[library/tool name] [error message] known issue"
- "[library/tool name] [behavior] bug github"
- "[library/tool name] [version] issue"
- "site:github.com [library] [error] issue"
```

### Step 3: Evaluate Evidence

Evidence MUST include at least ONE of:
- GitHub issue with multiple confirmations
- Official documentation mentioning the limitation
- Stack Overflow answer with significant upvotes
- Official bug tracker entry
- Release notes acknowledging the bug

### Step 4: Sub-Agent Consensus

Launch a verification agent to review the evidence:

```
Use Task tool with subagent_type="general-purpose":
- Provide the claim you want to make
- Provide the evidence URLs found
- Ask: "Does this evidence support claiming this is a 'known issue'?"
```

### Step 5: Report with Citations

If verified, state the claim WITH citations:

```markdown
This is a known issue with [X].

Evidence:
- [GitHub Issue #123](url) - Reported by N users
- [Official docs](url) - Documents this limitation
```

If NOT verified, rephrase:

```markdown
I encountered [behavior]. I couldn't find documentation
confirming this is a known issue, so it may be:
- A configuration problem
- An edge case
- A misunderstanding on my part

Let me investigate further...
```

## Decision Tree

```
About to claim "known issue"?
    │
    ▼
┌─────────────────────────────┐
│ STOP - Do not write claim   │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ WebSearch for evidence      │
│ (3+ different queries)      │
└─────────────────────────────┘
    │
    ▼
Found credible sources?
    │
    ├─► NO ──► Rephrase as observation, not fact
    │
    ▼ YES
┌─────────────────────────────┐
│ Launch verification agent   │
│ with evidence context       │
└─────────────────────────────┘
    │
    ▼
Agent confirms?
    │
    ├─► NO ──► Rephrase as observation
    │
    ▼ YES
┌─────────────────────────────┐
│ State claim WITH citations  │
└─────────────────────────────┘
```

## Examples

### BAD (Before This Skill)

```
Claude: "This is a known issue with Python 3.14's asyncio
module where get_event_loop() is deprecated."
```

No evidence provided. May be hallucinated.

### GOOD (After This Skill)

```
Claude: Let me verify this before claiming it's a known issue...

[WebSearch: "python 3.14 asyncio get_event_loop deprecated"]

Found:
- PEP 594: Confirms deprecation
- Python docs: Documents new pattern
- GitHub cpython#12345: Migration guide

[Verification agent confirms evidence]

Claude: "This is a known issue with Python 3.14 -
`get_event_loop()` was deprecated per PEP 594.

Evidence: [PEP 594](url), [Python Docs](url)

The fix is to use `asyncio.run()` or create an explicit loop."
```

## Exceptions

This skill does NOT apply to:
- Errors you just observed and reproduced yourself
- Issues you personally verified in the current session
- Statements about Claude's own limitations
- General programming concepts (not external tool bugs)

## Anti-Patterns

| Don't | Do |
|-------|-----|
| "This is a known issue" (no source) | Search first, cite sources |
| Skip verification for "obvious" bugs | All external claims need evidence |
| Cite memory alone | Fresh search required |
| Single unverified source | Multiple sources or official docs |
| Trust outdated information | Check issue is still open/relevant |

## Checklist

- [ ] Identified trigger phrase ("known issue", "known bug", etc.)
- [ ] Performed 3+ web searches with different queries
- [ ] Found credible evidence (GitHub, official docs, etc.)
- [ ] Launched verification sub-agent with context
- [ ] Sub-agent confirmed evidence supports claim
- [ ] Included citations in final statement
- [ ] If unverified, rephrased as observation
