---
name: ln-005-multi-agent-context-review
description: "Multi-agent context review: delegates plans, decisions, documents, architecture proposals to external agents (Codex + Gemini) for independent review with debate protocol. Works in Plan Mode."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Multi-Agent Context Review (Universal)

Runs parallel external agent reviews on arbitrary context, critically verifies suggestions, returns filtered improvements.

## Purpose & Scope
- Standalone utility in 0XX category (like ln-003, ln-004)
- Delegate any context to codex-review + gemini-review as background tasks in parallel
- Context always passed via file references (never inline in prompt)
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions

## When to Use
- Manual invocation by user for independent review of any artifact
- Called by any skill needing external second opinion on plans, decisions, documents
- NOT tied to Linear, NOT tied to any pipeline
- Works with any context that can be saved to a file

## Plan Mode Support

Follows `shared/references/plan_mode_pattern.md` (Workflow B) and `shared/references/agent_review_workflow.md` Plan Mode Behavior. Step 7e (Compare & Correct): output findings to chat, apply edits only after user approval.

## Parameters

| Parameter | Value |
|-----------|-------|
| `review_type` | `contextreview` |
| `skill_group` | `005` |
| `prompt_template` | `shared/agents/prompt_templates/context_review.md` |
| `verdict_acceptable` | `CONTEXT_ACCEPTABLE` |

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `context_files` | Yes | List of file paths containing context to review (relative to CWD) |
| `identifier` | No | Short label for file naming (default: `review_YYYYMMDD_HHMMSS`) |
| `focus` | No | List of areas to focus on (default: all 6) |
| `review_title` | No | Human-readable title (default: `"Context Review"`) |
| `tech_stack` | No | Technology stack override (e.g., `"Python FastAPI"`, `"C# ASP.NET Core"`). Auto-detected if not provided. |

**Context delivery rule:** Context is ALWAYS passed via files.
- If context already exists as files (plans, docs, code) -> pass file paths directly
- If context is a statement/decision from chat -> caller creates a temporary file in `.agent-review/context/` with the content, then passes the file path

## Workflow

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` for Health Check, Ensure .agent-review/, Load Review Memory, Run Agents, Critical Verification + Debate, Aggregate + Return, Save Review Summary, Fallback Rules, Critical Rules, and Definition of Done. Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol.

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `005`.

2) **Resolve identifier:** If `identifier` not provided, generate `review_YYYYMMDD_HHMMSS`. Sanitize: lowercase, replace spaces with hyphens, ASCII only.

3) **Ensure .agent-review/:** per shared workflow. Additionally create `.agent-review/context/` subdir if it doesn't exist (for materialized context files).

4) **Materialize context (if needed):** If context is from chat/conversation (not an existing file):
   - Write content to `.agent-review/context/{identifier}_context.md`
   - Add this path to `context_files` list

5) **Build prompt:** Read template `shared/agents/prompt_templates/context_review.md`.
   - Replace `{review_title}` with title or `"Context Review"`
   - Replace `{context_refs}` with bullet list: `- {path}` per context file
   - Replace `{focus_areas}` with filtered subset or `"All default areas"` if no focus specified
   - Save to `.agent-review/{identifier}_contextreview_prompt.md` (single shared file -- both agents read the same prompt)

### Shared Workflow Steps

6) **Launch Agents (background) — MANDATORY: before any foreground research:**

Per shared workflow "Step: Run Agents". Prompt file is ready (step 5). Launch BOTH agents as background tasks NOW.

- `{review_type}` in challenge template = review_title or "Context Review"
- `{story_ref}` in challenge template = identifier

7) **Foreground Research (while agents are running in background):**

Agents are already thinking. Use this time for Review Memory + MCP Ref research.

```
Agents (background)                    Claude (foreground)
  codex-review ──┐                       7a) Load Review Memory
  gemini-review ─┤                       7b) Applicability Check
                 │                       7c) Stack Detection
                 │                       7d) Extract Topics
                 │                       7e) MCP Ref Research
                 │                       7f) Compare & Correct
                 ├── first completes ──→ 7g) Save Findings
                 └── second completes    8) Critical Verification (informed by memory + findings)
