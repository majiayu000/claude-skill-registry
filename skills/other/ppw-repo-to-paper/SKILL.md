---
name: ppw:repo-to-paper
description: >-
  Scan an experiment repo and generate a complete paper outline (H1/H2/H3)
  with user approval checkpoints at each level, then generate body text
  with evidence annotations, citations, and bilingual output. Python ML repos.
  扫描实验仓库，逐级生成论文大纲（H1/H2/H3），每级用户确认后推进，
  然后生成带证据标注、引用和双语输出的正文文本。
triggers:
  primary_intent: generate paper outline from experiment repo
  examples:
    - "Generate a paper outline from my repo"
    - "帮我从实验仓库生成论文大纲"
    - "Scan my project and create paper structure"
    - "把我的代码仓库转成论文框架"
    - "Create paper sections from experiment code"
    - "从代码生成论文结构"
tools:
  - Read
  - Write
  - Structured Interaction
  - External MCP
references:
  required:
    - references/repo-patterns.md
    - references/bilingual-output.md
    - references/body-generation-rules.md
    - references/journals/ceus.md
  leaf_hints: []
input_modes:
  - repo_path
output_contract:
  - scan_summary
  - paper_outline
  - literature_refs
  - body_text
---

## Purpose

This Skill scans a Python ML experiment repository and generates a hierarchical paper outline
(H1/H2/H3) with user approval checkpoints at each heading level. It serves researchers who
have completed experiments and need to structure findings into an academic paper. The scan
categorizes repo files using patterns from `references/repo-patterns.md`, then progressively
generates headings from coarse (sections) to fine (sub-subsections), with the user confirming
or modifying each level before proceeding. After H2 confirmation, the Skill automatically
collects academic references via Semantic Scholar MCP and saves them as per-section ref files
for downstream body generation.

## Trigger

**Activates when the user asks to:**
- Generate a paper structure, outline, or skeleton from a repository or codebase
- Scan a project and create paper sections from experiment code or results
- 从实验仓库/代码仓库生成论文大纲或论文结构

**Example invocations:**
- "Generate a paper outline from my repo"
- "帮我从实验仓库生成论文大纲"
- "Scan my project and create paper structure"
- "把我的代码仓库转成论文框架"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `guided` | Yes | Full 5-step workflow with confirmation at each heading level and section-by-section body generation |
| `direct` | | Not supported -- outline generation inherently requires user validation at each level |
| `batch` | | Not supported -- each repo requires unique analysis |

**Default mode:** `guided`. The layered confirmation design is central to this Skill.

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/repo-patterns.md` | File categorization patterns and section mapping rules |
| `references/bilingual-output.md` | Bilingual output format (Skill is bilingual-eligible) |
| `references/body-generation-rules.md` | Anti-hallucination rules, citation integration, bilingual format, references.bib algorithm |
| `references/journals/ceus.md` | CEUS journal formatting contract (writing style, section guidance) |

### Leaf Hints

None. All reference files are in `required` because Step 5 body generation always needs CEUS formatting.

### Loading Rules

- Load `repo-patterns.md` and `bilingual-output.md` at Step 1 start.
- Load `body-generation-rules.md` and `journals/ceus.md` at Step 5 start.
- If journal template file is missing, refuse: "Journal template for [X] not found. Available: CEUS."

## Ask Strategy

**Before starting, ask about:**
1. **Repo path** (required): "Which repository should I scan?" -- use Structured Interaction if available
2. **Target journal** (optional): "Which journal is this paper targeting?" -- options: CEUS, Other, None/General.
   If CEUS, load template at Step 2. If Other, ask for journal name. If None, use IMRaD default

**Bilingual mode:** Inferred from trigger text. Check for opt-out keywords per `references/bilingual-output.md`
(exact phrases: `english only`, `no bilingual`, `only english`, `不要中文`). Do not ask explicitly.

**Rules:**
- Never ask more than 2 explicit questions (repo path + journal)
- In direct mode, skip -- but direct mode is not supported for this Skill

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:repo-to-paper` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:repo-to-paper？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.
- **Note:** This Skill does not support full `direct` mode. If user accepts the recommendation, skip the Ask Strategy questions (repo path, journal) using inferred context, but retain all guided Step checkpoints (Steps 2-5 confirmations). The output contract is not altered.

