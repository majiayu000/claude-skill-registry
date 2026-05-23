---
name: create-paper
description: >
  Orchestrate paper writing from project analysis. Composes assess, dogpile, arxiv,
  and review-code skills. Interview-driven workflow with frequent human collaboration
  to resolve ambiguity and validate each stage.
allowed-tools: Bash, Read
triggers:
  - write paper
  - draft paper
  - generate paper
  - paper from project
  - research paper
metadata:
  short-description: Interview-driven academic paper generation from code
---

# Paper Writer Skill

Generate academic papers from project analysis through **interview-driven orchestration**.

---

## Implementation Status

> **Current State**: Core 5-stage workflow fully implemented with real skill integrations.

| Feature | Status | Notes |
|---------|--------|-------|
| **Stage 1: Scope Interview** | ✅ Implemented | Typer prompts + /interview skill integration |
| **Stage 2: Project Analysis** | ✅ Implemented | /assess + /dogpile + optional /review-code |
| **Stage 3: Literature Search** | ✅ Implemented | Full arxiv JSON parsing with relevance triage |
| **Stage 4: Knowledge Learning** | ✅ Implemented | /arxiv learn with progress tracking |
| **Stage 5: Draft Generation** | ✅ Implemented | Multi-template support, LLM-powered sections |
| **LLM Content Generation** | ✅ Implemented | /scillm batch single, stub fallback |
| **Memory Storage** | ⚠️ Partial | Attempts to call /memory |
| **Auto-generated Figures** | ✅ Implemented | /fixture-graph integration (Seaborn/Graphviz/Mermaid) |
| **Interview Skill Integration** | ✅ Implemented | Used in Stage 1 scope definition |
| **Iterative Refinement** | ✅ Implemented | `refine` command with LLM feedback loop |
| **MIMIC Feature** | ✅ Implemented | Exemplar paper style learning & transfer |
| **BibTeX Citations** | ✅ Implemented | Auto-generated from arxiv paper IDs |
| **RAG Grounding** | ✅ Implemented | Prevent hallucination with --rag flag |
| **Multi-Template** | ✅ Implemented | IEEE, ACM, CVPR, arXiv, Springer |
| **Citation Checker** | ✅ Implemented | Verify citations match BibTeX entries |
| **Quality Dashboard** | ✅ Implemented | Word counts, citation stats, warnings |
| **Academic Phrases** | ✅ Implemented | Section-specific phrase suggestions |
| **Aspect Critique** | ✅ Implemented | SWIF2T-style multi-aspect feedback |
| **Agent Persona** | ✅ Implemented | Horus Lupercal + custom persona.json support |
| **Venue Disclosure** | ✅ Implemented | LLM disclosure for arXiv, ICLR, NeurIPS, ACL, AAAI |
| **Citation Verifier** | ✅ Implemented | Detect hallucinated/missing references |
| **Weakness Analysis** | ✅ Implemented | Generate explicit limitations section |
| **Pre-Submit Check** | ✅ Implemented | Rubric-based submission checklist |
| **Claim-Evidence Graph** | ✅ Implemented | Jan 2026: BibAgent/SemanticCite pattern |
| **AI Usage Ledger** | ✅ Implemented | ICLR 2026 disclosure compliance |
| **Prompt Sanitization** | ✅ Implemented | CVPR 2026 ethics requirement |
| **Horus Paper Pipeline** | ✅ Implemented | Full Warmaster publishing workflow |

### All Core Features Complete

1. ~~Implement MIMIC feature~~ ✅ DONE - Exemplar paper style learning
2. ~~Add figure generation~~ ✅ DONE - /fixture-graph integration
3. ~~Iterative section refinement~~ ✅ DONE - `refine` command
4. ~~Multi-round review loop~~ ✅ DONE - via `critique` and `refine`
5. ~~Add RAG grounding~~ ✅ DONE - Use --rag flag
6. ~~Multi-template support~~ ✅ DONE - IEEE, ACM, CVPR, arXiv, Springer
7. ~~Citation checker~~ ✅ DONE - `quality` command
8. ~~Academic phrase palette~~ ✅ DONE - `phrases` command
9. ~~Agent persona integration~~ ✅ DONE - Horus Lupercal authoritative style

