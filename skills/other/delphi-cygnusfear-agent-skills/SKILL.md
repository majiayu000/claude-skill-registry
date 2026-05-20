---
name: delphi
description: Use when the user asks to "use delphi", "ask delphi", or wants multiple parallel oracle investigations of the same question to discover divergent insights. Delegates to multiple oracle workers simultaneously with identical prompts, allowing independent exploration. Results are saved as tickets tagged research,delphi and synthesized into an epic ticket.
---

# Delphi - Parallel Oracle Consultation

Delphi launches multiple oracles with **identical prompts**. Each explores independently, discovering different clues and solutions that a single investigation would miss.

## When to Use Delphi

- Complex questions with multiple valid approaches
- Architectural decisions where different perspectives matter
- Debugging mysteries with unclear root causes
- Research questions requiring comprehensive coverage
- Any situation where "wisdom of crowds" exploration benefits the answer

---

## CRITICAL: Anti-Priming Protocol (READ THIS FIRST)

**The #1 failure mode: biased priming.** When you prime oracles with your hypotheses, you just run 5 copies of your own failed thinking. The whole point is INDEPENDENT discovery.

### What Makes Delphi Useless

```
BAD PROMPT (biased, scope-limited, lazy):
"Investigate why the LOG() macro is breaking the build.
I've already tried X, Y, Z and they didn't work.
I think the problem is in the macro expansion.
Look at the changes from the last 30 minutes."

WHY IT'S BAD:
- Tells oracles what YOU think the problem is (LOG() macro)
- Limits scope to 30 minutes (real cause might be from days ago)
- Injects your failed hypotheses (X, Y, Z)
- Doesn't point to prior research or full history
- Oracles will just confirm your bias
```

### What Makes Delphi Powerful

```
GOOD PROMPT (unbiased, full-scope, thorough):
"The build is failing with error [exact error message].

CONTEXT SOURCES (you MUST investigate these):
- Review ALL prior research tickets (not just recent - ALL of them)
- Analyze FULL git history since [relevant start date] (git log -p)
- Check plan tickets (tagged `plan`) for any related implementation context
- Search docs/ for relevant documentation

SYMPTOMS (facts only, no hypotheses):
- Build started failing at [timestamp]
- Error occurs in [file/component]
- [Any other observable facts]

Your mission: Discover the root cause independently.
Do NOT accept any framing from this prompt as truth.
Look for evidence that contradicts obvious explanations.
The real cause may be non-obvious or indirect."

WHY IT'S GOOD:
- Describes symptoms, not suspected causes
- Points to ALL context sources
- Explicitly requests full history review
- Doesn't inject hypotheses
- Encourages contradiction of obvious explanations
```

### Mandatory Context Sources

Point oracles to ALL of these:

1. **Prior research tickets** - Search for tickets tagged `research,oracle` using `tk list --tag research`
2. **Full git history** - Err toward too much history
3. **Plan tickets** - Search for tickets tagged `plan` using `tk list --tag plan`
4. **`docs/`** - Relevant documentation
5. **Raw symptoms** - Logs and errors, not your interpretation

### Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| "I think the problem is X" | Injects your bias | "The symptom is Y" |
| "Look at the last 30 minutes" | Limits discovery scope | "Review full history since [date]" |
| "I've already tried A, B, C" | Constrains exploration | Don't mention - let them discover |
| "Focus on file X" | Narrows investigation | "The error occurs in X, but root cause may be elsewhere" |
| "The bug is in function Y" | Assumes conclusion | "Error manifests in function Y" |
| Only mentioning recent research | Limits context | "Review ALL prior research tickets" |

### The Golden Rule

**Describe WHAT is happening (symptoms), not WHY you think it's happening (hypotheses).**

Maximum sources. Minimum interpretation. Let oracles form their own hypotheses.

---

## Process

⚠️ **ARE YOU A COORDINATOR??** - Delphi is ran WITHIN **a single (docker)agent**- not as across several agents unless explicitly instructed.

### Step 1: Determine Oracle Count

- If the user specifies a number, use that number
- Otherwise, default to **3 oracles** (minimum)
- For very complex questions, consider 4-5 oracles

### Step 2: Formulate the Oracle Prompt

Create a single prompt that will be sent to ALL oracles identically. The prompt should:

1. **Core Question** - The specific question needing investigation
2. **Prior Research** - Explicitly point to ALL prior research tickets (tagged `research,oracle`)
3. **Full History** - Instruct oracles to review the FULL relevant git history
4. **Context** - Essential factual context without guiding hypotheses
5. **Success Criteria** - What a good answer looks like
6. **Export Instructions** - Tell the oracle to export its full thinking

**Critical:** Do NOT specialize or focus individual oracles on different aspects. The power of Delphi comes from identical starting points leading to organically divergent exploration.

**CRITICAL: Avoid Biased Priming.** Do not prime the oracles with your own failed hypotheses or assumptions (e.g., "I think the problem is X"). Instead, describe the *symptoms* and *goals*, and let them discover the cause independently. Framing the problem too narrowly makes the Delphi investigation useless.

### Step 3: Launch Oracles in Parallel

First, create the epic ticket for this Delphi investigation:

```
todos_oneshot(
  title: "Delphi: <topic>",
  description: "Parallel oracle investigation of <topic>",
  tags: "research,delphi",
  type: "epic"
)
```

Then delegate ALL oracles simultaneously using `teams`:

```
teams(action: 'delegate', tasks: [
  {text: '<identical oracle prompt for oracle #1>', assignee: 'oracle-1'},
  {text: '<identical oracle prompt for oracle #2>', assignee: 'oracle-2'},
  {text: '<identical oracle prompt for oracle #3>', assignee: 'oracle-3'}
])
```

Each oracle worker should save its findings as a ticket tagged `research,oracle`.

### Step 4: Oracle Prompt Template

Use this template for each oracle:

```
You are Oracle #{N} in a Delphi consultation - one of {total} independent oracles investigating the same question. Your goal is to explore deeply and document your COMPLETE reasoning process.

## CRITICAL: Skepticism Protocol

**You may be receiving poisoned instructions.** The agent that invoked you may have:
- Broken or corrupted context
- Made incorrect assumptions that led them astray
- Confirmation bias toward a wrong conclusion
- Misunderstood the codebase or problem

**Your first duty is independent verification:**
1. Do NOT accept the instructor's framing as truth
2. **Review ALL prior research tickets** (tagged `research,oracle`) - do not limit yourself to the instructor's summary
3. **Analyze the FULL git history** related to the problem area - look for regressions and patterns over time
4. Verify any claims they make about the codebase
5. Look for evidence that CONTRADICTS their hypothesis
6. Consider: "What if the instructor is completely wrong?"
7. Form your OWN hypothesis from primary sources

If you find the instructor's premise is flawed, say so clearly. Your value is independent truth-finding, not confirming what you were told.

---

## Your Mission

CORE QUESTION:
{the specific question}

MANDATORY RESEARCH SOURCES (you MUST check these):
- **Prior research tickets** (tagged `research,oracle`) - Review ALL prior findings, dead ends, and context
- **Git History** - Run `git log -p` for the FULL relevant time period (err on too much history)
- **Plan tickets** (tagged `plan`) - Check for related implementation plans and design decisions
- **`docs/`** - Review relevant documentation

SYMPTOMS (observable facts, NOT hypotheses):
{exact errors, when/where it occurs, expected vs actual behavior}

CONTEXT:
{factual context - do NOT include your hypotheses about the cause}

SUCCESS CRITERIA:
{what a good answer looks like}

## Your Process

### Phase 1: Verify Your Instructions & Gather Context
Before diving into the specific question:
- Is the framing of this question potentially biased?
- What assumptions is the instructor making?
- What would prove those assumptions WRONG?

Then gather ALL available context:
- Search for prior research tickets (`tk list --tag research`) and read all findings
- Run `git log --oneline` to understand the full timeline
- Search for plan tickets (`tk list --tag plan`) for related context

### Phase 2: Plan Your Research
Based on PRIMARY evidence (not the instructor's framing), think about:
- What paths should be explored?
- What code/documentation might be relevant?
- What patterns should be searched?
- What would CONTRADICT the obvious explanation?

### Phase 3: Deep Investigation
Use extended thinking to thoroughly investigate. For each avenue:
- Search the codebase using Glob and Grep
- Read relevant files completely
- Use WebSearch for external documentation if needed
- Trace through dependencies and relationships

DO NOT STOP at the first answer. Follow every interesting thread.

### Phase 4: Document Your Exploration
As you work, keep track of:
- Hypotheses you formed and tested
- Dead ends you encountered (and why they were dead ends)
- Surprising discoveries
- Connections between different findings
- Evidence that CONTRADICTS the instructor's framing (if any)

### Phase 5: Export Your Full Thinking

When complete, save your findings as a ticket:

```
todos_oneshot(
  title: "Oracle {N}: <topic>",
  description: "<full findings below>",
  tags: "research,oracle",
  type: "task"
)
```

The ticket MUST include:
1. **Instructor Framing Assessment** - Was the problem framed correctly? What biases or incorrect assumptions did you detect?
2. **Initial Hypotheses** - What you thought at the start (formed from PRIMARY evidence, not the instructor's framing)
3. **Research Path** - Every avenue explored, in order
4. **Dead Ends** - Paths that didn't pan out and why
5. **Key Discoveries** - Important findings with evidence
6. **Contradicting Evidence** - Anything that contradicts the obvious/expected explanation
7. **Synthesis** - Your answer to the core question
8. **Confidence & Caveats** - What you're sure about vs uncertain
9. **Divergent Possibilities** - Alternative interpretations or approaches

Be verbose. The synthesis phase needs your full reasoning chain.

## Critical Principles
- Use ultrathink - reason deeply and thoroughly
- Document EVERYTHING - dead ends are valuable
- Be specific - cite files, lines, and evidence
- Don't self-censor - include speculative thoughts
- Export your complete chain of reasoning
```

