---
name: nist-cybersecurity-skills
description: >
  Comprehensive NIST cybersecurity framework reference covering SP 800-53 Rev 5
  (security/privacy controls), SP 800-171 (CUI protection), CSF 2.0
  (Cybersecurity Framework), SP 800-53A (assessment procedures), SP 800-37 (RMF),
  SP 800-207 (Zero Trust), SP 800-30 (risk assessment), SP 800-61 (incident
  response), SP 800-63 (digital identity), SP 800-161 (supply chain), and FIPS
  standards. Use when working with NIST controls, compliance, FedRAMP baselines,
  security assessments, or cybersecurity frameworks.
license: MIT
metadata:
  author: ethanolivertroy
  version: "1.1.0"
  source_dataset: ethanolivertroy/nist-cybersecurity-training
---

# NIST Cybersecurity Skills

Unified reference for NIST cybersecurity frameworks, controls, and standards.

## Framework Routing

Use this table to determine which reference file to load based on the user's question.

| User Intent | Framework | Reference Path |
|---|---|---|
| Security/privacy controls, control families, control baselines | SP 800-53 Rev 5 | `references/800-53/` |
| Protecting Controlled Unclassified Information (CUI), CMMC | SP 800-171 Rev 3 | `references/800-171/` |
| Assessment procedures, control testing, evidence | SP 800-53A Rev 5 | `references/800-53a/` |
| Cybersecurity Framework, CSF functions, categories, subcategories | CSF 2.0 | `references/csf/` |
| Risk Management Framework, authorization, ATO | SP 800-37 Rev 2 | `references/800-37/` |
| Zero Trust Architecture, ZTA | SP 800-207 | `references/800-207/` |
| Risk assessment, threat modeling | SP 800-30 Rev 1 | `references/800-30/` |
| Incident response, handling, reporting | SP 800-61 Rev 3 | `references/800-61/` |
| Digital identity, authentication, identity proofing | SP 800-63 Rev 4 | `references/800-63/` |
| Supply chain risk management, C-SCRM | SP 800-161 Rev 1 | `references/800-161/` |
| Cryptographic modules, security categorization, minimum security | FIPS | `references/fips/` |
| Cross-framework mappings, baselines, control relationships | Cross-References | `references/cross-references/` |
| Definitions, terms, acronyms | Glossary | `references/glossary.md` |

## SP 800-53 Rev 5 — Control Families Quick Reference

These are the 20 control families. Each has a dedicated reference file.

| Code | Family | File | Controls |
|---|---|---|---|
| AC | Access Control | `references/800-53/ac.md` | AC-1 through AC-25 |
| AT | Awareness and Training | `references/800-53/at.md` | AT-1 through AT-6 |
| AU | Audit and Accountability | `references/800-53/au.md` | AU-1 through AU-16 |
| CA | Assessment, Authorization, and Monitoring | `references/800-53/ca.md` | CA-1 through CA-9 |
| CM | Configuration Management | `references/800-53/cm.md` | CM-1 through CM-14 |
| CP | Contingency Planning | `references/800-53/cp.md` | CP-1 through CP-13 |
| IA | Identification and Authentication | `references/800-53/ia.md` | IA-1 through IA-13 |
| IR | Incident Response | `references/800-53/ir.md` | IR-1 through IR-10 |
| MA | Maintenance | `references/800-53/ma.md` | MA-1 through MA-7 |
| MP | Media Protection | `references/800-53/mp.md` | MP-1 through MP-8 |
| PE | Physical and Environmental Protection | `references/800-53/pe.md` | PE-1 through PE-23 |
| PL | Planning | `references/800-53/pl.md` | PL-1 through PL-11 |
| PM | Program Management | `references/800-53/pm.md` | PM-1 through PM-32 |
| PS | Personnel Security | `references/800-53/ps.md` | PS-1 through PS-9 |
| PT | PII Processing and Transparency | `references/800-53/pt.md` | PT-1 through PT-8 |
| RA | Risk Assessment | `references/800-53/ra.md` | RA-1 through RA-10 |
| SA | System and Services Acquisition | `references/800-53/sa.md` | SA-1 through SA-23 |
| SC | System and Communications Protection | `references/800-53/sc.md` | SC-1 through SC-51 |
| SI | System and Information Integrity | `references/800-53/si.md` | SI-1 through SI-23 |
| SR | Supply Chain Risk Management | `references/800-53/sr.md` | SR-1 through SR-12 |

## CSF 2.0 — Functions Quick Reference

