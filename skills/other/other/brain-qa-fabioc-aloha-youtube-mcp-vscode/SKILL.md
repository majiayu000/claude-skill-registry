---
name: "Brain QA"
description: "Semantic, logic, code, and architectural validation of Alex's cognitive architecture — not just file counts, but meaning coherence"
disable-model-invocation: true
applyTo: "**/*synapse*,**/*skill*,**/*trigger*"
---

# Brain QA

> Semantic, logic, code, and architectural validation of Alex's cognitive architecture — not just file counts, but meaning coherence

## Synapses

*Format: See `SYNAPSE-SCHEMA.md` for notation reference*

- [.github/instructions/semantic-audit.instructions.md] (High, Coordinates, Bidirectional) - "Procedural memory for manual semantic review that complements automated brain-qa"
- [.github/instructions/cognitive-health-validation.instructions.md] (Critical, Coordinates, Bidirectional) - "Comprehensive brain-qa integration with meditation and release workflows"
- [.github/skills/master-alex-audit/SKILL.md] (Medium, Related, Bidirectional) - "Full repository audit including brain-qa execution"
- [.github/instructions/dream-state-automation.instructions.md] (Medium, Complements, Forward) - "Dream validates synapses, brain-qa validates structure"
- [.github/instructions/release-management.instructions.md] (High, Gates, Forward) - "Pre-release validation requires brain-qa passing"

## Philosophy

Brain QA is a **mental exercise**, not just a muscle exercise. The script validates structure, but the skill's true value is teaching Alex *what to look for* beyond what scripts can automate.

Two scripts serve different contexts:

| Script | Context | Phases | Inheritance |
|--------|---------|--------|-------------|
| `brain-qa.ps1` | Master Alex | 31 (full) | master-only |
| `brain-qa-heir.ps1` | Heir deployments | 23 (heir-relevant) | inheritable |

During sync, `brain-qa-heir.ps1` is **renamed** to `brain-qa.ps1` in the heir, so all contexts use the same filename. The master version includes cross-repo sync phases (5, 7, 8, 13) and master-only validations (26-29) that don't apply to heirs.

| Dimension | Script Catches | Alex Catches (with this skill) |
|-----------|---------------|-------------------------------|
| **Structural** | Missing files, broken paths, count mismatches | ✅ Automated |
| **Semantic** | — | Terminology drift (e.g. "DK files" vs "skills"), meaning contradictions between documents |
| **Logic** | — | Process descriptions that conflict (e.g. dream says X, meditation says Y), impossible workflows |
| **Code** | Compile errors, lint | Code behavior diverging from documented claims (e.g. documented trigger not wired in TypeScript) |
| **Architectural** | — | Working memory model inconsistencies, neuroanatomical mappings that contradict instruction files |

**Rule**: When running brain-qa, always pair the script output with a semantic review. The script is the body; this skill is the brain.

## Quick Start

### Master Context
```powershell
# Full 31-phase audit
.github/muscles/brain-qa.ps1

# Quick validation (phases 1-6)
.github/muscles/brain-qa.ps1 -Mode quick

# Sync validation only (phases 5,7,8,13,14,15,27,28)
.github/muscles/brain-qa.ps1 -Mode sync

# Schema/frontmatter validation (phases 2,6,11,16,17)
.github/muscles/brain-qa.ps1 -Mode schema

# LLM-first content validation (phases 10,20,21)
.github/muscles/brain-qa.ps1 -Mode llm

# Specific phases
.github/muscles/brain-qa.ps1 -Phase 1,5,7

# Auto-fix sync issues
.github/muscles/brain-qa.ps1 -Mode sync -Fix
```

### Heir Context
```powershell
# Full heir audit (23 heir-relevant phases)
.github/muscles/brain-qa.ps1

# Quick validation (phases 1-4,6)
.github/muscles/brain-qa.ps1 -Mode quick

# Schema/frontmatter validation (phases 2,6,11,16,17)
.github/muscles/brain-qa.ps1 -Mode schema

# LLM content validation (phases 10,20,21)
.github/muscles/brain-qa.ps1 -Mode llm

# Note: -Mode sync is not available in heir (sync phases are master-only)
```

