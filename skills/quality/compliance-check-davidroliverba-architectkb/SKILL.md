---
name: compliance-check
context: fork
description: Evaluate an architecture artifact (ADR, HLD, LLD) against the vault's established architecture principles
model: opus
---

# /compliance-check

Evaluate any architecture artifact against the vault's established architecture principles. Produces a structured compliance assessment with per-principle scoring, evidence mapping, and actionable remediation steps.

## Usage

```
/compliance-check <artifact title>
/compliance-check "ADR - SAP Data Product"
/compliance-check "HLD - Remote Vault Access Architecture"
/compliance-check "LLD - Vault Bot Message Processing"
```

## Arguments

- **$ARGUMENTS**: The title of the architecture artifact to assess (required). Must match an existing `ADR - *.md`, `HLD - *.md`, or `LLD - *.md` file in the vault.

## Supported Artifact Types

| Type | Location | Naming Pattern |
|------|----------|----------------|
| ADR  | `ADRs/`  | `ADR - *.md`   |
| HLD  | Root     | `HLD - *.md`   |
| LLD  | Root     | `LLD - *.md`   |

## Instructions

### Phase 1: Load the Target Artifact

1. **Parse the command** -- extract the artifact title from `$ARGUMENTS`
2. **Find the artifact file:**
   - For ADRs: search in `ADRs/` folder
   - For HLDs and LLDs: search at vault root
   - If the title does not include the type prefix (`ADR -`, `HLD -`, `LLD -`), try all three locations
   - If not found, search using Grep for partial title matches
   - If still not found, report the error and list available artifacts of each type
3. **Read the artifact** -- load the full content including frontmatter and body
4. **Extract metadata:**
   - `type` -- to confirm it is an architecture artifact
   - `relatedTo` wiki-links from frontmatter
   - `tags` for domain context (e.g., `domain/security`, `project/beta`)
   - `project` if specified
   - `status` (draft, proposed, accepted, etc.)
   - Any inline wiki-links in the body text

### Phase 2: Discover Architecture Principles

Principles are stored as `Concept` notes with `conceptType: principle` in frontmatter. There are two categories:

1. **Individual principle notes** -- standalone `Concept - *.md` files with `conceptType: principle`
2. **Principle collection notes** -- notes like `Concept - Beta Solution Architecture Principles` that contain multiple numbered principles in the body

#### 2.1 Find Individual Principle Notes

The graph index does not include `conceptType` in its indexed fields. Use Grep to find principle notes:

```bash
grep -rl "conceptType: principle" *.md Concept\ -\ *.md
```

Read each discovered principle note and extract:
- **title** -- the principle name
- **statement** -- the principle statement (from `statement` frontmatter field or the first blockquote in the body)
- **implications** -- what follows from the principle (from `implications` frontmatter field)
- **domain** -- which domain it applies to (from `domain` frontmatter field)
- **tags** -- for domain matching against the artifact

#### 2.2 Find Principle Collection Notes

Some notes contain multiple principles as sections (e.g., `Concept - Beta Solution Architecture Principles` with AP01-AP07). Search for these:

```bash
grep -rl "conceptType: principle" Concept\ -\ *.md
```

For collection notes, extract each individual principle:
- **Reference number** (e.g., AP01)
- **Name** (e.g., "Adopt, Don't Adapt")
- **One-liner** (the blockquote after the heading)
- **Statement** (the paragraph after the one-liner)
- **Fitness Function** (the measurable criteria)

#### 2.3 Determine Applicable Principles

Not all principles apply to every artifact. Use domain matching:

1. **Check artifact tags** -- extract domain tags (e.g., `domain/security`, `project/beta`, `technology/ai`)
2. **Check artifact content** -- scan for domain indicators (security, data, integration, cloud, AI references)
3. **Match principle domains** -- a principle applies if:
   - Its `domain` field matches the artifact's domain tags, OR
   - Its `tags` overlap with the artifact's tags, OR
   - Its `statement`/`implications` are relevant to the artifact's subject matter
4. **Project-scoped principles** -- if the artifact references a project (e.g., Beta), include project-specific principle collections
5. **Universal principles** -- principles without a narrow domain scope always apply

If in doubt about applicability, include the principle and mark as NOT APPLICABLE in the output rather than silently excluding it.

### Phase 3: Evaluate Compliance

For each applicable principle, assess the artifact against it using this rubric:

| Status | Criteria |
|--------|----------|
| **COMPLIANT** | The artifact explicitly addresses this principle. Specific evidence exists in the design, decision rationale, or implementation approach. |
| **PARTIAL** | The artifact partially addresses this principle. Some elements are present but gaps remain -- the principle is not fully satisfied. |
| **NON-COMPLIANT** | The artifact does not address this principle despite it being applicable. The design contradicts the principle, or a relevant concern is entirely absent. |
| **NOT APPLICABLE** | The principle does not apply to this artifact's scope, domain, or context. Justify why. |

**How to assess:**

1. **Read the principle statement and implications carefully**
2. **Search the artifact** for evidence of compliance:
   - Design choices that align with the principle
   - Explicit mentions of the principle's concerns
   - Trade-offs or decisions that satisfy the principle's intent
3. **Check for contradictions** -- does the artifact make choices that conflict with the principle?
4. **Check for gaps** -- does the principle raise concerns the artifact should address but does not?
5. **For collection principles with fitness functions** -- note whether the artifact's approach would pass the fitness function criteria

### Phase 4: Generate Compliance Assessment

Output the assessment directly to the console. Use the template below.

---

## Output Template

