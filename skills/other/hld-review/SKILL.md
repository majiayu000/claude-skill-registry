---
name: hld-review
context: fork
description: Evaluate an HLD note against linked ADRs, requirements, and architecture principles across six dimensions
model: opus
---

# /hld-review

Evaluate a High-Level Design (HLD) note against linked ADRs, requirements, and architecture principles. Produces a structured review with scoring across six dimensions, severity-rated findings, and actionable next steps.

## Usage

```
/hld-review <HLD note title>
/hld-review HLD - Remote Vault Access Architecture
/hld-review HLD - SecureTransfer Azure Files to S3 Mirroring
```

## Arguments

- **$ARGUMENTS**: The title of the HLD note to review (required). Must match an existing `HLD - *.md` file in the vault root.

## Review Dimensions

| Dimension | What Is Checked |
|---|---|
| **ADR Coverage** | Does each significant design choice have a corresponding ADR? Are referenced ADRs accepted? |
| **Requirements Traceability** | Are all referenced requirements (from `relatedTo`, project notes, linked concepts) addressed in the design? |
| **Principle Compliance** | Does the design align with vault architecture principles (`Concept` notes with `conceptType: principle`)? |
| **Security Architecture** | Are threat mitigations documented? Are security boundaries, encryption, and access controls explicit? |
| **Integration Clarity** | Are system interfaces, data flows, protocols, and error handling paths clearly defined? |
| **Operational Readiness** | Are monitoring, deployment strategy, runbook considerations, and rollback plans addressed? |

## Instructions

### Phase 1: Load the HLD

1. **Parse the command** — extract the HLD note title from `$ARGUMENTS`
2. **Find the HLD file** — search for the file at the vault root matching the title
   - If not found, search using Grep for partial title matches across `HLD - *.md` files
   - If still not found, report the error and list available HLD notes
3. **Read the HLD note** — load the full content including frontmatter and body
4. **Extract metadata:**
   - `relatedTo` wiki-links from frontmatter
   - `tags` for domain context
   - `confidence`, `freshness`, `verified` quality indicators
   - Any inline wiki-links in the body text (`[[...]]` references)

### Phase 2: Gather Context

1. **Read linked notes** — for each wiki-link found in `relatedTo` and body text:
   - Read each linked note (ADRs, Systems, Concepts, Projects, Patterns)
   - Categorise by type: ADR, System, Concept (principle/capability), Project, Pattern, Threat, other
   - Note the status of each ADR (draft/proposed/accepted/deprecated/superseded)

2. **Query for architecture principles** — find all `Concept` notes with `conceptType: principle`:
   ```bash
   node .claude/scripts/graph-query.js --type=Concept --tag=conceptType/principle
   ```
   If the graph query returns no results, fall back to:
   ```bash
   grep -rl "conceptType: principle" *.md
   ```
   Read each principle note to extract:
   - `statement` — the principle itself
   - `implications` — what follows from the principle
   - `domain` — which domain it applies to

3. **Query for related threats** — search for Threat notes relevant to the HLD's domain:
   - Check tags on the HLD for domain indicators (e.g., `domain/security`, `domain/cloud`, `domain/integration`)
   - Search: `node .claude/scripts/graph-query.js --type=Threat`
   - Match threats by `affectedSystems` and domain overlap

4. **Check for related ADRs not yet linked** — search for ADRs whose `relatedTo` or `project` fields reference the same systems or projects as the HLD:
   ```bash
   node .claude/scripts/graph-query.js --type=Adr --tag=status/accepted
   ```

### Phase 3: Evaluate Each Dimension

Score each dimension as **PASS**, **PARTIAL**, or **FAIL** using the criteria below.

#### 3.1 ADR Coverage

| Score | Criteria |
|---|---|
| **PASS** | Every significant design choice (technology selection, architectural pattern, integration approach) has a corresponding accepted ADR |
| **PARTIAL** | Some design choices have ADRs but others are undocumented, or ADRs exist but are still in draft/proposed status |
| **FAIL** | Major design choices lack ADR coverage entirely |

**How to assess:**
- Identify each significant design choice in the HLD (technology selections, architectural patterns, protocol choices)
- Check whether an ADR exists for each choice (via `relatedTo` links or vault search)
- Note any ADRs that are `draft` or `proposed` rather than `accepted`
- Flag design choices that contradict accepted ADRs