### Step 1: Scan Repository

**Prepare:**
- Load `references/repo-patterns.md` and `references/bilingual-output.md`
- Read the repository directory structure (top 2 levels: root + first-level subdirectories)
- Categorize each file using the File Identification Patterns table from `repo-patterns.md`
- Apply ambiguity rules for files matching multiple categories (lowest priority number wins)
- Skip hidden files, test files, and binary data files per the Skip Rules in `repo-patterns.md`

**Present:**
- Display a categorized summary table:

  | Category | Files Found | Key Items |
  |---|---|---|
  | documentation | 3 | README.md, docs/overview.md |
  | results | 5 | results/metrics.csv, scores.json |

- Mark missing categories: "No [category] files found"
- Summary line: "Scanned N files in M categories. Proceeding to H1 outline generation..."
- If user wants to review or correct, they can interrupt; otherwise auto-proceed to Step 2
- **Record workflow:** Append `{"skill": "ppw:repo-to-paper", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

---

### Step 2: Generate H1 Outline

**Prepare:**
- If journal specified (e.g., CEUS), load `references/journals/[journal].md` and use its Section
  Guidance headings as H1 structure. CEUS sections: Abstract, Introduction, Study Area / Data /
  Methods, Results, Discussion, Conclusion
- If no journal specified, use IMRaD default: Introduction, Methods, Results and Discussion, Conclusion
- Adjust base sections based on scan summary (e.g., add "Study Area" if spatial data detected)

**Present:**
- Display H1 headings with one-sentence descriptions:
  ```
  # 1. Introduction
      Establish research context, literature gap, and contribution statement.
  # 2. Methods
      Describe the analytical approach, data sources, and model architecture.
  ```
- Bilingual: if bilingual mode is ON, add Chinese translation of each description using
  Markdown blockquote format: `> **[Chinese]** ...` per `references/bilingual-output.md`
- Summary line: "Generated N H1 sections. Please confirm, modify, or add before proceeding to H2."
- Wait for user confirmation ("ok") or modification instructions

**On modification:** Revise H1 headings per user feedback and re-display. Loop until confirmed.

**Section adjustment examples:**
- If scan found spatial data files (shapefiles, GeoJSON) -> consider adding "Study Area" H1 section
- If scan found no result files -> mark Results section with warning placeholder
- If scan found multiple distinct model implementations -> consider splitting Methods into sub-approaches

---

### Step 3: Generate H2 Outline

**Prepare:**
- For each confirmed H1 section, read relevant repo files to generate H2 sub-headings
- Use the Category to Paper Section Mapping from `repo-patterns.md` to identify which files
  inform each H1 section
- Read actual file contents (README for Introduction, config files for Methods, result files
  for Results) -- H2 generation requires content reading, not just directory structure
- Generate 2-4 H2 sub-headings per H1 section, each with a one-sentence description

**Present:**
- Display full H1 + H2 hierarchy with source annotations on each H2:
  ```
  # 1. Introduction
  ## 1.1 Research Background and Motivation  <- from: README.md
      Urban heat island measurement requires fine-grained spatial analysis approaches.
  ## 1.2 Literature Gap and Contribution  <- from: README.md
      Existing methods lack integration of street-level semantics with thermal data.
  ```
- Source annotations: list the 1-3 most directly relevant files (highest-priority per `repo-patterns.md`)
- Bilingual: if ON, add Chinese descriptions in `> **[Chinese]** ...` blockquote format
- Same confirmation loop as Step 2: "Generated N H2 subsections across M H1 sections. Please
  confirm, modify, or add before proceeding to H3."

---

### Step 2.5: Literature Collection

**Pre-flight:**
- Call `mcp__semantic-scholar__papers-search-basic` with `{"query": "test", "limit": 1}`
- If call succeeds: proceed to literature collection below
- If call fails or tool unavailable: skip Step 2.5 entirely
  - Insert `[CITATION NEEDED]` after each H2 subsection description in the outline
  - Display: "Semantic Scholar MCP not available. Skipping literature collection. [CITATION NEEDED] markers added."
  - Proceed directly to Step 4 (H3 generation)

**Collect references:**

FOR each H1 section:
  FOR each H2 subsection under this H1:
    1. Derive search query: extract 2-5 key technical terms from the H2 title and description,
       contextualized by the H1 section title. Use English terms only (ignore Chinese translations
       in bilingual mode). Strip filler words (and, of, the, for).
       Example: H1="Methods", H2="Gradient Boosting Prediction Framework",
       description="Feature engineering using street-level semantic segmentation data"
       -> query: "gradient boosting prediction street-level semantic segmentation"
    2. Call `mcp__semantic-scholar__papers-search-basic` with `{"query": derived_query, "limit": 10}`
    3. For each result where the abstract field is empty: call `mcp__semantic-scholar__get-paper-abstract`
       with the paper's `paperId`. If abstract is still empty after fetch, mark as "Abstract not available"
    4. Filter results by relevance: assess how many distinct claims/arguments the H2 subsection needs
       to make, then keep 5-10 papers that best support those claims. Discard papers that are only
       tangentially related based on title and abstract content
    5. Display progress line: `✓ 1.1 Research Background: 8 refs found` (or `⚠ 1.1 Research Background: 0 refs found` for zero results)
    6. If a search call fails mid-batch: mark that H2 as `[CITATION NEEDED]`, display warning, continue to next H2
  END FOR
END FOR

**Write ref files:**

Create `{repo_path}/.paper-refs/` directory. Write one Markdown file per H1 section, named by
the section topic in lowercase (e.g., `introduction.md`, `methods.md`, `results.md`).

Each file uses this structure:

```markdown
# [H1 Section Title] - References

