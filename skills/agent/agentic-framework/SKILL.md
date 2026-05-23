---
name: agentic-framework
description: "Infinite Improvement Framework: Move from Probabilistic Agents to Deterministic Workflows."
trigger: framework OR agentic flow OR deterministic code OR directives OR workflow structure
scope: global
---

# Agentic Framework - The "Infinite Improvement" Loop

> [!NOTE]
> Transform "Probabilistic Hype" into "Deterministic Revenue". Stop asking Agents to _do_ the work; ask them to _build the machine_ that does the work.

## 1. The Paradigm Shift

- **Old Way (Probabilistic)**: User -> Prompt -> Agent -> Action (Result varies, error rate high).
- **New Way (Deterministic)**: User -> Prompt -> Agent -> **Code/Script** -> Action (Result consistent, error rate -> 0).

**Mantra**: _The Agent is not the worker; the Agent is the Engineer building the worker._

## 2. Core Structure: The Directory System

Organize your project to support this flow:

```
project_root/
├── directives/       # The "INTENT" - What we want to do (Markdown/Specs)
├── scripts/          # The "MACHINE" - Python/Node scripts that do the work
├── output/           # The "RESULT" - Deterministic artifacts
└── knowledge/        # The "CONTEXT" - Shared truths/docs
```

## 3. The "Infinite Improvement" Loop (IIL)

1. **Plan (Directives)**:
   - Don't just start coding. Define a `Directive`.
   - Format: "Input -> Process -> Output".
   - Example: `directives/linkedin_post_generator.md` containing the rules (Tone, Format, Constraints).

2. **Build (Scripts)**:
   - The Agent reads the Directive and writes a **Script** (e.g., `scripts/generate_post.py`).
   - The Script uses deterministic inputs (APIs, specific logic) where possible.
   - Ideally, the Script _calls_ an LLM only for the specific creative step, constrained by code.

3. **Execute**:
   - Run the script: `python scripts/generate_post.py`.
   - Cost is low (API calls controlled), execution is fast.

4. **Verify & Optimize**:
   - Check the `output/`.
   - If bad: **Do NOT just ask the Agent to "try again"**.
   - **Update the Directive**: Refine your instructions in the MD file.
   - **Rebuild the Script**: Agent updates the code based on new Directive.
   - **Loop**: This creates a flywheel of increasing precision.

## 4. Context Engineering

Reduce "Hallucinations" by engineering the context:

- **Directives**: Hard rules the Agent must follow when writing code.
- **Reference Docs**: API docs, Examples, Previous successes.
- **System Prompts**: Enforce acting as a "Senior Engineer" who respects the framework.

## 5. Practical Workflow Example (YouTube -> LinkedIn)

1. **Directive**: `directives/yt_to_linkedin.md`
   - "Input: YouTube URL. Output: LinkedIn Post in Spanish, no emojis, professional tone."
2. **Script**: `scripts/yt_converter.py`
   - Uses `Apify` to get transcript (Deterministic).
   - Uses `Gemini Flash` to summarize (Probabilistic but constrained).
   - Writes result to `Google Docs` (Deterministic).
3. **Action**: User runs `python scripts/yt_converter.py <url>`.
4. **Result**: Consistent output every time.

## 6. Why? (Business Value)

- **Scalability**: Scripts run cheaply and endlessly.
- **Predictability**: 1% error rate in Finance/Ops is unacceptable. Deterministic pipelines fix this.
- **Asset Generation**: You are building IP (Intellectual Property) in the form of a reusable codebase, not just transient chat history.
