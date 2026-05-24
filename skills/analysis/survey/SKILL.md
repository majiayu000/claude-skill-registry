---
name: survey
description: Survey State of the Art (SOTA) literature for an Artificial Intelligence / Machine Learning (AI/ML) topic, method, or architecture. Finds relevant papers, builds a comparison table, and recommends the best implementation strategy for the current codebase. Delegates deep analysis to the ai-researcher agent.
argument-hint: <topic, method, or problem>
allowed-tools: Read, Write, Grep, Glob, Agent, WebSearch, WebFetch, TaskCreate, TaskUpdate
context: fork
---

<objective>

Survey the literature on an AI/ML topic and return actionable findings: what SOTA methods exist, which fits best for the current use case, and a concrete implementation plan. This skill is an orchestrator — it gathers codebase context, delegates literature search and analysis to the ai-researcher agent, and packages results into a structured report.

This skill is NOT for doing research or designing experiments — use the `ai-researcher` agent directly for hypothesis generation, ablation design, and experiment validation.

</objective>

<inputs>

- **$ARGUMENTS**: topic, method name, or problem description (e.g. "object detection for small objects", "efficient transformers", "self-supervised pretraining for medical images").

</inputs>

<workflow>

## Step 1: Understand the codebase context

Before searching, read the current project to extract constraints:

- Framework in use (PyTorch, JAX, TensorFlow, scikit-learn)?
- Task being solved (classification, detection, generation, regression)?
- Constraints (latency, memory, dataset size, compute budget)?

## Step 2: Research & codebase check (run in parallel)

### 2a: Spawn ai-researcher agent (issue with 2b simultaneously in one response)

Task the ai-researcher with a single objective: find the top 5 papers for `$ARGUMENTS`, produce a comparison table (method, key idea, benchmark results, compute, code availability), and recommend the single best method given the codebase constraints in Step 1 — with a brief implementation plan. The agent's own workflow handles the research and experiment design details.

Use this prompt scaffold (adapt the constraints from Step 1):

```
Survey the literature on: <$ARGUMENTS>
Codebase constraints: <framework, Python version, compute budget, existing dependencies from Step 1>
Deliver: comparison table (method, key idea, benchmarks, compute, code available), recommendation for best method, and a 3-step implementation plan for this codebase.
Write your full findings (comparison table, paper analysis, recommendation, implementation plan, Confidence block) to `tasks/survey-research-$(date +%Y-%m-%d).md` using the Write tool.
Then return ONLY a compact JSON envelope on your final line — nothing else after it:
{"status":"done","papers":N,"recommendation":"<method name>","file":"tasks/survey-research-<date>.md","confidence":0.N}
```

**If the Agent tool is unavailable** (running as a subagent where nested agent spawning is blocked), skip the Agent call and conduct the research inline: use WebSearch and WebFetch to find the top 5 papers, then synthesize the comparison table yourself. Notify the user: "Note: ai-researcher agent could not be spawned in this context — conducting research inline."

### 2b: Check for existing implementations (main context)

Use the Grep tool to search the codebase for any existing related code:

- Pattern: `$ARGUMENTS` (literal)
- Glob: `**/*.py`
- Output mode: `files_with_matches`
- Limit to 10 results

## Step 3: Report

```
## Survey: $ARGUMENTS

### SOTA Overview
[2-3 sentence summary of the current state of the field]

### Method Comparison
| Method | Key Idea | SOTA Result | Compute | Code Available |
|--------|----------|-------------|---------|----------------|
| ...    | ...      | ...         | ...     | Yes/No + link  |

### Recommendation
**Use [method]** because [specific reason matching the current codebase constraints].

### Implementation Plan
1. [step with file/component to change]
2. [step]
3. [step]

### Key Hyperparameters
- [param]: [typical range] — [what it controls]

### Gotchas
- [common failure mode and how to avoid it]

### Integration with Current Codebase
- Files to modify: [list with file:line references]
- New dependencies needed: [package versions]
- Estimated effort: [hours/days]
- Risk assessment: [what could go wrong during integration]

### References
- [Paper title] ([year]) — [link]

### Agent Confidence
<!-- One row per spawned ai-researcher; team mode spawns 2–3 -->
| Agent | Score | Gaps |
|---|---|---|
| ai-researcher | [score] | [gaps] |
```

