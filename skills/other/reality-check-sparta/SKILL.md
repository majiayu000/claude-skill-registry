---
name: reality-check-sparta
description: Adversarial data quality assessment for the SPARTA QRA pipeline with self-correction loop. Actively hunts for flaws using multiple fresh verification techniques. Models The Aerospace Corporation's SPARTA Framework.
triggers: reality check sparta, sparta check, sparta quality, adversarial check, sparta fidelity, brandon review

provides:
  - reality-check-sparta
composes: [, task-monitor]
---

# reality-check-sparta

**ADVERSARIAL** data quality assessment for the SPARTA QRA pipeline with **self-correction loop**. Actively hunts for flaws using multiple fresh verification techniques.

## Client Knowledge

This skill models **The Aerospace Corporation's SPARTA Framework**:

| Attribute | Value |
|-----------|-------|
| Website | https://aerospace.org/sparta |
| Full Name | Space Attack Research & Tactic Analysis |
| Purpose | Taxonomy of space system threats and countermeasures |
| Comparable To | MITRE ATT&CK (but for space systems) |
| Source Excel | `data/source/SPARTA-Data.xlsx` |

### SPARTA Structure

- **216 Techniques**: Categorized by tactic (REC=Reconnaissance, EX=Execution, IA=Initial Access, etc.)
- **91 Countermeasures**: Security controls mapped to techniques
- **Cross-references**: MITRE ATT&CK, NIST 800-53, D3FEND, CWE, ESA SPACE-SHIELD

### Technique Categories

| Prefix | Category |
|--------|----------|
| REC | Reconnaissance |
| EX | Execution |
| IA | Initial Access |
| P | Persistence |
| PE | Privilege Escalation |
| DE | Defense Evasion |
| C | Collection |
| EXF | Exfiltration |
| IMP | Impact |
| LM | Lateral Movement |

## Philosophy

- **Any mismatch is a flaw to investigate**, not "compensate for"
- **Trust nothing, verify everything** - high scores might be gamed
- **Use fresh techniques each iteration** - not just re-running same checks
- **Model the client** - verify against original SPARTA data source
- **A PASS is hard to earn** - multiple warnings = FAIL

## Self-Correction Loop

The skill implements an iterative self-correction workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SELF-CORRECTION LOOP                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CHECK (adversarial)                                        │
│     ├── Database sampling + file inspection                    │
│     ├── SPARTA source fidelity (verify against Excel)          │
│     ├── URL/file alignment detection                           │
│     ├── Fresh URL fetch via httpx                              │
│     └── Verbatim grounding verification                        │
│                         │                                       │
│                         ▼                                       │
│  2. ANALYZE (identify issues)                                  │
│     ├── Categorize by severity (CRITICAL > HIGH > MEDIUM)      │
│     ├── Suggest root causes                                    │
│     └── Map to pipeline owners                                 │
│                         │                                       │
│                         ▼                                       │
│  3. SUGGEST FIXES                                              │
│     ├── Specific actionable fixes per issue category           │
│     └── Track convergence over time                            │
│                         │                                       │
│                         ▼                                       │
│  4. APPLY FIXES (human/pipeline)                               │
│                         │                                       │
│                         ▼                                       │
│  5. RE-CHECK (fresh techniques)                                │
│     ├── Use DIFFERENT verification methods                     │
│     ├── Cross-reference against SPARTA website                 │
│     └── Fresh fetch URLs to compare                            │
│                         │                                       │
│                         ▼                                       │
│  6. CONVERGENCE ANALYSIS                                       │
│     ├── Track issue counts over iterations                     │
│     ├── IMPROVING / STABLE / REGRESSING status                 │
│     └── Store learnings in /memory                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/reality-check-sparta

# Run adversarial check with fix suggestions
./run.sh check --run-id run-recovery-verify --samples 20

# Self-correction loop (check + convergence)
./run.sh iterate --run-id run-recovery-verify