## [H2 Number] [H2 Subsection Title]

### [FirstAuthor] et al. ([Year])
**Title:** [Full title from MCP]
**Authors:** [Author1; Author2; ...]
**Year:** [YYYY] | **Citations:** [N]
**Relevance:** [[H2 number] [H2 subsection title]]
[One-sentence explanation of why this paper is relevant to this subsection]

> [Abstract summary: 1-2 sentences from MCP abstract data. If abstract not available, write "Abstract not available"]

```bibtex
@article{[citationkey], ...}
```
```

BibTeX rules (reuse literature-skill patterns):
- Citation key format: `firstAuthorLastnameLowercaseYYYYfirstKeyword` (e.g., `smith2023urban`)
- Entry type: `@article` for journal, `@inproceedings` for conference, `@misc` for preprints (follow MCP paper type)
- All BibTeX fields MUST come from MCP-returned data. If a field is not in the MCP response, OMIT it
- If DOI missing, add comment: `% DOI not available -- verify manually`
- Never fill missing fields from prior knowledge

Duplicate handling: allow same paper to appear in multiple section files. Each file is self-contained.

**Display summary table:**

After all H2 subsections processed, display:

```
| Section | Subsection | Refs | Top Reference |
|---------|-----------|------|---------------|
| 1. Introduction | 1.1 Research Background | 8 | Smith et al. (2023) - 142 citations |
| ... | ... | ... | ... |

