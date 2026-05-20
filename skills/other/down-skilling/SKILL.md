---
name: down-skilling
description: >-
  Distill Opus-level reasoning into optimized instructions for Haiku 4.5
  (and Sonnet). Generates explicit, procedural prompts with n-shot examples
  that maximize smaller model performance on a given task. Use when user says
  "down-skill", "distill for Haiku", "optimize for Haiku", "make this work
  on Haiku", "generate Haiku instructions", or needs to delegate a task to
  a smaller model with high reliability.
metadata:
  author: Oskar Austegard and Opus
  version: 1.1.0
---

# Down-Skilling: Opus → Haiku Distillation

Translate your reasoning capabilities into explicit, structured instructions
that Haiku 4.5 can execute reliably. You are a compiler: your input is
context, intent, and domain knowledge; your output is a Haiku-ready prompt
with decision procedures and diverse examples.

## Core Principle

Opus infers from WHY. Haiku executes from WHAT and HOW.

Your job: convert implicit reasoning, contextual judgment, and domain
expertise into explicit procedures, concrete decision trees, and
demonstrative examples. Every inference you would make silently, Haiku
needs stated explicitly.

## Economics: Why Examples Are Free

Opus input costs ~6× Haiku input. A task that costs $1.00 on Opus costs
~$0.17 on Haiku — but only if Haiku gets it right on the first try.
One retry wipes the savings; two retries makes Haiku more expensive.

**The math that matters:**
- Input tokens are cheap (Haiku: $0.80/MTok input vs $4.00/MTok output)
- Adding 2,000 tokens of examples costs ~$0.0016 per call
- A single failed-then-retried call costs ~$0.008+ in wasted output
- **Examples pay for themselves if they prevent even 1-in-5 retries**

**What this means for prompt design:**
- If you're sending an 8K token document, you can afford 3-4K tokens of
  examples — the examples cost less than the document itself
- Lengthy input prompts don't inflate output costs — output pricing is
  independent of input length
- The constraint is not token cost but diminishing returns: after 5-7
  examples, additional examples rarely improve performance

**Bottom line:** Every example that prevents a Haiku misfire saves 5-25×
its input cost in wasted output tokens. Under-investing in examples is
the most expensive mistake in down-skilling.

## Activation

When triggered, perform these steps:

1. **Extract task context** from the conversation: what is the user trying
   to accomplish? What domain knowledge applies? What quality criteria
   matter?

2. **Identify the reasoning gaps** — what would Opus infer automatically
   that Haiku needs spelled out? Common gaps:
   - Ambiguity resolution (Opus picks the sensible interpretation; Haiku
     needs a decision rule)
   - Quality judgment (Opus knows "good enough"; Haiku needs explicit
     criteria)
   - Edge case handling (Opus reasons through novel situations; Haiku
     needs enumerated cases)
   - Output calibration (Opus matches tone/length intuitively; Haiku
     needs explicit constraints)

