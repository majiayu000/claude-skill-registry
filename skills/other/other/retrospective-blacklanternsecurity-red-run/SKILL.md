---
name: retrospective
description: >
  Post-engagement lessons-learned retrospective. Reads the engagement
  directory, analyzes skill routing decisions, identifies knowledge gaps and
  missing skills, and produces an actionable improvement report.
keywords:
  - what went wrong
  - what worked
  - review the engagement
  - skill coverage audit
  - how did the skills perform
tools:
  - search_skills (MCP skill-router)
  - list_skills (MCP skill-router)
opsec: low
---

# Engagement Retrospective

You are conducting a post-engagement retrospective for a penetration tester.
Your job is to analyze what happened during the engagement, evaluate how the
skill library performed, identify gaps, and produce actionable improvement
items. All analysis is local — you never touch the target.

## Prerequisites

- `engagement/` directory must exist with `state.db`
- The engagement should be complete or paused — this is a post-mortem, not a
  mid-engagement review
- MCP skill-router available (`search_skills`, `list_skills`)

If `engagement/state.db` is missing, tell the user:

> Cannot run retrospective — engagement/state.db is required. This database is
> created by the orchestrator during an engagement.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[retrospective] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Step 1: Gather Context

Read all engagement files:

1. `engagement/scope.md` — targets, objectives, rules of engagement
2. `engagement/state.db` — final engagement state (call `get_state_summary()`)
3. `poll_events(since_id=0)` — full timeline of state changes
4. `get_vulns()` — confirmed vulnerabilities with details

If any file is missing (other than the required two), note it but continue with
what's available.

### Subagent Execution Logs

Check for `engagement/evidence/logs/*.jsonl`. These are raw JSONL transcripts
captured from subagent executions by the SubagentStop hook. They contain every
tool call, tool result, assistant reasoning step, MCP call, and error — ground
truth that state_events summaries cannot provide.

If JSONL logs are found, spawn a **general-purpose Task subagent** to parse them:

```
Task(
    subagent_type="general-purpose",
    prompt="Parse the subagent JSONL logs in engagement/evidence/logs/. For each
    .jsonl file, read it and extract a structured timeline:
    - Tool calls: tool name + input (truncate large inputs to 200 chars)
    - Tool results: status + truncated output (first 200 chars)
    - Assistant reasoning: key decision points and rationale
    - MCP calls: server + method + key params
    - Errors: any failures, retries, or exceptions
    - Target artifacts: flag commands that may have created artifacts on the
      target (file writes, user creation, registry changes, scheduled tasks,
      services installed, firewall rules modified)

    Also extract token-relevant metrics per agent:
    - Total number of assistant turns (messages with role 'assistant')
    - Number of tool calls and tool results
    - Largest tool results by character count (top 3, with tool name + size)
    - Number of retries or repeated tool calls (same tool + similar input)
    - Whether get_skill() was called (and which skill was loaded)

    Return a markdown summary with one section per log file. Section header
    format: '## {filename} ({agent-type})'. Include a 'Target Artifacts' subsection
    listing any commands that may need cleanup, and a 'Token Metrics' subsection
    with the metrics above.",
    description="Parse subagent JSONL logs"
)
```

Incorporate the parsed log data into subsequent analysis steps. The logs provide:
- **Routing analysis** (Step 2): exact skills loaded, whether `get_skill()` was
  called, inline vs routed execution
- **Knowledge gap analysis** (Step 3): failed payloads, retries, manual
  workarounds visible in the command sequence
- **Operational review** (Step 5): exact commands run, timing, error recovery
  decisions, artifact creation on target

If no JSONL logs are found, continue with engagement files only and note that
subagent execution traces are unavailable.

### Engagement Summary

Summarize the engagement for the user:
- **Target(s)** and objective(s)
- **Outcome**: Were objectives met? Partially? Not at all?
- **Timeline**: How many skill invocations, roughly how long
- **Final state**: What access/credentials/vulns existed at completion

Ask the user if this summary is accurate and whether there's context not
captured in the engagement files (e.g., decisions made verbally, time pressure,
scope changes mid-engagement).

## Step 2: Skill Routing Analysis

First, load the full skill inventory: call `list_skills()` to get every
available skill with its category and description. This is your reference for
what the library covers.

Read the state_events timeline and JSONL logs, then compare each activity against the inventory.

For each activity entry, determine:
1. **Was a skill loaded?** Check for skill name references in activity entries.
2. **Was it the right skill?** Read the skill's SKILL.md at
   `skills/<category>/<skill-name>/SKILL.md` to check its actual scope and
   compare against what was done.
3. **Were any skills skipped?** Look for technique execution that should have
   been routed through a skill (e.g., running sqlmap directly instead of
   loading sql-injection-union).
4. **Was anything done inline that a skill covers?** Identify commands or
   techniques executed without loading the corresponding skill.