Total: [N] references collected. Confirm to proceed to H3 outline generation.
```

Wait for user confirmation before proceeding to Step 4.

---

### Step 4: Generate H3 Outline

**Prepare:**
- For each confirmed H2 subsection, read deeper file contents to generate H3 sub-sub-headings
- H3 captures specific technical details: individual model components, specific metrics,
  particular datasets, analysis steps
- Not every H2 needs H3 -- generate only where repo content supports further breakdown
  (typically Methods and Results). Generate 0-3 H3 entries per H2 subsection

**Present:**
- Display full H1 + H2 + H3 hierarchy with source annotations on H3 entries:
  ```
  ## 1.1 Research Background and Motivation
  ### 1.1.1 Urban Heat Island Measurement Challenges  <- from: README.md:L15-30
      Current approaches to UHI measurement rely on satellite imagery with limited resolution.
  ```
- Bilingual: if ON, add Chinese descriptions in `> **[Chinese]** ...` blockquote format
- Same confirmation loop as Step 2: "Generated N H3 sub-subsections. Please confirm, modify,
  or add. This completes the outline structure."

---

### Step 5: Body Generation

Step 5 auto-continues in the same session after H3 confirmation. It uses the H3 outline already in memory -- does not re-read `paper_outline.md`.

**Prepare:**
- Load `references/body-generation-rules.md` and `references/journals/ceus.md`
- Check if `{repo_path}/.paper-refs/` exists. If missing: note that all citation positions will use `[CITATION NEEDED]`
- Create `{repo_path}/.paper-output/` directory if it does not exist

**Section selection:**
- Display all H1 sections via AskUserQuestion (multiSelect):

  ```
  AskUserQuestion({
    question: "Which sections should I generate body text for?",
    options: [
      { label: "1. [H1 title]", description: "[H2 subsection summary]" },
      ...one option per H1 section from confirmed outline
    ]
  })
  ```

- User selects which sections to generate in this session

**Generation loop (for each selected H1 section, sequentially):**

1. Read relevant repo files using the Category to Paper Section Mapping from `references/repo-patterns.md`
2. Read `{repo_path}/.paper-refs/{section}.md` if it exists -- extract `\cite{key}` citation keys
3. Generate full section `.tex` content following ALL rules in `references/body-generation-rules.md`:
   - `\section{}`, `\subsection{}`, `\subsubsection{}` LaTeX heading commands from confirmed H2/H3 structure
   - Academic prose following CEUS writing style from `references/journals/ceus.md`
   - `\cite{key}` inline citations (keys from `.paper-refs/` only; `[CITATION NEEDED]` for unsupported claims)
   - `[SOURCE: file:line]` annotations on all repo-derived claims (specific numbers, configs, model names)
   - `[RESULTS NEEDED]` / `[EXACT VALUE: metric]` for unknown quantitative data
   - Bilingual: `% --- Paragraph N ---` markers + `%` Chinese comment lines before each English paragraph (skip if opt-out detected)
4. Write to `{repo_path}/.paper-output/{section}.tex`
5. Display the generated section content to the user
6. AskUserQuestion for confirmation:

   ```
   AskUserQuestion({
     question: "Section [N]: [Title] generated. Please review above.",
     options: [
       { label: "Confirm", description: "Accept this section and proceed to next" },
       { label: "Modify", description: "Describe changes needed (will regenerate entire section)" },
       { label: "Skip", description: "Skip this section, move to next" }
     ]
   })
   ```

   - **Confirm:** proceed to next selected section
   - **Modify:** user describes changes -> regenerate entire section -> re-display -> loop until confirmed
   - **Skip:** move to next section without writing file

**After all selected sections confirmed:**
- Generate `references.bib` following the algorithm in `references/body-generation-rules.md`
- Display completion summary: number of sections generated, files written, references.bib entry count

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `scan_summary` | Categorized summary table | Always -- Step 1 |
| `paper_outline` | Hierarchical H1/H2/H3 with descriptions and source annotations | After all steps confirmed |
| `literature_refs` | Per-section Markdown files in `{repo_path}/.paper-refs/` with reference cards | After Step 2.5 (skipped if MCP unavailable) |
| `body_text` | Per-H1 `.tex` files in `{repo_path}/.paper-output/` + `references.bib` | After Step 5 sections confirmed |

**Bilingual eligibility:** This Skill produces academic text (one-sentence heading descriptions).
Bilingual mode is ON by default; opt-out via keywords in `references/bilingual-output.md`.

After final H3 confirmation, offer to save the complete outline to a file using Write tool:
- Default filename: `paper_outline.md` in the repo root
- Include all heading levels with descriptions and source annotations
- Bilingual descriptions included if bilingual mode is ON

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Empty repository (no recognized files) | Refuse: "No scannable files found in [path]. Please verify the repository path." |
| No README.md found | Warn in scan summary; proceed with available files; Introduction H2 will have limited source annotations |
| No result files found | Warn in scan summary; Results H2/H3 use placeholder: "[RESULTS NEEDED: add result files to populate this section]" |
| Journal specified but template missing | Refuse: "Journal template for [X] not found. Available: CEUS." |
| Non-Python repo | Warn: "Scan patterns are calibrated for Python ML projects. Non-Python files may be miscategorized." Proceed with best-effort |
| Very large repo (>500 files in top 2 levels) | List only top 10 files per category in scan summary; note total count |
| All files in one category | Proceed -- outline may be unbalanced; user corrects at confirmation step |
| Semantic Scholar MCP unavailable | Skip Step 2.5; insert [CITATION NEEDED] markers in outline; proceed to Step 4 |
| Zero search results for an H2 | Display warning with ⚠ prefix; mark H2 as [CITATION NEEDED]; continue to next H2 |
| MCP call fails mid-batch | Mark that specific H2 as [CITATION NEEDED]; continue with remaining H2 subsections |
| Springer papers with empty abstracts | Call get-paper-abstract; if still empty, display "Abstract not available" in ref card; still include paper |
| .paper-refs/ directory missing | Continue generating; all citation positions use `[CITATION NEEDED]` placeholders; do not block |
| User selects zero sections in Step 5 | Skip body generation entirely; display "No sections selected. Body generation skipped." |
| Modification loop exceeds 3 iterations | Proceed with current version; warn "Multiple revision cycles detected. Consider manual editing for fine adjustments." |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask repo path and journal as plain-text questions |
| `references/repo-patterns.md` missing | Refuse: "Required reference file references/repo-patterns.md not found. Cannot categorize repo files." |
| `references/bilingual-output.md` missing | Proceed with English-only output; warn user |
| Journal template missing | Refuse with message from Edge Cases |
| Write tool unavailable | Present final outline in conversation; user saves manually |
| Semantic Scholar MCP unavailable | Skip Step 2.5 entirely; add [CITATION NEEDED] after each H2 description; warn user; proceed to H3 generation |
| `references/body-generation-rules.md` missing | Refuse: "Required reference file references/body-generation-rules.md not found. Cannot generate body text." |

## Examples

**Minimal invocation:** User provides repo path `~/projects/uhi-prediction/` and selects CEUS as target journal.

**Step 1 output (scan summary):**
```
| Category      | Files Found | Key Items                               |
|---------------|-------------|-----------------------------------------|
| documentation | 2           | README.md, docs/data-sources.md         |
| config        | 3           | config.yaml, params.json, .env.example  |
| results       | 4           | results/metrics.csv, results/ablation/  |
| code          | 8           | src/model.py, src/train.py, src/eval.py |
| figures       | 3           | figures/heatmap.png, figures/scatter.svg |
| dependencies  | 1           | requirements.txt                        |

