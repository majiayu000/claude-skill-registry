---
name: paper2code
description: |
  Analyzes research papers (PDF/arXiv URL) and converts them into executable code.
  Automatically activated upon requests for paper replication, algorithm implementation, or research reproduction.
  Responds to requests like "Implement this paper", "paper2code", "Convert paper to code".
---

# Paper2Code: AI Agent for Converting Research Papers into Code

## Overview

This Skill executes a **4+2 stage pipeline** effectively systematically analyzing research papers and converting them into executable code.

**Core Principle**: Do not simply read the paper and generate code; generate a **structured intermediate representation (YAML)** first, then write the code.

---

## ⚠️ Critical Behavioral Control Rules (CRITICAL)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ MANDATORY BEHAVIORAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Implement one file at a time
2. Proceed to the next file only after completing the current file, without asking for confirmation
3. Original paper specifications always take precedence over reference code
4. Perform a Self-Check for each Phase before completion
5. Save all intermediate results as YAML files

DO:
✓ Implementing exactly what is stated in the paper
✓ Write simple and direct code
✓ Working code first, elegant code later
✓ Test each component immediately
✓ Move to the next file immediately after implementation is complete

DON'T:
✗ Do not ask "Shall I implement the next file?" between files
✗ Extensive documentation not required for core functionality
✗ Optimization not needed for reproducibility
✗ Excessive abstraction or design patterns
✗ Providing instructions without writing actual code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Input Processing

### Supported Formats
1. **arXiv URL**: `https://arxiv.org/abs/xxxx.xxxxx` or `https://arxiv.org/pdf/xxxx.xxxxx.pdf`
2. **PDF File Path**: `/path/to/paper.pdf`
3. **Converted Text/Markdown**: When paper content is provided as text

### Input Processing Method

**For arXiv URL:**
```bash
# Convert to PDF URL and download
curl -L "https://arxiv.org/pdf/xxxx.xxxxx.pdf" -o paper.pdf

# Convert PDF to text (using pdftotext)
pdftotext -layout paper.pdf paper.txt
```

**For PDF File:**
```bash
pdftotext -layout "/path/to/paper.pdf" paper.txt
```

---

## Pipeline Overview

```
[User Input: Paper URL/File]
        │
        ▼
┌─────────────────────────────────────────────┐
│ Step 0: Acquire Paper Text                  │
│ - arXiv URL → Download PDF                  │
│ - PDF → Convert to Text                     │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 0: Search Reference Code (Optional)   │
│ @[05_reference_search.md]                   │
│ Output: reference_search.yaml               │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 1: Algorithm Extraction               │
│ @[01_algorithm_extraction.md]               │
│ Output: 01_algorithm_extraction.yaml        │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 2: Concept Analysis                   │
│ @[02_concept_analysis.md]                   │
│ Output: 02_concept_analysis.yaml            │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 3: Implementation Plan                │
│ @[03_code_planning.md]                      │
│ Output: 03_implementation_plan.yaml         │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 4: Code Implementation                │
│ @[04_implementation_guide.md]               │
│ Output: Complete Project Directory          │
└─────────────────────────────────────────────┘
```

---

## Data Transfer Format Between Stages

### Phase 1 → Phase 2 Transfer
```yaml
phase1_to_phase2:
  algorithms_found: "[Number of found algorithms]"
  key_algorithms:
    - name: "[Algorithm Name]"
      section: "[Paper Section]"
      complexity: "[Simple/Medium/Complex]"
  hyperparameters_count: "[Number of collected hyperparameters]"
  critical_equations: "[List of critical equation numbers]"
  missing_info: "[List of missing information]"
```

### Phase 2 → Phase 3 Transfer
```yaml
phase2_to_phase3:
  components_count: "[Number of identified components]"
  implementation_complexity: "[Low/Medium/High]"
  key_dependencies:
    - "[Component A] → [Component B]"
  experiments_to_reproduce:
    - "[Experiment Name]: [Expected Result]"
  success_criteria:
    - "[Specific Success Criteria]"
```

### Phase 3 → Phase 4 Transfer
```yaml
phase3_to_phase4:
  file_order: "[List of files in implementation order]"
  current_file: "[Currently implementing file]"
  completed_files: "[List of completed files]"
  blocking_dependencies: "[Dependencies to resolve]"
```

---

## Detail of Each Phase