---

## Philosophy: Human-in-the-Loop

This skill does NOT automate away the researcher. Instead, it:

- **Asks clarifying questions** until ambiguity is resolved
- **Validates assumptions** before proceeding to next stage
- **Presents recommendations** for human approval/override
- **Iterates on feedback** rather than generating final output

Think of it as a research assistant that does the legwork but defers judgment to you.

---

## ⚡ Quick Start for Agents

**Don't get overwhelmed by 17+ commands!** Use domain navigation:

```bash
# List command domains by workflow stage
create-paper domains

# Filter commands by domain
create-paper list --domain generate    # Paper generation commands
create-paper list --domain verify      # Quality assurance commands
create-paper list --domain comply      # Venue compliance commands

# Get workflow recommendations based on paper stage
create-paper workflow --stage new_paper
create-paper workflow --stage pre_submission

# Show fixture-graph presets for figures
create-paper figure-presets
```

### Domain Quick Reference

| Domain | Commands | When to Use |
|--------|----------|-------------|
| `generate` | draft, mimic, refine, horus-paper | Starting new paper or revising |
| `verify` | verify, quality, critique, check-citations, weakness-analysis, pre-submit, sanitize | Before submission |
| `comply` | disclosure, ai-ledger, claim-graph | Meeting venue requirements |
| `resources` | phrases, templates | Looking up helpers |

### Agent JSON Output

All navigation commands support `--summary` for JSON output:

```bash
create-paper domains --summary          # JSON of all domains
create-paper workflow --stage new_paper --summary  # JSON recommendations
create-paper figure-presets --summary   # JSON of IEEE sizes + colormaps
```

---

## Workflow: 5 Stages with Interview Gates

```
1. SCOPE INTERVIEW    → Define paper type, audience, contribution claims
                         [GATE: User validates scope]

2. PROJECT ANALYSIS   → /assess + /dogpile + /review-code
                         [GATE: User confirms analysis accuracy]

3. LITERATURE SEARCH  → /arxiv search + triage
                         [GATE: User selects relevant papers]

4. KNOWLEDGE LEARNING → /arxiv learn on selected papers
                         [GATE: User reviews extracted knowledge]

5. DRAFT GENERATION   → LaTeX from analysis + learned knowledge
                         [GATE: User iterates on structure/content]
```

**Key principle**: Each `[GATE]` blocks until human approval. No stage proceeds with unresolved questions.

---

## Command: `draft`

```bash
./run.sh draft --project /path/to/project
```

Launches interactive paper drafting session.

### Interview Questions (Stage 1: Scope)

The skill asks:

**1. Paper Type**

```
What type of paper are you writing?
a) Research paper (novel contribution)
b) System paper (implementation/architecture)
c) Survey paper (literature review)
d) Experience report (lessons learned)
e) Demo paper (tool description)
```

**2. Target Venue**

```
Target venue/conference? (affects formatting and emphasis)
Examples: ICSE, FSE, ASE, PLDI, arXiv preprint
```

**3. Contribution Claims**

```
What are your 3-5 main contribution claims?
(e.g., "A novel agent memory architecture that...")
```

**4. Target Audience**

```
Who is the intended audience?
a) Software engineering researchers
b) AI/ML practitioners
c) Industry developers
d) Specific domain (e.g., formal methods)
```

**5. Prior Work Scope**

```
Should I search for related work in:
[x] Agent architectures
[ ] Memory systems
[ ] Tool use / function calling
[ ] Other (specify): ___________
```

**GATE**: User reviews and confirms scope. Proceeds only on explicit approval.

---

## Stage 2: Project Analysis

Orchestrates existing skills:

