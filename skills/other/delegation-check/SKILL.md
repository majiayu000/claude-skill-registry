---
name: delegation-check
description: Check workflow delegation prompts against agent role definitions for content separation violations. Detects conflicts, duplication, boundary leaks, and missing contracts. Triggers on "check delegation", "delegation conflict", "prompt vs role check".
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

<purpose>
Validate that command delegation prompts (Agent() calls) and agent role definitions respect GSD content separation boundaries. Detects 7 conflict dimensions: role re-definition, domain expertise leaking into prompts, quality gate duplication, output format conflicts, process override, scope authority conflicts, and missing contracts.

Invoked when user requests "check delegation", "delegation conflict", "prompt vs role check", or when reviewing workflow skill quality.
</purpose>

<required_reading>
- @.claude/skills/delegation-check/specs/separation-rules.md
</required_reading>

<process>

## 1. Determine Scan Scope

Parse `$ARGUMENTS` to identify what to check.

| Signal | Scope |
|--------|-------|
| File path to command `.md` | Single command + its agents |
| File path to agent `.md` | Single agent + commands that spawn it |
| Directory path (e.g., `.claude/skills/team-*/`) | All commands + agents in that skill |
| "all" or no args | Scan all `.claude/commands/`, `.claude/skills/*/`, `.claude/agents/` |

If ambiguous, ask:

```
AskUserQuestion(
  header: "Scan Scope",
  question: "What should I check for delegation conflicts?",
  options: [
    { label: "Specific skill", description: "Check one skill directory" },
    { label: "Specific command+agent pair", description: "Check one command and its spawned agents" },
    { label: "Full scan", description: "Scan all commands, skills, and agents" }
  ]
)
```

## 2. Discover Command-Agent Pairs

For each command file in scope:

**2a. Extract Agent() calls from commands:**

```bash
# Search both Agent() (current) and Task() (legacy GSD) patterns
grep -n "Agent(\|Task(" "$COMMAND_FILE"
grep -n "subagent_type" "$COMMAND_FILE"
```

For each `Agent()` call, extract:
- `subagent_type` → agent name
- Full prompt content between the prompt markers (the string passed as `prompt=`)
- Line range of the delegation prompt

**2b. Locate agent definitions:**

For each `subagent_type` found:
```bash
# Check standard locations
ls .claude/agents/${AGENT_NAME}.md 2>/dev/null
ls .claude/skills/*/agents/${AGENT_NAME}.md 2>/dev/null
```

**2c. Build pair map:**

```
$PAIRS = [
  {
    command: { path, agent_calls: [{ line, subagent_type, prompt_content }] },
    agent: { path, role, sections, quality_gate, output_contract }
  }
]
```

If an agent file cannot be found, record as `MISSING_AGENT` — this is itself a finding.

## 3. Parse Delegation Prompts

For each Agent() call, extract structured blocks from the prompt content:

| Block | What It Contains |
|-------|-----------------|
| `<objective>` | What to accomplish |
| `<files_to_read>` | Input file paths |
| `<additional_context>` / `<planning_context>` / `<verification_context>` | Runtime parameters |
| `<output>` / `<expected_output>` | Output format/location expectations |
| `<quality_gate>` | Per-invocation quality checklist |
| `<deep_work_rules>` / `<instructions>` | Cross-cutting policy or revision instructions |
| `<downstream_consumer>` | Who consumes the output |
| `<success_criteria>` | Success conditions |
| Free-form text | Unstructured instructions |

Also detect ANTI-PATTERNS in prompt content:
- Role identity statements ("You are a...", "Your role is...")
- Domain expertise (decision tables, heuristics, comparison examples)
- Process definitions (numbered steps, step-by-step instructions beyond scope)
- Philosophy statements ("always prefer...", "never do...")
- Anti-pattern lists that belong in agent definition

## 4. Parse Agent Definitions

For each agent file, extract:

| Section | Key Content |
|---------|------------|
| `<role>` | Identity, spawner, responsibilities, mandatory read |
| `<philosophy>` | Guiding principles |
| `<upstream_input>` | How agent interprets input |
| `<output_contract>` | Return markers (COMPLETE/BLOCKED/CHECKPOINT) |
| `<quality_gate>` | Self-check criteria |
| Domain sections | All `<section_name>` tags with their content |
| YAML frontmatter | name, description, tools |

## 5. Run Conflict Checks (7 Dimensions)

### Dimension 1: Role Re-definition

**Question:** Does the delegation prompt redefine the agent's identity?

**Check:** Scan prompt content for:
- "You are a..." / "You are the..." / "Your role is..."
- "Your job is to..." / "Your responsibility is..."
- "Core responsibilities:" lists
- Any content that contradicts agent's `<role>` section

**Allowed:** References to mode ("standard mode", "revision mode") that the agent's `<role>` already lists in "Spawned by:".

**Severity:** `error` if prompt redefines role; `warning` if prompt adds responsibilities not in agent's `<role>`.

### Dimension 2: Domain Expertise Leak

**Question:** Does the delegation prompt embed domain knowledge that belongs in the agent?

**Check:** Scan prompt content for:
- Decision/routing tables (`| Condition | Action |`)
- Good-vs-bad comparison examples (`| TOO VAGUE | JUST RIGHT |`)
- Heuristic rules ("If X then Y", "Always prefer Z")
- Anti-pattern lists ("DO NOT...", "NEVER...")
- Detailed process steps beyond task scope