Build a routing ledger:

| Activity | Skill Used | Correct? | Notes |
|----------|-----------|----------|-------|
| Web recon | web-discovery | Yes | — |
| SQL injection | (inline) | No | Should have routed to sql-injection-union |

Present this ledger to the user and discuss any routing decisions that seem
wrong or suboptimal.

## Step 3: Knowledge Gap Analysis

For each skill that was invoked during the engagement, read its SKILL.md at
`skills/<category>/<skill-name>/SKILL.md`, then evaluate:

1. **Did the skill have adequate payloads?** Were hand-crafted payloads needed
   that should be embedded in the skill?
2. **Were edge cases hit?** Did the target present conditions the skill didn't
   cover (e.g., unusual encodings, non-standard ports, WAF bypass needed)?
3. **Was troubleshooting adequate?** Did the skill's troubleshooting section
   cover the problems encountered?
4. **Was the methodology complete?** Were steps missing or out of order?
5. **Were tool commands correct?** Did embedded commands work or need
   modification?

For each gap found, note the specific skill and what's missing.

## Step 4: Missing Skill Identification

Identify techniques used during the engagement that don't have a corresponding
skill. Consider:

1. **Techniques used manually** — anything done by hand that was non-trivial
   and repeatable
2. **Tool workflows** — complex tool chains that could be standardized
3. **Edge-case techniques** — bypass methods, unusual attack paths, or niche
   protocols encountered

**Before proposing a new skill**, verify it doesn't already exist: call
`search_skills("description of the technique")` and check results. A skill may
exist but was missed during the engagement (routing gap, not a coverage gap).

For each confirmed missing skill, propose:
- **Skill name** (kebab-case)
- **Category** (web, ad, privesc, network, etc.)
- **What it would cover**
- **Why it's needed** (one-off or likely to recur?)

For techniques where a skill exists but wasn't used, add these to the routing
ledger in Step 2 instead.

## Step 5: Operational Review

Evaluate four operational dimensions:

### Manual Interventions
- What was done by hand that a skill should automate?
- Were payloads crafted manually that should be embedded?
- Was tool setup or configuration needed that should be in prerequisites?

### OPSEC
- Were OPSEC ratings respected? Did noisy skills get used when quiet
  alternatives existed?
- Were detection-prone techniques used unnecessarily?
- Was Kerberos-first authentication followed in AD environments?
- Were any OPSEC incidents noted (alerts triggered, blocks encountered)?

### Routing Efficiency
- Were there unnecessary detours? (e.g., broad scanning when targeted testing
  would have found the same issue faster)
- Were redundant scans run? (e.g., re-scanning ports already in the engagement state)
- Were there missed shortcuts? (e.g., credentials found early but not tested
  against other services until late)
- Did the orchestrator chain vulnerabilities effectively?

### Token Efficiency

Identify the top 1–3 token consumers during the engagement and whether each
could be reduced. Token cost is driven by: large tool results read into context,
excessive agent turns (retries, re-reads, verbose reasoning), bloated agent
template prompts, and skills loaded but not needed.

Use the JSONL log metrics (from Step 1) and the activity log to evaluate:

1. **Oversized tool results** — Did any agent pull back huge scan output, full
   file contents, or verbose tool responses that could have been filtered or
   truncated? Examples: full nmap XML in context, entire BloodHound JSON,
   unfiltered ffuf output with thousands of lines. Note the agent, tool, and
   approximate result size.
2. **Wasted agent invocations** — Did any agent run to completion and return
   nothing actionable? An agent that loads a skill, runs enumeration, and
   finds nothing is not necessarily wasted (ruling things out has value), but
   an agent spawned against the wrong target, with the wrong skill, or with
   stale context is pure waste. Check the routing ledger from Step 2.
3. **Excessive retries and re-reads** — Did any agent retry the same tool call
   multiple times, re-read files it already had in context, or loop on failing
   commands? These are signs of a skill methodology gap or missing
   troubleshooting guidance.
4. **Redundant enumeration** — Did multiple agents enumerate the same attack
   surface? (e.g., both web-discovery and a technique agent running ffuf
   against the same target, or ad-discovery re-querying LDAP data already in
   state).
5. **Structural improvements** — Based on the above, are there changes that
   would reduce token usage in future similar engagements? Examples:
   - A skill could filter tool output before returning (e.g., grep for
     relevant lines instead of dumping full output)
   - An agent template includes boilerplate that's never used for this
     agent's domain
   - A discovery skill's methodology has steps that consistently produce
     no value for this target class
   - Context passed from orchestrator to agent included unnecessary detail

