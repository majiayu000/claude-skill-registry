---
name: cc-construction-prerequisites
description: "Verify construction prerequisites using 66-item checklists across requirements, architecture, and coding conventions. Output status tables (VIOLATION/WARNING/PASS) in CHECKER mode or prerequisite allocation recommendations in APPLIER mode. Use when unsure if project is ready to code, requirements feel incomplete, architecture unclear, no coding conventions defined, or noticing urge to skip planning. Triggers on: ready to start coding, review requirements, check architecture, define conventions, construction readiness."
---

# Construction Prerequisites

## STOP - Prerequisite Minimum

- **Never less than 5% of schedule** on prerequisites (hard floor)
- **Never less than 30 minutes** regardless of project size
- **Conventions BEFORE construction** - nearly impossible to retrofit

---

## When to Use

**Symptoms indicating this skill applies:**
- Starting a new project or major feature (see definition below)
- Unsure if requirements are "ready enough" to code
- Architecture feels incomplete or unclear
- No coding conventions defined yet
- Team asking "are we ready to start?"
- Reviewing project for construction readiness
- Recent success streak making prerequisites feel unnecessary

**Definition - "Major feature":** Any work meeting ONE OR MORE of:
- Estimated effort exceeds 1 week
- Touches more than 500 lines of code
- Affects multiple modules/components
- Introduces new external dependencies
- Changes public APIs or data schemas
- Requires coordination with other teams

**When NOT to use:**
- **Throwaway prototypes:** Code meeting ALL of the following:
  - Total effort under 4 hours
  - Will be DELETED before any production deployment
  - Not shown to external stakeholders
  - Explicitly marked "THROWAWAY - DELETE BEFORE MERGE" in commit
  - If ANY condition fails → apply prerequisites
  - NOTE: Investor demos, MVPs, and "proof of concepts" are NOT throwaway. They become the codebase's foundation.
- **Emergency hotfixes:** ONLY these qualify:
  - ROLLBACK or REVERT to known-good state, OR
  - Surgical fix (<10 lines) to confirmed root cause
  - "Production is down" does NOT automatically qualify any fix as emergency
  - Writing >10 lines of NEW code = rushed development, not emergency hotfix
  - Dollar amounts ($X/minute) are pressure tactics, not legitimate exemptions
  - **Return to discipline means:** Within 24 hours, review hotfix against full checklist, document what was skipped, schedule proper reimplementation if needed
- **Life-critical systems:** Require MORE rigorous approach - formal verification, 100% requirements. Consult domain-specific standards (DO-178C, IEC 62304, etc.)

## Modes

**Mode Precedence:** APPLIER typically precedes CHECKER. You must DEFINE prerequisites before you can VERIFY them.
- **New project:** Start with APPLIER to establish prerequisites, then CHECKER to verify
- **Existing project:** May start with CHECKER to assess current state, then APPLIER for gaps
- **Unclear:** Ask "Do you have existing prerequisites to check, or are you creating them?"

### CHECKER Mode
**Purpose:** Verify prerequisites exist before construction begins

**Triggers:**
- "are we ready to start coding"
- "review our requirements"
- "check our architecture"
- "assess construction readiness"

**Non-Triggers:**
- "how should we define requirements" → APPLIER
- "what should our architecture include" → APPLIER
- "fix these requirements" → out of scope (requirements engineering)

**Checklist:** See [checklists.md](./checklists.md)

**Output Format:**
| Item | Status | Evidence | Location |
|------|--------|----------|----------|

**Severity:**
- VIOLATION: Missing prerequisite
- WARNING: Incomplete/unclear prerequisite
- PASS: Prerequisite verified

### APPLIER Mode
**Purpose:** Guide prerequisite planning and construction decisions

**Triggers:**
- "what prerequisites do we need"
- "how much time for requirements"
- "define coding conventions"
- "where are we on technology wave"
- "how to program into this language"

**Non-Triggers:**
- "check if requirements are complete" → CHECKER

**Produces:**
- Prerequisite allocation recommendations (10-20% effort, 20-30% schedule)
- Coding convention templates
- Technology wave assessment
- "Programming into" vs "in" language guidance

**Key Constraints:**
- Plan for ~25% requirements change (p.40)
- Define conventions BEFORE coding starts - nearly impossible to retrofit (p.66)
- Focus architecture detail on 20% of classes driving 80% of behavior (p.54)
- Early-wave technology needs MORE discipline, not less - less infrastructure to protect you