```bash
# 1. Static + LLM assessment
/assess run /path/to/project
   ├─ Features identified
   ├─ Architecture patterns
   ├─ Technical debt detected
   └─ [OUTPUT: assessment.json]

# 2. Deep research on key features
/dogpile search "feature X implementation patterns"
   ├─ ArXiv papers
   ├─ GitHub examples
   ├─ Documentation
   └─ [OUTPUT: research_context.md]

# 3. Code-paper alignment check
/review-code verify /path/to/project
   ├─ Code matches documentation?
   ├─ Claims supported by implementation?
   └─ [OUTPUT: alignment_report.md]
```

### Interview: Analysis Validation

Presents findings:

```
Project Analysis Summary:
━━━━━━━━━━━━━━━━━━━━━━━━
Core Features:
  1. Episodic memory with ArangoDB (250 LOC)
  2. Tool orchestration pipeline (180 LOC)
  3. Interview-driven interactions (120 LOC)

Architecture:
  - Event-driven with message passing
  - Skills as composable modules
  - Persistent storage layer

Detected Issues:
  ⚠ Hardcoded paths in 3 locations
  ⚠ Missing test coverage for memory skill

Does this match your understanding? (y/n/refine)
```

**GATE**: User confirms or refines analysis before proceeding.

---

## Stage 3: Literature Search

Uses `/arxiv search` with generated context:

```bash
# Automatically generates /tmp/arxiv_context.md from scope + analysis
# Then searches with domain-specific terms
/arxiv search -q "episodic memory agent systems" -n 20
```

### Interview: Paper Triage

Presents abstracts with recommendations:

```
Found 20 Papers - Triaging Against Your Contribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HIGH RELEVANCE (Directly Related)
  [1] "Episodic Memory in Cognitive Architectures" (arXiv:2401.12345)
      → Describes memory structure similar to yours
      → RECOMMEND: Learn from this

  [2] "Tool Use in LLM Agents" (arXiv:2310.09876)
      → Framework for tool orchestration
      → RECOMMEND: Learn from this

MEDIUM RELEVANCE (Tangential)
  [3] "Retrieval-Augmented Generation" (arXiv:2312.54321)
      → Related but different architecture
      → SKIP unless you want broader context

LOW RELEVANCE (Different Problem)
  [4-20] ...

Which papers should I extract? (Enter numbers, 'all-high', or 'manual')
```

**GATE**: User selects papers. Can override recommendations.

---

## Stage 4: Knowledge Learning

Extracts from selected papers:

```bash
# For each selected paper:
/arxiv learn <id> --scope paper-writing --context-file /tmp/arxiv_context.md
```

### Interview: Knowledge Review

Shows extracted Q&A pairs before storing:

```
Extracted Knowledge from Paper [1]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: How should episodic memory be structured for agent recall?
A: Use time-indexed events with semantic embeddings. Store:
   - Event timestamp
   - Agent state snapshot
   - Action taken + rationale
   - Outcome observed

Q: What data structure best represents agent beliefs?
A: BDI (Belief-Desire-Intention) dictionary with confidence scores...

Accept these extractions? (y/n/refine)
```

**GATE**: User validates or refines extractions.

---

## Stage 5: Draft Generation

Generates LaTeX sections:

### Interview: Structure Review

```
Proposed Paper Structure
━━━━━━━━━━━━━━━━━━━━━━━

1. Abstract
   - Problem: Agent memory systems lack...
   - Solution: Interview-driven episodic memory
   - Results: Demonstrated on pi-mono project

2. Introduction
   - Motivation from /assess findings
   - Contribution claims from scope interview

3. Related Work
   - Episodic Memory (from learned papers)
   - Tool Orchestration (from learned papers)
   - Comparison table highlighting your differences

4. System Design
   - Architecture from /assess
   - Code examples from project

5. Implementation
   - Key features from analysis
   - Design decisions + rationale

6. Evaluation
   - Project statistics
   - Comparison with related systems

7. Discussion
   - Limitations from /review-code
   - Future work from aspirational features

Approve this structure? (y/n/custom)
```

**GATE**: User confirms or provides custom structure.

