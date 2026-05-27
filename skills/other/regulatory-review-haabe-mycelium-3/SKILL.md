---
name: regulatory-review
description: "Use to assess regulatory applicability for products that may fall under AI regulation (EU AI Act, Article 50 transparency)."
metadata:
  instruction_budget: "42"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Regulatory Review Skill

Assess whether the product falls under AI regulation and identify compliance requirements.

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it.

**Edit vs Write — different cost profiles** (verified 2026-05-14):
- **`Edit`** (exact-string replacement): `Read` with `limit: 1` satisfies the check at ~50 tokens. State-tracking is per-file, not per-byte — subsequent `Edit` calls work anywhere in the file. Use this for partial updates against large canvas files (e.g., `purpose.yml` at 800+ lines).
- **`Write`** (full replacement): do a **full Read** first. Write obliterates the file; you should see what you're about to replace. The `limit:1` shortcut is *not* appropriate here.

**ID-bearing entries — scan the ID space before assigning** (added 2026-05-15, v0.23.19): When adding a new component, opportunity, solution, or any other ID-bearing entry to a canvas file, run a Bash grep first to confirm the next ID in your prefix sequence is actually free:

```
grep "^  - id: <prefix>-" .claude/canvas/<file>.yml | sort -u
```

Replace `<prefix>` with the canvas's ID prefix (`comp` for landscape, `opp` for opportunities, `sol` for solutions, `ht` for human-tasks, etc.). Then pick the next free integer. `validate_canvas.py` has a duplicate-ID check (lines 230-239) that catches the failure on CI, but a duplicate can persist in the working tree for days if CI isn't run between edit and discovery — see roadmap-repo `corrections.md` 2026-05-15 "Duplicate canvas ID created in landscape.yml" for the worked example.

Original failure mode: anti-pattern #7 instance #5, 2026-05-09 — agent conflated Bash `head` with the Read tool, lost ~14k tokens to a Write-fail → remedial-full-Read → re-Write loop. The `limit:1` discipline (graduated 2026-05-14, v0.23.18) prevents the second-order cost where the agent *correctly* follows the rule but full-Reads every time. The ID-scan discipline (graduated 2026-05-15, v0.23.19) prevents the related class where the agent reads enough of the file to satisfy the Edit check but not enough to see existing ID assignments — kin to anti-pattern #8 (Stale State Read).

If this skill writes to multiple canvas files, register each one first (limit:1 for Edit-only paths; full Read for Write paths) AND ID-scan any prefix you intend to assign.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## When to Use

- At L3 Define->Develop and Develop->Deliver transitions (Regulatory Gate)
- At L4 Develop->Deliver when product_type is `ai_tool`
- At L5 Develop->Deliver for any product with user-facing AI features
- When guardrails G-S7 or G-S8 are triggered

## Workflow

1. **Determine AI presence**: Does this product contain AI/ML components?
   - If no: document "No AI components -- Regulatory Gate N/A" and stop
   - If yes: proceed to classification

2. **EU AI Act risk classification** (Regulation 2024/1689):
   - [ ] Check Annex III high-risk categories:
     - Biometric identification/categorization
     - Critical infrastructure management
     - Education and vocational training (access, assessment)
     - Employment (recruitment, screening, evaluation)
     - Essential services (credit scoring, insurance, social benefits)
     - Law enforcement
     - Migration and border control
     - Justice and democratic processes
   - [ ] Classify risk level: Minimal / Limited / High / Unacceptable

3. **Article 50 transparency check** (applies from 2 August 2026):
   - [ ] Does the system interact directly with people? -> Must disclose AI nature
   - [ ] Does it generate synthetic content? -> Must machine-mark outputs
   - [ ] Does it generate deepfakes? -> Must disclose artificial generation

4. **Product-type-specific checks**:
   - **ai_tool**: Full classification required. Check eval results for bias, safety review for harm potential.
   - **software**: Check if any feature uses AI/ML (recommendations, search, classification). If yes, assess that feature.
   - **content_***: Check if AI generates or curates content shown to users. If yes, transparency disclosure needed.
   - **service_offering**: Check if AI assists in service delivery decisions. If yes, explainability required.

5. **Document findings**:
   - Update `.claude/canvas/threat-model.yml` with regulatory classification
   - Update `.claude/canvas/privacy-assessment.yml` if data processing is involved
   - Log classification decision in `.claude/harness/decision-log.md`

6. **Determine compliance path**:
   - Minimal risk: No action required beyond documentation
   - Limited risk: Transparency obligations (Article 50)
   - High risk: Conformity assessment path must be planned before L4 delivery
   - Unacceptable risk: Product cannot proceed in current form

## Output Format

```
## Regulatory Review: [Product Name]

AI Components: [Yes/No]
Risk Classification: [Minimal/Limited/High/Unacceptable]

### Annex III Assessment
| Category | Applicable? | Rationale |
|----------|------------|-----------|
| Biometric | No | ... |
| Critical infra | No | ... |
| ... | ... | ... |

### Transparency Requirements
- AI disclosure needed: [Yes/No]
- Synthetic content marking: [Yes/No]
- Deepfake disclosure: [Yes/No]

### Compliance Path
[What needs to happen before delivery]

### Decision
Regulatory Gate: [Pass/Fail/N-A]
```

## Important Disclaimer

Mycelium is not a legal compliance tool. This skill raises awareness and prompts assessment of regulatory applicability. For actual compliance decisions, consult qualified legal counsel specializing in AI regulation.

## Theory Citations
- EU AI Act (Regulation 2024/1689)
- Article 50 transparency obligations
- Annex III high-risk categories
