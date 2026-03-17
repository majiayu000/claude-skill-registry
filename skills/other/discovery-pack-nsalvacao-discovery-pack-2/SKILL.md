---
name: discovery-pack
description: Complete project discovery workflow using Jobs-to-be-Done, Amazon PR/FAQ, ADR, and Lean Startup validation. Transforms ambiguous ideas into structured specifications ready for implementation. Activate when user mentions "discovery", "requirements discovery", "project framing", "validate assumptions", "JTBD analysis", or before starting implementation of unclear ideas.
license: MIT
metadata:
  author: nsalvacao
  version: "2.0.0"
  requires: "Python 3.11+ for optional automation scripts"
  changelog:
    - "2.0.0: Flat architecture consolidation, cross-agent portability, schema-template sync, progressive disclosure"
    - "1.1.0: Enhanced mode selection enforcement, output directory fallback strategy, automation workflow"
    - "1.0.0: Initial release"
---

# Discovery Pack Workflow

Structured project discovery using proven methodologies (JTBD, Amazon PR/FAQ, ADR, Lean Startup, DDD). Transforms ambiguous ideas into clear, validated specifications ready for spec-kit handoff.

## Quick Start

**Activation Triggers**: "discovery", "requirements discovery", "project framing", "validate assumptions", "JTBD analysis"

**Two Modes**:
- **Lite** (3 artifacts, 15-30 min): Small projects, <5 people, low risk, personal/startup
- **Full** (8 artifacts, 1-2 hours): Enterprise, compliance, security-critical, high risk

**Pre-Flight Check**:
```bash
bash scripts/pre-flight-check.sh <output-dir> <mode>
```

## Core Methodologies

| Methodology | Purpose | Applied In |
|-------------|---------|------------|
| **Jobs-to-be-Done (JTBD)** | User motivation & context | Problem framing (00) |
| **Amazon PR/FAQ** | Customer clarity | Problem framing (00) |
| **ADR** | Decision rationale | Decision log (06) |
| **Lean Startup** | Assumption validation | Validation plan (05) |
| **DDD** | Domain language | Domain model (02) |

📖 Details: `shared-references/methodologies.md`, `shared-references/glossary.md`

## Installation & Paths

**Supported Locations**:
- `~/.copilot/skills/discovery-pack/` (GitHub Copilot CLI)
- `~/.claude/skills/discovery-pack/` (Claude Code)
- `.claude/skills/discovery-pack/` (project-local)
- Any custom location (relative path resolution)

**Script Invocation**:
```bash
# From skill root:
python3 scripts/validate.py <output-dir>

# From anywhere:
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py <output-dir>
```

All scripts use relative path resolution (`Path(__file__)` / `${BASH_SOURCE[0]}`).

---

## Workflow Orchestration

### Step 1: Mode Selection (MANDATORY)

🛑 **ALWAYS ask first**:

| Mode | Artifacts | Time | Best For |
|------|-----------|------|----------|
| **lite** | 3 (00, 03, 07) | 15-30 min | Small projects, low risk, <5 people |
| **full** | 8 (00-07) | 1-2 hours | Enterprise, compliance, high risk |

**Decision Tree**:
- Enterprise/regulated/security-critical? → **full**
- Multi-team/multi-stakeholder? → **full**
- Personal/startup/prototype? → **lite**
- Unsure? → **lite** (can upgrade later)

**Automation Check**:
```bash
# Optional but recommended (30-40% token savings)
pip install -r scripts/requirements.txt
```

### Step 2: Output Directory

**Target**: `<project-root>/docs/discovery/YYYY-MM-DD-<topic-slug>`

**Examples**:
- `/docs/discovery/2026-01-07-user-auth`
- `/docs/discovery/2026-01-07-api-redesign`

**Auto-create if missing** (scripts handle this).

### Step 3: Execute Workflow

**Progressive Disclosure Strategy**: Load detailed workflow only when starting execution.

#### 🔵 Lite Mode (3 artifacts)

**Workflow File**: `shared-references/workflows/lite-mode.md`

**Quick Overview**:
1. **Problem Framing** (00) → Load `templates/00_problem-frame.md`, fill YAML, validate
2. **Option Analysis** (03) → Load `templates/03_option-space.md`, compare 2+ options, recommend
3. **Handoff** (07) → Load `templates/07_speckit-handoff.md`, prepare spec-kit input

**Load detailed instructions**: Read `shared-references/workflows/lite-mode.md` before starting Phase 1.

#### 🟣 Full Mode (8 artifacts)

**Workflow File**: `shared-references/workflows/full-mode.md`

**Quick Overview**:
1. **Problem Framing** (00) → Foundation
2. **Constraints** (01) → Security, performance, observability boundaries
3. **Domain Model** (02) → Entities, bounded contexts, ubiquitous language
4. **Option Analysis** (03) → Alternatives comparison
5. **Assumptions** (04) → **Auto-generated** via `extract_assumptions.py`
6. **Validation Plan** (05) → Experiments to test assumptions
7. **Decision Log** (06) → ADR format decisions
8. **Handoff** (07) → Spec-kit integration

**Load detailed instructions**: Read `shared-references/workflows/full-mode.md` before starting Phase 1.

### Step 4: Validation Gate (MANDATORY)