```

**MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

#### 7a) Load Review Memory

Per shared workflow "Step: Load Review Memory". Not passed to agents — used only in step 8 (Critical Verification).

#### 7b) Applicability Check

Scan `context_files` for technology decision signals (skip 7c-7e if no signals found):

| Signal Type | Weight | Examples |
|-------------|--------|---------|
| Infrastructure choice | 5 | Redis, PostgreSQL, K8s, Docker, RabbitMQ |
| API/protocol decision | 4 | REST vs GraphQL, WebSocket, gRPC, OAuth 2.0 |
| Security mechanism | 4 | JWT, PKCE, CORS, rate limiting, OWASP |
| Library/framework choice | 3 | FastAPI, Polly, SQLAlchemy, Pydantic |
| Architectural pattern | 3 | CQRS, event sourcing, middleware chain, DI |
| Configuration/tooling | 1 | ESLint, Prettier, CI config |

- No signals found → skip MCP Ref research, log `"MCP Ref skipped: no technology decisions detected"`
- Fewer than 3 topics with weight >= 3 → skip

#### 7c) Stack Detection

Priority order:
1. `tech_stack` input parameter → use directly as `query_prefix`
2. `docs/tools_config.md` Research section → extract stack hints
3. Glob for indicator files:

| Indicator | Stack | Query Prefix |
|-----------|-------|--------------|
| `*.csproj`, `*.sln` | .NET | `"C# ASP.NET Core"` |
| `package.json` + `tsconfig.json` | Node.js | `"TypeScript Node.js"` |
| `requirements.txt`, `pyproject.toml` | Python | `"Python"` |
| `go.mod` | Go | `"Go Golang"` |
| `Cargo.toml` | Rust | `"Rust"` |
| `build.gradle`, `pom.xml` | Java | `"Java"` |

4. Parse context_files for technology mentions (fallback heuristic)

Output: `detected_stack = {query_prefix}` or empty (generic queries)

#### 7d) Extract Topics (3-5)

- Parse all context_files for technology decisions
- Score each by weight from 7b table
- Take top 3-5 with weight >= 3
- Format: `{topic_name, plan_statement, file_path, line_ref}`

#### 7e) MCP Ref Research

Per `research_tool_fallback.md` chain: Ref -> Context7 -> WebSearch -> built-in knowledge.

For each topic:
- Query: `"{query_prefix} {topic} RFC standard best practices {current_year}"`
- Collect: `{official_position, source, matches_plan: bool}`
- Run queries in parallel where possible

#### 7f) Compare & Correct

For each topic where `matches_plan == false` (high confidence):
- Apply surgical Edit to plan file (single-line or minimal multi-line change)
- Add inline rationale: `"(per {RFC/standard}: ...)"`
- Record correction in findings

For each topic where finding is ambiguous:
- Record as `"REVIEW NEEDED"` (not auto-corrected)

`IF Plan Mode -> corrections applied to plan-mode file directly.`

**Safety rules:**
- Max 5 corrections per run
- Each correction must cite specific RFC/standard/doc
- Only correct when official docs directly contradict plan statement

#### 7g) Save Findings

Write to `.agent-review/context/{identifier}_mcp_ref_findings.md` (per `references/mcp_ref_findings_template.md`).

`IF Plan Mode -> output findings to chat, skip file write.`

Display: `"MCP Ref: {N} topics validated, {M} corrections, {K} confirmed"`

---

8) **Critical Verification + Debate:** per shared workflow, with MCP Ref enhancement:
   - If MCP Ref research completed (7b-7g), use findings to inform AGREE/DISAGREE decisions
   - Agent suggestion contradicts MCP Ref finding → DISAGREE with RFC/standard citation
   - Agent suggestion aligns with MCP Ref finding → AGREE with higher confidence
   - Agent suggests something MCP Ref didn't cover → standard verification (no enhancement)

9) **Aggregate + Return:** per shared workflow. Merge agent suggestions + MCP Ref corrections into unified output.

10) **Save Review Summary:** per shared workflow "Step: Save Review Summary". `IF Plan Mode → output to chat, skip file save.`

## Output Format

```yaml
verdict: CONTEXT_ACCEPTABLE | SUGGESTIONS | SKIPPED
mcp_ref_corrections:
  count: 2
  topics_validated: 5
  corrections:
    - topic: "OAuth 2.0"
      file: "plan.md"
      line: 42
      before: "Use implicit flow"
      after: "Use Authorization Code + PKCE (RFC 6749)"
      source: "ref_search_documentation"
  findings_file: ".agent-review/context/{identifier}_mcp_ref_findings.md"
suggestions:
  - area: "logic | feasibility | completeness | consistency | best_practices | risk"
    issue: "What is wrong or could be improved"
    suggestion: "Specific actionable change"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | accepted_after_followup | rejected"
```

- `mcp_ref_corrections`: present only when MCP Ref research ran. Omitted when skipped.
- Agent stats and debate log per shared workflow output schema.

## Verdict Escalation
- **No escalation.** Suggestions are advisory only.
- Caller decides how to apply accepted suggestions.

## Reference Files
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/context_review.md`
- **Review schema:** `shared/agents/schemas/context_review_schema.json`
- **Research fallback:** `shared/references/research_tool_fallback.md`
- **MCP Ref findings template:** `references/mcp_ref_findings_template.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-03-06
