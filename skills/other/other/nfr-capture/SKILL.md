---
name: nfr-capture
skill: nfr-capture
description: Generate pre-populated NFR table for a system's HLD based on tier and project type
context: fork
arguments:
  - name: system
    description: System name (e.g., "ERPSystem", "DataPlatform", "AlertHub")
    required: true
  - name: tier
    description: CS tier (CS1-CS4) — if omitted, skill will ask or run scoping questionnaire
    required: false
  - name: types
    description: Comma-separated project types (all,pci,gdpr,caa_nis) — if omitted, skill will ask
    required: false
  - name: output
    description: Output format — "markdown" (default), "confluence" (wiki markup), "jira" (for epic creation)
    required: false
  - name: flags
    description: Comma-separated flags — "with-evidence-prompts" (include AI draft prompts per NFR), "from-hld:<page-id>" (pre-fill evidence from existing HLD)
    required: false
model: opus
---

# /nfr-capture

Generate a pre-populated NFR requirements table for a system's HLD, filtered by classification tier and project type. Reads from the NFR-as-Code YAML single source of truth.

## Usage

```
/nfr-capture ERPSystem
/nfr-capture ERPSystem CS2
/nfr-capture "AlertHub" CS1 all,gdpr
/nfr-capture DataPlatform CS2 all,pci,gdpr confluence
/nfr-capture ERPSystem CS2 all,gdpr markdown with-evidence-prompts
/nfr-capture ERPSystem CS2 all,gdpr markdown from-hld:664765269
```

## Data Source

All NFR data is read from `.claude/data/nfr-reference.yaml` — the single source of truth for all 66 NFRs. Do NOT hard-code NFR content; always read from the YAML.

## Instructions

### Phase 1: Read NFR Data

1. **Read** `.claude/data/nfr-reference.yaml`
2. Parse the YAML to extract all sections, NFRs, scoping questions, and archetypes
3. Note the classification tiers from `classification_tiers`

### Phase 2: Determine System Classification

**Option A: Direct arguments** — If `tier` and `types` are provided, use them.

**Option B: Scoping questionnaire** — If arguments are omitted, offer the user a choice:

1. **Quick scoping** — ask the 6 plain-English questions from `scoping_questions` in the YAML. Map answers to tier and types using the `maps_to` fields.
2. **Archetype selection** — show the archetypes from `archetypes` in the YAML and let the user pick one.
3. **Manual selection** — show the tier/type selection tables (original behaviour).

If only `tier` is omitted, show the tier selection table:

```
What is the Criticality / Service Level tier for [system]?

| Tier | Criticality | Availability | RTO | RPO |
|------|-------------|-------------|-----|-----|
| CS1/SL1 | Critical | 99.95% | 4 hours | Zero data loss |
| CS2/SL2 | High | 99.50% | 8 hours | 1 hour |
| CS3/SL3 | Medium | 99.00% | 5 working days | 1 day |
| CS4/SL4 | Low | 98.50% | 10 working days | 5 days |
```

If only `types` is omitted, show the type selection:

```
Which project types apply to [system]? (select all that apply)

- [ ] All Projects (mandatory baseline)
- [ ] PCI — system handles payment card data
- [ ] GDPR — system processes personal data of UK/EEA subjects
- [ ] CAA/NIS — system supports essential aviation services
```

**Note:** "All Projects" should always be selected as it is the mandatory baseline.

### Phase 3: Filter NFRs

Using the selected tier and project types:

1. **Include sections** where the section's `applicability` overlaps with the selected project types:
   - Sections with `applicability: [all]` are always included
   - Sections with `applicability: [pci]` only included if PCI is selected
   - Sections with `applicability: [gdpr]` only included if GDPR is selected
   - Sections with `applicability: [caa_nis]` only included if CAA/NIS is selected
   - Some sections have multiple applicability values (e.g., `[all, pci, gdpr, caa_nis]`) — include if ANY match

2. **Map CS tier to SL tier**: CS1→SL1, CS2→SL2, CS3→SL3, CS4→SL4

3. **Pre-fill tier values** for tiered NFRs using the selected SL tier's `tier_values`

### Phase 3b: Pre-fill from HLD (if `from-hld:<page-id>` flag)

If the `from-hld` flag is present:

1. **Fetch the HLD page** from Confluence using Atlassian MCP `getConfluencePage` with the given page ID
2. **Parse the HLD content** to identify sections that map to NFR requirements
3. **For each applicable NFR**, search the HLD content for evidence that addresses the requirement:
   - Look for mentions of: encryption configuration, IAM/RBAC setup, backup policies, monitoring stack, VPC/network design, scaling approach, DR strategy, data handling, compliance controls
   - Use keyword matching against the NFR's `requirement`, `guidance`, and `aws_services` fields
4. **Pre-populate the evidence column** with extracted content and source attribution:
   - Format: `"Pre-filled from HLD page [ID], section [name]: [extracted evidence]"`
5. **Mark remaining empty cells** for manual completion

### Phase 4: Generate Output

Generate the NFR table in the requested format (default: markdown).

#### Markdown Output

For each applicable section, generate:

```markdown
### [Section Name]

> **Purpose:** [section.purpose]
>
> **Compliance:** [section.compliance_frameworks joined]
>
> **Applicability:** [section.applicability_notes]

**Tier Targets ([CS tier] / [SL tier]):**

[If section has tier_guidance, render the selected tier's values as a summary table]

| NFR ID | Requirement | Target ([SL tier]) | Verification / Evidence | Status |
|--------|------------|---------------------|------------------------|--------|
| [nfr.id] | [nfr.title]: [nfr.requirement] | [tier_values for SL tier if tiered, else "See guidance"] | _[nfr.evidence_guidance]_ | |
```

**Important formatting rules:**
- Tier-specific values in the "Target" column should show the actual value for the selected tier, not all tiers
- Evidence guidance should be in italics as prompts for the team to fill in
- Status column is empty — teams fill this in (Met / Partial / Not Met / N/A)
- Include section intro boxes (purpose, compliance, applicability) as blockquotes
- If a section has tier_guidance at the section level, include a summary of the selected tier's values

#### With Evidence Prompts (`with-evidence-prompts` flag)

When this flag is present, add an additional column or section per NFR with an **AI Evidence Prompt** — a structured template the team can use to draft their evidence statement.

For each NFR, generate a prompt block after the table row:

```markdown
<details>
<summary>AI Evidence Prompt for [NFR-ID]</summary>

**To draft evidence for this NFR, describe:**
- [Specific questions based on evidence_guidance field]
- [For automated evidence_type]: Which AWS Config rules or CLI commands can verify this? (See nfr-evidence-rules.yaml)
- [For manual evidence_type]: What documents, diagrams, or procedures demonstrate compliance?

**Example evidence statement:**
> [Generate a realistic example based on the NFR's requirement and evidence_guidance, using the system name and tier context]

</details>
```

For NFRs with `evidence_type: automated`, also include the specific AWS checks from `.claude/data/nfr-evidence-rules.yaml`:

```markdown
**Automated checks available:**
- [check description]: `[command or config rule]`
```

#### Confluence Output

If `output` is `confluence`, generate Confluence wiki markup instead of markdown:
- Use `||` for header rows and `|` for data rows
- Use `{info}` macros for section intro boxes
- Use `{status}` macros for the Status column placeholders
- Include `{page-properties}` block at the top (see Phase 4b)

#### Confluence Page Properties (always included in Confluence output)

Add a `{page-properties}` block at the top of Confluence output:

```
{page-properties}
| NFR Status | Draft |
| NFR Tier | [CS tier] |
| NFR Sections Applicable | [included] of 13 |
| NFR Completion | 0/[total] (0%) |
| NFR Last Reviewed | [today's date] |
{page-properties}
```

This enables estate-wide dashboards via Confluence `{page-properties-report}`.

#### Jira Output

If `output` is `jira`, generate a structured list suitable for creating a Jira Epic:
- Epic: "NFR Compliance — [System Name] ([CS tier])"
- One story per NFR with:
  - Summary: "[NFR ID] — [NFR title]"
  - Description: requirement text + guidance + evidence guidance
  - Labels: nfr, [section-id lowercase]
  - Priority mapped from tier (CS1→Critical, CS2→High, CS3→Medium, CS4→Low)

### Phase 5: Write Output

1. **Console output** (default): Print the generated table to the terminal
2. **If the user requests**, write to a vault note:
   - Location: Root directory
   - Filename: `Concept - NFR Capture - [System Name].md`
   - Include proper frontmatter:

```yaml
---
type: Concept
title: "NFR Capture - [System Name]"
created: [today]
modified: [today]
tags:
  - activity/governance
  - activity/architecture
  - domain/engineering
confidence: high
freshness: current
source: synthesis
verified: false
reviewed: [today]
keywords: [nfr, nfr-capture, [system-name lowercase]]
relatedTo:
  - "[[Pattern - NFR Standards and Governance]]"
---
```

3. **Optionally push to Confluence** using Atlassian MCP tools:
   - Use `createConfluencePage` to create as child of system's HLD page
   - Only if user explicitly requests Confluence push

## Output Summary

After generating the table, print a summary:

```
NFR Capture Summary for [System Name] ([CS tier]/[SL tier])
- Sections included: [count] of 13
- NFRs included: [count] of 66
- Sections excluded: [list excluded section names with reason]
- Tiered NFRs: [count] with [SL tier] values pre-filled
- Evidence types: [count automated] automated, [count manual] manual
- Pre-filled from HLD: [count] NFRs (if from-hld flag used)
- Evidence prompts: included (if with-evidence-prompts flag used)
```

## Related

- `.claude/data/nfr-reference.yaml` — NFR single source of truth
- `.claude/data/nfr-evidence-rules.yaml` — Automated AWS evidence checks for 37 NFRs
- `.claude/skills/nfr-review/SKILL.md` — Gap analysis against existing HLDs
- `.claude/skills/nfr-jira-epic/SKILL.md` — Create Jira Epic with stories per NFR
- `Pattern - NFR Standards and Governance` — Tiered framework context
- `Pattern - NFR Compliance Evidence Best Practices` — Evidence patterns