# Check convergence trend
./run.sh convergence

# Full deep check
./run.sh check --run-id run-recovery-verify --full --store
```

## Fresh Verification Techniques

Each iteration uses different methods to avoid blind spots:

| Technique | Description | Method |
|-----------|-------------|--------|
| `database_sampling` | Random stratified sampling from DuckDB | Internal |
| `fresh_url_fetch` | Re-fetch select URLs live via httpx | External |
| `browser_verification` | Headless browser via /surf | External |
| `excel_crossref` | Cross-reference against SPARTA-Data.xlsx | Internal |
| `mitre_api_verify` | Verify against MITRE ATT&CK STIX API | External |
| `sparta_source_fidelity` | Verify DB matches original client data | Internal |

## What It Checks (Adversarially)

### 1. SPARTA Source Fidelity (NEW)
- Verifies DB accurately represents original SPARTA Excel
- Checks technique/countermeasure counts (216/91)
- Validates ID format matches SPARTA convention
- Verifies cross-reference column coverage

### 2. URL/File Integrity
- Detects mismatched downloads (file contains wrong technique)
- **>5% mismatch = FAIL**
- Fresh-fetches URLs to compare against cached content

### 3. Verbatim Grounding Verification
- Actually checks if QRA answers match source text
- 20-char phrase matching
- Detects hallucination patterns

### 4. QRA Structure Integrity
- Empty/null answers
- Orphan QRAs (no relationship)
- Duplicate questions

### 5. Coverage Gap Analysis
- Weak frameworks (avg grounding < 0.85)
- Low relationship coverage

## Fix Suggestions

The skill suggests specific fixes for each failing check:

```
🔴 [CRITICAL] url_file_alignment: FAIL
   Description: Files downloaded for MITRE ATT&CK URLs contain wrong technique content
   Root Cause: Likely redirect handling, hash collision, or race condition
   Owner: fetch/download logic in SPARTA pipeline
   Suggested Fixes:
      1. Check download function for proper redirect following
      2. Add URL->content validation in download pipeline
      3. Re-download mismatched URLs individually
      4. Implement checksumming for downloaded files
```

## Convergence Analysis

Track issue resolution over time:

```bash
./run.sh convergence

# Output:
CONVERGENCE ANALYSIS
Status: IMPROVING
Message: Issues decreased from 25 to 18

Recent History:
  2026-02-06T08:42:53: 25 issues
  2026-02-06T09:15:00: 22 issues
  2026-02-06T10:30:00: 18 issues