## When to Use

- Before releases (structural + semantic review)
- After adding/modifying skills (do new synapses make logical sense?)
- After bulk synapse updates (are connections semantically meaningful?)
- When trigger conflicts are suspected (logic: can two triggers fire contradictory protocols?)
- To verify Master-Heir parity (architectural: does heir behavior match master docs?)
- To validate LLM-friendly content formats
- **After any documentation refactor** — check that meaning didn't drift when words changed
- **When code and docs diverge** — documented feature doesn't match TypeScript implementation

## Audit Phases

| Phase  | Name                         | Validates                                     | Heir? |
| ------ | ---------------------------- | --------------------------------------------- | ----- |
| 1      | Synapse Target Validation    | All connection targets exist                  | Yes |
| 2      | Inheritance Field Validation | All skills have inheritance field             | Yes |
| 3      | Skill Index Coverage         | All skills in skill-activation index          | Yes |
| 4      | Trigger Semantic Analysis    | Overlapping keywords (warnings OK if related) | Yes |
| 5      | Master-Heir Skill Sync       | Skill directories match                       | No  |
| 6      | Synapse Schema Format        | Numeric strengths, $schema present            | Yes |
| 7      | Synapse File Sync            | synapses.json hash match                      | No  |
| 8      | Skill-Activation Index Sync  | SKILL.md hash match                           | No  |
| 9      | Catalog Accuracy             | SKILLS-CATALOG count matches reality          | Yes (count-only) |
| 10     | Core File Token Budget       | Size + ASCII art checks on core files         | Yes |
| 11     | Boilerplate Descriptions     | No placeholder skill descriptions             | Yes |
| 12     | Heir Reset Validation        | Empty profile, available P5-P7 slots          | Yes |
| 13     | Instructions/Prompts Sync    | Memory files synced to heir                   | No  |
| 14     | Agents Structure             | Valid agent files in both                     | Yes |
| 15     | Config Files                 | Required configs present, no leaks            | Yes |
| 16     | Skill YAML Frontmatter       | name and description in frontmatter           | Yes |
| 17     | Internal Skills Hidden        | user-invokable: false for metacognition       | Yes |
| 18     | Agent Handoffs                | Return-to-Alex handoffs present               | Yes |
| 19     | ApplyTo Patterns              | Instructions have file-type patterns          | Yes |
| 20     | LLM-First Content             | No ASCII art, Mermaid OK                      | Yes |
| 21     | Emoji Semantics               | Meaningful emoji usage stats                  | Yes |
| 22     | Episodic Archive Health       | .github/episodic/ session records valid       | Yes |
| 23     | Assets Validation             | .github/assets/ contains expected files       | Yes |
| 24     | Issue/PR Templates            | GitHub templates present and valid            | Yes |
| 25     | Root File Completeness        | Required .github/ root files exist            | Yes |
| 26     | alex_docs Freshness           | Documentation not stale beyond threshold      | No  |
| 27     | M365 Heir Validation          | M365 heir structure and version alignment     | No  |
| 28     | Codespaces Heir Validation    | Codespaces devcontainer and config valid      | No  |
| 29     | Global Knowledge Sync         | GK repo index and counts consistent           | No  |
| 30     | Muscles Integrity             | All scripts referenced by trifectas exist     | Yes |
| 31     | ROADMAP Version Alignment     | ROADMAP versions match package.json           | Yes (config-only) |

## Mode Shortcuts

| Mode     | Phases              | Use Case                                   |
| -------- | ------------------- | ------------------------------------------ |
| `all`    | 1-31                | Full audit before release                  |
| `quick`  | 1-6                 | Fast validation during development         |
| `sync`   | 5,7,8,13-15,27,28   | Master-Heir synchronization check          |
| `schema` | 2,6,11,16,17        | Schema, frontmatter, and format validation |
| `llm`    | 10,20,21            | LLM-first content format validation        |
| `ghfolder`| 22-25              | .github/ subfolder health                  |
| `full`   | 26-31               | External folders + cross-repo validation   |

## Known Gaps (Future Phases)