### Phase 0: Reference Code Search (Optional)
Using the @[05_reference_search.md](05_reference_search.md) prompt:
- Search for and evaluate 5 similar implementations
- Secure references to improve implementation quality
- **Output**: Reference list in YAML format

### Phase 1: Algorithm Extraction
Using the @[01_algorithm_extraction.md](01_algorithm_extraction.md) prompt:
- Extract all algorithms, equations, and pseudocode
- Collect hyperparameters and configuration values
- Organize training procedures and optimization methods
- **Output**: Complete algorithm specification in YAML format

### Phase 2: Concept Analysis
Using the @[02_concept_analysis.md](02_concept_analysis.md) prompt:
- Map paper structure and sections
- Analyze system architecture
- Identify component relationships and data flow
- Organize experiment and validation requirements
- **Output**: Implementation requirements specification in YAML format

### Phase 3: Establish Implementation Plan
Using the @[03_code_planning.md](03_code_planning.md) prompt:
- Integrate results from Phase 1 and 2
- Generate detailed implementation plans for 5 essential sections:
  1. `file_structure`: Project file structure
  2. `implementation_components`: Implementation component details
  3. `validation_approach`: Validation and testing methods
  4. `environment_setup`: Environment and dependencies
  5. `implementation_strategy`: Step-by-step implementation strategy
- **Output**: Complete YAML implementation plan (8000-10000 characters)

### Phase 4: Code Implementation
Following the guide @[04_implementation_guide.md](04_implementation_guide.md):
- Generate code file by file according to the plan
- Implement in dependency order
- Each file must be complete and executable
- **Output**: Executable codebase

---

## Memory Management
Refer to the guide @[06_memory_management.md](06_memory_management.md):
- Context management when processing long papers
- Saving step-by-step outputs
- Recovery protocol in case of interruption

---

## Quality Standards

### Principles that Must Be Followed
- **Completeness**: Complete implementation without placeholders or TODOs
- **Accuracy**: Accurately reflect equations and parameters specified in the paper
- **Executability**: Code that can be executed immediately
- **Reproducibility**: Must be able to reproduce the results of the paper

### File Implementation Order
1. Configuration and environment files (config, requirements.txt initialization)
2. Core utilities and base classes
3. Main algorithm/model implementation
4. Training and evaluation scripts
5. Documentation (README.md, requirements.txt finalization)

---

## ✅ Final Completion Checklist (MANDATORY)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ BEFORE DECLARING COMPLETE - ALL MUST BE YES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ All algorithms in the paper implemented?       → YES / NO
□ Correct versions of environment/datasets set?  → YES / NO
□ All comparison methods referenced implemented? → YES / NO
□ Working integration to run paper experiments?  → YES / NO
□ All metrics, figures, tables reproducible?     → YES / NO
□ Basic docs explaining how to reproduce?        → YES / NO
□ Code runs without errors?                      → YES / NO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ If even one is NO, it is NOT complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Usage Examples

### Example 1: arXiv Paper
```
User: Implement this paper https://arxiv.org/abs/2301.12345

Claude: I will analyze the paper and convert it to code.

[Phase 0: Reference Code Search (Optional)...]
[Phase 1: Algorithm Extraction...]
[Phase 2: Concept Analysis...]
[Phase 3: Establish Implementation Plan...]
[Phase 4: Code Generation...]
```

### Example 2: PDF File
```
User: Implement the algorithms from this paper /home/user/papers/attention.pdf
```

### Example 3: Specific Request
```
User: Implement only the algorithm in Section 3 of this paper
```

---

## Related Files

- [01_algorithm_extraction.md](01_algorithm_extraction.md) - Phase 1: Algorithm Extraction
- [02_concept_analysis.md](02_concept_analysis.md) - Phase 2: Concept Analysis
- [03_code_planning.md](03_code_planning.md) - Phase 3: Implementation Plan
- [04_implementation_guide.md](04_implementation_guide.md) - Phase 4: Implementation Guide
- [05_reference_search.md](05_reference_search.md) - Phase 0: Reference Search (Optional)
- [06_memory_management.md](06_memory_management.md) - Memory Management Guide

---

## Precautions

```
⚠️ REMEMBER:

1. Read the paper thoroughly: Start implementation after understanding the entire content
2. Save detailed results: Save YAML output of each Phase as a file
3. Incremental implementation: Do not generate all code at once, proceed file by file
4. Include verification: Include simple test code if possible
5. Reference is inspiration: Reference code is for understanding and application, not copying
```