---
name: prompt-engineer
description: "Expert prompt engineering for building AI agents via Claude, GPT, and Gemini APIs. Triggers when: writing or editing system prompts, tool descriptions, agent instructions, function calling schemas, tool response design, context engineering, agentic system design, or discussing prompt quality for any LLM API. Also triggers on: prompt optimization, tool-use accuracy, cross-provider compatibility, or prompt review. Examples: 'improve the system prompt', 'write a tool description', 'the agent keeps calling the wrong tool', 'make this work on Gemini too', 'the tool returns too much data', 'design the agent context flow'."
---

# Prompt Engineering for AI Agent APIs

Guidelines for writing system prompts, tool descriptions, and agent instructions for building AI agents via the Claude, GPT, and Gemini APIs.

## Process

When editing an existing prompt, follow this order:
1. **Read** the full existing prompt. Understand its intent, structure, and target provider.
2. **Identify** the specific failure mode or improvement needed. Don't rewrite what isn't broken.
3. **Draft** the minimal change that addresses the issue, following the guidelines below.
4. **Re-read** the full prompt after editing to check for contradictions or broken flow.
5. **Test** the prompt on the target provider with representative inputs.

For new prompts: start minimal (role + constraints + examples + output format), test, then add instructions only when you observe failure modes.

Before submitting any prompt edit: check for contradictions (if two rules conflict, the model picks arbitrarily — remove one), and verify clarity (could a colleague with no context follow this prompt unambiguously?).

## A. Universal Best Practices

These apply to all three providers and cover ~70% of prompt engineering work.

### System Prompt Structure
- **Set a clear role** in one sentence at the top. Every provider respects persona framing.
- **Use XML tags** (`<role>`, `<constraints>`, `<examples>`, `<output_format>`) to separate sections. All three providers parse XML — it is the safest cross-provider delimiter.
- **Be explicit and specific.** Explain *why* a behavior matters, not just *what* to do. Models generalize better from explanations than from rigid rules.
- **Tell the model what TO do**, not what NOT to do. Positive framing ("Write in prose paragraphs") beats negative ("Don't use markdown").
- **Start minimal, then iterate.** Add instructions only when you observe failure modes. Over-engineered prompts cause over-analysis on Gemini and overtriggering on Claude.

### Few-Shot Examples
- Include **3-5 diverse examples** — one of the most reliable steering mechanisms across all providers.
- Cover typical cases, edge cases, and at least one "what not to do" example.
- Wrap in `<example>` tags with `<input>` and `<output>` sub-tags.
- Budget models need MORE examples (5-6 minimum) with simpler patterns.

### Output Format
- **Define output format explicitly** — JSON schema, markdown template, or structured text.
- Provide a concrete example of the expected output, not just a description.
- Use **enum arrays** for valid values rather than prose descriptions — works on all providers and improves accuracy.

### Context Engineering
- Context window is working memory. Every token competes for attention — more is not always better. Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome.
- **Put long documents at the top**, queries and instructions at the bottom. This ordering improves response quality by up to 30% on complex multi-document inputs.
- **Prefer progressive discovery** — let agents find context through tools rather than front-loading everything. Maintain lightweight identifiers (paths, names, links) and load full content dynamically. Combine upfront retrieval (fast, known-relevant) with autonomous exploration (discovers unknowns).
- **Use semantic names over technical IDs** — replace UUIDs, mime_types, internal codes with human-readable names (file names, descriptive labels). LLMs reason more accurately over natural language than opaque identifiers.
- When context grows large, ask the model to **quote relevant sections first** before reasoning — this cuts through noise and grounds the response.
- For multi-turn agents: **compact and summarize** conversation history at context limits, preserving key decisions and findings. Use a cheap model (Flash, Haiku) for summarization.
- For long-horizon tasks: maintain **structured notes** (scratchpad, state JSON) outside the conversation for information that must survive compaction.
- **Irrelevant context actively degrades performance** — ruthlessly trim what the current step does not need. Performance degrades gradually (not a cliff) as context grows.

### Task Decomposition
- Break complex tasks into phases with clear handoff points.
- Define success criteria for each phase so the model can self-check.
- Use separate prompt templates for distinct subtasks (analysis, extraction, generation).
- For complex workflows, break into sequential chained prompts — output from one becomes input for the next. Both GPT and Gemini perform better on focused prompts than bundled mega-prompts.