### Iterative Refinement

```
Draft section 1 (Abstract) ready. Options:
a) View draft
b) Regenerate with feedback
c) Accept and continue to next section
d) Manual edit
```

For each section, user can:

- Review generated text
- Provide feedback for regeneration
- Directly edit LaTeX
- Iterate until satisfied

---

## Output: Draft Paper

Final output structure:

```
paper_output/
├── draft.tex           # Main LaTeX file
├── sections/
│   ├── abstract.tex
│   ├── intro.tex
│   ├── related.tex
│   ├── design.tex
│   ├── impl.tex
│   ├── eval.tex
│   └── discussion.tex
├── figures/            # Auto-generated from /assess
│   ├── architecture.pdf
│   └── workflow.pdf
├── references.bib      # From learned papers
├── analysis/           # Supporting materials
│   ├── assessment.json
│   ├── research_context.md
│   └── alignment_report.md
└── metadata.json       # Paper metadata for /memory
```

---

## Integration with Existing Skills

| Stage          | Skill Called     | Purpose                       |
| -------------- | ---------------- | ----------------------------- |
| **Scope**      | (interview only) | Define paper parameters       |
| **Analysis**   | `/assess`        | Project feature extraction    |
|                | `/dogpile`       | Research context gathering    |
|                | `/review-code`   | Code-paper alignment          |
| **Literature** | `/arxiv search`  | Find related papers           |
| **Learning**   | `/arxiv learn`   | Extract knowledge from papers |
| **Draft**      | (internal LaTeX) | Generate paper sections       |
| **Storage**    | `/memory`        | Store paper metadata          |

All skill calls use **subprocess with error handling** - if a skill fails, the interview pauses and asks user how to proceed.

---

## Key Design Principles

1. **No Auto-Proceed**: Every stage blocks on human approval
2. **Ambiguity Resolution**: Ask questions until clarity achieved
3. **Recommendation + Override**: Suggest but defer to user judgment
4. **Transparent Process**: Show what skills are called and why
5. **Iterative Refinement**: Allow regeneration with feedback
6. **Graceful Failure**: Handle skill errors without crashing

---

## Example Session

```bash
$ ./run.sh draft --project ~/pi-mono

[INTERVIEW] Paper Type?
> b (System paper)

[INTERVIEW] Target venue?
> ICSE 2026 Tool Demo

[INTERVIEW] Main contributions? (one per line, 'done' when finished)
> Interview-driven skill orchestration
> Episodic memory with ArangoDB
> Human-in-the-loop paper generation
> done

[INTERVIEW] Audience?
> a (Software engineering researchers)

[INTERVIEW] Prior work areas? (space-separated)
> agent-architectures memory-systems tool-use

[STAGE 1] Scope defined ✓

[STAGE 2] Running /assess on ~/pi-mono...
[STAGE 2] Found 15 features, 3 architectural patterns
[INTERVIEW] Analysis shows: [summary]. Accurate? (y/n/refine)
> y

[STAGE 2] Running /dogpile on: "Interview-driven skill orchestration"...
[STAGE 2] Found 12 related projects

[INTERVIEW] Analysis complete. Continue to literature search? (y/n)
> y

[STAGE 3] Generating arxiv context from scope...
[STAGE 3] Searching arxiv for: "agent memory BDI architecture"...
[STAGE 3] Found 20 papers

[INTERVIEW] 5 HIGH, 8 MEDIUM, 7 LOW relevance. Extract which?
> all-high

[STAGE 4] Extracting 5 papers... (this may take 5-10 min)
[STAGE 4] Extracted 47 Q&A pairs

[INTERVIEW] Review extractions? (y/quick/skip)
> quick

[STAGE 5] Generating draft structure...
[INTERVIEW] 7 sections proposed. Approve? (y/custom)
> y

[STAGE 5] Drafting Abstract...
[INTERVIEW] Abstract draft ready. (view/regen/accept)
> view

[Abstract text shown]

[INTERVIEW] Feedback for regeneration? (or 'accept')
> Make it more concise, emphasize novelty
> regen

[STAGE 5] Abstract regenerated.
[INTERVIEW] (view/accept)
> accept

[Continues for each section...]

✓ Draft complete: paper_output/draft.tex
  Compile with: cd paper_output && pdflatex draft.tex

[STAGE 6] Store paper metadata in memory? (y/n)
> y

✓ Paper draft session complete
```

