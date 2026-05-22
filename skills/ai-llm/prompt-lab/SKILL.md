---
name: prompt-lab
description: >
  Iterate on LLM prompts with structured evaluation and self-correction.
  Test prompts against ground truth, compare models, track version history.
  Self-correction loop sends invalid outputs back to LLM for fixing.
  Supports both taxonomy classification and QRA (Question-Reasoning-Answer) generation.
allowed-tools: ["Bash", "Read", "Write"]
triggers:
  - prompt-lab
  - eval prompt
  - test prompt
  - compare models
  - compare models
  - extract prompts
  - test sparta qra
  - prompt evaluation
  - prompt-validator
  - qra evaluation
  - citation grounding
metadata:
  short-description: Iterate and evaluate LLM prompts with self-correction
---

# Prompt Lab

Systematic prompt engineering with ground truth evaluation and **self-correction loop**.

## Key Feature: Self-Correction Loop

Unlike simple validation that silently filters invalid outputs, this skill:

1. **Presents vocabulary in prompt** - LLM knows valid options upfront
2. **Validates response** - Pydantic catches invalid tags
3. **Sends correction back to LLM** - "You used invalid tags X. Valid options are Y. Please fix."
4. **Tracks correction rounds** - Metrics show how often LLM needed help

This gives the model a chance to self-correct rather than silently failing.

## Quick Start

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/prompt-lab

# Run evaluation with self-correction enabled (default)
./run.sh eval --prompt taxonomy_v1 --model deepseek

# Compare multiple models on same prompt
./run.sh compare --prompt taxonomy_v1 --models "deepseek,gpt-4o"



# View evaluation history
./run.sh history --prompt taxonomy_v1
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: LLM Call with Vocabulary in Prompt                │
│     - Vocabulary clearly defined (Tier 0, Tier 1 tags)      │
│     - JSON response format enforced                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Pydantic Validation                               │
│     - Parse JSON response                                   │
│     - Detect invalid/hallucinated tags                      │
│     - Track rejected tags for metrics                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Self-Correction Loop (if invalid tags detected)   │
│     - Send assistant message: "Invalid tags: X"             │
│     - Ask LLM to fix: "Valid options are: Y"                │
│     - Retry up to N times (default: 2)                      │
│     - Track correction rounds in metrics                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 4: Evaluation Metrics                                │
│     - Precision/Recall/F1 vs ground truth                   │
│     - Correction rounds needed                              │
│     - Correction success rate                               │
└─────────────────────────────────────────────────────────────┘
```

## Commands

### eval - Run Evaluation

```bash
./run.sh eval --prompt taxonomy_v1 --model deepseek

# Options:
#   --prompt NAME           Prompt version to test
#   --model NAME            Model to use (deepseek, gpt-4o, etc.)
#   --cases N               Number of test cases (default: all)
#   --max-corrections N     Max self-correction rounds (default: 2)
#   --no-correction         Disable self-correction loop
#   --task-name NAME        Task-monitor task name for quality gate
#   --verbose               Show per-case details
```

### compare - Compare Models

```bash
./run.sh compare --prompt taxonomy_v1 --models "deepseek,gpt-4o"

# Output:
# | Model    | F1    | Corrections | Time  |
# |----------|-------|-------------|-------|
# | deepseek | 0.90  | 3           | 2.3s  |
# | gpt-4o   | 0.93  | 1           | 1.1s  |
```

### extract-prompts - Extract Prompts from Python

```bash
./run.sh extract-prompts --file /path/to/12_qra.py --output prompts/
```

### test-sparta - End-to-End SPARTA QRA Test

```bash
./run.sh test-sparta --db-path /path/to/sparta.duckdb --cases 100
```

## Advanced Usage

### test-sparta Options

- `--phase <0|1>`: 0=Relationships (Technique->Control), 1=Simple Control QRA
- `--threshold <float>`: Citation grounding threshold (default: 0.85)

### Validation Features

- **Ambiguity Gate**: Checks for sufficient length and context keyword usage.
- **Entity Anchoring**: Verifies questions explicitly name the subject entities.
- **Citation Grounding**: Verifies answers are derived verbatim from source text.

### history - View History

```bash
./run.sh history --prompt taxonomy_v1

# Shows all evaluation runs with scores over time
```

### analyze - Analyze Past Results

```bash
./run.sh analyze --prompt taxonomy_v1

# Analyzes error patterns across all previous evaluations:
# - Most common invalid tags
# - Cases needing correction
# - Performance trend over time
# - Suggests improvements based on patterns
```

### optimize - LLM-Powered Prompt Optimization

```bash
./run.sh optimize --prompt taxonomy_v1