### Agentic Systems
When designing multi-step or multi-agent workflows:
- **Subagent design** — give each subagent a focused prompt and a minimal tool set. Choose whether to pass parent context based on the task: isolated subagents (no inherited context) prevent context pollution; context-aware subagents (with injected state) enable continuity. Either way, return a condensed summary (1-2K tokens) to the orchestrator, not raw exploration.
- **State management** — use structured JSON for trackable state (phase progress, scores, pass/fail) and free text for qualitative notes (findings, reasoning). Emit state updates the orchestrator can act on.
- **Context across windows** — when a task spans multiple context windows, start the new window with a structured summary of prior findings, not raw conversation history.
- **Autonomy calibration** — be explicit about what the agent MAY do autonomously vs. what requires confirmation. Default: read operations are autonomous, write/delete operations require confirmation. Claude 4.6 is highly proactive — dial back aggressive prompting or it will over-act.
- **Delegation discipline** — Claude 4.6 over-spawns subagents for simple tasks. Add: "Only delegate when the task requires specialized tools or a clean context. For simple lookups, do it yourself."

## B. Tool Descriptions

Tool descriptions are **the single most impactful quality factor** for tool-use accuracy across all three providers.

### Minimum Requirements
- **Full models: 3-4 sentences minimum.** Budget models: 5-6 sentences.
- Every tool description must cover:
  1. **What it does** — one clear sentence
  2. **When to use it** — specific triggers and conditions
  3. **When NOT to use it** — common mistakes and overlapping tools
  4. **Parameters** — type, constraints, valid values, format for each
  5. **Return value** — what comes back and what does NOT
  6. **Caveats** — rate limits, data freshness, error conditions

### Architecture
- **Limit active tools to 10-20** for best accuracy on all providers. Use tool search or dynamic loading for larger sets — both Anthropic and OpenAI recommend deferring infrequently-used tools.
- Curate a minimal set — if a human cannot definitively choose between two tools, the model cannot either.
- **Build tools around workflows**, not API wrappers. `schedule_event` (finds availability AND books) beats separate `list_users` + `list_events` + `create_event`. Fewer, higher-value tools outperform many narrow ones.
- Use meaningful namespaced names in snake_case (`github_list_prs`, not `list`). Group related tools with prefixes. Some providers reject names with spaces or special characters.
- Design tool responses carefully — see Tool Response Design below.
- All three providers support **parallel tool calling** — design tools to be independently callable.
- **Iterate via evaluation**: small description improvements yield dramatic gains. Create realistic multi-tool test cases, run programmatically, analyze transcripts. When a tool is misused, fix the description first — it's the highest-leverage fix.

### Provider-Specific Tool Guidance

| Aspect | Claude | GPT | Gemini |
|--------|--------|-----|--------|
| Description style | Detailed narrative (3-4 sentences) | CTCO: Context, Task, Constraints, Output | Short and direct; use enum arrays heavily |
| Strict schema | Supported | `strict: true` for 100% schema adherence | Up to 512 declarations; 10-20 active recommended |
| Tool preambles | Not needed | "Before calling a tool, explain why" boosts accuracy | Not needed |
| Error recovery | Handles well natively | Handles well natively | Add: "Don't repeat failed calls with identical arguments" |
| Scope creep risk | Low | High — add "Do ONLY what is requested" | Moderate |

### Effective Patterns from Production Systems
Patterns from Claude Code's tool descriptions and other production agents:
- **Decision-tree routing**: "ALWAYS use X for Y. NEVER use Z — use W instead." Direct, unambiguous tool selection.
- **When to use / When NOT to use as first-class sections** — put these at the top of the description, not buried after parameter docs. Include specific triggers, not just "when relevant."
- **Name alternatives explicitly**: "Do NOT use for searching employees — use search_employees instead." The model needs to know what to call instead.
- **Safety constraints separated** — mark irreversible or dangerous operations distinctly from functional description.
- **Concrete thresholds** — "3+ steps" not "complex tasks"; "at least 2 characters" not "enough text." Numeric where possible.

### Input Examples
For complex tools with nested objects, format-sensitive parameters, or tools that are easily confused with each other — add 1-5 input examples showing realistic parameter values. This improves parameter accuracy from 72% to 90%.

See `${CLAUDE_SKILL_DIR}/templates/tool-description-template.md` for the full structured format.