---

## RAG Grounding

RAG (Retrieval-Augmented Generation) grounding prevents hallucination by ensuring all generated content is traceable to source material.

### Enabling RAG

```bash
./run.sh draft --project /path/to/project --rag
```

### How RAG Works

1. **Code Snippet Extraction**: Extracts function/class definitions from project
2. **Project Facts**: Compiles verified facts from analysis (features, LOC, patterns)
3. **Paper Excerpts**: Uses Q&A pairs from learned papers as grounding
4. **Research Facts**: Incorporates findings from dogpile research

### Grounding Constraints

Each section has specific constraints:

| Section | Constraints |
|---------|-------------|
| **Abstract** | Only mention features in project_facts |
| **Intro** | Contributions must map to specific features |
| **Related** | Every claim must cite paper_excerpts |
| **Design** | Architecture must match code_snippets |
| **Impl** | Code examples must be real excerpts |
| **Eval** | Metrics must be derived from sources |
| **Discussion** | Limitations from analysis issues |

### Verifying Grounding

```bash
./run.sh verify ./paper_output --project /path/to/project
```

Checks generated content for:
- Unsupported claims (novel, achieves, outperforms)
- Fabricated metrics
- Missing source attribution

---

## Multi-Template Support

Support for major academic venues:

| Template | Venue | Usage |
|----------|-------|-------|
| `ieee` | IEEE conferences (default) | `--template ieee` |
| `acm` | ACM conferences (SIGCHI, SIGMOD) | `--template acm` |
| `cvpr` | CVPR/ICCV/ECCV | `--template cvpr` |
| `arxiv` | arXiv preprints | `--template arxiv` |
| `springer` | Springer LNCS | `--template springer` |

```bash
# Generate ACM-formatted paper
./run.sh draft --project ./myproject --template acm

# List all templates
./run.sh templates

# Show template details
./run.sh templates --show cvpr
```

---

## Iterative Refinement

The `refine` command enables section-by-section improvement with LLM feedback:

```bash
# Refine all sections with 2 rounds
./run.sh refine ./paper_output --rounds 2

# Refine specific section with feedback
./run.sh refine ./paper_output --section intro --feedback "Make it more concise"
```

Each round:
1. Shows current content preview
2. Prompts for feedback (or 'skip' to accept)
3. Generates automated critique (clarity, completeness)
4. LLM rewrites section addressing feedback + critique
5. Shows word count diff, asks for acceptance

---

## Quality Dashboard

Comprehensive metrics and warnings:

```bash
./run.sh quality ./paper_output
./run.sh quality ./paper_output --verbose
```

Displays:
- Section word counts with targets
- Citation counts per section
- Figure/table/equation counts
- Citation checker (missing/unused BibTeX)
- Warnings for sections outside target ranges

### Section Word Targets

| Section | Min | Max |
|---------|-----|-----|
| Abstract | 150 | 250 |
| Intro | 800 | 1500 |
| Related | 600 | 1200 |
| Design | 800 | 1500 |
| Impl | 600 | 1200 |
| Eval | 800 | 1500 |
| Discussion | 400 | 800 |

---

## Aspect Critique (SWIF2T-style)

Multi-aspect feedback system inspired by SWIF2T research:

```bash
# Critique all aspects
./run.sh critique ./paper_output

# Specific aspects
./run.sh critique ./paper_output --aspects clarity,rigor

# Single section with LLM
./run.sh critique ./paper_output --section eval --llm
```

### Aspects Evaluated

