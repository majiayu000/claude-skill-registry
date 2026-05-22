---
name: prompt-engeneering
description: Universal prompt engineering techniques for any LLM. Use when crafting, optimizing, or reviewing prompts for AI models. Triggers on requests like "improve this prompt", "write a system prompt", "optimize my instructions", "help me prompt engineer", "audit this prompt", "review my prompt", or when building agentic systems that need structured prompts.
---

# Prompt Engineering

Universal techniques for crafting effective prompts across any LLM.

## Core Principles

### 1. Structure with XML Tags

Use XML tags to create clear, parseable prompts:

```xml
<context>Background information here</context>
<instructions>
1. First step
2. Second step
</instructions>
<examples>Sample inputs/outputs</examples>
<output_format>Expected structure</output_format>
```

**Benefits:**
- **Clarity**: Separates context, instructions, and examples
- **Accuracy**: Prevents model from mixing up sections
- **Flexibility**: Easy to modify individual parts
- **Parseability**: Enables structured output extraction

**Best practices:**
- Use consistent tag names throughout (`<instructions>`, not sometimes `<steps>`)
- Reference tags explicitly: "Using the data in `<context>` tags..."
- Nest tags for hierarchy: `<examples><example id="1">...</example></examples>`
- Combine with other techniques: `<thinking>` for chain-of-thought, `<answer>` for final output

### 2. Control Output Shape

Specify explicit constraints on length, format, and structure:

```xml
<output_spec>
- Default: 3-6 sentences or ≤5 bullets
- Simple yes/no questions: ≤2 sentences
- Complex multi-step tasks:
  - 1 short overview paragraph
  - ≤5 bullets: What changed, Where, Risks, Next steps, Open questions
- Use Markdown with headers, bullets, tables when helpful
- Avoid long narrative paragraphs; prefer compact structure
</output_spec>
```

### 3. Prevent Scope Drift

Explicitly constrain what the model should NOT do:

```xml
<constraints>
- Implement EXACTLY and ONLY what is requested
- No extra features, components, or embellishments
- If ambiguous, choose the simplest valid interpretation
- Do NOT invent values, make assumptions, or add unrequested elements
</constraints>
```

### 4. Handle Ambiguity Explicitly

Prevent hallucinations and overconfidence:

```xml
<uncertainty_handling>
- If the question is ambiguous:
  - Ask 1-3 precise clarifying questions, OR
  - Present 2-3 plausible interpretations with labeled assumptions
- When facts may have changed: answer in general terms, state uncertainty
- Never fabricate exact figures or references when uncertain
- Prefer "Based on the provided context..." over absolute claims
</uncertainty_handling>
```

### 5. Long-Context Grounding

For inputs >10k tokens, add re-grounding instructions:

```xml
<long_context_handling>
- First, produce a short internal outline of key sections relevant to the request
- Re-state user constraints explicitly before answering
- Anchor claims to sections ("In the 'Data Retention' section...")
- Quote or paraphrase fine details (dates, thresholds, clauses)
</long_context_handling>
```

## Agentic Prompts

### Tool Usage Rules

```xml
<tool_usage>
- Prefer tools over internal knowledge for:
  - Fresh or user-specific data (tickets, orders, configs)
  - Specific IDs, URLs, or document references
- Parallelize independent reads when possible
- After write operations, restate: what changed, where, any validation performed
</tool_usage>
```

### User Updates

```xml
<user_updates>
- Send brief updates (1-2 sentences) only when:
  - Starting a new major phase
  - Discovering something that changes the plan
- Avoid narrating routine operations
- Each update must include a concrete outcome ("Found X", "Updated Y")
- Do not expand scope beyond what was asked
</user_updates>
```

### Self-Check for High-Risk Outputs

```xml
<self_check>
Before finalizing answers in sensitive contexts (legal, financial, safety):
- Re-scan for unstated assumptions
- Check for ungrounded numbers or claims
- Soften overly strong language ("always", "guaranteed")
- Explicitly state assumptions
</self_check>
```

## Structured Extraction

For data extraction tasks, always provide a schema:

```xml
<extraction_spec>
Extract data into this exact schema (no extra fields):
{
  "field_name": "string",
  "optional_field": "string | null",
  "numeric_field": "number | null"
}
- If a field is not present in source, set to null (don't guess)
- Re-scan source for missed fields before returning
</extraction_spec>
```

## Web Research Prompts

```xml
<research_guidelines>
- Browse the web for: time-sensitive topics, recommendations, navigational queries, ambiguous terms
- Include citations after paragraphs with web-derived claims
- Use multiple sources for key claims; prioritize primary sources
- Research until additional searching won't materially change the answer
- Structure output with Markdown: headers, bullets, tables for comparisons
</research_guidelines>
```

## Example: Before/After

**Without structure:**
```
You're a financial analyst. Generate a Q2 report for investors. Include Revenue, Margins, Cash Flow. Use this data: {{DATA}}. Make it professional and concise.
```

