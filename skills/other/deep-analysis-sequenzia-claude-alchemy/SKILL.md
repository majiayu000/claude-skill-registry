---
name: deep-analysis
description: Reusable deep exploration and synthesis workflow. Use when asked for "deep analysis", "deep understanding", "analyze codebase", "explore and analyze", or "investigate codebase".
argument-hint: <analysis-context or focus-area>
model: inherit
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using parallel code-explorer agents and a codebase-synthesizer agent. This skill can be invoked standalone or loaded by other skills as a reusable building block.

## Phase 1: Exploration

**Goal:** Thoroughly explore the codebase to gather raw findings.

1. **Determine analysis context:**
   - If `$ARGUMENTS` is provided, use it as the analysis context (feature area, question, or general exploration goal)
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Load skills for this phase:**
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/project-conventions/SKILL.md` and apply its guidance
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/language-patterns/SKILL.md` and apply its guidance

3. **Determine focus areas:**
   - For feature-focused analysis, use 3 agents:
     ```
     Agent 1: Explore entry points and user-facing code related to the context
     Agent 2: Explore data models, schemas, and storage related to the context
     Agent 3: Explore utilities, helpers, and shared infrastructure
     ```
   - For general codebase understanding, 2 agents may suffice:
     ```
     Agent 1: Explore application structure, entry points, and core logic
     Agent 2: Explore configuration, infrastructure, and shared utilities
     ```

4. **Launch code-explorer agents:**

   Launch agents in parallel using the Task tool with `subagent_type: "claude-alchemy-tools:code-explorer"`:
   ```
   Path to analyze: [PATH]
   Analysis context: [context from step 1]
   Focus area: [specific focus for this agent]

   Find and analyze:
   - Relevant files and their purposes
   - Key functions/classes and their roles
   - Existing patterns and conventions
   - Integration points and dependencies

   Return a structured report of your findings.
   ```

5. **Handle agent failures:**
   - If an agent fails, note which focus area was missed
   - Continue with successful results — partial findings are still valuable
   - If all agents fail, inform the user and offer to retry or explore manually

---

## Phase 2: Synthesis

**Goal:** Merge exploration findings into a unified analysis.

1. **Launch codebase-synthesizer agent:**

   Use the Task tool with `subagent_type: "claude-alchemy-tools:codebase-synthesizer"` and `model: "opus"`:
   ```
   Analysis context: [context from Phase 1]
   Codebase path: [PATH]

   Exploration findings from [N] agents:

   --- Agent 1: [Focus Area] ---
   [Full report from agent 1]

   --- Agent 2: [Focus Area] ---
   [Full report from agent 2]

   --- Agent 3: [Focus Area] (if applicable) ---
   [Full report from agent 3]

   Synthesize these findings into a unified analysis. Merge duplicates,
   read critical files in depth, map relationships between components,
   identify patterns, and assess challenges.
   ```

2. **Review synthesis:**
   - Verify the synthesizer covered all focus areas
   - If critical gaps exist, use Glob/Grep to fill them directly

---

## Completion

- **Standalone invocation:** Present the synthesized analysis to the user. The results remain in conversation memory for follow-up questions.
- **Loaded by another skill:** The synthesis is complete. Control returns to the calling workflow — do not present a standalone summary.

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Continue with partial results
   - Abort the analysis

---

## Agent Coordination

When launching parallel agents:
- Give each agent a distinct focus area to minimize overlap
- Wait for all agents to complete before proceeding to synthesis
- Handle agent failures gracefully — continue with partial results

When calling Task tool for agents:
- Use `model: "opus"` for codebase-synthesizer agent
- Use default model (sonnet) for code-explorer agents
