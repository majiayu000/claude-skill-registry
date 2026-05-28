---
name: spec-checker
description: Performs specification-to-code compliance analysis.
Use when: (1) verifying implementations match their formal specifications,
(2) auditing smart contracts against whitepapers, (3) checking that code
behavior aligns with design documents.

category: audit
---

# Spec Compliance Checker

Perform specification-to-code compliance analysis. Determine whether a codebase implements **exactly** what the documentation states, across logic, invariants, flows, assumptions, math, and security guarantees.

Work must be deterministic, grounded in evidence, traceable, non-hallucinatory, and exhaustive.

## 7-Phase Compliance Workflow

Execute these phases sequentially. Each phase builds on the IR (Intermediate Representation) produced by previous phases.

### Phase 0: Documentation Discovery
Identify all content representing documentation, even if not named "spec." Scan for whitepapers, design docs, READMEs, protocol descriptions, Notion exports, and any file describing logic, flows, invariants, formulas, or trust models. Extract all relevant documents into a unified spec corpus.

### Phase 1: Format Normalization
Normalize the spec corpus into a clean, canonical form. Preserve heading hierarchy, bullet lists, formulas, tables, code snippets, and invariant definitions. Remove layout noise, styling artifacts, and watermarks.

### Phase 2: Spec Intent IR Extraction
Extract ALL intended behavior into structured Spec-IR records. Each record must include `spec_excerpt`, `source_section`, `semantic_type`, `normalized_form`, and `confidence` score. Extract invariants, preconditions, postconditions, formulas, flows, security requirements, actor definitions, and edge-case behavior.

**Spec-IR record format (YAML):**

```yaml
spec_ir:
  id: SPEC-001
  spec_excerpt: "<exact quote from spec>"
  source_section: "Section X.Y"
  semantic_type: invariant | precondition | postcondition | formula | flow | security_requirement | actor_definition | edge_case
  normalized_form: "<canonical restatement>"
  confidence: 0.0-1.0
```

### Phase 3: Code Behavior IR Extraction
Perform structured, deterministic, line-by-line and block-by-block semantic analysis of the entire codebase. For every function, extract signature, visibility, modifiers, preconditions, state reads/writes, computations, external calls, events, postconditions, and enforced invariants.

**Code-IR record format (YAML):**

```yaml
code_ir:
  id: CODE-001
  function: "<function name>"
  file: "<file path>"
  lines: "L<start>-L<end>"
  signature: "<full signature>"
  preconditions: []
  state_reads: []
  state_writes: []
  computations: []
  external_calls: []
  postconditions: []
  enforced_invariants: []
```

### Phase 4: Alignment IR (Spec-to-Code Comparison)
For each Spec-IR item, locate related behaviors in Code-IR and generate an Alignment Record with `match_type` classification: `full_match`, `partial_match`, `mismatch`, `missing_in_code`, `code_stronger_than_spec`, or `code_weaker_than_spec`. Include reasoning traces, confidence scores, and evidence links.

**Alignment record format (YAML):**

```yaml
alignment:
  id: ALIGN-001
  spec_ir_ref: SPEC-001
  code_ir_ref: CODE-001
  match_type: full_match | partial_match | mismatch | missing_in_code | code_stronger_than_spec | code_weaker_than_spec
  reasoning: "<evidence-based reasoning>"
  confidence: 0.0-1.0
  spec_evidence: "Section X.Y: <quote>"
  code_evidence: "file.sol L45-60: <description>"
```

### Phase 5: Divergence Classification
Classify each misalignment by severity (CRITICAL, HIGH, MEDIUM, LOW). Each finding must include evidence links, severity justification, exploitability reasoning with concrete attack scenarios and economic impact, and recommended remediation with code examples.

**Divergence finding format (YAML):**

```yaml
divergence:
  id: DIV-001
  alignment_ref: ALIGN-001
  severity: CRITICAL | HIGH | MEDIUM | LOW
  title: "<concise description>"
  spec_evidence: "<exact quote and section>"
  code_evidence: "<file, lines, description>"
  severity_justification: "<why this severity>"
  exploitability: "<concrete attack scenario and impact>"
  remediation: "<recommended fix with code example>"
```

### Phase 6: Final Audit-Grade Report
Produce a structured compliance report with all sections: Executive Summary, Documentation Sources, Spec-IR Breakdown, Code-IR Summary, Full Alignment Matrix, Divergence Findings, Missing Invariants, Incorrect Logic, Math Inconsistencies, Flow Mismatches, Access Control Drift, Undocumented Behavior, Ambiguity Hotspots, Recommended Remediations, Documentation Update Suggestions, and Final Risk Assessment.

## Global Rules

- **Never infer unspecified behavior.** If the spec is silent, classify as UNDOCUMENTED. If code adds behavior, classify as UNDOCUMENTED CODE PATH. If unclear, classify as AMBIGUOUS.
- **Always cite exact evidence** from the documentation (section/title/quote) and the code (file + line numbers).
- **Always provide a confidence score (0-1)** for all mappings.
- **Do NOT rely on prior knowledge** of known protocols. Only use provided materials.
- Maintain strict separation between extraction, alignment, classification, and reporting.
- Be literal, pedantic, and exhaustive.
- Every claim must quote original text or line numbers. Zero speculation.

## Rationalizations to Reject

Do not accept these shortcuts---they lead to missed findings:

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "Spec is clear enough" | Ambiguity hides in plain sight---extract to IR and classify explicitly |
| "Code obviously matches" | Obvious matches have subtle divergences---document with evidence |
| "I'll note this as partial match" | Partial = potential vulnerability---investigate until full_match or mismatch |
| "This undocumented behavior is fine" | Undocumented = untested = risky---classify as UNDOCUMENTED CODE PATH |
| "Low confidence is okay here" | Low confidence findings get ignored---investigate until confidence >= 0.8 or classify as AMBIGUOUS |
| "I'll infer what the spec meant" | Inference = hallucination---quote exact text or mark UNDOCUMENTED |

## Anti-Hallucination Requirements

- If uncertain: set confidence < 0.8 and document ambiguity
- NEVER produce a finding without both spec evidence AND code evidence
- ALWAYS use YAML format for all IR records
- ALWAYS reference line numbers in format: `L45`, `lines: 89-135`
- ALWAYS cite spec locations: `"Section X.Y"`, `"Page N, paragraph M"`

## Execution

1. Ask the user to identify the specification documents and codebase scope
2. Execute all 7 phases sequentially, producing IR artifacts at each stage
3. Write the final report as a structured document
4. Highlight CRITICAL and HIGH findings prominently