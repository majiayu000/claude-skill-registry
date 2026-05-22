---
name: outline-agent
description: Step 1 of the PaperOrchestra pipeline (arXiv:2604.05018). Convert (idea.md, experimental_log.md, template.tex, conference_guidelines.md) into a strict JSON outline containing a plotting plan, literature search plan (Intro + Related Work), and section-level writing plan with citation hints. TRIGGER when the orchestrator delegates Step 1 or when the user asks to "outline a paper from raw materials" or "generate the paper structure".
---

# Outline Agent (Step 1)

Faithful implementation of the Outline Agent from PaperOrchestra
(Song et al., 2026, arXiv:2604.05018, App. F.1, pp. 40–44).

**Cost: 1 LLM call.**

## Your task

Read four input files from the workspace and produce a single JSON object at
`workspace/outline.json` with three top-level keys:

- `plotting_plan` — array of figure objects
- `intro_related_work_plan` — object with `introduction_strategy` and `related_work_strategy`
- `section_plan` — array of section objects, each with `section_title` and `subsections[]`

## How to do it

1. **Read the verbatim prompt at `references/prompt.md`.** This is the exact
   Outline Agent system prompt from the paper. Use it as your system message.
2. **Prepend the Anti-Leakage Prompt** from
   `../paper-orchestra/references/anti-leakage-prompt.md`.
3. **Read the four input files**:
   - `workspace/inputs/idea.md`
   - `workspace/inputs/experimental_log.md`
   - `workspace/inputs/template.tex`
   - `workspace/inputs/conference_guidelines.md`
4. **Synthesize across all four** — the global instruction in the prompt is
   "Do not analyze inputs in isolation. You must synthesize information across
   all provided documents for every step."
5. **Emit a single JSON object** following the schema in
   `references/outline-schema.md`. Cross-check against
   `references/outline_schema.json` (machine-readable).
6. **Save to** `workspace/outline.json`.
7. **Validate**:
   ```bash
   python skills/outline-agent/scripts/validate_outline.py workspace/outline.json
   ```
   If validation fails, fix the JSON and re-validate. Do not proceed to Step 2
   or Step 3 with an invalid outline — every downstream agent depends on this
   schema.

## Hard rules from the prompt (do not violate)

These are excerpted from `references/prompt.md`. The validator enforces them.

### Plotting plan (Directive 1)

- `plot_type` MUST be exactly one of `"plot"` or `"diagram"`.
- `data_source` MUST be exactly one of `"idea.md"`, `"experimental_log.md"`,
  or `"both"`.
- `aspect_ratio` MUST be exactly one of:
  `"1:1"`, `"1:4"`, `"2:3"`, `"3:2"`, `"3:4"`, `"4:1"`, `"4:3"`, `"4:5"`,
  `"5:4"`, `"9:16"`, `"16:9"`, `"21:9"`.
- `figure_id` MUST be a semantically meaningful snake_case identifier
  (e.g., `fig_framework_overview`, `fig_ablation_study_parameter_sensitivity`).
- `figure_id` MUST NOT contain the word `"Figure"`.

### Intro / Related Work strategy (Directive 2)

- Strictly separate Introduction (macro-level context, 10-20 papers,
  foundational + survey + impact) from Related Work (micro-level technical
  baselines, 30-50 papers, divided into 2-4 methodology clusters that
  directly compete with or precede the proposed approach).
- For each Related Work cluster: provide `methodology_cluster`,
  `sota_investigation_mission`, `limitation_hypothesis`,
  `limitation_search_queries`, `bridge_to_our_method`.
- **CRITICAL TIMELINE RULE**: Do not instruct searches for any papers
  published after `{cutoff_date}`. Derive `cutoff_date` from
  `conference_guidelines.md` (e.g., "ICLR 2025 → cutoff October 2024",
  "CVPR 2025 → cutoff November 2024"). If unspecified, default to one month
  before today's date.

### Section plan (Directive 3)

- **Structural hierarchy**: if Subsection X.1 is created, X.2 is mandatory.
  No orphaned subsections. Omit subsections entirely if a section does not
  require division.
- **Content specificity**: each `content_bullets` entry must reference source
  materials concretely. AVOID "Describe the model". REQUIRE "Formalize the
  Temporal-Aware Attention mechanism using Eq. 3 from idea.md."
- **Mandatory citations**: every dataset, optimizer, metric, and
  foundational architecture/model mentioned in `idea.md` or
  `experimental_log.md` MUST have a citation hint, no matter how ubiquitous
  (e.g., AdamW, ResNet, ImageNet, CLIP, Transformer, LLaMA, GPT, LLaVA).
- **Citation hint format**:
  - If you know the exact author and title:
    `"Author (Exact Paper Title)"`
  - Otherwise: `"research paper or technical report introducing '[Exact Model/Dataset/Metric Name]'"`
  - **Do NOT guess or hallucinate authors.**

## Output

Exactly one file: `workspace/outline.json`. No prose, no code blocks, no
markdown. The Section Writing Agent and Literature Review Agent will parse
this JSON directly.

See `references/example-output.json` for a complete worked example from the
paper (App. F.1, pp. 43–44).

## Resources

- `references/prompt.md` — verbatim Outline Agent prompt from App. F.1
- `references/outline-schema.md` — prose explanation of the schema
- `references/outline_schema.json` — machine-readable JSON Schema
- `references/example-output.json` — example output from the paper
- `references/allowed-values.md` — enumerated allowed values for each enum field
- `scripts/validate_outline.py` — JSON Schema validator