| Function | Code | File | Focus |
|---|---|---|---|
| Govern | GV | `references/csf/govern.md` | Organizational context, strategy, policy, roles, oversight |
| Identify | ID | `references/csf/identify.md` | Asset management, risk assessment, improvement |
| Protect | PR | `references/csf/protect.md` | Access control, training, data security, platform security |
| Detect | DE | `references/csf/detect.md` | Continuous monitoring, adverse event analysis |
| Respond | RS | `references/csf/respond.md` | Incident management, analysis, mitigation, reporting |
| Recover | RC | `references/csf/recover.md` | Recovery planning, execution, communication |

## Common Tasks

### Find controls for a specific topic
1. Identify the relevant control family from the table above
2. Load the family reference file (e.g., `references/800-53/ac.md` for Access Control)
3. Search for the specific control by ID or keyword

### Compare FedRAMP baselines
1. Load `references/cross-references/baselines.md`
2. Look up Low, Moderate, or High baseline control selections
3. Cross-reference with specific control family files for details

### Map 800-53 controls to CSF
1. Load `references/cross-references/800-53-to-csf.md`
2. Find the CSF function/category of interest
3. See which 800-53 controls implement that category

### Map 800-53 to 800-171
1. Load `references/cross-references/800-53-to-800-171.md`
2. Find the 800-53 control of interest
3. See the corresponding 800-171 requirement (if any)

### Look up related controls
1. Load the family reference file (e.g., `references/800-53/ac.md`)
2. Each non-withdrawn control has a `**Related Controls:**` line listing cross-references
3. These are sourced from the authoritative NIST OSCAL catalog

### Check baseline applicability
1. Each non-withdrawn control has a `**Baselines:**` line showing Low, Moderate, and/or High
2. For a full listing: `python scripts/lookup.py baseline moderate` (or `low`, `high`)
3. Filter by family: `python scripts/lookup.py baseline moderate AC`
4. See also `references/cross-references/baselines.md` for FedRAMP details

### Map CSF 2.0 to 800-53 controls
1. By function: `python scripts/lookup.py map csf PR` (shows all Protect mappings)
2. By category: `python scripts/lookup.py map csf PR.AA` (shows specific category)
3. Or load `references/cross-references/800-53-to-csf.md` directly

### Look up assessment procedures
1. Identify the control from 800-53
2. Load the corresponding family file under `references/800-53a/`
3. Find the assessment objectives and methods

### Understand a NIST term
1. Load `references/glossary.md`
2. Search for the term alphabetically

## Cross-Framework Relationships

```
CSF 2.0 (strategic)
  └── SP 800-37 (RMF process)
       └── SP 800-53 Rev 5 (controls catalog)
            ├── SP 800-53A Rev 5 (assessment procedures)
            ├── SP 800-171 Rev 3 (CUI subset → CMMC)
            ├── SP 800-30 (risk assessment for control selection)
            └── FedRAMP Baselines (Low/Moderate/High selections)

Supporting Publications:
  ├── SP 800-207 (Zero Trust Architecture)
  ├── SP 800-61 (Incident Response)
  ├── SP 800-63 (Digital Identity)
  ├── SP 800-161 (Supply Chain Risk)
  └── FIPS 140-3, 199, 200 (foundational standards)
```

## Usage Notes

- **Control IDs** follow the pattern: `{FAMILY}-{NUMBER}` (e.g., AC-2, SI-4)
- **Enhancements** append a parenthetical: `AC-2(1)`, `SI-4(5)`
- **Baselines**: Low ⊂ Moderate ⊂ High (each higher baseline includes all controls from lower ones). Each control in 800-53 files has a `**Baselines:**` tag showing which baselines include it.
- **Related Controls**: Every non-withdrawn control has a `**Related Controls:**` line sourced from the NIST OSCAL catalog.
- **800-171** requirements map to a subset of 800-53 Moderate baseline controls
- **CSF categories** use dot notation: `GV.OC-01`, `PR.AC-01`
- **OSCAL** (Open Security Controls Assessment Language) provides machine-readable versions of these frameworks

## Data Sources

Reference content is derived from:
- **Dataset**: `ethanolivertroy/nist-cybersecurity-training` (530,912 structured examples from 596 NIST publications)
- **Raw PDFs**: `ethanolivertroy/nist-publications-raw` (596 PDFs, 2 GB)
- **NIST OSCAL**: Official machine-readable catalogs for 800-53, 800-171, and FedRAMP baselines
