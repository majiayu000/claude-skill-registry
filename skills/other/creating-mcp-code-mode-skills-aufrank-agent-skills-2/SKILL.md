---
name: creating-mcp-code-mode-skills
description: >
  A meta-skill for authoring high-performance, verifiable, long-running MCP skills
  using Code Mode. This skill blends Anthropic and OpenAI skill-authoring guidance
  with Code-Mode-first, MCP-backed execution, dynamic context discovery, and
  file-backed agent harnesses.

metadata:
  short-description: Author modular, deterministic, token-efficient MCP skills.
  audience: skill-authors
  stability: stable
  version: "1.3.0"
---

# Creating MCP Code Mode Skills

This skill teaches **how to author agent skills**, not how to prompt models. You are designing **deterministic scaffolding for a probabilistic system**. Assume the model is capable. Favor **constraints, structure, and files** over prose.

## Mental Model

> **The model reasons.  
> Code executes.  
> The filesystem remembers.**

A Code Mode MCP skill is a **closed-loop control system**, not a function call.

- Reasoning lives in the model
- Work happens in code
- Truth persists on disk

If information is large, fragile, repetitive, or stateful, it does **not** belong in the context window.

## 0. Prior art

Before you start skill creation, and if you have any questions about how to proceed, check the following references (you can examine the first line of the file to understand its contents before deciding whether to read it):

- reference/skill_creator_from_codex.md
- reference/skill_creator_from_anthropic.md
- reference/skill_authoring_best_practices_from_anthropic.md
- reference/dynamic_context_from_cursor.md

## 1. What a Skill *Is*

A skill is:

- A **capability contract**, not a conversation
- A **repeatable procedure**, not a one-off answer
- A **tool-augmented behavior**, not just text generation

Every skill must clearly define:

- What problem it solves
- When it should be used
- What it is allowed to do
- How it makes progress
- How it fails safely

## 1.1 Metadata taxonomy

Use `metadata` in frontmatter for custom attributes (one level deep, lists allowed). Preferred keys:

- `short-description`
- `audience`
- `stability`
- `owner`
- `tags`

Avoid adding other top-level frontmatter keys; migrate them into `metadata`.

## 1.2 Spec-aligned frontmatter

Follow the Agent Skills spec: optional frontmatter fields are `license`, `compatibility`, `metadata`, `allowed-tools`.

## 2. Architectural First Principles

### 2.1 Code Is the Only Tool Interface

When code execution is available:

- The model MUST NOT call tools directly
- MCP access MUST occur via executable code
- Validation, retries, and error handling live in scripts

Models are more reliable at **writing code** than emitting fragile tool calls.

### 2.2 Dynamic Context Discovery (Cursor)

Static context is a liability.

Do NOT preload:

- Full MCP schemas
- Large tool responses
- Logs or tables

Instead:

- Start minimal
- Discover on demand
- Write to files
- Query selectively

Context must be **discoverable, queryable, and discardable**.

Dynamic context patterns (do these instead of dumping blobs into chat):

- Write large tool/MCP responses to files; inspect the tail first, then read more only as needed.
- Treat long chat history and terminal output as files you can grep to recover details after summarization.
- Cache MCP tool descriptions/status to files and load only the tools needed for the task (empirically cuts token use nearly in half in Cursor A/B).
- Use files as the durable interface for anything that must outlive the current context window.

### 2.3 Files Are the Context Boundary

For long-running agents, files are the **only reliable memory**.

Anything that must survive:

- retries
- summarization
- context eviction
- multi-phase execution

**must be written to disk**.

Canonical artifacts:

- `plan.json` — immutable intent
- `progress.txt` — append-only log
- `results.json` — structured outputs # you can use more output files than just results.json, and you should be thoughtful about clobbering
- `errors.log` — diagnostics

### 2.4 Portable command blocks

Make examples cross-platform and low-friction:

- Prefer `text` fences and Python one-liners over bash heredocs.
- Use placeholders like `<CODEX_HOME>`, `<REPO_ROOT>`, `<TOOL_HOME>` instead of hard-coded paths.
- Call scripts via absolute paths; never require `cd` into the skill directory.

## 3. Skill Structure & Naming

### 3.1 Naming

Use **gerund form** to describe capability:

- `provisioning-infrastructure`
- `syncing-databases`
- `auditing-permissions`

Skills describe **process**, not outcome.

### 3.2 Directory Layout