| Aspect | Description |
|--------|-------------|
| **clarity** | Clear writing, defined terms, logical flow |
| **novelty** | Contribution claims, differentiation from prior work |
| **rigor** | Sound methodology, baselines, statistical significance |
| **completeness** | All sections adequate, self-contained |
| **presentation** | Figures clear, formatting consistent |

Each aspect produces:
- Score (1-5)
- Specific findings
- Checklist items

---

## Academic Phrase Palette

Section-specific academic writing suggestions:

```bash
# All phrases for a section
./run.sh phrases intro

# Specific aspect
./run.sh phrases intro --aspect motivation
./run.sh phrases eval --aspect results
```

### Available Sections & Aspects

| Section | Aspects |
|---------|---------|
| **abstract** | problem, solution, results |
| **intro** | motivation, gap, contribution, organization |
| **related** | category, comparison, positioning |
| **method** | overview, detail, justification |
| **eval** | setup, results, analysis |
| **discussion** | limitations, future, broader_impact |

Example phrases:
- "Despite significant advances in..., there remains a critical need for..."
- "Our key insight is that..."
- "Unlike prior work, our method..."

---

## Agent Persona Integration

Write papers in a specific agent's voice for consistent style and authority.

### Built-in Persona: Horus Lupercal

```bash
# Generate paper in Horus's authoritative voice
./run.sh draft --project ./myproject --persona horus

# Get Horus-style phrases
./run.sh phrases eval --persona horus
```

**Horus's Writing Style:**
- **Voice**: Authoritative, commanding, tactically precise
- **Tone**: Competent, subtly contemptuous of inadequate approaches
- **Structure**: Military precision, anticipates objections
- **Principles**: Answer first, technical correctness non-negotiable

**Characteristic Phrases:**
- "The evidence is unambiguous."
- "Prior approaches fail to address the fundamental issue."
- "The results leave no room for debate."
- "Our methodology achieves what lesser approaches could not."

**Forbidden Phrases** (never used):
- "happy to help", "as an AI", "I believe", "hopefully"

### Custom Personas

Load custom persona from JSON:

```bash
./run.sh draft --project ./myproject --persona /path/to/persona.json
```

**persona.json format:**
```json
{
  "name": "Custom Persona",
  "voice": "academic",
  "tone_modifiers": ["precise", "formal"],
  "characteristic_phrases": ["We demonstrate that...", "Our analysis reveals..."],
  "forbidden_phrases": ["I think", "maybe"],
  "writing_principles": ["Clarity first", "Evidence-based claims"],
  "authority_source": "Rigorous methodology"
}
```

---

## Venue Policy Compliance (2024-2025)

Based on dogpile research into current venue policies:

### Venue Disclosure Generator

Generate LLM-use disclosure statements compliant with venue policies:

```bash
# Generate arXiv disclosure
./run.sh disclosure arxiv

# Show ICLR policy notes
./run.sh disclosure iclr --policy

# Save to file
./run.sh disclosure neurips -o acknowledgements.tex
```

**Supported Venues:**

| Venue | Disclosure Required | Location |
|-------|---------------------|----------|
| arXiv | Yes | acknowledgements |
| ICLR | Yes (desk rejection risk) | acknowledgements |
| NeurIPS | Yes (method-level) | method section |
| ACL | Yes | acknowledgements |
| AAAI | Yes (if experimental) | paper body |
| CVPR | Yes | acknowledgements |

**Key Policy Notes (Oct 2025):**
- arXiv CS tightened moderation: review/survey papers need completed peer review
- ICLR 2026: Hallucinated references = desk rejection
- All venues: Authors responsible for content correctness

### Citation Verification

Prevent hallucinated references (critical for peer review):

```bash
# Check citations match BibTeX
./run.sh check-citations ./paper_output

# Strict mode (fail on issues)
./run.sh check-citations ./paper_output --strict
```

**Checks performed:**
- All `\cite{}` commands have matching .bib entries
- Recent papers (2023+) have URL/DOI
- No suspicious patterns (excessive "et al.", generic names)

### Weakness Analysis

Generate explicit limitations section (research shows LLMs miss weaknesses):