```markdown
## Principles Compliance Assessment

**Target:** [[{artifact title}]]
**Artifact Type:** {ADR / HLD / LLD}
**Artifact Status:** {status from frontmatter}
**Date:** {today}
**Principles Evaluated:** {count of applicable principles}
**Principles Excluded (not applicable):** {count}

---

### Compliance Summary

| Metric | Count |
|--------|-------|
| **Compliant** | {n} / {total applicable} |
| **Partial** | {n} / {total applicable} |
| **Non-compliant** | {n} / {total applicable} |
| **Not applicable** | {n} / {total evaluated} |

---

### Detailed Assessment

| # | Principle | Source | Status | Evidence | Gap |
|---|-----------|--------|--------|----------|-----|
| 1 | {Principle Title} | [[{source note}]] | COMPLIANT | {where in the artifact this is addressed} | -- |
| 2 | {Principle Title} | [[{source note}]] | PARTIAL | {partially addressed here} | {what is missing} |
| 3 | {Principle Title} | [[{source note}]] | NON-COMPLIANT | -- | {what is missing and why it matters} |
| 4 | {Principle Title} | [[{source note}]] | NOT APPLICABLE | -- | {why this principle does not apply} |

---

### Compliance by Domain

| Domain | Compliant | Partial | Non-compliant | N/A |
|--------|-----------|---------|---------------|-----|
| {domain} | {n} | {n} | {n} | {n} |

---

### Recommended Actions

For each PARTIAL or NON-COMPLIANT principle, provide a specific, actionable remediation step:

1. **{Principle Title}** (PARTIAL)
   - **Gap:** {what is missing}
   - **Action:** {specific change to achieve compliance}
   - **Priority:** {high / medium / low -- based on principle criticality}

2. **{Principle Title}** (NON-COMPLIANT)
   - **Gap:** {what is missing and the risk of non-compliance}
   - **Action:** {specific change to achieve compliance}
   - **Priority:** {high / medium / low}

---

### Context

**Principles sources consulted:**
- [[{principle note 1}]] -- {n} principles
- [[{principle note 2}]] -- {n} principles

**Artifact domain tags:** {list of domain/project tags from the artifact}

**Artifact linked notes:** {list of relatedTo references}

---

*Compliance assessment generated by Claude Code /compliance-check skill. Evaluates document completeness against established principles -- does not assess implementation quality.*
```

---

## Scoring Guidance

### COMPLIANT Examples

- Principle says "encrypt data at rest and in transit" -- the artifact specifies TLS for transport and AES-256 for storage
- Principle says "define API contracts" -- the artifact references OpenAPI specifications for each interface
- Principle says "single source of truth for data" -- the artifact designates an authoritative system for each data entity

### PARTIAL Examples

- Principle says "encrypt data at rest and in transit" -- the artifact mentions TLS but does not address encryption at rest
- Principle says "design for failure" -- the artifact has an availability target but no recovery procedure
- Principle says "observe everything" -- the artifact mentions logging but not alerting or distributed tracing

### NON-COMPLIANT Examples

- Principle says "no point-to-point integrations" -- the artifact proposes a direct database link between two systems
- Principle says "Zero Trust" -- the artifact assumes a trusted network perimeter
- Principle says "adopt, don't adapt" -- the artifact proposes building a custom solution where COTS products exist

### NOT APPLICABLE Examples

- A data governance principle assessed against an ADR about UI framework selection
- An AI governance principle assessed against an HLD for a file transfer pipeline
- A project-specific principle (e.g., Beta AP01-AP07) assessed against an artifact for a different project

## Examples

### Example 1: ADR Compliance Check

```
/compliance-check "ADR - SAP Data Product"
```

Evaluates the ADR against all applicable principles -- likely including data governance, integration, and security principles.

### Example 2: HLD Compliance Check

```
/compliance-check "HLD - Remote Vault Access Architecture"
```

Evaluates the HLD against all applicable principles. For a remote access architecture, security principles (Zero Trust, encryption) and operational principles (observability, failure recovery) would be particularly relevant.

### Example 3: Project-Scoped Check

```
/compliance-check "HLD - SecureTransfer Azure Files to S3 Mirroring"
```

If the HLD is tagged with `project/beta`, the Beta Solution Architecture Principles (AP01-AP07) would be included alongside any universal principles.

## Error Handling

- **Artifact not found:** List available ADR, HLD, and LLD notes and ask the user to confirm the title
- **No principle notes found:** Report that no `conceptType: principle` notes exist in the vault. Suggest creating principles using the `/incubator` skill or referencing industry frameworks
- **Empty artifact:** Report that the artifact has minimal content -- compliance cannot be meaningfully assessed. Flag as INFORMATIONAL
- **Artifact is draft status:** Proceed with the assessment but note in the output that the artifact is still in draft and compliance gaps may be addressed before finalisation
- **No applicable principles:** If all principles are NOT APPLICABLE, report this finding and suggest that the artifact's domain may not yet have established principles

## Related Skills

- `/hld-review` -- Full six-dimension HLD review (includes principle compliance as one dimension)
- `/nfr-review` -- Review against NFR requirements (complementary -- NFRs and principles serve different governance purposes)
- `/adr` -- Create new ADRs for design choices identified as gaps
- `/impact-analysis` -- Analyse the impact of changes to systems referenced in the artifact

## Related Notes

- `Concept - Beta Solution Architecture Principles` -- Seven Beta SA principles with fitness functions
- `Concept - Beta Digital Team Principles` -- Beta Digital Team Principles
- `.claude/context/architecture.md` -- Architecture governance context
- `.claude/context/frontmatter-reference.md` -- Frontmatter schemas for ADR, HLD, LLD
