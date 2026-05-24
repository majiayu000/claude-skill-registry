---
name: research:create
description: Create a research plan with parallel investigation tasks. Use when exploring a topic, analyzing external code, or gathering information to inform an implementation plan.
allowed-tools: Bash(git log:*), Bash(git diff:*)
---

# Research Create Skill

Design a research plan that decomposes a topic into parallel investigation tasks.

## Process

1. **Invoke an Explore subagent** using the Task tool with `subagent_type=Explore` to understand the current codebase context relevant to the research topic. **Capture the `agentId`** from the Task result.

2. **Design the research plan.** Break the topic into independent questions that can be investigated in parallel. For each question, define:
   - The question itself (what we need to find out)
   - The where/what/how/why framework:
     - **Where:** Which codebases, files, docs, or external sources to investigate
     - **What:** What specific information to extract
     - **How:** How the system/algorithm/feature works
     - **Why:** Why it was designed this way, what tradeoffs were made
   - The output file name for findings
   - Which sources to consult (local code, external repos, docs, web)

3. **Find the next research number** by checking both `research/` and `research/archive/` for the highest `NNNN-*` prefix. Unnumbered directories are legacy and should be ignored when determining the next number.

4. **Create the research directory:** `research/NNNN-topic-name/`

5. **Write `research-plan.md`** with this format:

   ```markdown
   # Research: Topic Name

   ## Status: PLANNED

   ---

   ## Goal

   [What we're trying to learn and why]

   ## Context

   [Current state, what prompted this research, relevant background]

   ## Questions

   ### Q1: [Question title]

   **Where:** [Sources to investigate]
   **What:** [Specific information needed]
   **How:** [Methodology — read code, run experiments, compare implementations]
   **Why:** [Why this matters for our goals]

   **Output file:** `q1-descriptive-name.md`

   ---

   ### Q2: [Question title]

   **Where:** [Sources to investigate]
   **What:** [Specific information needed]
   **How:** [Methodology]
   **Why:** [Why this matters]

   **Output file:** `q2-descriptive-name.md`

   ---

   [Continue for each question]

   ## Sources

   | Source | Location | Used by |
   |--------|----------|---------|
   | [Source name] | [Path or URL] | Q1, Q2 |

   ## Expected Outputs

   | File | Question | Status |
   |------|----------|--------|
   | `q1-descriptive-name.md` | Q1: Title | Pending |
   | `q2-descriptive-name.md` | Q2: Title | Pending |
   | `synthesis.md` | Combined findings | Pending |
   ```

6. **Write `.research-state.json`** with initial state:

   ```json
   {
     "status": "planned",
     "created_at": "2026-01-28T10:30:00Z",
     "updated_at": "2026-01-28T10:30:00Z",
     "planning_agent_id": "abc-123-def",
     "agent_ids": [],
     "synthesis_agent_id": null,
     "last_session_notes": null
   }
   ```

   - `status`: `"planned"` — research plan created but agents not yet spawned
   - `planning_agent_id`: agentId from the Explore subagent
   - `agent_ids`: empty array, populated when `/research:resume` spawns agents
   - `synthesis_agent_id`: null until synthesis is performed

7. **Do not spawn research agents yet.** The plan should be reviewed first. Agents are spawned by `/research:resume`.

8. **Present the plan** to the user:

   ```
   **Research plan created:** `research/NNNN-topic-name/`
   **Created:** YYYY-MM-DD HH:MM UTC
   **Questions:** N questions defined
   **Planning agent:** `{agentId}` (resume for additional context)

   **Questions:**
   - Q1: [Title] -> `q1-output-file.md`
   - Q2: [Title] -> `q2-output-file.md`
   - Q3: [Title] -> `q3-output-file.md`

   Review the research plan, then run `/research:resume` to spawn parallel investigation agents.

   *Research summary: Brief description of what we're investigating*
   ```

## Findings File Template

Each subagent should produce findings following this structure:

```markdown
# Q1: [Question Title]

## Summary

[2-3 sentence answer to the question]

## Where

[Sources consulted — files read, repos explored, docs referenced]

## What

[Detailed findings — the factual information discovered]

## How

[How the system/algorithm/feature works, with code references and examples]

## Why

[Why it was designed this way, tradeoffs, constraints, design rationale]

## Key Takeaways

- [Bullet point takeaway 1]
- [Bullet point takeaway 2]
- [Bullet point takeaway 3]

## Open Questions

- [Any follow-up questions that emerged during investigation]
```

## Hierarchical Research

If a research plan needs deeper investigation on a subtopic:
- Create a subdirectory: `research/NNNN-topic-name/subtopic-name/`
- The subdirectory gets its own `research-plan.md` and `.research-state.json`
- The parent's synthesis should reference the child research