🛑 **After artifact generation**:

```bash
python3 scripts/validate.py <output-dir>
```

**Expected Output**:
```
✅ 00_problem-frame.md: Valid
✅ 03_option-space.md: Valid
✅ 07_speckit-handoff.md: Valid
📊 Summary: 3/3 artifacts valid (100%)
```

**If validation fails**:
1. Read error message (shows file + field + expected format)
2. Fix YAML frontmatter (common: missing fields, wrong types, invalid enums)
3. Re-validate until 100% pass

**No progression without 100% validation pass** (schema compliance mandatory).

---

## Artifact Reference

| ID | Name | Lite | Full | Auto | Template |
|----|------|------|------|------|----------|
| 00 | Problem Frame | ✓ | ✓ | - | `templates/00_problem-frame.md` |
| 01 | Constraints & NFRs | - | ✓ | - | `templates/01_constraints-nfr.md` |
| 02 | Domain Model | - | ✓ | - | `templates/02_domain-model.md` |
| 03 | Option Space | ✓ | ✓ | - | `templates/03_option-space.md` |
| 04 | Assumptions | - | ✓ | ✓ | Auto via `extract_assumptions.py` |
| 05 | Validation Plan | - | ✓ | - | `templates/05_validation-plan.md` |
| 06 | Decision Log | - | ✓ | - | `templates/06_decision-log.md` |
| 07 | Spec-Kit Handoff | ✓ | ✓ | - | `templates/07_speckit-handoff.md` |

**Template Loading**: Load template **only** when generating that specific artifact (progressive disclosure).

---

## Automation Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `scripts/pre-flight-check.sh` | Validate environment | Before starting workflow |
| `scripts/discovery-pack-run.sh` | Full workflow executor | Automated end-to-end execution |
| `scripts/validate.py` | Schema validation | After each artifact / end of workflow |
| `scripts/extract_assumptions.py` | Generate 04 from 00-03 | Full mode, after 00-03 complete |
| `scripts/ci-validate.sh` | CI/CD integration | Automated validation in pipelines |

**Token Savings**: Automation provides ~30-40% token reduction vs manual execution.

---

## Quality Gates

### Pre-Flight Requirements
- [ ] Mode selected (lite/full)
- [ ] Output directory determined
- [ ] Python 3.11+ available (if using automation)
- [ ] Templates accessible via relative paths

### Artifact Quality
- [ ] 100% schema validation pass
- [ ] All required YAML fields present
- [ ] Epistemic tags used ([ASSUMPTION], [HYPOTHESIS], [CONSTRAINT])
- [ ] Cross-references between artifacts (e.g., 05 links to 04 assumption IDs)

### Handoff Criteria
- [ ] All planned artifacts generated
- [ ] Validation passes 100%
- [ ] 07_speckit-handoff.md marks `ready_for_speckit: true`
- [ ] Stakeholder review complete

---

## Token Optimization

**Progressive Disclosure Pattern**:
1. Load workflow file **only** when starting execution (not upfront)
2. Load template **only** when generating that artifact
3. Load methodology details **only** when user asks clarifying questions
4. Use automation scripts (reduces 30-40% tokens)

**Target Token Budget**:
- Lite mode: ≤15k tokens
- Full mode: ≤25k tokens

**High Token Operations** (avoid unless necessary):
- Reading all templates upfront
- Inline methodology explanations (use references)
- Verbose examples (use workflow files)

---

## Troubleshooting

### Validation Errors

| Error Type | Symptom | Fix |
|------------|---------|-----|
| Missing field | `Missing required field: X.Y.Z` | Add field to YAML frontmatter |
| Type mismatch | `Expected array, got object` | Convert format (e.g., single → list) |
| Invalid enum | `Value not in enum: [...]` | Use valid enum value from error |
| YAML syntax | `could not parse YAML` | Check indentation, colons, quotes |

### Common Issues

**Scripts not found**:
- Verify working directory (should be skill root)
- Or use full path: `~/.copilot/skills/discovery-pack/scripts/...`

**Automation unavailable**:
- Install dependencies: `pip install -r scripts/requirements.txt`
- Or proceed manually (workflow files guide you)

**Template loading fails**:
- Check `templates/` directory exists relative to skill root
- Verify path resolution working (run `scripts/pre-flight-check.sh`)

---

## Next Steps After Discovery

1. **Review artifacts** with stakeholders
2. **Execute validation experiments** from 05_validation-plan.md (if full mode)
3. **Start spec-kit workflow**: Use 07_speckit-handoff.md as input to `/speckit.constitution`
4. **Discovery complete** → Proceed to specification phase

---

## Version History

- **2.0.0** (2026-01-07): Flat architecture (1 SKILL.md), cross-agent portability, 100% schema validation
- **1.1.0** (2026-01-06): Enhanced enforcement, automation workflow
- **1.0.0** (2026-01-05): Initial release with 8 sub-skills

## Support & References

- **Methodologies**: `shared-references/methodologies.md`
- **Glossary**: `shared-references/glossary.md`
- **Lite Workflow**: `shared-references/workflows/lite-mode.md`
- **Full Workflow**: `shared-references/workflows/full-mode.md`
- **Schemas**: `schemas/*.schema.json`
- **Templates**: `templates/*.md`