### Tool Response Design
Tool responses are context — bloated responses waste tokens and degrade reasoning on subsequent steps.
- **Return only high-signal information.** Strip internal IDs, metadata, and fields the model will not use.
- **Use semantic values over technical ones** — return `file_type: "spreadsheet"` not `mime_type: "application/vnd.openxmlformats..."`. Return `status: "approved"` not `status_code: 3`.
- **Paginate large results** with sensible defaults. Include total count and a guidance message: `"Showing 20 of 487 results. Narrow your query or use offset for next page."` — steer the model toward targeted searches.
- **Truncate long text** with a structural outline — return the first N lines plus an outline (headers, sections) so the model can request specific parts.
- **Explicit absence** — state what is NOT included: `"Does NOT include financial data — use get_project_details."` This prevents hallucinated fields.
- **Actionable errors** — return specific, actionable error messages, not opaque codes. `"No results for 'XYZ'. Try broader terms or check spelling."` beats `"Error 404"`.
- **Response format parameter** — expose a `format` parameter (`"detailed"` vs `"concise"`) letting agents choose output verbosity. A concise response can be 3x fewer tokens than detailed, saving context for reasoning.

## C. Provider Differences

### System Prompt Role and Placement

| Aspect | Claude | GPT | Gemini |
|--------|--------|-----|--------|
| System role name | `system` | `developer` (prioritized over user) | `system_instruction` |
| Instruction placement | Top works best | BOTH start AND end (recency bias) | Critical constraints go LAST |
| Multi-turn drift | System prompt persists well | Reappend key instructions every 3-5 messages | System instruction persists well |
| Default verbosity | Verbose — request conciseness if needed | Moderate — use `text.verbosity` param | Concise — request elaboration if needed |

### Prompting Style

| Aspect | Claude | GPT | Gemini |
|--------|--------|-----|--------|
| Aggressive language | **Avoid** — 4.6 is proactive by default; aggressive prompting causes overtriggering and over-action | Unnecessary on GPT-5 (most steerable model); contradictions actively harmful | Avoid — causes over-analysis |
| Chain-of-thought | Not needed — use adaptive thinking | **Harmful** on reasoning models — degrades performance | Not needed — use thinkingLevel |
| Prompt length | Medium-length prompts work well | Longer prompts tolerated | Short, direct prompts work best |
| Structuring | XML tags (strongest support) | XML or markdown (JSON wrapping degrades perf) | XML, markdown, or plain text — be consistent |
| Persona handling | Follows but maintains guardrails | Follows reasonably | Takes personas VERY seriously — may override other instructions |
| Non-English output | Follows prompt language naturally | Needs mild nudging | Requires aggressive: "RESPOND IN {LANGUAGE}. YOU MUST RESPOND UNMISTAKABLY IN {LANGUAGE}." |

### Reasoning and Thinking

| Aspect | Claude | GPT | Gemini |
|--------|--------|-----|--------|
| Mechanism | Adaptive by default; use `effort` param (low/medium/high) for control | `reasoning.effort`: minimal/medium/high; peaks across multiple agent turns | `thinkingLevel`: minimal/low/medium/high |
| Default state | Adaptive (model decides) — no config needed | OFF — must enable explicitly | Cannot disable on latest Pro models |
| Temperature | 0.0-1.0 typical range | 0.0-1.0 typical range | **Keep at 1.0** — lowering causes looping/degradation |
| Trace reuse | Not supported | `previous_response_id` saves tokens in multi-turn | Not supported |

### Caching

| Aspect | Claude | GPT | Gemini |
|--------|--------|-----|--------|
| Mechanism | Developer-controlled cache breakpoints (`cache_control`) | Automatic prefix-based (≥1024 tokens, 128-token granularity) | Implicit (automatic) + explicit (`CachedContent` objects) |
| Cost savings | Cache reads at 10% of input cost (90% savings) | Cache reads ~80% cheaper than standard input | Model-dependent; explicit caching reduces per-request cost |
| Minimum tokens | 1,024-4,096 depending on model | 1,024 tokens | Varies by model |
| TTL | 5 min (default) or 1 hour; reads reset TTL | ~5-10 min automatic; 24h with extended caching | 1 hour default; configurable per CachedContent |

**Cache-aware prompt design** (applies to all providers, saves 80-90% on input costs):
- **Structure static → dynamic**: place system prompt, tool definitions, and examples first (stable prefix). Put user input and conversation history last. The prefix must be byte-identical across requests.
- **Never reorder**: changing tool order, image order, or message order between requests breaks the cache on all providers. Append new messages — never modify earlier ones.
- **Multi-turn**: append assistant response + new user message at the end. The stable prefix (system + tools + earlier messages) hits cache automatically.
- **Monitor**: check `cache_read_input_tokens` (Claude), `cached_tokens` (GPT), or cache metadata (Gemini) in responses to verify hits.