# Uses LLM to analyze error cases and suggest prompt improvements:
# - Reviews cases with low F1 scores
# - Identifies ambiguous tag definitions
# - Generates revised prompt sections
# - Saves suggestions for review
```

## Self-Correction Prompt

When invalid tags are detected, this correction message is sent back to the LLM:

```
Your response contained invalid tags that are not in the allowed vocabulary.

Invalid tags you used: {rejected_tags}

Valid conceptual tags (Tier 0): Corruption, Fragility, Loyalty, Precision, Resilience, Stealth
Valid tactical tags (Tier 1): Detect, Evade, Exploit, Harden, Isolate, Model, Persist, Restore

Please correct your response. Return ONLY valid JSON with tags from the allowed vocabulary above.
Do NOT invent new categories. Only use the exact tag names listed.
```

## Quality Gates

Evaluation enforces quality gates:

- **F1 >= 0.8** - Must achieve 80% F1 score against ground truth
- **Correction Success >= 90%** - Self-correction must succeed 90% of the time

If quality gates fail, exit code is 1 (for CI/CD integration).

## Task-Monitor Integration

```bash
# Notify task-monitor of evaluation result
./run.sh eval --prompt taxonomy_v1 --task-name "prompt-validation"

# Task-monitor receives:
# - Task name
# - Pass/fail status
# - Metrics (F1, correction rounds, rejected tags)
```

## Directory Structure

```
prompt-lab/
├── SKILL.md
├── run.sh
├── prompt_lab.py           # Main CLI with self-correction
├── ground_truth/
│   └── taxonomy.json       # Test cases with expected outputs
├── prompts/
│   ├── taxonomy_v1.txt     # Prompt version 1
│   └── taxonomy_v2.txt     # Prompt version 2
├── results/
│   └── taxonomy_v1_deepseek_20260128.json  # Evaluation results
├── models.json             # Model configurations
└── pyproject.toml
```

## Metrics

- **F1**: Combined precision/recall across all tag types
- **Conceptual Precision/Recall**: Tier 0 tag accuracy
- **Tactical Precision/Recall**: Tier 1 tag accuracy
- **Correction Rounds**: Total self-correction attempts across all cases
- **Correction Success Rate**: Percentage of cases where self-correction worked
- **Rejected Tags**: Total hallucinated tags caught (before and after correction)

## Model Configuration

Models are configured in `models.json`:

```json
{
  "deepseek": {
    "provider": "chutes",
    "model": "deepseek-ai/DeepSeek-V3-0324-TEE",
    "api_base": "$CHUTES_API_BASE",
    "api_key": "$CHUTES_API_KEY"
  },
  "gpt-4o": {
    "provider": "openai",
    "model": "gpt-4o",
    "api_key": "$OPENAI_API_KEY"
  }
}
```

## Use Cases

1. **Taxonomy Prompt Iteration**: Improve SPARTA bridge tag extraction
2. **QRA Prompt Testing**: Test question-reasoning-answer extraction with citation grounding
3. **Classification Tasks**: Any structured output with controlled vocabulary
4. **Model Selection**: Compare providers for quality/cost tradeoffs
5. **Self-Correction Analysis**: Understand which models need more guidance

## QRA Evaluation (Roadmap)

Prompt-lab currently supports taxonomy classification. Based on real-world usage in SPARTA QRA generation, the following enhancements are planned:

### Current Limitations

- Only evaluates conceptual/tactical tag F1 scores
- No citation grounding validation
- No multi-item response support (QRA generates 4-7 items per input)
- No hallucination detection
- No question type diversity metrics

### Planned Features

**QRA Evaluation Mode:**

```bash
./run.sh eval-qra --prompt qra_v2 --model deepseek --cases 5
```

**New Metrics:**

- Citation grounding rate (% of citations that match source text verbatim)
- Question type distribution (simple/medium/complex/reversal_curse)
- Persona distribution (lay_person/project_manager/cybersecurity_expert)
- Hallucination count (citations not found in source)
- Duplicate answer detection
- Confidence distribution (strong/partial/inference)

**Citation Grounding Validation:**
Uses rapidfuzz to verify every citation is an exact verbatim excerpt from source text:

```python
def validate_citation(citation: str, source_text: str, threshold: float = 0.85) -> bool:
    from rapidfuzz import fuzz
    return fuzz.partial_ratio(citation.lower(), source_text.lower()) >= threshold * 100