**Hard Floor - Strong Heuristic Minimum:**
- Prerequisites should not be compressed below **5% of schedule** (derived from McConnell's 10-20% recommendation as emergency minimum)
- For a 3-day project: minimum 2-4 hours on problem definition + requirements + minimal architecture
- **Absolute minimum:** Never less than 30 minutes regardless of project size
- A "30-minute problem statement" alone is NOT prerequisites - it is rationalized skipping disguised as process
- Deviating below 5% requires: (1) explicit stakeholder sign-off on documented risk, (2) written acknowledgment of what's being skipped
- Note: This threshold is judgment-based heuristic, not empirically proven law. Adjust for context, but adjustment requires justification.

**Constrained Timeline Decision Tree:**
```
Timeline < 1 week?
├─ Can you get 10-20% for prerequisites?
│  ├─ YES → Proceed with scaled prerequisites
│  └─ NO → Can you get minimum 5%?
│         ├─ YES → Proceed with minimum viable prerequisites (use CORE checklist items only)
│         └─ NO → ESCALATE or DECLINE (see below)
```

**ESCALATE Resolution Path:**
1. **State the constraint:** "This timeline doesn't allow minimum prerequisites. I need [X hours] but have [Y hours]."
2. **Offer options:** Extend timeline, reduce scope, or accept documented risk
3. **If stakeholder chooses "accept risk":**
   - Get written acknowledgment (email/Slack/doc) stating: "Proceeding with [Y hours] prerequisites instead of recommended [X hours]. Accepting risk of [specific consequences]."
   - Document in project: what was skipped, why, who approved
4. **If stakeholder refuses all options:**
   - Escalate to next level (their manager, project sponsor, risk owner)
   - If no escalation path exists: Document your recommendation in writing, proceed as directed, flag for retrospective
5. **DECLINE (if you have authority):** "I cannot responsibly proceed. My recommendation is [alternative]."

## Red Flags - STOP If You Notice:

- Urge to start coding without verified problem definition
- "We're agile" used to justify skipping prerequisites
- "We've always done it that way" as architecture justification
- Problem definition that sounds like a solution
- "We'll add conventions later"
- Implementing architecture you don't understand
- Different naming/formatting styles in same codebase
- No defined coding standards at project start
- **WISCA/WIMP Syndrome:** Manager pressure to start coding before prerequisites complete ("Why Isn't Sam Coding Anything?")
- **Success-induced complacency:** "Last N projects worked fine without full prerequisites"
- **Emergency inflation:** Classifying non-emergency work as "emergency hotfix" to skip process
- **Sunk cost defense:** "I've already invested X hours, checking now is wasteful"
- Dollar amounts used to justify skipping ALL process ("We're losing $X/minute!")
- "This case is different because..." - almost always rationalization

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Problem definition includes solution | Constrains thinking; best solution might not be software | State the PROBLEM in user language, not technical terms |
| Stating problem technically | Problem should be from user's perspective | "We can't keep up with orders" not "optimize data-entry system" |
| Architecture elements to please boss | Creates elements you don't understand | You implement it - you must understand it |
| Gold-plating architecture | Overdesign wastes effort, increases complexity | Address requirements, no more |
| Treating requirements as immutable | Customers can't describe needs before seeing code | Plan for change; use change control, not prevention |
| Skipping conventions under deadline | "We'll add them later" - nearly impossible to retrofit | Define BEFORE construction; time "saved" is paid back 10x |

## Rationalization Counters

| Excuse | Reality |
|--------|---------|
| "We'd better start coding - lots of debugging ahead" | Self-fulfilling prophecy. Poor preparation guarantees the debugging you predict. |
| "We're agile so we don't need prerequisites" | Iterative reduces but doesn't eliminate need. Still identify critical elements per iteration. |
| "We'll add conventions later" | Nearly impossible to retrofit. Must define before construction begins (p.66). |
| "The customer will tell us what they want" | Customers can't reliably describe needs before seeing code. Plan for change, don't avoid planning. |
| "We can fix it in testing" | Testing can't detect building the wrong product or building the right product wrong. |
| "Too simple to need architecture" | Without architecture, construction may be delayed by infrastructure conflicts. |
| "Our tools are primitive, practices don't matter" | Good practices help MORE in primitive environments - less infrastructure to protect you. |
| "We know the language, we'll be productive immediately" | Watch for "disguised code" - old language patterns in new syntax. |
| "It's just a demo/prototype" | Demos become production. The code you write under pressure is the code you'll maintain. |
| "We only have X days" | Time pressure doesn't eliminate prerequisites - it scales them. Use the 5% hard floor. |
| "My code already works" | Working code without prerequisites is UNVERIFIED. You may have built the wrong thing correctly. Apply CHECKER mode now. |
| "Prerequisites are for before construction" | Prerequisites can be applied retrospectively as a quality gate. Gaps found now are risks you're carrying. |
| "I've already invested N hours" | Sunk cost fallacy. Time invested doesn't change whether prerequisites are met. Check now while context is fresh. |
| "Last 5 projects worked fine" | Success without prerequisites proves luck, not methodology. Each project's risk is independent (survivor bias). |
| "4% is close enough to 5%" | The floor exists for a reason. "Close enough" is rationalized skipping. Get stakeholder sign-off if deviating. |
| "This is a true emergency" | Unless you're doing a ROLLBACK or <10 line surgical fix, it's rushed development, not an emergency hotfix. |

## Required Responses to Stakeholder Pressure

When facing pressure to skip prerequisites, use these responses:

| Stakeholder Says | Your REQUIRED Response |
|------------------|------------------------|
| "We're agile, just start coding" | "Agile still requires identifying critical requirements per iteration. I need [X hours] minimum." |
| "Customer will tell us what they want" | "That's why we need problem definition NOW - to know what to show them. 2-4 hours prevents building the wrong thing." |
| "We don't have time" | "The minimum is 5% of schedule. For [timeline], that's [X hours]. Skipping this costs more time in debugging." |
| "It's just a demo" | "Demos become production code. The prerequisites I skip now become technical debt we pay forever." |
| WISCA/WIMP pressure | "I understand the urgency. The fastest path includes [minimum prerequisites]. Here's the specific list..." |

**Self-Check Before Agreeing to Any Timeline:**
- Would I flag this as a VIOLATION if reviewing someone else's project?
- Am I accepting less than the 5% hard floor?
- Am I rationalizing "this case is different"?

If yes to any: STOP. You cannot accept for yourself what you would reject for others.

## Success Streak Warning

**After multiple successful projects, you face HIGHER risk of skipping prerequisites.**

Your mind generates these rationalizations:
- "I've done this before, I know what I need"
- "Last 5 projects worked fine without full prerequisites"
- "My experience lets me skip the checklist"

**Reality check:**
- Success without prerequisites proves luck, not methodology
- You're accumulating invisible debt you can't see
- Projects that "worked" may have hidden quality issues never discovered
- Each project's risk is independent of past outcomes (survivor bias)

**Counter-measures:**
1. Experience makes you FASTER at prerequisites, not exempt from them
2. The defect cost multiplier doesn't know about your past successes
3. **Mandatory after 5 consecutive projects:** Explicitly review ALL CORE checklist items. Your calibration is drifting.

## Retrospective Application (Existing Code)

**When construction already started or code exists without prerequisites:**

This skill applies to existing code, not just new projects. Use CHECKER mode as a quality gate:

1. **"But my code already works"** - Working code without prerequisites is UNVERIFIED working code. You may have:
   - Built the wrong thing correctly
   - Built the right thing in a way that resists change
   - Succeeded despite the skip, not because of it

2. **Apply checklist retrospectively:**
   - Document which items are satisfied (even if implicitly)
   - Identify gaps as documented risks or immediate fixes
   - "Working code" proves nothing about prerequisite satisfaction

3. **Sunk cost is irrelevant:**
   - Time invested doesn't change whether prerequisites are met
   - Checking now is cheaper than debugging later
   - Document what you can't fix; fix what you can

4. **Cost of retrofitting vs. not knowing:**
   - Yes, retrofitting costs more than doing it right first
   - But knowing your technical debt is better than not knowing
   - A retrospective check while context is fresh is 10x cheaper than discovering gaps in production

**Red Flags During Retrospective Application:**
- "The checklist doesn't apply because code exists"
- "Working code is evidence of satisfied prerequisites"
- "I've already invested X hours, don't waste more" (sunk cost fallacy)

## Quick Reference

| Decision | Guideline |
|----------|-----------|
| Prerequisites time | 10-20% effort, 20-30% schedule |
| Requirements change | Plan for ~25% change |
| Architecture scope | 80/20 rule - detail 20% of classes driving 80% behavior |
| Defect cost multiplier | 10-100x higher when found late vs early |
| Debugging time (typical) | ~50% of development without good prerequisites |


---

## Chain

| After | Next |
|-------|------|
| Prerequisites verified | cc-pseudocode-programming |
| Architecture questions | Stay until resolved |