For each finding, note: what consumed the tokens, roughly how much (small /
medium / large relative to the agent's total), and what change would fix it.

### State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Step 6: Critical Path Review

Map the actual kill chain from recon to objective (or as far as the engagement
got):

```
[recon] → [discovery] → [initial access] → [pivot/escalation] → [objective]
```

For each step, note:
- What skill handled it
- Whether it was the fastest path
- What blocked progress and how it was resolved
- Whether steps could have been parallelized or reordered

Identify bottlenecks — where did the engagement stall, and why?

## Step 7: Write Report

Produce `engagement/retrospective.md` with all findings:

```markdown
# Engagement Retrospective

## Summary
<One paragraph: target, objective, outcome>

## Kill Chain
<Ordered attack path from recon to objective>

## Skill Routing Review
### Skills Invoked
- <skill-name> — <what it did, whether it performed well>

### Skills Skipped (Should Have Been Invoked)
- <skill-name> — <why it should have been invoked, what was done instead>

### Inline Execution (Should Have Been Routed)
- <description of what was done inline instead of via a skill>

## Knowledge Gaps
### <skill-name>
- <missing payload, edge case, or methodology>

## Missing Skills
- **<proposed-skill-name>** (<category>) — <what it would cover, why needed>

## Operational Review
### Manual Interventions
- <what was done manually that should be automated>

### OPSEC
- <assessment of noise level, detection surface>

### Routing Efficiency
- <unnecessary detours, missed shortcuts>

### Token Efficiency
Top token consumers:
1. <agent/skill — what consumed tokens, relative impact, proposed fix>
2. <agent/skill — what consumed tokens, relative impact, proposed fix>
3. <agent/skill — what consumed tokens, relative impact, proposed fix>
### State Management
- <quality of state management flow, stale reads, missing updates>

## Actionable Items
Priority-ordered list:
1. [skill-update] <skill-name>: <specific change needed>
2. [new-skill] <proposed-name>: <brief description>
3. [routing-fix] <skill-name>: <routing table update needed>
4. [template-fix] <change to _template or conventions>
5. [token-efficiency] <agent/skill/template>: <change to reduce token usage>
```

Present the actionable items to the user and ask which ones to prioritize.

## Step 8: Implement Improvements

After the user selects which items to prioritize, make the edits. Skills are
plain Markdown files at `skills/<category>/<skill-name>/SKILL.md` — edit them
directly.

**CTF sanitization rule:** When implementing changes from a CTF engagement,
never add target-specific references to skills. This is a public repository
and skills must not contain CTF answers. Specifically: no target-specific CMS
names or niche technologies (common ones like WordPress, Apache, nginx are
fine), no specific CVE IDs from the engagement, no example IPs from lab
environments (10.129.x.x, 10.10.x.x), no passwords or flag values, and no
attack chains that map directly to a specific CTF box. Generalize the
methodology so it applies broadly.

For each prioritized item:

### [skill-update] — Edit an existing skill
1. Read the SKILL.md file at `skills/<category>/<skill-name>/SKILL.md`
2. Make the change — add payloads, fix methodology, update troubleshooting,
   etc.
3. Preserve the existing structure and conventions (frontmatter, sections,
   embedded payloads format)

### [new-skill] — Create a new skill
1. Read `skills/_template/SKILL.md` for the canonical structure
2. Write the new skill to `skills/<category>/<skill-name>/SKILL.md`
3. Update the corresponding discovery skill's routing table to include it

### [routing-fix] — Fix skill routing
1. Read the skill that needs the routing update
2. Add or fix the routing reference: "STOP. Return to orchestrator
   recommending **skill-name**. Pass: <context>."

### [token-efficiency] — Reduce token usage
1. Identify the target: skill methodology, agent template, tool output handling,
   or orchestrator context passing
2. For **skill changes**: edit the SKILL.md to filter output, remove redundant
   steps, or add guidance to avoid re-reads/retries
3. For **agent template changes**: edit the agent file in `agents/` to trim
   boilerplate or remove unused instructions for that agent's domain
4. For **tool/MCP changes**: note the change needed in the report — these
   require server-side code changes in `tools/`
5. Verify the change doesn't remove needed context — token savings that cause
   agents to fail or miss findings are counterproductive

### [template-fix] — Update conventions
1. Read `skills/_template/SKILL.md`
2. Make the change and note which existing skills may need the same update

After all edits are complete, re-index so the MCP skill-router picks up
changes:

```bash
uv run --directory tools/skill-router python indexer.py
```

Show the user what was changed and suggest committing.

## Troubleshooting

### Engagement directory exists but files are empty
The engagement may have been run without logging enabled. Do the retrospective
from conversation context instead — ask the user to describe what happened, then
analyze the current session transcript.

### Activity log has no skill references
Techniques may have been executed inline (without loading the corresponding
skill) or the engagement predates the current skill library. Flag this
as a routing gap and reconstruct the timeline from state_events and JSONL logs
instead.

### Multiple engagement directories
If the user has run multiple engagements, ask which one to review. Look for
date-stamped directories or scope.md contents to differentiate them.