```

### Key Learnings from SPARTA QRA Generation

**What Worked:**

| Technique                                      | Outcome                                              |
| ---------------------------------------------- | ---------------------------------------------------- |
| "Think like a LEGAL LLM - cite precedent"      | Enforced verbatim citation behavior                  |
| "STRICT GROUNDING - if not in text, don't add" | Eliminated hallucinated mitigation advice            |
| "Generate ALL reasonable questions"            | Increased diversity from 1-2 to 4-7 QRAs per input   |
| "Each extracts DIFFERENT information"          | Reduced duplicate answers                            |
| "EXACT verbatim excerpt" for citations         | Stopped control ID citations, enforced text snippets |

**What Didn't Work:**

| Anti-Pattern                       | Problem                                 |
| ---------------------------------- | --------------------------------------- |
| Template examples in prompts       | Caused repetitive outputs               |
| Generic "be grounded" instructions | Too vague, still hallucinated           |
| "Generate ONE per type"            | Limited coverage of source material     |
| No deduplication guidance          | Repeated same answer in different words |
| "Citation: [CONTROL_ID]"           | Generated IDs instead of text excerpts  |

### Refined QRA Prompt Template

The following prompt pattern generates properly grounded QRAs:

```
You are a space-based cybersecurity expert generating Question-Reasoning-Answer pairs
for SPARTA. Think like a LEGAL LLM: every claim MUST cite precedent from the provided text.

STRICT GROUNDING RULE: If information is NOT in the provided text, you CANNOT include
it in your answer. Do NOT add external knowledge, mitigation advice, or implications
not directly stated.

Return JSON: {"items": [{"question": "...",
  "question_type": "simple|medium|complex|reversal_curse",
  "questioner_persona": "lay_person|project_manager|cybersecurity_expert",
  "reasoning": "...", "answer": "...",
  "citations": ["EXACT verbatim excerpt from text"],
  "confidence": "strong|partial",
  "conceptual_tags": [], "tactical_tags": []}]}

GENERATE ALL REASONABLE NON-DUPLICATE QUESTIONS:
- Simple, Medium, Complex levels + Reversal curse where applicable
- Each extracts DIFFERENT information from the text
- NEVER add information not in the source text

TAXONOMY: C=[Corruption,Fragility,Loyalty,Precision,Resilience,Stealth],
T=[Detect,Evade,Exploit,Harden,Isolate,Model,Persist,Restore]
```

### Implementation Status

- [x] Create [`citation_validator.py`](citation_validator.py) with rapidfuzz
- [x] Add `QRAEvalSummary`, `QRAGroundedTestCase`, `QRAGroundedResult` dataclasses to [`evaluation.py`](evaluation.py)
- [x] Create [`ground_truth/qra_grounded.json`](ground_truth/qra_grounded.json) schema
- [x] Create example prompt [`prompts/qra_grounded_v1.txt`](prompts/qra_grounded_v1.txt)
- [x] Add `load_qra_grounded_truth()` function to [`evaluation.py`](evaluation.py)
- [x] Add `eval-qra` command to [`prompt_lab.py`](prompt_lab.py) CLI
- [x] [`run.sh`](run.sh) automatically supports eval-qra (passes all args to CLI)
- [x] QRA-specific metrics in evaluation output

### Files Added

- [`citation_validator.py`](citation_validator.py) - Citation grounding validation with rapidfuzz fuzzy matching
- [`ground_truth/qra_grounded.json`](ground_truth/qra_grounded.json) - Schema with source_text and citation requirements
- [`prompts/qra_grounded_v1.txt`](prompts/qra_grounded_v1.txt) - Working prompt template from SPARTA production use

### Usage

The `eval-qra` command is now available:

```bash
# Run QRA evaluation with default settings
./run.sh eval-qra --prompt qra_grounded_v1 --model deepseek

# With custom threshold and verbose output
./run.sh eval-qra --prompt qra_grounded_v1 --model deepseek --threshold 0.90 --verbose

# Test on limited cases
./run.sh eval-qra --prompt qra_grounded_v1 --model deepseek --cases 2
```

**Output includes:**

- Total QRAs generated
- Average QRAs per input
- Citation grounding rate
- Hallucination count
- Duplicate detection
- Question type coverage
- Average latency

**Quality Gates:**

- Citation grounding ≥ 85%
- Zero hallucinations

For details, see: [`../../.agent/inbox/memory_prompt-lab-qra-improvements_20260131_125541.md`](../../.agent/inbox/memory_prompt-lab-qra-improvements_20260131_125541.md)