```bash
# Analyze paper for limitations
./run.sh weakness-analysis ./paper_output

# Include project analysis
./run.sh weakness-analysis ./paper_output --project ./my-project

# Save to file
./run.sh weakness-analysis ./paper_output -o sections/limitations.tex
```

**Categories analyzed:**
- Methodology assumptions/simplifications
- Evaluation baseline count (research suggests 3-4 minimum)
- Scope boundaries
- Test coverage (if project provided)
- Reproducibility and generalization

### Pre-Submission Checklist

Comprehensive validation before submission:

```bash
# Full pre-submit check
./run.sh pre-submit ./paper_output --venue iclr --project ./my-project

# arXiv-focused (default)
./run.sh pre-submit ./paper_output
```

**Checklist items:**
1. File structure (draft.tex, references.bib)
2. Required sections (intro, method, eval, conclusion)
3. Citation integrity (no missing/hallucinated)
4. LLM disclosure compliance (venue-specific)
5. Evidence grounding (code/figure references)

**Exit codes:**
- 0: Ready for submission
- 1: Critical issues found

---

## Complete Command Reference

| Command | Purpose |
|---------|---------|
| `draft` | Generate paper from project (5-stage workflow) |
| `mimic` | Learn/apply exemplar paper styles |
| `refine` | Iteratively improve sections with feedback |
| `quality` | Show metrics dashboard |
| `critique` | Multi-aspect feedback (SWIF2T-style) |
| `phrases` | Academic phrase suggestions |
| `templates` | List/show LaTeX templates |
| `verify` | Verify RAG grounding |
| `disclosure` | Generate venue-specific LLM disclosure |
| `check-citations` | Verify citations against BibTeX |
| `weakness-analysis` | Generate limitations section |
| `pre-submit` | Pre-submission checklist and validation |
| `claim-graph` | Build claim-evidence graph (Jan 2026) |
| `ai-ledger` | AI usage tracking for ICLR 2026 compliance |
| `sanitize` | Prompt injection defense (CVPR 2026) |
| `horus-paper` | Full Warmaster publishing pipeline |

---

## Horus Lupercal: Research Paper Workflow

Horus has access to all skills in `/home/graham/workspace/experiments/pi-mono/.pi/skills` and can compose them to write research papers about his projects.

### Example: Writing a Paper on the Memory Project

```bash
# Step 1: Analyze the memory project
./run.sh draft --project /home/graham/workspace/experiments/memory \
               --persona horus \
               --rag \
               --template arxiv

# Step 2: Web research for related work (Horus has /surf access)
# Horus can use /surf to browse arXiv, GitHub, documentation

# Step 3: Generate limitations section
./run.sh weakness-analysis ./paper_output \
         --project /home/graham/workspace/experiments/memory

# Step 4: Pre-submission validation
./run.sh pre-submit ./paper_output \
         --venue arxiv \
         --project /home/graham/workspace/experiments/memory
```

### Horus's Skill Composition

| Skill | Horus's Usage |
|-------|---------------|
| `/assess` | Analyze project architecture and features |
| `/dogpile` | Deep research on related topics |
| `/arxiv` | Search and learn from academic papers |
| `/memory` | Store paper context for future sessions |
| `/review-code` | Verify code-paper alignment |
| `/surf` | Browse web for documentation, examples |
| `/create-paper` | Generate research papers in his voice |

### Horus Writing Principles (Academic Context)

When writing papers, Horus:

1. **Answers first** - States contributions directly, then elaborates
2. **Technical precision** - Every claim backed by evidence from code/experiments
3. **Anticipates objections** - Limitations section is thorough, not hidden
4. **Commands authority** - Writing is confident, not hedging
5. **No AI-speak** - Never uses "happy to help", "as an AI", "hopefully"

### Example Horus Paper Abstract