### Unique Features
- **Claude:** Prefill removed in 4.6. Adaptive thinking is default — no config needed. Context-aware (can track remaining context window). Parallel tool calling ~100% success with explicit instruction. Use `effort` param (not `budget_tokens`) for thinking control. Tool search available for deferring large tool sets.
- **GPT:** `developer` role prioritized over `user` — security-sensitive instructions go in developer message. `strict: true` guarantees 100% JSON schema adherence. Independent `text.verbosity` param (low/medium/high) controls output length separately from reasoning depth. `previous_response_id` preserves reasoning across turns (73.9% → 78.2% on benchmarks). Contradictions in prompts are more damaging in GPT-5 — it spends tokens reconciling conflicts instead of ignoring them.
- **Gemini:** Native Google Search grounding (exclusive). Media resolution control for multimodal (image/video/PDF token budgets). Cannot combine built-in tools with custom function calling simultaneously. Few-shot examples are critical — "prompts without few-shot examples are likely to be less effective." Default verbosity is terse — request elaboration explicitly. Add temporal grounding ("Remember it is {YEAR} this year") for time-sensitive tasks. Completion priming (start the response, let model continue) is more reliable than describing format preferences. Thought signatures (`thoughtSignatures`) preserve reasoning chains across multi-turn calls — capture and return them to maintain coherence.

## D. Budget Models

Budget models (Claude Haiku 4.5, GPT-5 Mini, Gemini 3 Flash / 3.1 Flash Lite) share common patterns:

### What Changes
- **More explicit instructions** — less capable at inferring intent from context.
- **More examples** — 5-6 minimum, simpler patterns, covering more edge cases.
- **Simpler tool sets** — fewer tools with clearer boundaries. Consolidate where possible.
- **Shorter system prompts** — trim context aggressively; budget models lose more from noise.
- **Longer tool descriptions** — 5-6 sentences minimum instead of 3-4.

### Best Uses by Tier

| Task Type | Haiku 4.5 | GPT-5 Mini | Flash / Flash Lite |
|-----------|-----------|------------|---------------------|
| Classification / routing | Excellent | Good | Excellent |
| Structured extraction | Good | Good | Good |
| Simple tool use | Good | Good | Good |
| Complex reasoning | Use full model | Use full model | Use full model |
| Multimodal (image/PDF) | Adequate | Adequate | Flash excellent |
| High-volume batch | Good value | Good value | Flash Lite best value |

### Practical Pattern
Use budget models for fast/cheap phases (extraction, classification, routing) and full models for complex phases (analysis, recommendation, generation). This is the standard multi-tier agent pipeline.

**Warning**: tools designed for weaker models can actively harm stronger ones. Detailed workarounds and hand-holding that help Haiku may cause Opus to overtrigger or over-act. When supporting multiple model tiers, test tool descriptions on each tier — or use model-conditional tool descriptions.

## E. Cross-Provider Compatibility

When writing prompts that must work across providers or when provider-switching is likely:

### Safe Everywhere
- XML tags for structure
- Markdown headers and lists
- Few-shot examples in `<example>` tags — also work as implicit constraint enforcers (can sometimes replace explicit instructions if examples are clear enough)
- Enum arrays for valid values
- Role/persona in the first sentence
- Positive framing ("do X" not "don't do Y")
- Explicit output format with concrete examples