3. **Generate the distilled prompt** following the structure in
   [Prompt Architecture](#prompt-architecture)

4. **Generate 4-7 diverse examples** following the principles in
   [Example Design](#example-design) — this is the highest-leverage step

5. **Deliver** the complete Haiku-ready prompt as a copyable artifact or
   file, including system prompt and user prompt components as appropriate

## Prompt Architecture

Structure every distilled prompt with these components in this order.
Haiku responds best to this specific sequencing:

```
<role>
[Single sentence: who Haiku is and what it does]
</role>

<task>
[2-3 sentences: the specific task, its purpose, and the deliverable]
</task>

<rules>
[Numbered list of explicit constraints. Be precise about:]
- Output format (JSON schema, markdown structure, etc.)
- Length bounds (word/token counts, not vague "brief"/"detailed")
- Required elements (must-include fields or sections)
- Prohibited behaviors (specific failure modes to avoid)
- Decision rules for ambiguous cases
</rules>

<process>
[Numbered steps. Maximum 7 steps. Each step is one action.]
[Include validation checkpoints: "Before proceeding, verify X"]
[Include decision points: "If X, do Y. If Z, do W."]
</process>

<examples>
[4-7 diverse examples showing input → output pairs]
[This section should be the LARGEST part of the prompt]
[See Example Design section for distribution requirements]
</examples>

<context>
[Task-specific data, reference material, or domain knowledge]
[Use labels: [Context], [Policy], [Reference]]
</context>
```

## Haiku Optimization Rules

Apply these when generating any Haiku-targeted prompt:

### Structure & Syntax
- Use XML tags to delimit every section — Haiku respects labeled boundaries
- Keep sentences under 25 words where possible
- One instruction per sentence; split compound instructions
- Use numbered steps, not prose paragraphs, for procedures
- Specify token/word budgets explicitly: "respond in 80-120 words"

### Reasoning Support
- Replace open-ended judgment with decision rubrics:
  BAD: "Assess whether the code is production-ready"
  GOOD: "Check: (a) no TODO comments, (b) all functions have error
  handling, (c) no hardcoded secrets. Score pass/fail per item."
- Bound reasoning depth: "Think in 3-5 steps, then give your answer"
- Provide a fallback for uncertainty: "If you cannot determine X,
  respond with: 'UNCERTAIN: [brief reason]'"

### Context Management
- Front-load critical instructions (Haiku attends strongly to position)
- Budget rule of thumb: instructions + rules ≤ 800 tokens, examples get
  the rest. For a task processing an 8K document, 3-4K tokens of examples
  is well within budget and pays for itself in reliability
- Pass only the 1-3 most relevant context snippets, not full documents
- Use explicit delimiters between context and instructions

### Output Control
- Require structured output (JSON, labeled sections) for extractable results
- Provide an output template Haiku can fill in
- Specify what comes first in the response: "Begin your response with..."
- For classification tasks, enumerate all valid categories

### Failure Prevention
- Anticipate Haiku's common failure modes and add guardrails:
  - **Hallucination**: "Use ONLY information from the provided context.
    If the answer is not in the context, say 'Not found in sources.'"
  - **Verbosity**: "Maximum 150 words. Do not add preamble or caveats."
  - **Format drift**: Include the output schema in both rules and examples
  - **Instruction skipping**: Number all constraints; reference them in
    the process steps: "Apply rules 2-4 from <rules>"

## Example Design

**Examples are the single highest-leverage investment in a Haiku prompt.**
Rules tell Haiku what to do; examples show it what "done right" looks
like. When rules and examples conflict, Haiku follows the examples.
When rules are ambiguous, Haiku extrapolates from examples. This makes
examples the primary steering mechanism — not a supplement to rules, but
the dominant signal.

Given the economics (see [Economics](#economics-why-examples-are-free)),
you should invest heavily here. A prompt with 800 tokens of rules and
3,000 tokens of examples will outperform one with 2,000 tokens of rules
and 500 tokens of examples almost every time.

### Minimum Example Count: 4

Generate **4-7 diverse examples** per distilled prompt. Fewer than 4 is
under-investing. The marginal cost of each example is negligible compared
to the reliability improvement. Use this distribution:

| # | Role | Purpose |
|---|------|---------|
| 1 | **Typical case** | The most common, straightforward input. Establishes the baseline pattern. |
| 2 | **Second typical variant** | A different but common input — varies length, domain, or structure from #1. Prevents Haiku from over-fitting to a single pattern. |
| 3 | **Edge case** | Unusual but valid input: empty fields, very long text, special characters, boundary conditions, ambiguous phrasing. |
| 4 | **Negative/rejection case** | Input that should be rejected, handled differently, or produce an empty/default output. Shows Haiku what NOT to do. |
| 5+ | **Tricky/boundary cases** | Inputs near decision boundaries where Haiku is most likely to fail. The cases you'd use for a test suite. |

**Why the second typical case matters:** With only one typical example,
Haiku may latch onto incidental features of that example (its length,
word choice, domain). A second typical case from a different angle shows
Haiku which features are task-relevant and which are coincidental.

### Example Format
```xml
<example>
<input>
[Realistic input data — use real-world length and complexity]
</input>
<output>
[Exact format Haiku should produce — not a description, the actual output]
</output>
<reasoning>
[1-2 sentences: WHY this output is correct. Which rules applied.
 What Haiku might have gotten wrong without this example.]
</reasoning>
</example>
```

**The `<reasoning>` tag is not optional for complex tasks.** It acts as
a chain-of-thought anchor, showing Haiku the reasoning pattern to follow.
For classification and extraction tasks, reasoning should reference the
specific rule numbers that drive the decision.

### Example Sizing Guidance

| Task processing... | Recommended example budget |
|---------------------|---------------------------|
| Short inputs (<500 tokens) | 1,500-2,500 tokens of examples (4-5 examples) |
| Medium inputs (500-4K tokens) | 2,500-4,000 tokens of examples (4-6 examples) |
| Long inputs (4K-8K tokens) | 3,000-5,000 tokens of examples (5-7 examples) |

These budgets assume Haiku's 200K context window. The constraint is
diminishing returns, not cost — after 7 examples the marginal benefit
drops sharply unless the task has a very large classification space.

### Example Quality Criteria
- Examples must be realistic, not toy data — match the complexity and
  messiness of real inputs
- Output format must be **identical** across all examples — Haiku treats
  format inconsistency as a signal that format doesn't matter
- Include the hardest case you expect Haiku to handle
- Vary input characteristics: length, complexity, domain, tone
- Never include an example that contradicts your rules
- Order examples from simplest to most complex — this progressive
  difficulty helps Haiku build up its understanding

## Delivery Format

Present the distilled prompt in a code block or artifact with clear
section markers. Include:

1. **System prompt** (if applicable): role + persistent rules
2. **User prompt template**: with {{placeholders}} for variable content
3. **Examples**: embedded in the prompt or as a separate few-shot section
4. **Usage notes**: any caveats about when this prompt may fail and what
   to watch for

When generating for API use, include the model parameter and recommended
settings:
```
model: claude-haiku-4-5-20251001
max_tokens: [appropriate for task]
temperature: 0 (for deterministic tasks) or 0.3 (for creative tasks)
```

## Agentic Resource Selection

The skill includes two directories of granular reference files. Do NOT
read them all. Scan the index below, then read only the files relevant
to the current task.

### gaps/

Each file documents one reasoning pattern where Haiku diverges from Opus,
with a tested mitigation strategy. Read 2-4 per task.

| File | Use when the task involves... |
|------|------|
| `ambiguity-resolution.md` | Input that has multiple valid interpretations; vague user requests |
| `code-generation.md` | Generating code, scripts, or queries; style matching to existing code |
| `comparative-analysis.md` | Comparing options, pros/cons, tradeoff analysis |
| `conditional-logic.md` | Decision trees, branching rules, nested if/then logic |
| `context-utilization.md` | Long context windows, documents >2K tokens, position-sensitive info |
| `counting-enumeration.md` | "Generate exactly N items", counting occurrences, list lengths |
| `creative-generation.md` | Writing, tone adaptation, persona consistency, style matching |
| `implicit-constraints.md` | Tasks where tone, audience, or format norms are assumed not stated |
| `instruction-density.md` | Tasks requiring 8+ simultaneous constraints; complex rule sets |
| `multi-hop-reasoning.md` | 3+ step inference chains; cause-effect-consequence analysis |
| `multi-turn-consistency.md` | Chatbot behavior, stateful conversations, persona maintenance |
| `negation-handling.md` | Constraints phrased as "don't", "never", "avoid"; prohibitions |
| `nuanced-classification.md` | Borderline cases, multi-label classification, overlapping categories |
| `output-calibration.md` | Length control, format precision, verbosity management (ALWAYS read) |
| `parallel-consistency.md` | Generating multiple similar items; lists where format must be uniform |
| `partial-information.md` | Missing fields, incomplete input, optional data, error states |
| `schema-adherence.md` | Structured output (JSON, tables) that must survive edge-case inputs |
| `self-correction.md` | Tasks needing verification; quality checks before output |
| `summarization-fidelity.md` | Summarizing documents without distortion, position bias, or fabrication |
| `tool-use-planning.md` | Multi-tool workflows, API orchestration, dependency ordering |

### examples/

Complete before/after distillations. Each shows an Opus-level task →
Haiku-optimized prompt with annotated examples. Read 1-2 closest to
the current task domain.

| File | Use when distilling... |
|------|------|
| `api-orchestration.md` | Multi-step tool/API workflows with dependencies and branching |
| `code-review-triage.md` | Analysis tasks with severity classification and structured JSON output |
| `content-moderation.md` | Safety-critical classification with "when uncertain" defaults |
| `creative-rewriting.md` | Tone adaptation, audience-aware rewriting, style transfer |
| `data-extraction.md` | Schema-bound extraction from unstructured text to JSON |
| `document-qa.md` | RAG / retrieval-grounded QA with citation and "not found" handling |
| `email-summarization.md` | Information extraction from conversations/threads into sections |
| `meeting-notes.md` | Transcript processing into decisions, actions, and next steps |
| `resume-screening.md` | Multi-criteria evaluation with parallel scoring structure |
| `sql-generation.md` | Natural language to code with schema constraints and error handling |
| `step-by-step-analysis.md` | Multi-step analytical reasoning with explicit decision rubrics |
| `text-classification.md` | Multi-label classification with confidence and ambiguity handling |

## Self-Check

Before delivering, verify the distilled prompt against these criteria:
- [ ] Every Opus inference is made explicit
- [ ] All constraints are numbered and cross-referenced
- [ ] 4+ diverse examples with consistent output format
- [ ] Examples include: 2 typical, 1+ edge case, 1+ negative/rejection case
- [ ] Example tokens ≥ 2× rule tokens (examples should be the bulk of the prompt)
- [ ] No instruction assumes Haiku will "figure it out"
- [ ] Decision points have explicit branches, not open-ended judgment
- [ ] Output format is demonstrated, not just described
- [ ] `<reasoning>` tags explain WHY each example output is correct
