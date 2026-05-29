# Human Gating Anti-Pattern Skill

> Version: 1.0.0
> Compiler: manual (bootstrap)
> Last Updated: 2026-01-22

Recognize and avoid using humans as proxies for automatable verification tasks.

## When to Activate

Use this skill when:
- About to ask user to test something
- About to ask user to click something
- About to ask user for a screenshot
- About to ask user to verify UI
- Tempted to write "please check if"

## Core Principles

### 1. Humans Are Not CI Systems
Every request to a human for verification is a context switch for them and a blocking wait for you.

*Humans have better things to do than be button-clicking proxies for AI agents.*

### 2. Recognize the Pattern
Before asking a human to do something, ask yourself - could a script do this?

*Most verification tasks feel like they need humans but are actually automatable.*

### 3. The Ratio Matters
Time spent writing automation vs time saved by not asking humans tips heavily toward automation after 2-3 iterations.

*One click feels fast; ten iterations of one click is slow.*

### 4. Respect Human Attention
Human attention is precious and finite; spend it only on tasks that genuinely require judgment.

*Good agent-human collaboration reserves humans for what only humans can do.*

---

## Workflow

### Phase 1: Recognize

Identify when you are about to human-gate.

1. Notice phrases like "please test this", "can you check if", "click this and tell me"
2. Notice when you are waiting for human confirmation to proceed
3. Notice when you are asking for verification of something that has a clear pass/fail

**Outputs:** Recognition that human-gating is about to occur

### Phase 2: Assess

Determine if the task is genuinely human-required.

1. Ask - is this a judgment call or a binary verification?
2. Ask - could I write a script to do this in under 5 minutes?
3. Ask - how many iterations might this require?
4. Ask - what am I actually asking the human to do?

**Outputs:** Classification (automatable vs genuinely human-required)

### Phase 3: Redirect

If automatable, redirect to autonomous testing instead.

1. Identify the right tool (Puppeteer, curl, script, etc.)
2. Write the verification test
3. Run it yourself
4. Report results with evidence

**Outputs:** Automated test execution, Evidence-backed result

### Phase 4: Escalate Properly

If genuinely human-required, escalate with full context.

1. Explain what you already tried and verified
2. Be specific about what subjective judgment you need
3. Provide screenshots/evidence gathered so far
4. Make the human task as minimal as possible

**Outputs:** Well-scoped request for human judgment

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Self-Verification Check** | About to type "please test" or "can you verify" | Pause and ask whether this could be automated | The pause creates space to redirect to better approaches |
| **Screenshot Instead of Ask** | Need to show something to the user | Take a screenshot programmatically and include it in your response | Shows the result without requiring human action |
| **Iteration Threshold** | Already asked human to verify something once | Automate before the second request | One iteration might be acceptable; two indicates a pattern that should be automated |
| **Evidence-First Escalation** | Must escalate to human for genuine judgment | Include all evidence gathered, attempts made, and specific question needing judgment | Respects human time by making their task as efficient as possible |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Button-Click Proxy** | Human becomes a test runner; slow, frustrating, breaks flow | Write Puppeteer script to click and verify |
| **Refresh-and-Check** | Human is doing what curl or a browser script could do | Automate the refresh and assertion |
| **Screenshot Request** | Async back-and-forth; manual image comparison | Take screenshot programmatically during automated test |
| **Manual Regression Testing** | Human is running a test suite manually | Write automated tests for each scenario |
| **Polling for Status** | Human is a glorified while-loop | Poll programmatically with appropriate waits |
| **Lazy Verification** | Short-term laziness becomes long-term inefficiency | Invest 2 minutes in automation; save 20 minutes of back-and-forth |

---

## Quality Checklist

Before completing:

- [ ] Recognized potential human-gating before acting on it
- [ ] Assessed whether the task is genuinely human-required
- [ ] If automatable, wrote and ran verification test instead
- [ ] If genuinely human-required, provided full context and minimal task scope
- [ ] Avoided asking for the same type of verification twice without automating

---

## Examples

**Verifying a CSS fix**

BAD: "I made the CSS change. Can you refresh the page and check if the button is now blue?"

GOOD: Write Puppeteer script that loads page, finds button, extracts computed style, asserts color is blue.

Report: "CSS fix applied. Automated test confirms button color is now #0066cc. Screenshot attached."

**Verifying an API endpoint**

BAD: "I fixed the endpoint. Can you try calling it and see if it returns 200?"

GOOD: Use curl or httpx to call the endpoint, assert status code, log response.

Report: "Endpoint fix deployed. curl confirms 200 response. Response body: {...}"

**Subjective design review (genuinely human-required)**

BAD: "Does this look good?" (too vague)

GOOD: "I've implemented the layout change. Here's a screenshot. Specific question: Is the spacing between these elements appropriate for the design system, or should it be adjusted? I verified it renders correctly on mobile and desktop (screenshots attached)."

---

## References

- Autonomous testing skill - for how to write verification tests
- Iterative debugging skill - for how to verify fixes
- Session insight - realized during Oracy debugging that asking human to repeatedly test UI was inefficient