#### 3.2 Requirements Traceability

| Score | Criteria |
|---|---|
| **PASS** | All requirements referenced in linked project/concept notes are explicitly addressed in the HLD |
| **PARTIAL** | Most requirements are addressed but some are missing or only implicitly covered |
| **FAIL** | Significant requirements gaps — linked requirements not addressed in the design |

**How to assess:**
- Extract requirements from linked Project notes (goals, constraints, scope)
- Extract requirements from linked Concept notes (capabilities, principles)
- Verify each requirement has a corresponding design element in the HLD
- Check for orphaned requirements (mentioned in links but not in design)

#### 3.3 Principle Compliance

| Score | Criteria |
|---|---|
| **PASS** | Design explicitly aligns with all applicable architecture principles; no contradictions |
| **PARTIAL** | Design is broadly consistent but some principles are not explicitly addressed |
| **FAIL** | Design contradicts one or more architecture principles, or ignores critical principles |

**How to assess:**
- For each principle note loaded in Phase 2, check whether the HLD design aligns with the principle's `statement` and `implications`
- Focus on principles whose `domain` matches the HLD's domain tags
- Flag any contradictions between the design and established principles

#### 3.4 Security Architecture

| Score | Criteria |
|---|---|
| **PASS** | Security boundaries, encryption (in-transit and at-rest), authentication, authorisation, and threat mitigations are all explicitly documented |
| **PARTIAL** | Some security aspects are covered but gaps exist (e.g., encryption mentioned but no auth model) |
| **FAIL** | Security is not meaningfully addressed in the HLD |

**How to assess:**
- Check for explicit security boundaries (network isolation, trust zones)
- Verify encryption is specified for data in transit and at rest
- Look for authentication and authorisation mechanisms
- Cross-reference with Threat notes — are relevant threats mitigated?
- Check for data classification and GDPR considerations if personal data is involved

#### 3.5 Integration Clarity

| Score | Criteria |
|---|---|
| **PASS** | All system interfaces are documented with protocols, data formats, error handling, and SLAs |
| **PARTIAL** | Interfaces are identified but details are incomplete (missing protocols, no error handling) |
| **FAIL** | System interfaces are vague or missing — unclear how components communicate |

**How to assess:**
- Identify all system boundaries and interfaces in the HLD
- Check each interface for: protocol, data format, authentication method, error handling
- Verify data flow direction is explicit (which system initiates, which responds)
- Look for SLA/latency/throughput specifications where applicable
- Check for retry and failure handling strategies

#### 3.6 Operational Readiness

| Score | Criteria |
|---|---|
| **PASS** | Monitoring, alerting, deployment strategy, rollback plan, and operational runbook considerations are documented |
| **PARTIAL** | Some operational aspects are covered but the design lacks deployment or monitoring detail |
| **FAIL** | No operational considerations — the HLD focuses only on functional architecture |

**How to assess:**
- Check for monitoring and alerting strategy
- Look for deployment approach (blue/green, rolling, canary)
- Verify rollback/recovery procedures are considered
- Check for logging and observability mentions
- Look for capacity planning and scaling considerations
- Check for runbook or operational handover references

### Phase 4: Compile Findings

Categorise each finding by severity:

| Severity | Definition | Action Required |
|---|---|---|
| **BLOCKING** | Fundamental gap that must be resolved before the design can proceed to implementation | Rework required |
| **ADVISORY** | Gap that should be addressed but does not prevent progress | Address before go-live |
| **INFORMATIONAL** | Observation or suggestion for improvement | Consider in future iterations |

### Phase 5: Determine Review Status

Based on the dimension scores and finding severities:

| Status | When Applied |
|---|---|
| **APPROVED** | All dimensions PASS, no BLOCKING findings |
| **APPROVED WITH CONDITIONS** | No dimensions FAIL, but PARTIAL scores exist or ADVISORY findings need attention |
| **NEEDS REWORK** | Any dimension scores FAIL, or any BLOCKING findings exist |

### Phase 6: Generate Review Output

Output the review directly to the console. Use the template below.

---

## Output Template