Write the full report to `tasks/output-survey-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full report to terminal**.

Then print a compact terminal summary:

```
---
Survey — [topic]
SOTA:        [1–2 sentence summary of current landscape]
Best method: [recommended approach / architecture]
Key papers:  [top 2–3 papers with year]
Gaps:        [what the survey couldn't cover or needs runtime validation]
Confidence:  [aggregate score] — [key gaps]
→ saved to tasks/output-survey-[date].md
---
```

End your response with a `## Confidence` block per CLAUDE.md output standards.

## Team Mode

Use when the topic warrants exploring multiple competing method families with adversarial cross-evaluation.

When to trigger: 3+ distinct method families exist for the topic AND the field has no clear leading method (benchmark spread \<5% between top methods, or no SOTA consensus in the past 12 months). Skip for topics with a clear dominant approach — the default single ai-researcher is sufficient.

**Workflow with team:**

1. Lead completes Step 1 (codebase context) as normal
2. Spawn 2–3 **ai-researcher** teammates, each assigned a distinct method cluster
3. Broadcast constraints to all: `broadcast {topic: <topic>, constraints: <framework/compute/dataset from Step 1>}`
4. Each teammate researches independently, reports with `deltaT# HOOK:verify` and a compressed comparison table
5. Lead routes key findings from one researcher to others for cross-challenge: `@AR2: AR1 found [finding] — does it hold under [condition]?`
6. Lead synthesizes into the Step 3 report, noting where researchers agreed or diverged

**Note on CLAUDE.md §8 (background agent monitoring)**: Team mode spawns in-process teammates via TeamCreate — not background agents writing to a run directory. In-process teammates send TeammateIdle notifications on completion, which serve as synchronous completion signals. The file-activity polling protocol (§8) does not apply here; TeammateIdle is the equivalent liveness signal.

**Spawn prompt template:**

```
You are an ai-researcher teammate surveying: [topic].
Read .claude/TEAM_PROTOCOL.md — use AgentSpeak v2 for inter-agent messages.
Your cluster: [method family N] (e.g., "attention-free architectures" vs "linear attention variants").
Survey the top 3 methods in your cluster: comparison table + recommendation given constraints.
Write your full findings (comparison table, analysis, Confidence block) to `tasks/survey-<teammate-name>-$(date +%Y-%m-%d).md` using the Write tool.
Report completion with deltaT# HOOK:verify and include: papers=N recommendation="<method>" confidence=0.N file=tasks/survey-<teammate-name>-<date>.md
Compact Instructions: preserve paper titles, benchmarks, code links. Discard protocol handshakes.
Task tracking: call TaskUpdate(in_progress) when you start your assigned task; call TaskUpdate(completed) when done, before sending your delta message.
```

Lead synthesizes by reading teammate file paths from their delta messages. For 3 teammates, spawn a consolidator ai-researcher agent: "Read the survey files at [paths from deltas]. Synthesize into the Step 3 unified report structure. Write to `tasks/output-survey-$(date +%Y-%m-%d).md`. Return ONLY: `papers=N best_method=<name> confidence=0.N file=<path>`"

</workflow>

<notes>

- This skill orchestrates — it gathers context and delegates research to `ai-researcher`. For direct hypothesis/experiment work, use the agent directly.
- **Link integrity**: All URLs cited in the survey report must be fetched and verified before inclusion. Use WebFetch to confirm each URL exists and says what you claim.
- Follow-up chains:
  - Survey recommends a method for implementation → `/develop feature` for Test-Driven Development (TDD)-first implementation of the chosen approach
  - Survey integrates into existing code → `/develop refactor` first to prepare the module, then `/develop feature`
  - Survey reveals security concerns with a dependency → run `pip-audit` or `uv run pip-audit` for a Common Vulnerabilities and Exposures (CVE) scan

</notes>