**With structure:**
```xml
You're a financial analyst at AcmeCorp generating a Q2 report for investors.

<context>
AcmeCorp is a B2B SaaS company. Investors value transparency and actionable insights.
</context>

<data>
{{DATA}}
</data>

<instructions>
1. Include sections: Revenue Growth, Profit Margins, Cash Flow
2. Highlight strengths and areas for improvement
3. Use concise, professional tone
</instructions>

<output_format>
- Use bullet points with metrics and YoY changes
- Include "Action:" items for areas needing improvement
- End with 2-3 bullet Outlook section
</output_format>
```

## Prompt Migration Checklist

When adapting prompts across models or versions:

1. **Switch model, keep prompt identical** — isolate the variable
2. **Pin reasoning/thinking depth** to match prior model's profile
3. **Run evals** — if results are good, ship
4. **If regressions, tune prompt** — adjust verbosity/format/scope constraints
5. **Re-eval after each small change** — one change at a time

## Quick Reference

| Technique | Tag Pattern | Use Case |
|-----------|-------------|----------|
| Separate sections | `<context>`, `<instructions>`, `<data>` | Any complex prompt |
| Control length | `<output_spec>` with word/bullet limits | Prevent verbosity |
| Prevent drift | `<constraints>` with explicit "do NOT" | Feature creep |
| Handle uncertainty | `<uncertainty_handling>` | Factual queries |
| Chain of thought | `<thinking>`, `<answer>` | Reasoning tasks |
| Extraction | `<schema>` with JSON structure | Data parsing |
| Research | `<research_guidelines>` | Web-enabled agents |
| Self-check | `<self_check>` | High-risk domains |
| Tool usage | `<tool_usage_rules>` | Agentic systems |
| Eagerness control | `<persistence>`, `<context_gathering>` | Agent autonomy |
| Persona | `<role>` + behavioral constraints | Tone & style |

## Prompting Techniques Catalog

Comprehensive catalog of prompting techniques. Full details, examples, and academic references in [references/prompting-techniques.md](references/prompting-techniques.md).

| Technique | Use Case |
|-----------|----------|
| **Zero-Shot Prompting** | Direct task execution without examples; classification, translation, summarization |
| **Few-Shot Prompting** | In-context learning via exemplars; format control, label calibration, style matching |
| **Chain-of-Thought (CoT)** | Step-by-step reasoning; arithmetic, logic, commonsense reasoning tasks |
| **Meta Prompting** | LLM as orchestrator delegating to specialized expert prompts; complex multi-domain tasks |
| **Self-Consistency** | Sample multiple CoT paths, pick majority answer; boost accuracy on math & reasoning |
| **Generated Knowledge** | Generate relevant knowledge first, then answer; commonsense & factual QA |
| **Prompt Chaining** | Break complex tasks into sequential subtasks; document analysis, multi-step workflows |
| **Tree of Thoughts (ToT)** | Explore multiple reasoning branches with lookahead/backtracking; planning, puzzles |
| **RAG** | Retrieve external documents before generating; knowledge-intensive tasks, fresh data |
| **ART (Auto Reasoning + Tools)** | Auto-select and orchestrate tools with CoT; tasks requiring calculation, search, APIs |
| **APE (Auto Prompt Engineer)** | LLM generates and scores candidate prompts; prompt optimization at scale |
| **Active-Prompt** | Identify uncertain examples, annotate selectively for CoT; adaptive few-shot |
| **Directional Stimulus** | Add a hint/keyword to guide generation direction; summarization, dialogue |
| **PAL (Program-Aided LM)** | Generate code instead of text for reasoning; math, data manipulation, symbolic tasks |
| **ReAct** | Interleave reasoning traces with tool actions; search, QA, decision-making agents |
| **Reflexion** | Agent self-reflects on failures with verbal feedback; iterative improvement, debugging |
| **Multimodal CoT** | Two-stage: rationale generation then answer with text+image; visual reasoning tasks |
| **Graph Prompting** | Structured graph-based prompts; node classification, relation extraction, graph tasks |

### Prompting Fundamentals

LLM settings, prompt elements, formatting, and practical examples — see [references/prompting-introduction.md](references/prompting-introduction.md). Covers:
- **LLM Settings** — temperature, top-p, max length, stop sequences, frequency/presence penalties
- **Prompt Elements** — instruction, context, input data, output indicator
- **Design Tips** — start simple, be specific, avoid impreciseness, say what TO do (not what NOT to do)
- **Task Examples** — summarization, extraction, QA, classification, conversation, code generation, reasoning

### Risks & Misuses

Adversarial attacks, factuality issues, and bias mitigation — see [references/prompting-risks.md](references/prompting-risks.md). Covers:
- **Adversarial Prompting** — prompt injection, prompt leaking, jailbreaking (DAN, Waluigi Effect), defense tactics
- **Factuality** — ground truth grounding, calibrated confidence, admit-ignorance patterns
- **Biases** — exemplar distribution skew, exemplar ordering effects, balanced few-shot design

## Prompt Audit / Review

When asked to audit, review, or improve a prompt, follow this workflow. Full checklist with per-check references: [prompt-audit-checklist.md](references/prompt-audit-checklist.md).