```markdown
# HLD Review: [HLD Title]

**Reviewed:** [today's date]
**HLD Created:** [created date from frontmatter]
**Last Reviewed:** [reviewed date from frontmatter]
**Confidence:** [confidence from frontmatter]

---

## Review Status: [APPROVED / APPROVED WITH CONDITIONS / NEEDS REWORK]

---

## Scoring Summary

| Dimension | Score | Evidence | Gaps |
|---|---|---|---|
| ADR Coverage | [PASS/PARTIAL/FAIL] | [what ADRs exist and cover] | [what design choices lack ADRs] |
| Requirements Traceability | [PASS/PARTIAL/FAIL] | [requirements addressed] | [requirements not addressed] |
| Principle Compliance | [PASS/PARTIAL/FAIL] | [principles aligned with] | [principles not addressed or contradicted] |
| Security Architecture | [PASS/PARTIAL/FAIL] | [security measures documented] | [security aspects missing] |
| Integration Clarity | [PASS/PARTIAL/FAIL] | [interfaces documented] | [interfaces lacking detail] |
| Operational Readiness | [PASS/PARTIAL/FAIL] | [operational aspects covered] | [operational aspects missing] |

---

## Findings

### BLOCKING

[If none: "No blocking findings."]

1. **[Finding Title]** — [Description of the gap, which dimension it affects, and why it blocks progress]
   - **Dimension:** [affected dimension]
   - **Recommendation:** [specific action to resolve]

### ADVISORY

[If none: "No advisory findings."]

1. **[Finding Title]** — [Description and recommendation]
   - **Dimension:** [affected dimension]
   - **Recommendation:** [specific action to resolve]

### INFORMATIONAL

[If none: "No informational findings."]

1. **[Finding Title]** — [Observation or suggestion]

---

## Conditions

[Only include if status is APPROVED WITH CONDITIONS]

The following conditions must be addressed before implementation:

- [ ] [Condition 1 — specific, actionable item]
- [ ] [Condition 2]

---

## Context Analysed

### Linked ADRs
| ADR | Status | Relevance |
|-----|--------|-----------|
| [[ADR - Title]] | accepted | [how it relates to the HLD] |

### Architecture Principles Assessed
| Principle | Domain | Compliance |
|-----------|--------|------------|
| [[Concept - Principle Name]] | [domain] | [aligned/not addressed/contradicted] |

### Threat Coverage
| Threat | Severity | Mitigated? |
|--------|----------|------------|
| [[Threat - Name]] | [severity] | [yes/partial/no] |

### Systems Referenced
[List of System notes referenced in the HLD with their status]

---

## Next Steps

- [ ] [Action item based on findings — e.g., "Create ADR for Docker orchestration choice"]
- [ ] [Action item — e.g., "Add monitoring section to HLD"]
- [ ] [Action item — e.g., "Link Threat - Denial of Service and document mitigation"]
- [ ] Update HLD `reviewed` date to today
- [ ] Update HLD `verified` to `true` once conditions are met
```

---

## Examples

### Example 1: Quick Review

```
/hld-review HLD - Remote Vault Access Architecture
```

Reviews the HLD against all six dimensions, checking linked ADRs, vault principles, relevant threats, and operational completeness.

### Example 2: Review After ADR Changes

```
/hld-review HLD - SecureTransfer Azure Files to S3 Mirroring
```

Useful after new ADRs are accepted to verify the HLD still aligns with the latest decisions.

## Error Handling

- **HLD not found:** List all available HLD notes in the vault and ask the user to confirm
- **No linked notes:** Report that the HLD has an empty `relatedTo` field — this is itself a finding (ADVISORY: "HLD lacks cross-references to ADRs, systems, and requirements")
- **Graph index unavailable:** Fall back to Grep-based search for principles and threats
- **No principles found:** Note this as INFORMATIONAL — the vault may not yet have principle notes established

## Related Skills

- `/nfr-review` — Review an HLD against NFR requirements (complementary to this skill)
- `/diagram-review` — Analyse architecture diagrams for readability and quality
- `/adr` — Create new ADRs for design choices identified as gaps
- `/diagram` — Generate architecture diagrams referenced in the HLD
- `/impact-analysis` — Analyse the impact of changes to systems in the HLD

## Related Notes

- `.claude/rules/naming-conventions.md` — HLD naming patterns
- `.claude/context/frontmatter-reference.md` — HLD frontmatter schema
- `.claude/context/architecture.md` — Architecture governance context