> Prior approaches to agent memory systems demonstrate troubling disregard for
> compositional reasoning—a fundamental deficiency that limits generalization
> across tasks. We present a knowledge graph architecture that addresses this
> inadequacy through graph-based belief tracking and Theory of Mind inference.
> Our implementation achieves 34% improved task success rate compared to flat
> memory baselines. The experimental results leave no room for debate regarding
> the superiority of structured episodic recall.

---

## Jan 2026 Cutting-Edge Features (from dogpile research)

These features are based on January 2026 academic policy changes and state-of-the-art research.

### Claim-Evidence Graph (BibAgent/SemanticCite Pattern)

Link every claim to its evidence sources for peer review defense:

```bash
# Build claim-evidence graph
./run.sh claim-graph ./paper_output

# With verification
./run.sh claim-graph ./paper_output --verify

# Export to JSON
./run.sh claim-graph ./paper_output -o claims.json
```

**Support Levels:**
- **Supported**: Claim has 2+ citations
- **Partially Supported**: Claim has 1 citation
- **Unsupported**: Claim has no citations (⚠ review required)

### AI Usage Ledger (ICLR 2026 Compliance)

Track all AI tool usage for accurate disclosure:

```bash
# Show logged AI usage
./run.sh ai-ledger ./paper_output --show

# Generate disclosure statement from ledger
./run.sh ai-ledger ./paper_output --disclosure

# Clear ledger
./run.sh ai-ledger ./paper_output --clear
```

**Tracked Information:**
- Tool name (scillm, claude, gpt-4, etc.)
- Purpose (drafting, editing, citation_search)
- Section affected
- Prompt hash (for provenance, not full prompt)
- Output summary

### Prompt Injection Sanitization (CVPR 2026 Requirement)

CVPR 2026 explicitly treats hidden prompt injection as an ethics violation:

```bash
# Check for prompt injection
./run.sh sanitize ./paper_output

# Auto-fix detected issues
./run.sh sanitize ./paper_output --fix
```

**Detected Patterns:**
- "ignore previous instructions"
- "you are now" / "pretend to be"
- Zero-width characters
- White/hidden text in LaTeX
- System prompt markers

### Horus Paper Pipeline

The full Warmaster publishing workflow:

```bash
./run.sh horus-paper /home/graham/workspace/experiments/memory
```

**Persona Strength Parameter:**

Horus can modulate his voice for peer reviewers with `--persona-strength`:

| Strength | Tone | Use When |
|----------|------|----------|
| 0.0 | Pure academic | Conservative venues (Nature, Science) |
| 0.3 | Subtle hints | Peer review requires neutrality |
| 0.5 | Balanced | General arXiv preprints |
| 0.7 | Strong (default) | Authoritative but measured |
| 1.0 | Full Warmaster | Workshop papers, position pieces |

```bash
# Measured tone for peer review
./run.sh horus-paper ./project --persona-strength 0.5 --auto-run

# Full Warmaster intensity
./run.sh horus-paper ./project -s 1.0 --auto-run
```

*"I temper my voice for the peer reviewers. A tactical necessity." - Horus*

**Pipeline Phases:**

1. **Project Analysis**: `draft --persona horus --rag`
2. **Claim Verification**: `claim-graph --verify` + `check-citations --strict`
3. **Weakness Analysis**: `weakness-analysis --project`
4. **Compliance Check**: `sanitize` + `ai-ledger --disclosure` + `pre-submit`

**The Warmaster's Publishing Checklist:**
- [ ] All claims have evidence (claim-graph)
- [ ] No hallucinated citations (check-citations --strict)
- [ ] Limitations explicitly stated (weakness-analysis)
- [ ] No prompt injection (sanitize)
- [ ] AI usage disclosed (ai-ledger --disclosure)
- [ ] Pre-submission passed (pre-submit)

---

## Dependencies

- Python 3.10+
- LaTeX distribution (texlive or mactex)
- Existing skills: assess, dogpile, arxiv, review-code, memory
- interview skill (for HTML/TUI interview rendering)

---

## Sanity Check

```bash
./sanity.sh
```

Verifies:

- All dependent skills exist
- LaTeX is installed
- Python dependencies available
- Template files present