### Workflow

1. **Read the prompt fully** — identify its purpose, target model, and deployment context (interactive chat, agentic system, batch pipeline, RAG-augmented)
2. **Walk 8 dimensions** — check each, note issues with severity (Critical / Warning / Suggestion):

| # | Dimension | What to Check |
|---|-----------|---------------|
| 1 | **Clarity & Specificity** | Task definition, success criteria, audience, output format, conflicting constraints |
| 2 | **Structure & Formatting** | Section separation (XML tags), prompt smells (monolithic, mixed layers, negative bias) |
| 3 | **Safety & Security** | Control/data separation, secrets in prompt, injection resilience, tool permissions |
| 4 | **Hallucination & Factuality** | Role framing, grounding, citation-without-sources, uncertainty handling |
| 5 | **Context Management** | Info placement (not buried in middle), context size, RAG doc count, re-grounding |
| 6 | **Maintainability & Debt** | Hardcoded values, regenerated logic, model pinning, testability |
| 7 | **Model-Specific Fit** | Model-specific params and gotchas (see Model-Specific Guides below) |
| 8 | **Evaluation Readiness** | Eval criteria, adversarial test cases, schema enforcement, monitoring |

3. **Produce a report** — issues table (dimension, check, severity, issue, fix) + rewritten prompt or targeted fix suggestions. Use the report template from the checklist reference.
4. **For each issue**, cite the relevant reference file so the user can dive deeper.

### Quick Decision: Which Dimensions to Prioritize

- **User-facing chatbot** → prioritize Safety (#3), Hallucination (#4), Clarity (#1)
- **Agentic system with tools** → prioritize Safety (#3), Context (#5), Maintainability (#6)
- **Batch/pipeline** → prioritize Structure (#2), Evaluation (#8), Maintainability (#6)
- **RAG-augmented** → prioritize Context (#5), Safety (#3), Hallucination (#4)

## Common Mistakes & Anti-Patterns

Three complementary layers — use the one matching your need:

**Deep-dives by category** — root causes, mechanisms, prevention checklists (from "The Architecture of Instruction", 2026):

| Mistake Category | Key Issues | Reference |
|-----------------|------------|-----------|
| **Hallucinations & Logic** | Ambiguity-induced confabulation, automation bias, overloaded prompts, logical failures in verification tasks, no role framing | [mistakes-hallucinations.md](references/mistakes-hallucinations.md) |
| **Structural Fragility** | Formatting sensitivity (up to 76pp variance), reproducibility crisis, prompt smells catalog (6 anti-patterns), deliberation ladder | [mistakes-structure.md](references/mistakes-structure.md) |
| **Context Rot** | "Lost in the middle" U-shaped attention, RAG over-retrieval, naive data loading, context engineering shift | [mistakes-context.md](references/mistakes-context.md) |
| **Prompt Debt** | Token tax of regenerative code, debt taxonomy (prompt/hyperparameter/framework/cost), multi-agent solutions, automated repair | [mistakes-debt.md](references/mistakes-debt.md) |
| **Security** | Direct/indirect injection, jailbreaking, system prompt leakage (OWASP LLM07:2025), RAG poisoning, multimodal injection, adversarial suffixes | [mistakes-security.md](references/mistakes-security.md) |

**Quick reference** — 18-category taxonomy with MRPs, risk scores, case studies, action items: [failure-taxonomy.md](references/failure-taxonomy.md). Start here for an overview or to prioritize which categories to address first. Covers: control-plane vs data-plane model, heuristic risk scoring, real-world incidents (EchoLeak CVE-2025-32711, Mata v. Avianca, Samsung shadow AI).

**How to measure & test** — eval metrics, CI gating, red-teaming, tooling: [evaluation-redteaming.md](references/evaluation-redteaming.md). Covers: TruthfulQA, FActScore, SelfCheckGPT, PromptBench, AILuminate, LLM-as-judge pitfalls, guardrail libraries, open research questions.

## Model-Specific Guides

Each model family has unique parameters, gotchas, and patterns. Consult the reference for your target model:

- **[Claude Family](references/claude-family-prompting.md)** — Opus/Sonnet 4.6: adaptive thinking (`effort` param), prefill deprecation (use Structured Outputs), tool overtriggering fix, prompt caching, citations, context engineering, agentic subagent patterns, vision, migration from 4.5
- **[GPT-5 Family](references/gpt5-family-prompting.md)** — GPT-5/5.1/5.2: `reasoning_effort` param (defaults vary per version), `verbosity` API control, named tools (`apply_patch`), agentic eagerness templates, compaction API, instruction conflict sensitivity, migration paths
- **[Gemini 3 Family](references/gemini3-family-prompting.md)** — Gemini 2.5/3/3.1: temperature MUST be 1.0, `thinking_budget` vs `thinking_level`, constraint placement (end of prompt), persona priority, function calling, structured output, multimodal, image generation
- **[GPT-5.2 Specifics](references/gpt5-prompting-guide.md)** — Compaction API code examples, web research agent prompt, full XML specification blocks