```

## Commands

| Command | Description |
|---------|-------------|
| `check` | Run adversarial check with fix suggestions |
| `iterate` | Self-correction loop (check + convergence) |
| `convergence` | Show issue trend over time |
| `status` | Quick pipeline status |
| `history` | Past findings from /memory |

## QRA Convergence Model

QRA quality improvement follows the same dynamics as **model training convergence**:

| ML Training | SPARTA QRA Pipeline |
|-------------|---------------------|
| Training data | SPARTA controls, relationships, knowledge excerpts |
| Model weights | QRA corpus (generated answers) |
| Loss function | Brandon's issue count (anchoring failures, grounding gaps) |
| Learning rate | Prompt aggressiveness (how much we demand per QRA) |
| Gradient descent | generate → assess → fix prompts → regenerate |
| Epoch | One convergence cycle (10K QRA checkpoint) |
| Overfitting | Gaming thresholds / lowering standards (NEVER DO THIS) |
| Plateau | Prompt ceiling → use `/prompt-lab` to redesign prompts |
| Validation set | Brandon's adversarial spot checks |
| Early stopping | Quality converged — stop changing prompts |

**Convergence Rules:**
1. Issue count MUST decrease cycle over cycle (like loss decreasing)
2. 3 consecutive regressions = stalled → human intervention needed
3. Plateau = prompt ceiling → redesign with `/prompt-lab`
4. NEVER lower thresholds to game the curve
5. Track metrics via `convergence_state.json`

**Use `sparta-review converge` for the full autonomous loop.**

## Dynamic Thresholds (Annealing Schedule)

**Brandon decides thresholds based on corpus size** - like annealing in model training:
- **Early (small corpus)**: Be lenient, allow learning
- **Middle (growing)**: Gradually tighten standards
- **Late (near target)**: Apply strictest standards

| Phase | QRA Range | Anchoring Fail | Generic Fail | Brandon Says |
|-------|-----------|----------------|--------------|--------------|
| Bootstrap | 0-5K | 50% | 80% | "Let's see what we're working with" |
| Early Growth | 5K-15K | 40% | 70% | "Time to raise the bar" |
| Mid Growth | 15K-40K | 35% | 65% | "No more excuses" |
| Late Growth | 40K-80K | 30% | 60% | "Tightening the screws" |
| Refinement | 80K-100K | 25% | 55% | "Time to be strict" |
| Gold Standard | 100K+ | 20% | 50% | "No compromises" |

The assessment now includes a `continue_decision` field:
- `CONTINUE` - Quality acceptable for current phase, keep generating
- `STOP_AND_FIX` - Quality below phase threshold, run auto-fix

## Static Thresholds (Non-Annealed)

| Check | PASS | WARN | FAIL |
|-------|------|------|------|
| Source fidelity | Exact match | Minor issues | Count mismatch |
| URL/File integrity | 0% mismatch | 1-5% mismatch | >5% mismatch |
| Verbatim grounding | >70% verified | 50-70% verified | <50% or suspicious |
| Structure | No issues | Minor issues | Empty/orphans |

## Memory Integration

Findings stored with adversarial framing:

```bash
# After check with --store:
# Stores: "SPARTA reality check run-X: 25 ISSUES FOUND"
# With: "ACTION REQUIRED: Investigate root causes"

# Query past findings:
./run.sh history
```

## Brandon Bailey Persona

The skill uses the **Brandon Bailey persona** for domain expert quality review. Brandon Bailey is the creator of SPARTA at The Aerospace Corporation.

### Persona Integration

```bash
# Run Brandon Bailey review (checks space terminology)
./run.sh check --run-id run-recovery-verify --brandon-review

# Full review with prompt optimization recommendations
./run.sh check --run-id run-recovery-verify --brandon-review --full
```

### Grading Scale

| Grade | Threshold | Description |
|-------|-----------|-------------|
| A+ EXCELLENT | <20% generic | Production ready |
| A GOOD | 20-30% generic | Minor improvements needed |
| B ACCEPTABLE | 30-50% generic | Significant work required |
| C NEEDS WORK | 50-70% generic | Major revision needed |
| F FAIL | >70% generic | Rejected |

### Required Space Terminology

Brandon requires every QRA answer to include space-specific terms:

- **Segment Context**: ground segment, link segment, space segment
- **Assets**: satellite, spacecraft, payload, bus, ground station
- **Communications**: RF, SATCOM, uplink, downlink, telemetry, TT&C
- **Threats**: jamming, spoofing, signal interference, ASAT
- **Standards**: CCSDS, SpaceWire, MIL-STD

### Persona Files

- `BRANDON_BAILEY_PERSONA.md` - Full persona definition
- `brandon_bailey_persona.yaml` - Create-persona manifest
- `LESSONS_LEARNED.md` - Session learnings (F → A+)

## Related Skills

| Skill | Use For |
|-------|---------|
| `/memory` | Store and recall findings |
| `/surf` | Browser-based URL verification |
| `/fetcher` | Fresh URL fetching |
| `/extractor` | Content extraction debugging |
| `/assess` | General project assessment |
| `/create-persona` | Register Brandon as formal persona |
| `/prompt-lab` | Optimize prompts based on Brandon's criteria |