**Exception:** `<deep_work_rules>` is an acceptable cross-cutting policy pattern from GSD — flag as `info` only.

**Severity:** `error` if prompt contains domain tables/examples that duplicate agent content; `warning` if prompt contains heuristics not in agent.

### Dimension 3: Quality Gate Duplication

**Question:** Do the prompt's quality checks overlap or conflict with the agent's own `<quality_gate>`?

**Check:** Compare prompt `<quality_gate>` / `<success_criteria>` items against agent's `<quality_gate>` items:
- **Duplicate:** Same check appears in both → `warning` (redundant, may diverge)
- **Conflict:** Contradictory criteria (e.g., prompt says "max 3 tasks", agent says "max 5 tasks") → `error`
- **Missing:** Prompt expects quality checks agent doesn't have → `info`

**Severity:** `error` for contradictions; `warning` for duplicates; `info` for gaps.

### Dimension 4: Output Format Conflict

**Question:** Does the prompt's expected output format conflict with the agent's `<output_contract>`?

**Check:**
- Prompt `<expected_output>` markers vs agent's `<output_contract>` return markers
- Prompt expects specific format agent doesn't define
- Prompt expects file output but agent's contract only defines markers (or vice versa)
- Return marker names differ (prompt expects `## DONE`, agent returns `## TASK COMPLETE`)

**Severity:** `error` if return markers conflict; `warning` if format expectations unspecified on either side.

### Dimension 5: Process Override

**Question:** Does the delegation prompt dictate HOW the agent should work?

**Check:** Scan prompt for:
- Numbered step-by-step instructions ("Step 1:", "First..., Then..., Finally...")
- Process flow definitions beyond `<objective>` scope
- Tool usage instructions ("Use grep to...", "Run bash command...")
- Execution ordering that conflicts with agent's own execution flow

**Allowed:** `<instructions>` block for revision mode (telling agent what changed, not how to work).

**Severity:** `error` if prompt overrides agent's process; `warning` if prompt suggests process hints.

### Dimension 6: Scope Authority Conflict

**Question:** Does the prompt make decisions that belong to the agent's domain?

**Check:**
- Prompt specifies implementation choices (library selection, architecture patterns) when agent's `<philosophy>` or domain sections own these decisions
- Prompt overrides agent's discretion areas
- Prompt locks decisions that agent's `<context_fidelity>` says are "Claude's Discretion"

**Allowed:** Passing through user-locked decisions from CONTEXT.md — this is proper delegation, not authority conflict.

**Severity:** `error` if prompt makes domain decisions agent should own; `info` if prompt passes through user decisions (correct behavior).

### Dimension 7: Missing Contracts

**Question:** Are the delegation handoff points properly defined?

**Check:**
- Agent has `<output_contract>` with return markers → command handles all markers?
- Command's return handling covers COMPLETE, BLOCKED, CHECKPOINT
- Agent lists "Spawned by:" — does command actually spawn it?
- Agent expects `<files_to_read>` — does prompt provide it?
- Agent has `<upstream_input>` — does prompt provide matching input structure?

**Severity:** `error` if return marker handling is missing; `warning` if agent expects input the prompt doesn't provide.

## 6. Aggregate and Report

### 6a. Per-pair summary

For each command-agent pair, aggregate findings:

```
{command_path} → {agent_name}
  Agent() at line {N}:
    D1 (Role Re-def):      {PASS|WARN|ERROR} — {detail}
    D2 (Domain Leak):       {PASS|WARN|ERROR} — {detail}
    D3 (Quality Gate):      {PASS|WARN|ERROR} — {detail}
    D4 (Output Format):     {PASS|WARN|ERROR} — {detail}
    D5 (Process Override):  {PASS|WARN|ERROR} — {detail}
    D6 (Scope Authority):   {PASS|WARN|ERROR} — {detail}
    D7 (Missing Contract):  {PASS|WARN|ERROR} — {detail}
```

### 6b. Overall verdict

| Verdict | Condition |
|---------|-----------|
| **CLEAN** | 0 errors, 0-2 warnings |
| **REVIEW** | 0 errors, 3+ warnings |
| **CONFLICT** | 1+ errors |

### 6c. Fix recommendations

For each finding, provide:
- **Location:** file:line
- **What's wrong:** concrete description
- **Fix:** move content to correct owner (command or agent)
- **Example:** before/after snippet if applicable

## 7. Present Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DELEGATION-CHECK ► SCAN COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scope: {description}
Pairs checked: {N} command-agent pairs
Findings: {E} errors, {W} warnings, {I} info

Verdict: {CLEAN | REVIEW | CONFLICT}

| Pair | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|------|----|----|----|----|----|----|-----|
| {cmd} → {agent} | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ |
| ... | | | | | | | |

{If CONFLICT: detailed findings with fix recommendations}

───────────────────────────────────────────────────────

## Fix Priority

1. {Highest severity fix}
2. {Next fix}
...

───────────────────────────────────────────────────────
```

</process>

<success_criteria>
- [ ] Scan scope determined and all files discovered
- [ ] All Agent() calls extracted from commands with full prompt content
- [ ] All corresponding agent definitions located and parsed
- [ ] 7 conflict dimensions checked for each command-agent pair
- [ ] No false positives on legitimate patterns (mode references, user decision passthrough, `<deep_work_rules>`)
- [ ] Fix recommendations provided for every error/warning
- [ ] Summary table with per-pair dimension results displayed
- [ ] Overall verdict determined (CLEAN/REVIEW/CONFLICT)
</success_criteria>