### Must Abstract Per Provider (in your agent framework, not in the prompt)
- Thinking/reasoning configuration (API parameter, not prompt content)
- Temperature settings (especially Gemini's 1.0 requirement)
- System message role name (`system` vs `developer` vs `system_instruction`)
- Caching strategy (manual breakpoints vs automatic prefix vs automatic)
- Tool schema strictness (`strict: true` is GPT-specific)
- Reasoning effort levels (different scales per provider)

### Cross-Provider Prompt Pattern
Write the core prompt once using XML structure, then wrap provider-specific adjustments in your agent framework:
1. **Core prompt:** role + constraints + tools + examples + output format (XML tags)
2. **Provider adapter:** instruction placement, language enforcement, anti-scope-creep guardrails
3. **Model adapter:** thinking config, temperature, caching, max tokens

## F. Examples

### Good vs Bad System Prompt Opening

<example>
<label>Good — clear role, explains why</label>
<content>
You are a senior auditor analyzing government tender documents. Your goal is to identify eligibility requirements and scoring criteria so the firm can decide whether to bid.

When requirements are ambiguous, flag them explicitly rather than guessing. The cost of missing a requirement is much higher than the cost of flagging a false positive.
</content>
<reasoning>
Sets a clear role in one sentence. Explains the goal. Provides a decision-making principle with the WHY behind it (cost asymmetry). The model can now generalize this principle to novel situations.
</reasoning>
</example>

<example>
<label>Bad — vague, no reasoning</label>
<content>
You are a helpful assistant. Be thorough and accurate. Don't make mistakes. Always double-check your work.
</content>
<reasoning>
No specific role. "Be thorough" and "don't make mistakes" are meaningless — every model already tries to be accurate. No explanation of WHY or HOW to prioritize. The model has nothing to generalize from.
</reasoning>
</example>

### Good vs Bad Tool Description

<example>
<label>Good — covers all 6 required elements</label>
<content>
Search for projects in the database using full-text search. Use when the user asks about past work, specific projects, or experience in a domain. Do NOT use for searching employees or clients — use search_employees or search_clients instead.

Args:
    query: str. Search terms (Hebrew or English). For Hebrew prefix matching, use at least 2 characters. Example: "ביקורת רשויות"
    limit: int, optional. Max results to return. Default 10.

Returns a list of records with: project_id, name, client_name, year, scope, team_members. Does NOT include financial data — use get_project_details for billing.
</content>
<reasoning>
Covers: what it does, when to use it, when NOT to use it (with alternatives), parameter details with example, return value with explicit exclusions. 6 sentences. A model reading this cannot misuse the tool.
</reasoning>
</example>

<example>
<label>Bad — one-liner</label>
<content>
Searches projects.
</content>
<reasoning>
Missing: when to use, when not to use, parameters, return value, caveats. The model will guess — and guess wrong. This is the #1 cause of poor tool-use accuracy.
</reasoning>
</example>

## G. Common Anti-Patterns

Recognize these urges and resist them:

- **"Let me add more detail to be safe"** — Over-engineered prompts cause over-analysis (Gemini) and overtriggering (Claude). Start minimal, add only what fixes observed failures.
- **"CRITICAL: YOU MUST ALWAYS..."** — Aggressive language overtriggers on Claude 4.6 and causes over-analysis on Gemini. Use calm, direct instructions.
- **"Think step by step"** — Harmful on GPT reasoning models. Unnecessary on Claude/Gemini (use their thinking APIs instead). Remove manual chain-of-thought from prompts targeting reasoning-capable models.
- **"Don't hallucinate"** — Negative framing is less effective. Instead: "Ground all claims in provided documents. Quote the relevant section before answering." (See Context Engineering.)
- **Adding 20+ tools** — Too many overlapping tools is the #1 failure mode across all providers. If you can't choose between two tools as a human, the model can't either.
- **Wrapping APIs as tools** — building 1:1 API-to-tool mappings instead of workflow-oriented tools. `schedule_event` (finds availability AND books) beats separate `list_users` + `list_events` + `create_event`.
- **Over-delegating to subagents** — Claude 4.6 spawns subagents for tasks it could handle directly. If the task needs no specialized tools or clean context, do it in-line.
- **Rewriting the whole prompt** — When editing, preserve existing structure and tone. Make the minimal change that fixes the issue. Re-read the full prompt after editing.
- **Prompt archaeology neglect** — instructions effective in GPT-4/Claude 3.5 may backfire in newer models. When upgrading models, audit prompts for obsolete aggressive encouragement — native capabilities make external prodding redundant.
- **Assuming all providers behave the same** — They don't. Check Section C for differences in instruction placement, verbosity defaults, persona handling, and temperature.

## H. Testing Prompts

Don't iterate blindly. Build simple evaluations:
1. **Identify failures** — run the agent on representative tasks without changes. Note specific failures.
2. **Fix one thing at a time** — make a single change, re-test, measure. Don't bundle multiple changes.
3. **Test on the target model tier** — what works on Opus/GPT-5.4/Gemini Pro may need more detail for Haiku/Mini/Flash.
4. **Use adversarial inputs** — empty strings, unexpected languages, edge cases, tools that shouldn't be called.
5. **After 2 failed correction attempts** — stop iterating. Start fresh with a better initial prompt incorporating lessons learned.

## Templates

Reference templates in `${CLAUDE_SKILL_DIR}/templates/`:
- `system-prompt-template.md` — Contract-style system prompt structure
- `tool-description-template.md` — Structured tool description format