Scanned 21 files in 6 categories. Proceeding to H1 outline generation...
```

**Step 2 output (H1 with CEUS template):**
```
# 1. Introduction
    Establish the urban heat island prediction problem and contribution.
    > **[Chinese]** 阐述城市热岛预测问题及本研究贡献。
# 2. Study Area and Data
    Describe the geographic scope and data sources for UHI analysis.
    > **[Chinese]** 描述研究区域范围及城市热岛分析的数据来源。
# 3. Methods
    Present the gradient boosting prediction framework and feature engineering.
    > **[Chinese]** 介绍梯度提升预测框架与特征工程方法。
# 4. Results
    Report prediction accuracy and spatial pattern analysis.
    > **[Chinese]** 报告预测精度与空间格局分析结果。
# 5. Discussion
    Interpret findings in the context of urban planning and prior UHI studies.
    > **[Chinese]** 在城市规划和既有热岛研究背景下解读发现。
# 6. Conclusion
    Summarize contributions and identify limitations.
    > **[Chinese]** 总结贡献并指出局限性。

Generated 6 H1 sections. Please confirm, modify, or add before proceeding to H2.
```

User confirms. Steps 3-4 follow the same pattern with increasing detail and source annotations.

---

*Skill: repo-to-paper-skill*
*Conventions: references/skill-conventions.md*
