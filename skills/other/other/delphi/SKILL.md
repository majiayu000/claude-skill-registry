---
name: delphi
description: This skill should be used when the user asks to "use delphi", "ask delphi", or wants multiple parallel oracle investigations of the same question to discover divergent insights. Delphi launches multiple oracle agents simultaneously with identical prompts, allowing them to independently explore and potentially discover different paths, clues, and solutions. Results are saved to .oracle/[topic]/ and synthesized into a final document.
---

# Delphi - Parallel Oracle Consultation

Delphi launches multiple oracle agents in parallel with the **same prompt** to discover divergent paths of exploration. By giving identical starting points, each oracle independently explores the problem space, potentially discovering different clues, solutions, and insights that a single investigation might miss.

## When to Use Delphi

- Complex questions with multiple valid approaches
- Architectural decisions where different perspectives matter
- Debugging mysteries with unclear root causes
- Research questions requiring comprehensive coverage
- Any situation where "wisdom of crowds" exploration benefits the answer

## Process

⚠️ **ARE YOU A COORDINATOR??** - Delphi is ran WITHIN **a single (docker)agent**- not as across several agents unless explicitly instructed.

### Step 1: Determine Oracle Count

- If the user specifies a number, use that number
- Otherwise, default to **3 oracles** (minimum)
- For very complex questions, consider 4-5 oracles

### Step 2: Formulate the Oracle Prompt

Create a single prompt that will be sent to ALL oracles identically. The prompt should:

1. **Core Question** - The specific question needing investigation
2. **Context** - All relevant information from the user
3. **Success Criteria** - What a good answer looks like
4. **Export Instructions** - Tell the oracle to export its full thinking

**Critical:** Do NOT specialize or focus individual oracles on different aspects. The power of Delphi comes from identical starting points leading to organically divergent exploration.

### Step 3: Launch Oracles in Parallel

First, create the output directory:

```bash
mkdir -p .oracle/[topic]
```

Then dispatch ALL oracles simultaneously in a **single message with multiple Task calls**:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <identical oracle prompt for oracle #1>
)

Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <identical oracle prompt for oracle #2>
)

Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <identical oracle prompt for oracle #3>
)
// ... etc
```

### Step 4: Oracle Prompt Template

Use this template for each oracle:

```
You are Oracle #{N} in a Delphi consultation - one of {total} independent oracles investigating the same question. Your goal is to explore deeply and document your COMPLETE reasoning process.

## Your Mission

CORE QUESTION:
{the specific question}

CONTEXT:
{all relevant context}

SUCCESS CRITERIA:
{what a good answer looks like}

## Your Process

### Phase 1: Plan Your Research
Think about what needs investigation:
- What paths should be explored?
- What code/documentation might be relevant?
- What patterns should be searched?

### Phase 2: Deep Investigation
Use extended thinking to thoroughly investigate. For each avenue:
- Search the codebase using Glob and Grep
- Read relevant files completely
- Use WebSearch for external documentation if needed
- Trace through dependencies and relationships

DO NOT STOP at the first answer. Follow every interesting thread.

### Phase 3: Document Your Exploration
As you work, keep track of:
- Hypotheses you formed and tested
- Dead ends you encountered (and why they were dead ends)
- Surprising discoveries
- Connections between different findings

### Phase 4: Export Your Full Thinking

When complete, write your ENTIRE elaborated thinking to:
`.oracle/{topic}/delphi-{topic}-{N}.md`

The export MUST include:
1. **Initial Hypotheses** - What you thought at the start
2. **Research Path** - Every avenue explored, in order
3. **Dead Ends** - Paths that didn't pan out and why
4. **Key Discoveries** - Important findings with evidence
5. **Synthesis** - Your answer to the core question
6. **Confidence & Caveats** - What you're sure about vs uncertain
7. **Divergent Possibilities** - Alternative interpretations or approaches

Be verbose. The synthesis phase needs your full reasoning chain.

## Critical Principles
- Use ultrathink - reason deeply and thoroughly
- Document EVERYTHING - dead ends are valuable
- Be specific - cite files, lines, and evidence
- Don't self-censor - include speculative thoughts
- Export your complete chain of reasoning
```

### Step 5: Synthesize Results

After all oracles complete, dispatch a synthesis oracle:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <synthesis prompt>
)
```

**Synthesis Prompt Template:**

```
You are the Synthesis Oracle for a Delphi consultation. Multiple oracles independently investigated the same question. Your job is to synthesize their findings into a unified analysis.

## Your Mission

Read all oracle reports in `.oracle/{topic}/delphi-{topic}-*.md` and create a synthesis.

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

Write to `.oracle/{topic}/{topic}-synthesis.md`:

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

1. Create `.oracle/api-latency/`
2. Launch 3 oracles in parallel with identical prompts about API latency investigation
3. Each oracle independently explores: logs, code changes, dependencies, infrastructure
4. Each exports to `delphi-api-latency-1.md`, `delphi-api-latency-2.md`, `delphi-api-latency-3.md`
5. Synthesis oracle reads all three and creates `api-latency-synthesis.md`
6. Present findings to user

## Key Principle

**Same prompt, divergent exploration.** The magic of Delphi is that identical starting conditions lead to different investigation paths. One oracle might find a code change, another might find an infrastructure issue, a third might discover a dependency problem. Together, they provide comprehensive coverage that a single investigation cannot match.
