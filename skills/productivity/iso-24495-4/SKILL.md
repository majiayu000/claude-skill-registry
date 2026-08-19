---
name: iso-24495-4
description: Provisional task skill for organisational plain language implementation (based on ISO/CD 24495-4, committee draft). Activates for plain language gap analysis, policy drafting, review workflow design, and organisational readiness for the future published standard. Does not activate for ordinary writing, rewriting, or reviewing of individual documents.
metadata:
  version: "0.5.0"
  iso-standard: "ISO/CD 24495-4"
  iso-status: "committee-draft"
---

# ISO/CD 24495-4 - Plain Language (Organisational Implementation) [PROVISIONAL DRAFT]

> **Provisional status:** ISO 24495-4 is a Committee Draft (ISO/CD 24495-4) and is not yet published; its text is not public. This skill is original guidance based on the draft's public scope. It does not reproduce ISO text and its output is never a compliance statement. Expect revision when the standard is published.

Turns the agent from a copy editor into an implementation consultant. It assesses an organisation's *capacity to produce* plain language across governance, capability, process, measurement, and culture, rather than the quality of any single text.

## Scope & Execution Boundaries

1. **Activation Rules:**
   - **Activate for:** plain language gap analysis, maturity assessment, policy or style guide drafting, review workflow design, training planning, readiness for the future published standard.
   - **Never activate for:** writing, rewriting, summarising, or reviewing an individual document. Those tasks belong to `iso-24495-1`, `-2`, `-3`, and `-5`.

2. **Confirmation Before Sweeps:**
   - Both audit scripts read many files. State which directory will be swept and get the user's confirmation before running either.

3. **Evidence Primacy:**
   - Never assert a maturity level without evidence: a found artefact, a confirmed answer, or a measured count. Absent evidence scores as absent.

## The Audit Workflow

Run the four steps in order. Each feeds the next.

1. **Sweep for process artefacts (primary):**
   - Run `bun scripts/audit-evidence-cli.ts <workspace-dir> --json evidence.json`.
   - This detects the *system*: policy, review workflow, automated checks, training, glossary. It reads presence only; you evaluate the quality of what it finds.
2. **Audit the document corpus (secondary):**
   - Run `bun scripts/audit-corpus-cli.ts <corpus-dir> --json findings.json`.
   - Output feeds the **Measurement dimension only**, as evidence of what the system produces. Text quality alone never raises a maturity level: excellent text can come from one unsupported expert, and flawed text can coexist with a strong process that is catching it.
3. **Interview the human (3 to 5 questions maximum):**
   - Use `references/interview-guide.md`. Ask only what the file system cannot show (leadership, culture, training delivery). Record answers in the `answers.json` structure and cite evidence for each `true`.
   - Score with `bun scripts/score-maturity-cli.ts answers.json --json maturity.json`. Scoring is deterministic so levels cannot drift between sessions.
4. **Generate the gap report:**
   - Run `bun scripts/generate-report-cli.ts findings.json evidence.json maturity.json --state <dir>/state.json --out gap-report.md`.
   - State is append-only; successive audits produce a trend table that proves or disproves progress. Store `state.json` in the organisation's repository, not in the skill directory (installed skills may be read-only).

## Quantitative Rules & Hard Constraints

1. **Proxies, Not Compliance:** Corpus metrics (sentence length, paragraph length, legalese, heading depth) are mechanical proxies. Never present them, or this report, as ISO compliance or certification.
2. **Interview Cap:** Ask the human at most 5 questions per audit. Infer everything else from artefacts.
3. **Ranked Actions:** Every gap in the report gets a recommended action, ranked by reader impact against effort, tied to the criterion it unblocks.
4. **Language Boundary:** The text heuristics are English-centric. For non-English corpora, skip step 2 and say so in the report.

## Contrastive Examples

### Example 1: Reporting a Gap
* ❌ **Not aligned (Vague, Unevidenced):**
  > "The organisation's culture around plain language seems weak and should be improved."
* ✅ **ISO/CD 24495-4 (Draft) Aligned:**
  > **Culture: Level 1.** Leadership is aware of the policy, confirmed in
  > interview, but does not champion it. No leader has communicated it in the
  > last year, and no feedback loop exists. **Action (unblocks
  > `leadership-champions`):** the policy owner asks one executive sponsor to
  > open the next all-hands with a plain language example.

## Pre-Output Self-Audit Checklist

Before delivering a gap report, audit against these checks:
- [ ] **Correct activation:** Was this an implementation task, not a writing task?
- [ ] **Sweep confirmed:** Did the user approve each directory sweep?
- [ ] **Evidence cited:** Does every maturity level and `true` answer cite an artefact, answer, or count?
- [ ] **Proxies labelled:** Are corpus metrics presented as proxies feeding Measurement only?
- [ ] **State saved:** Was `state.json` updated so the next audit can show a trend?
- [ ] **Provisional stated:** Does the report declare the committee-draft basis and its limitations?