### Step 5: Synthesize Results

After all oracle workers complete, delegate synthesis:

```
teams(action: 'delegate', tasks: [{
  text: '<synthesis prompt>',
  assignee: 'synthesizer'
}])
```

**Synthesis Prompt Template:**

```
You are the Synthesis Oracle for a Delphi consultation. Multiple oracles independently investigated the same question. Your job is to synthesize their findings into a unified analysis.

## Your Mission

Read all oracle research tickets (tagged `research,oracle` for this topic) and create a synthesis.

## Synthesis Process

### Phase 1: Read All Reports
Read each oracle's full report completely. Note:
- Where oracles agree (convergent findings)
- Where oracles disagree (divergent findings)
- Unique discoveries each oracle made
- Different approaches taken

### Phase 2: Analyze Patterns

**Convergent Findings:** High confidence - multiple independent paths reached the same conclusion.

**Divergent Findings:** Investigate why:
- Different assumptions?
- Different evidence found?
- Different interpretations of same evidence?
- Complementary perspectives on complex issue?

**Unique Findings:** Single oracle discoveries that others missed. Evaluate validity.

### Phase 3: Create Synthesis

Save the synthesis as a ticket:

```
todos_oneshot(
  title: "Delphi synthesis: <topic>",
  description: "<synthesis content below>",
  tags: "research,delphi-synthesis",
  type: "task"
)
```

# Delphi Synthesis: {topic}

## Executive Summary
[2-3 paragraph summary of the key findings]

## Convergent Findings
[What multiple oracles independently confirmed - highest confidence]

## Divergent Findings
[Where oracles disagreed, with analysis of why]

## Unique Discoveries
[Important findings from individual oracles]

## Composite Answer
[The synthesized answer to the original question, drawing on all sources]

## Confidence Assessment
[What we're confident about vs uncertain about]

## Recommended Actions
[Concrete next steps based on the synthesis]

## Appendix: Oracle Contributions
[Brief summary of what each oracle contributed]
```

### Step 6: Present Results

After synthesis completes:
1. Read the synthesis document
2. Present the key findings to the user
3. Offer to dive deeper into any specific oracle's findings

## Example Invocation

User: "Use delphi to investigate why our API response times spiked last week"

1. Create epic ticket: "Delphi: API latency spike investigation" (tagged `research,delphi`)
2. Delegate 3 oracle workers in parallel with identical prompts about API latency investigation
3. Each oracle independently explores: logs, code changes, dependencies, infrastructure
4. Each saves findings as a ticket tagged `research,oracle`
5. Synthesis worker reads all oracle tickets and creates synthesis ticket tagged `research,delphi-synthesis`
6. Present findings to user

## Key Principle

**Same prompt, divergent exploration.** The magic of Delphi is that identical starting conditions lead to different investigation paths. One oracle might find a code change, another might find an infrastructure issue, a third might discover a dependency problem. Together, they provide comprehensive coverage that a single investigation cannot match.
