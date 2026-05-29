---
name: research:resume
description: Resume a research plan. Spawns parallel agents if not started, checks progress, or synthesizes findings.
---

# Research Resume Skill

Resume work on a research plan. Handles three states: spawning agents, checking progress, and synthesizing findings.

## Process

1. **Scan for research plans:**
   - Look for `research/NNNN-*/research-plan.md` files (exclude `research/archive/`)
   - A research plan is active if its `.research-state.json` has `status` other than `"complete"` or `"archived"`
   - If no state file exists, treat as active if the research-plan.md exists

2. **Handle different scenarios:**

   **No active research found:**
   ```
   No active research plans found in `research/`.

   To create a new research plan, use `/research:create <topic description>`.
   ```

   **Multiple active research plans:**
   List all and ask user to choose:
   ```
   Found multiple active research plans:

   1. `research/0001-edge-routing/` - Status: in_progress (3/5 questions complete)
   2. `research/0002-layout-algo/` - Status: planned (not started)

   Which research plan would you like to resume?
   ```

   **Single plan found:** Proceed to state-based handling below.

3. **Read `.research-state.json`** and handle based on status:

### State: `planned` (agents not yet spawned)

1. Display the research plan summary
2. Ask user to confirm they want to start the research
3. **Spawn parallel subagents** using the Task tool:
   - Use `subagent_type=Explore` for codebase investigation questions
   - Use `subagent_type=general-purpose` for questions requiring web research or multi-source analysis
   - **Launch all agents in a single message** with multiple Task tool calls for true parallelism
   - Each agent's prompt should include:
     - The specific question to investigate
     - The where/what/how/why framework from the research plan
     - The sources to consult
     - Instructions to write findings to the output file using the findings template
     - The full path to the output file: `research/NNNN-topic/qN-filename.md`
   - **Run agents in the background** using `run_in_background: true` so they execute in parallel
4. **Collect agent IDs** from all Task results
5. **Update `.research-state.json`:**
   ```json
   {
     "status": "in_progress",
     "updated_at": "...",
     "agent_ids": ["agent-1-id", "agent-2-id", "agent-3-id"],
     ...
   }
   ```
6. **Update `research-plan.md`** status to `IN PROGRESS` and update the Expected Outputs table statuses
7. Display:
   ```
   **Research started:** `research/NNNN-topic-name/`
   **Agents spawned:** N parallel investigations
   **Agent IDs:** `id1`, `id2`, `id3`

   Agents are running in the background. Run `/research:resume` to check progress and synthesize findings when complete.
   ```

### State: `in_progress` (agents spawned, awaiting completion)

1. **Check each agent's output file** — if the file exists and has content, that question is complete
2. **Read completed findings files** to verify they have substantive content
3. **Update `research-plan.md`** Expected Outputs table with current status
4. Display progress:
   ```
   **Research progress:** `research/NNNN-topic-name/`
   **Questions:** X/N complete

   **Complete:**
   - Q1: [Title] -> `q1-file.md`
   - Q3: [Title] -> `q3-file.md`

   **Pending:**
   - Q2: [Title] -> `q2-file.md` (agent: `id2`)
   ```

5. **If all questions complete**, proceed to synthesis (see below)
6. **If some are pending**, offer to:
   - Wait and check again later (`/research:resume`)
   - Proceed to partial synthesis with available findings
   - Re-spawn failed agents

### State: `in_progress` with all questions complete -> Synthesis

1. **Read all findings files**
2. **Synthesize findings** into `synthesis.md`:

   ```markdown
   # Research Synthesis: Topic Name

   ## Summary

   [3-5 sentence executive summary of all findings]

   ## Key Findings

   ### [Finding 1 title]
   [Cross-cutting finding that draws from multiple questions]

   ### [Finding 2 title]
   [Another cross-cutting finding]

   ## Recommendations

   1. **[Recommendation]** — [Rationale based on findings]
   2. **[Recommendation]** — [Rationale]

   ## Where/What/How/Why Summary

   | Aspect | Key Points |
   |--------|------------|
   | **Where** | [Key locations/sources identified] |
   | **What** | [Core facts discovered] |
   | **How** | [Key mechanisms understood] |
   | **Why** | [Design rationale and tradeoffs] |

   ## Open Questions

   - [Questions that emerged and may warrant deeper research]

   ## Next Steps

   - [ ] [Suggested follow-up action]
   - [ ] [Suggested follow-up action]

   ## Source Files

   | File | Question |
   |------|----------|
   | `q1-file.md` | Q1: Title |
   | `q2-file.md` | Q2: Title |
   ```

3. **Update `.research-state.json`:**
   ```json
   {
     "status": "synthesized",
     "updated_at": "...",
     "synthesis_agent_id": null,
     "last_session_notes": "Synthesis complete. N findings, M recommendations.",
     ...
   }
   ```
   Note: `synthesis_agent_id` is null when synthesis is done inline. Set it to an agent ID if a separate agent performed synthesis.

4. **Update `research-plan.md`** status to `SYNTHESIZED` and mark synthesis as complete in Expected Outputs
5. Display:
   ```
   **Research synthesized:** `research/NNNN-topic-name/`
   **Findings:** N questions answered
   **Synthesis:** `synthesis.md`

   **Key findings:**
   - [Finding 1]
   - [Finding 2]

   **Recommendations:**
   - [Recommendation 1]
   - [Recommendation 2]

   To create an implementation plan based on this research, run `/plan:create` and reference `research/NNNN-topic-name/`.

   To archive this research, run `/research:archive NNNN`.
   ```

### State: `synthesized` (synthesis complete)

1. Display the synthesis summary
2. Offer options:
   - Create a deeper investigation on a subtopic (hierarchical research)
   - Create an implementation plan based on findings
   - Archive the research

### Deeper Investigation (Hierarchical Research)

If the user wants to investigate a subtopic further:

1. Create `research/NNNN-topic/subtopic-name/` subdirectory
2. Create a new `research-plan.md` and `.research-state.json` inside it
3. The parent research's synthesis should note the child investigation
4. Follow the same create/resume lifecycle for the child

## Session Notes

Before ending any session, update `.research-state.json` with:
- `updated_at`: current UTC timestamp
- `last_session_notes`: summary of what happened and what to do next