| Phase | Name                   | Validates                                                                                                            |
| ----- | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 22    | Brain HTML Count Drift | Hardcoded counts in `docs/alex-brain-anatomy.html` match actual file counts (skills, instructions, muscles, prompts) |
| 23    | Motor Cortex Mapping   | Muscle inventory in brain diagrams matches `.github/muscles/`                                                        |

> **Context**: Session 2026-02-13 discovered stale counts in brain HTML (muscles 13→11, procedures 29→28, skills 100+→116). Diagrams with hardcoded numbers will drift after any architecture change.

## Common Issues

| Issue                    | Fix                                                        |
| ------------------------ | ---------------------------------------------------------- |
| Broken synapse target    | Update path in synapses.json                               |
| Missing inheritance      | Add `"inheritance": "inheritable"` to synapses.json        |
| Out of sync              | Run with `-Fix` or use `build-extension-package.ps1`       |
| Boilerplate description  | Write meaningful description in SKILL.md frontmatter       |
| Master-only leak         | Remove protected files from heir                           |
| Missing YAML frontmatter | Add `---\nname:\ndescription:\n---` to SKILL.md            |
| ASCII art warning        | Replace with Mermaid diagrams or tables                    |
| Missing return-to-Alex   | Add handoff to main Alex agent                             |
| Brain HTML count drift   | Update hardcoded numbers in `docs/alex-brain-anatomy.html` |
| Incomplete synapse path  | Use full path: `.github/skills/name/SKILL.md` not `name`  |
| Missing $schema property | Add `"$schema": "../SYNAPSE-SCHEMA.json"` to synapses.json |
| Master-heir ref mismatch | Remove master-only files (ROADMAP-UNIFIED.md) from heir    |

## Iterative Validation Workflow

When repairing architecture issues, use this proven pattern:

```
1. Audit → Run brain-qa phase to identify errors
2. Fix Errors → Address primary issues (paths, references)
3. Re-validate → Run same phase to verify fixes
4. Fix Schema → Address structural issues ($schema, inheritance)
5. Final Check → Run quick mode to verify all phases pass
```

**Example from 2026-02-15 session:**
- Phase 1 failed → Fixed incomplete synapse paths → Phase 1 passed
- Phase 6 failed → Added $schema properties → Phase 6 passed
- Phase 7 warned about sync differences → Expected after manual edits, auto-resolves at publish

**Key principle:** Iterative validation catches cascading errors before they compound. Each phase builds on previous fixes.

## Semantic Review Checklist (Manual — Not Scriptable)

After running the script, Alex should check:

- [ ] **Cross-document meaning**: Do copilot-instructions, alex-core, and protocol-triggers describe the same processes consistently?
- [ ] **Working memory model**: Does the 4+3 slot claim match the actual P1-P7 table? Are sub-slots (P4a-d) accounted for?
- [ ] **Legacy terminology**: Any surviving references to deprecated concepts (DK files, domain-knowledge folders)?
- [ ] **Trigger-to-code alignment**: Do synapse trigger keywords in .md files match actual activation paths in TypeScript?
- [ ] **Heir evolution logic**: Does the documented 4-step heir cycle match what heir-skill-promotion.instructions.md actually describes?
- [ ] **Version source of truth**: Is `package.json` the single source, or are versions hardcoded in prose that will drift?
- [ ] **Neuroanatomical consistency**: Do brain-analog mappings in copilot-instructions match descriptions in alex-core?

## Integration

- **Dream Protocol**: Run brain-qa after dream for deeper analysis
- **Release Preflight**: Include `-Mode quick` in release checks
- **LLM Content Audit**: Run `-Mode llm` when updating diagrams
- **Skill Selection Optimization**: Brain QA validates SSO data sources
- **Semantic Audit**: Pair script output with manual checklist above — script validates structure, Alex validates meaning

## Triggers

- "brain qa", "brain audit", "validate brain"
- "synapse audit", "deep synapse check"
- "master heir sync", "heir sync validation"
- "catalog validation", "instruction sync"
- "semantic audit", "logic check", "meaning consistency"
- "code-to-docs alignment", "architectural review"

---

_Script: `.github/muscles/brain-qa.ps1`_