```text
SKILL.md
scripts/
references/
mcp_tools/
templates/
```

#### SKILL.md

- Entry point and behavioral contract
- Invocation rules
- Under 500 lines
- Progressive disclosure: static prompt carries only name/description; load SKILL.md body and references on demand; execute scripts for real work.

#### scripts/

- Deterministic executables
- Defensive and idempotent
- Use `mcpc --json`.

#### references/

- Lightweight, navigable context
- Tables of contents
- Explicit pointers from SKILL.md
- No monolithic dumps

#### mcp_tools/

- Dynamic Context Discovery cache
- Never pasted directly into prompts
- Generated on demand via:

```text
mcpc <target> tools-get <tool-name> --json
```

#### templates/

- Low-entropy schemas (JSON/YAML)
- Plans, approvals, reports

#### Keep the file set minimal

- Only include what the agent needs (SKILL.md + scripts + references + assets/templates).
- Avoid extra docs (README/CHANGELOG/etc.) that bloat discovery and add ambiguity.

## 4. Code Mode via mcpc (Proxy Pattern)

All MCP interaction MUST go through `mcpc`. Use `mcpc --help` to learn the tool. All arguments to tool calls are bound via `:=`.  session names must be quoted in powershell, `'@session'`.

Required properties:

- `--json` output only
- Filter before returning to context
- Prefer `jq` or equivalent

Example:

```text
mcpc --json @session tools-call get_data id:="123" | jq '{id, status, summary}' > results.json
```

The model may then read **only** `results.json`.

## 5. Scripts, References, Templates

### Scripts (Required)

- Execute work
- Validate inputs
- Verify MCP connectivity
- Handle retries
- Fail locally

### Templates (Required)

- Define shape, not content
- Used for `plan.json`, approvals, reports

### References (Required, Lightweight)

Good references:

- Are indexed and navigable
- Are pointed to, not dumped
- Respect token economy
- May include cached MCP schemas

Bad references:

- Large static blobs
- Blindly copied tool specs

## 6. Trust Policy (Always / Never / Ask)

Each skill MUST define its **own** trust policy.

Defaults are a baseline only.

### ALWAYS

- Read-only inspection
- Listing tools
- Viewing references

### NEVER

- Credential exfiltration
- Irreversible destructive actions
- Executing untrusted code

## ASK

- State-changing MCP calls
- Deletes, writes, deploys
- Any irreversible action

Skills SHOULD extend these rules.

## 7. Degrees of Freedom

Match freedom to task fragility and variability. Each level constrains **context, reasoning, and tools**.

### High Freedom — Explore, *Figure out what to do.*

- Context: natural language, summaries, file pointers
- Reasoning: prompt-style thinking, agents/subagents
- Tools: inspection, planning

### Medium Freedom — Shape, *Configure a known solution.*

- Context: templates, schemas, parameters
- Reasoning: constrained adaptation
- Tools: parameterized scripts, validation helpers

### Low Freedom — Execute, *Do exactly one safe thing.*

- Context: fully specified files
- Reasoning: none at execution time
- Tools: deterministic, validated scripts

**Rule:** Never mix freedom levels.
Split workflows: **decide → configure → execute**.

## 8. Long-Running Agent Harness

Assume interruption. Design for restart:

- Write progress after every step
- Make scripts idempotent
- Resume by reading files

If the agent restarts, it should know exactly where it is.

## 9. Canonical Execution Loop

1. Discover minimal context
2. Cache schemas/data as files
3. Write `plan.json`
4. Validate environment
5. Execute scripts
6. Persist results
7. Summarize selectively

## 10. Explicit Anti-Patterns

- Dumping MCP JSON into chat
- Copying full schemas into prompts
- Trusting tool calls without verification
- Relying on model memory instead of files

## 11. Reference-derived Practices

- Enforce progressive disclosure: static metadata → on-demand references → executed scripts.
- Challenge every paragraph for token cost; prefer concise examples over exposition.
- Match degree-of-freedom (explore/shape/execute) to task fragility, and keep phases separate.
- Default to files as the memory surface for tool outputs, history, terminal logs, and MCP tool caches.
- Keep the skill artifact set lean; remove auxiliary docs unless they unlock execution.

## Final Principle

> **If it matters, write it down.**

Code Mode MCP skills move truth *out of the model* and into code, files, and structure. The model is a strategist — not a storage device.
