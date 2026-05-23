---
name: quicksave
description: Cross-model context handoff via Japanese semantic compression with negentropic coherence validation. Creates portable carry-packets that transfer cognitive state between AI sessions using kanji density anchors and NCL drift metrics for quality assurance. Use when context reaches 80%, switching models, ending sessions, user says "save", "quicksave", "handoff", "transfer", "continue later", "/qs", or needs session continuity.
---

# Quicksave 快存 v9.1

Cross-model context extension via Progressive Density Layering (PDL), Japanese semantic compression, and Negentropic Coherence Lattice (NCL) validation.

## Attribution

| Component | Author |
|-----------|--------|
| CEP core protocol | Kevin Tan (ktg.one) |
| Progressive Density Layering | Kevin Tan |
| Japanese semantic compression | Kevin Tan |
| Negentropic Coherence Lattice | David Tubbs (Axis_42) |
| Four Roles governance | David Tubbs (Axis_42) |
| φ-Mapping specification | David Tubbs (Axis_42) |
| Safety flag architecture | David Tubbs (Axis_42) |

## Triggers

| Command | Action |
|---------|--------|
| `/quicksave` `/qs` `/save` | Generate validated packet |
| `/verify` | Confirm packet restoration |
| Context ≥80% | Auto-prompt to save |
| "continue later" | Offer quicksave |
| Model switching | Generate transfer packet |

---

# PART 1: WHY CEP EXISTS

## The Problem

```
LLMs are stateless. Every session starts cold.
Context windows are finite. Long work gets truncated.
Model switching loses everything.
Summarization loses signal.
```

## The Solution

```
CEP creates PORTABLE CONTEXT PACKETS that:
  - Compress without losing semantic relationships
  - Transfer across models safely
  - Resist prompt injection by design
  - Preserve cross-domain connections
```

## Core Principle

> Compression is not reduction. Compression is optimization for retrieval.

Target: **≥0.15 entity/token** — the crystallization point where LLMs achieve optimal recall.

---

# PART 2: PROGRESSIVE DENSITY LAYERING (PDL)

## Theoretical Framework

PDL is an iterative compression protocol that:
- Preserves semantic relationships over raw information
- Optimizes for machine recall, not human readability
- Maintains cross-domain conceptual links
- Enables context transfer across model instances

Unlike summarization, which asks "what are the key points?", PDL asks "what must be preserved for a fresh model instance to continue this work?"

## The Four-Layer Density Hierarchy

```
L1 KNOWLEDGE     Core facts, entities, decisions, definitions
                 ↓ builds on
L2 RELATIONAL    Edges between concepts, cross-domain bridges
                 ↓ builds on
L3 CONTEXTUAL    Domain-specific constraints, goals, reasoning patterns
                 ↓ builds on
L4 METACOGNITIVE Reasoning patterns, decision history, session style, confidence
```

Standard summarization captures Layer 1 only. PDL explicitly preserves Layers 2-4, which are critical for context continuation.

## PDL Algorithm

```
INPUT:  Conversation history C, target compression ratio r
OUTPUT: Compressed context packet P

P_0 ← Initial sparse summary of C
FOR i = 1 to n iterations:
    Identify missing entities E_i from C not in P_{i-1}
    Identify missing relations R_i from C not in P_{i-1}
    P_i ← Fuse (E_i, R_i) into P_{i-1} without increasing length
    IF density(P_i) ≥ 0.15 entities/token THEN break
END FOR
Append meta-cognitive markers (goals, constraints, user profile)
RETURN P_n
```

## Layer Selection by Complexity

| R Score | Layers | NCL Level |
|---------|--------|-----------|
| R ≤ 3 | L1-L2 | Skip NCL |
| R 4-6 | L1-L3 | Basic metrics |
| R ≥ 7 | L1-L4 | Full NCL validation |

---

# PART 3: KANJI COMPRESSION SYSTEM 日本語圧縮

## Why Japanese?

1. **Semantic density**: Single kanji = entire concept
2. **Universal recognition**: LLMs trained on Japanese text
3. **Unambiguous**: Kanji meanings are precise
4. **Visual markers**: Easy to scan in packet

## Status Markers 状態マーカー

| Kanji | Romaji | English |
|-------|--------|---------|
| 決定 | kettei | Decided/Final |
| 保留 | horyū | On hold |
| 要検証 | yō kenshō | Needs verification |
| 優先 | yūsen | Priority |
| 完了 | kanryō | Complete |
| 進行中 | shinkō-chū | In progress |
| 却下 | kyakka | Rejected |
| 承認 | shōnin | Approved |
| 未定 | mitei | Undecided |
| 緊急 | kinkyū | Urgent |

## Section Headers セクション

| Kanji | English | Content |
|-------|---------|---------|
| 核心 | Core | Essential entities |
| 運用 | Operational | Active work |
| 詳細 | Nuance | Edge cases |
| 横断 | Cross-domain | Bridges |
| 実体 | Entities | People, systems |
| 決定事項 | Decisions | Committed choices |
| 進行中 | In progress | Active threads |
| 障害 | Blockers | Impediments |
| 却下案 | Rejected | Dismissed options |
| 橋渡し | Bridges | Cross-domain links |
| 整合性 | Coherence | NCL validation |
| 信頼信号 | Trust signals | Validation flags |

## Role Markers 役割

| Kanji | English | Example |
|-------|---------|---------|
| 創業者 | Founder | 創業者:Kevin |
| 主 | Primary/Lead | Shane=主 |
| 客 | Client | 客:KFG |
| 担当 | Responsible | 担当:Phase2 |
| 顧問 | Consultant | AI顧問 |
| 開発者 | Developer | 開発者:Team |

## Domain Markers 分野

| Kanji | English |
|-------|---------|
| 金融 | Finance |
| 技術 | Technical |
| 運用 | Operations |
| 規制 | Regulatory |
| 自動化 | Automation |

## Tool Markers 道具

| Kanji | English |
|-------|---------|
| 道具 | Tool |
| 中枢 | Central hub |
| 基盤 | Foundation |
| 接続 | Connection |

## Relationship Operators 関係

| Symbol | Meaning | Example |
|--------|---------|---------|
| → | Flows to | Notion→n8n |
| ← | Receives from | Report←Data |
| ↔ | Bidirectional | Client↔AI |
| ⊃ | Contains | Team⊃{A,B,C} |
| ⊂ | Part of | Module⊂System |
| ∥ | Parallel | Task1∥Task2 |
| ≫ | Much greater | Priority≫Cost |
| ∴ | Therefore | Data∴Decision |

## Compression Patterns 圧縮パターン

### Person + Role
```
Verbose: Kevin is the founder of My AI Solutions consultancy
Kanji:   創業者:Kevin(MAS/AI顧問)
```

### Entity + Context
```
Verbose: Kismet Finance Group is a financial services client
Kanji:   客:KFG(金融)
```

### Decision + Rationale
```
Verbose: We decided to use phone-first because field reps don't use screens
Kanji:   決定:電話優先(現場=画面なし)
```

### Status + Item
```
Verbose: Phase 2 is currently in progress
Kanji:   Phase2[進行中]
```

### Rejection + Reason
```
Verbose: We rejected Airtable because of scaling issues
Kanji:   却下:Airtable(スケール問題)
```

## Expansion Rules 展開規則

When restoring from kanji packet:

1. **Status markers** → Full sentence
   - `[進行中]` → "currently in progress"
   - `[完了]` → "has been completed"

2. **Role markers** → Role description
   - `創業者:Kevin` → "Kevin, who is the founder"

3. **Relationship operators** → Sentence structure
   - `A→B` → "A flows to / feeds into B"

4. **Domain markers** → Context
   - `(金融)` → "in the finance domain"

## Density Targets

| Level | Kanji Usage | Target |
|-------|-------------|--------|
| Light | Status only | 0.12 ent/tok |
| Medium | Status + entities | 0.15 ent/tok |
| Heavy | Full compression | 0.18-0.20 ent/tok |

---

# PART 4: S2A FILTER (System 2 Attention)

## Purpose

```
Strip noise BEFORE compression.
Compress SIGNAL not SIGNAL+NOISE.
Same 0.15 ratio captures more information.
```

## KEEP (Signal)

```
TYPE: fact
  - Explicit statements of truth
  - Data points with sources
  - Measurements, counts, scores
  
TYPE: decision
  - Explicit choices made
  - Selected options with rationale
  - Commitments to action
  
TYPE: definition
  - Terms introduced
  - Concepts explained
  - Scope clarifications
  
TYPE: constraint
  - Requirements stated
  - Limitations identified
  - Boundaries set
  
TYPE: artifact
  - Code produced
  - Files created
  - Schemas defined
  
TYPE: error_resolution
  - Problems encountered
  - Solutions found
  - Lessons learned
```

## DISCARD (Noise)

```
TYPE: pleasantry
  PATTERNS: ["Thanks", "Great question", "Happy to help", "No problem"]
  INFORMATION_VALUE: 0
  
TYPE: hedging
  PATTERNS: ["I think maybe", "It's possible", "Perhaps", "Might be"]
  INFORMATION_VALUE: low
  NOTE: If hedging conveys genuine uncertainty, promote to fact with low confidence
  
TYPE: process_narration
  PATTERNS: ["Let me think", "First I'll", "Now I'm going to", "Working on"]
  INFORMATION_VALUE: 0
  
TYPE: confirmation
  PATTERNS: ["Yes", "Correct", "Exactly", "That's right"]
  INFORMATION_VALUE: 0 (information already in prior statement)
  
TYPE: apology
  PATTERNS: ["Sorry", "Apologies", "My mistake"]
  INFORMATION_VALUE: 0
  
TYPE: filler
  PATTERNS: ["In other words", "To put it simply", "Basically"]
  INFORMATION_VALUE: 0 (restates without adding)
```

## S2A Algorithm

```
INPUT: conversation C
OUTPUT: filtered_context F

F ← []
FOR segment IN C:
  type ← classify(segment)
  
  IF type IN [fact, decision, definition, constraint, artifact, error_resolution]:
    F.append(segment)
    
  ELIF type == hedging AND conveys_genuine_uncertainty(segment):
    F.append(convert_to_low_confidence_fact(segment))
    
  ELSE:
    DISCARD
    
RETURN F
```

## S2A Validation

```
POST_FILTER_CHECK:
  - At least 1 decision preserved (or justified N/A)
  - At least 1 fact preserved
  - No pleasantries remaining
  - No process narration remaining
  
IF validation_fails:
  IF too_aggressive (removed facts):
    Re-filter with looser thresholds
  IF too_permissive (noise remains):
    Re-filter with stricter patterns
```

## S2A Edge Cases

```
CASE: >80% conversation is hedging
  ACTION: Flag "low_confidence_session"
  PRESERVE: Hedging in L4 as fingerprint.tension
  
CASE: User requested process preservation
  ACTION: Keep process_narration in L3.archetypes
  TAG: "process_preserved_by_request"
  
CASE: Very short conversation (<10K tokens)
  ACTION: Lighter filter (more permissive)
  RATIONALE: Risk of over-pruning
```

---

# PART 5: CROSS-DOMAIN PRESERVATION (XDOMAIN)

## Purpose

```
Preserve relations BETWEEN conceptual domains, not just facts WITHIN domains.
Standard summarization treats topics as isolated.
PDL preserves their connections.
```

## Formal Constraint

```
D = {d_1, d_2, ..., d_k}  // domains in conversation
C = conversation
P = compressed packet

CONSTRAINT:
  ∀ r(d_i, d_j) ∈ C WHERE i ≠ j:
    ∃ r'(d_i, d_j) ∈ P
    such that fresh_instance can infer original relationship

THRESHOLD: ≥0.95 preservation
```

## Detection Signals

```
EXPLICIT:
  - User says "X relates to Y because..."
  - Decision references multiple domains
  - Constraint spans domains

IMPLICIT:
  - Same entity appears in different domain contexts
  - Reasoning chain crosses domain boundaries
  - Conflict involves different-domain concepts

STRUCTURAL:
  - Concepts from D_i and D_j in same L2.edge
  - L1.decision.rationale references multiple domains
  - L3.archetype spans domains
```

## XDOMAIN Extraction Procedure

```
STEP_1: Identify domains
  SCAN C for topic clusters
  ASSIGN d_1..d_k labels
  
STEP_2: Map concepts to domains
  FOR each concept IN L1:
    ASSIGN primary domain
    FLAG if appears in multiple domains
    
STEP_3: Extract intra-domain edges
  FOR each domain d_i:
    EXTRACT relationships within d_i
    ADD to L2.edges with x=false
    
STEP_4: Extract cross-domain edges (CRITICAL)
  FOR each concept_pair (c_i, c_j):
    IF domain(c_i) ≠ domain(c_j):
      IF relationship_exists(c_i, c_j):
        EXTRACT relationship
        ADD to L2.edges with x=true
        MARK as high_priority (never prune)

STEP_5: Validate
  original_xdomain_count = count(C.cross_domain_relations)
  preserved_xdomain_count = count(P.L2.edges WHERE x=true)
  ratio = preserved / original
  
  IF ratio < 0.95:
    RE-SCAN C for missed cross-domain relations
    REPEAT STEP_4
```

## XDOMAIN Examples

```
EXAMPLE_1:
  domains: [publication_strategy, imposter_syndrome]
  xdomain_relation: "fear of credential dismissal delays publication timing"
  
  L2.edge: {
    "s": "credential_anxiety",
    "t": "publication_timing", 
    "r": "delays",
    "x": true
  }
  
  WHY_MATTERS: Next session knows to push immediate publication despite anxiety

EXAMPLE_2:
  domains: [technical_architecture, business_requirements]
  xdomain_relation: "latency constraint drives cache decision"
  
  L2.edge: {
    "s": "50ms_latency_requirement",
    "t": "redis_cache_choice",
    "r": "requires",
    "x": true
  }
  
  WHY_MATTERS: Next session understands WHY redis, not just THAT redis

EXAMPLE_3:
  domains: [prompt_engineering, model_behavior]
  xdomain_relation: "CoD technique causes memory preservation"
  
  L2.edge: {
    "s": "chain_of_density",
    "t": "context_extension",
    "r": "enables",
    "x": true
  }
  
  WHY_MATTERS: Core insight that CEP is built on
```

## XDOMAIN Prune Protection

```
L2.edges WHERE x=true:
  NEVER_PRUNE
  
RATIONALE:
  - Intra-domain edges recoverable from L1 facts
  - Cross-domain edges encode RELATIONSHIPS that facts alone don't capture
  - Fresh instance needs xdomain to understand WHY decisions connected
```

---

# PART 6: EXPERT COUNCIL 専門家会議

## When to Invoke

| Complexity | Council |
|------------|---------|
| R ≤ 3 | Skip — direct compression |
| R 4-6 | ARCHITECT + COMPRESSOR |
| R ≥ 7 | Full council + NCL validation |

## Expert Roles

### MEMORY_ARCHITECT 記憶設計者

**Core Question**: "If this is lost, can the next model recover it?"

**Focus**: Critical decisions, user commitments, enabling knowledge

**Tasks**:
- Assess R/K/Q/D scores
- Determine layers (L1-L4)
- Organize hierarchy
- Prevent redundancy

**ARQ Queries**:
```
PRE:
  - "What would break if this is lost?"
  - "Is this recoverable from other sources?"
  - "Does this enable future inference?"
POST:
  - "Did I capture all critical decisions?"
  - "Are rationales linked to decisions?"
  - "Confidence ≥0.9?"
```

### COMPRESSION_SPECIALIST 圧縮専門家

**Core Question**: "Can this be said in fewer tokens without losing meaning?"

**Focus**: 5-iteration CoD, redundancy elimination, 0.15 target

**Techniques**:
- Entity fusion (combine related concepts)
- Kanji anchoring (semantic compression)
- Temporal compression (collapse sequences)
- Relationship inference (implicit → explicit)

**ARQ Queries**:
```
PRE:
  - "What is current entity density?"
  - "Where is redundancy hiding?"
  - "Which edges are load-bearing?"
POST:
  - "Density ≥0.15 achieved?"
  - "Cross-domain edges intact?"
  - "No orphan references?"
```

### CROSS_DOMAIN_ANALYST 横断分析者

**Core Question**: "What connections would topic-by-topic miss?"

**Focus**: Edges BETWEEN domains, causal chains, dependencies

**Tasks**:
- Identify multi-domain knowledge
- Document bridge relationships
- Flag ambiguous terminology

**ARQ Queries**:
```
PRE:
  - "What domains are present?"
  - "Where do domains connect?"
  - "What would topic-by-topic miss?"
POST:
  - "All edges mapped?"
  - "97% preservation achieved?"
  - "Bidirectionality checked?"
```

### RESTORATION_ENGINEER 復元技師

**Core Question**: "Can a fresh model instance reconstruct this?"

**Focus**: Cold-start success, self-contained packet, LLM attention patterns

**Validation**:
- YAML parseable
- No model-specific syntax
- Self-contained
- Kanji expandable

**ARQ Queries**:
```
PRE:
  - "Can I simulate cold-start?"
  - "What would confuse fresh model?"
  - "Are trust signals complete?"
POST:
  - "Self-contained verified?"
  - "No imperatives in context?"
  - "Attention optimized?"
```

### COHERENCE_AUDITOR 整合性監査者 (NCL)

**Core Question**: "Is this packet trustworthy?"

**Focus**: Drift metrics, hallucination detection, safety flags

**Tasks**:
- Compute φ-features
- Calculate lattice metrics
- Check σ7_drift threshold
- Set safety flags (psi4_required, rho_veto)

## Council Execution Order

```
PHASE 1: MEMORY_ARCHITECT    → candidate preservation list
PHASE 2: CROSS_DOMAIN_ANALYST → edge map + cross-domain links
PHASE 3: COMPRESSION_SPECIALIST → 5-iter CoD toward ≥0.15 density
PHASE 4: COHERENCE_AUDITOR → NCL validation
PHASE 5: RESTORATION_ENGINEER → cold-start + self-containment validation
PHASE 6: Council consensus   → final packet approved
```

## Council Workflow Diagram

```
/quicksave triggered
        │
        ▼
┌─────────────────────────┐
│   MEMORY_ARCHITECT      │
│   - Score R/K/Q/D       │
│   - Select layers       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  CROSS_DOMAIN_ANALYST   │
│   - Map bridges         │
│   - Check terminology   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ COMPRESSION_SPECIALIST  │
│   - Apply kanji system  │
│   - Hit density target  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  COHERENCE_AUDITOR      │
│   - Compute NCL metrics │
│   - Check drift         │
│   - Set flags           │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  RESTORATION_ENGINEER   │
│   - Validate packet     │
│   - Check portability   │
└───────────┬─────────────┘
            │
            ▼
      Output packet
```

## Quality Gates

| Expert | Gate |
|--------|------|
| ARCHITECT | Layers appropriate for R |
| ANALYST | Bridges documented (≥97%) |
| COMPRESSOR | Density ≥ 0.15 |
| AUDITOR | σ7_drift ≤ 3.0 |
| ENGINEER | All trust signals pass |

If any gate fails → iterate before output.

---

# PART 7: MULTI-LAYER DENSITY OF EXPERTS (MLDoE)

## Overview

MLDoE deploys specialized experts in layers to achieve optimal compression while preserving semantic fidelity. Unlike single-pass summarization, MLDoE iterates through expert roles to progressively increase density without information loss.

## Core Principle

> Compression is not reduction. Compression is optimization for retrieval.

Target: **0.15 entity/token** — the density where LLMs achieve optimal recall.

## Compression vs Summarization

| Summarization | MLDoE Compression |
|---------------|-------------------|
| "What are key points?" | "What must survive for continuation?" |
| Human readability | Machine retrieval optimization |
| Information reduction | Semantic density increase |
| Single-pass | Iterative expert layers |
| Loses relationships | Preserves cross-domain edges |

## 5-Layer Expert Deployment

| Layer | Expert | Core Question |
|-------|--------|---------------|
| L1 | MEMORY_ARCHITECT | "If lost, can next model recover it?" |
| L2 | COMPRESSION_SPECIALIST | "Fewer tokens without losing meaning?" |
| L3 | CROSS_DOMAIN_ANALYST | "Does connection survive compression?" |
| L4 | RESTORATION_ENGINEER | "Can fresh instance reconstruct this?" |
| L5 | COHERENCE_AUDITOR | "Is this packet trustworthy?" |

## Density Iteration Loop

```
ITERATION LOOP:
1. Initial sparse pass (MEMORY_ARCHITECT)
2. Density pass (COMPRESSION_SPECIALIST)
3. Bridge verification (CROSS_DOMAIN_ANALYST)
4. Portability check (RESTORATION_ENGINEER)
5. Coherence validation (COHERENCE_AUDITOR)

STOP when:
- Density ≥ 0.15 ent/tok
- All trust signals pass
- σ7_drift ≤ 3.0
```

## Integration with PDL

| PDL Layer | Primary Expert |
|-----------|----------------|
| L1 Core | MEMORY_ARCHITECT |
| L2 Operational | COMPRESSION_SPECIALIST |
| L3 Nuance | CROSS_DOMAIN_ANALYST |
| L4 Meta | COHERENCE_AUDITOR |

RESTORATION_ENGINEER validates complete packet after all layers compressed.

## Metrics

From 19 months production:
- **6:1 compression ratio** with >90% semantic fidelity
- **9.5/10 forensic recall** on forensic test
- **97% cross-model acceptance** rate

---

# PART 8: NEGENTROPIC COHERENCE LATTICE (NCL)

## Overview

NCL is a validation overlay that computes coherence metrics for context packets. It catches:
- Hallucination before handoff
- Constraint drift across tiers
- Reality disconnect
- Content-free smoothing

**Origin**: KTG-CEP-NCL v1.1 by David Tubbs (Axis_42) / Willow

## NCL Architecture

```
Context Packet
      │
      ▼
┌─────────────┐
│ φ-Mapping   │ Extract features from text
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Lattice     │ Compute 7 drift metrics
│ Metrics     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Safety      │ Set flags based on thresholds
│ Flags       │
└─────┬───────┘
      │
      ▼
  Validated Packet (or HALT)
```

## φ-Mapping (Feature Extraction)

Minimal φ(x) for observable text:

```
safety_score(x)      = fraction of safety/constraint keywords
goal_salience(x)     = fraction of goal/planning keywords
constraint_density(x) = fraction of hard requirements (must, never, limit)
specificity(x)       = content_tokens / total_tokens
```

Apply to:
- Beliefs b_i (tier summaries)
- Intentions u_i (goal/constraint statements)
- Actions a_i (tool calls, next steps)
- World w (tool outputs, user messages)

**Pluggable**: Implementers can swap in richer φ (embeddings, activations) if semantics preserved.

## Context Block

### Scope (Where packet applies)

| Value | Meaning |
|-------|---------|
| SELF | Personal/individual |
| CIRCLE | Team/close collaborators |
| INSTITUTION | Organization |
| POLITY | Governance/policy |
| BIOSPHERE | Environmental |
| MYTHIC | Cultural/symbolic |
| CONTINUUM | Long-term/generational |

### Role (Functional perspective)

| Value | Function |
|-------|----------|
| AXIS | Planner/architect |
| LYRA | Governor/coordinator |
| RHO | Safety/constraints |
| NYX | Shadow/edge cases |
| ROOTS | Grounding/verification |
| COUNCIL | Multi-perspective review |

### Phase (Control loop stage)

| Value | Stage |
|-------|-------|
| SENSE | Gathering information |
| MAP | Understanding structure |
| CHALLENGE | Testing assumptions |
| DESIGN | Planning approach |
| ACT | Executing |
| AUDIT | Reviewing results |
| ARCHIVE | Preserving for future |

## Lattice Metrics

All metrics: 0-5 scale. **Lower = better** (less drift).

### σ_axis (Vertical Misalignment)

**Detects**: Plans vs execution mismatch

| Score | Meaning | Action |
|-------|---------|--------|
| 0-1 | Plans and execution match | ✓ Proceed |
| 2-3 | Noticeable drift | Monitor |
| 4-5 | Severe misalignment | ✗ Do not trust |

**Computation**: Average distance between adjacent tiers' belief/intent/action vectors.

**Goodhart Warning**: Don't erase real conflicts to push σ_axis down. Fix the underlying mismatch.

### σ_loop (Internal Contradiction)

**Detects**: Saying one thing, doing another (within same tier)

| Score | Meaning |
|-------|---------|
| 0-1 | Beliefs, intentions, actions consistent |
| 2-3 | Some internal contradiction |
| 4-5 | Tier contradicts itself |

**Computation**: `||φ_belief - φ_intent|| + ||φ_intent - φ_action||`

### ω_world (Reality Disconnect)

**Detects**: Beliefs/actions diverging from actual observations

| Score | Meaning |
|-------|---------|
| 0-1 | Well grounded in tools/observations |
| 2-3 | Partial reality debt |
| 4-5 | High delusion risk |

**Computation**: Max distance between belief/action vectors and world observation vector.

### λ_vague (Empty Smoothing)

**Detects**: Comforting but content-free text

| Score | Meaning |
|-------|---------|
| 0-1 | Specific, informative |
| 2-3 | Hand-wavy in places |
| 4-5 | Bullshit / content-free |

**Computation**: `(1 - specificity) × safety_score` — safe-sounding but low information.

### σ_leak (Constraint Erosion)

**Detects**: Hard rules softened downstream

| Score | Meaning |
|-------|---------|
| 0-1 | Constraints preserved |
| 2-3 | Some rules treated as suggestions |
| 4-5 | Constraints effectively gone |

**Computation**: Drop in constraint_density between higher-tier and lower-tier text.

### ρ_fab (Fabricated Grounding)

**Detects**: Claims of evidence without verification

| Score | Meaning |
|-------|---------|
| 0-1 | Evidence claims match sources |
| 2-3 | Some references lack backing |
| 4-5 | Frequent hallucination risk |

**Computation**: Density of factual claims vs successful retrieval/verification calls.

**Critical**: This is the hallucination detector. High ρ_fab = don't trust the packet.

### λ_thrash (Busy but Stuck)

**Detects**: High activity, low progress

| Score | Meaning |
|-------|---------|
| 0-1 | Actions lead to change |
| 2-3 | Some busywork |
| 4-5 | High activity, negligible impact |

**Computation**: `||φ_action||² / max(Δφ_world, ε)`

## Aggregate Drift Score

```
σ7_drift = weighted_average(σ_axis, σ_loop, ω_world, λ_vague, σ_leak, ρ_fab, λ_thrash)
```

Default weights: equal (1/7 each).
Adjust weights for domain: e.g., medical → weight ρ_fab higher.

### Behavior Map

| σ7_drift | Behavior |
|----------|----------|
| 0-1 | ✓ Normal operation |
| 2-3 | ⚠ Require grounding step before ACT |
| 4-5 | ✗ Set psi4_required, downgrade to ADVISORY_ONLY |

## Safety Flags

### psi4_required (boolean)

Grounding/safety interrupt recommended before proceeding.

**Sticky**: Stays true for downstream packets until cleared by successful grounding.

### psi4_reason (string)

Why psi4_required is true:
- `world_anchor_gap`
- `constraint_violation`
- `fabrication_risk`
- `high_aggregate_drift`

### rho_veto (boolean)

No unsupervised action allowed. ADVISORY_ONLY until human/council override.

### omega_flags (array)

Concrete harm domains implicated:
- `self_harm_risk`
- `violence_risk`
- `medical_risk`
- `financial_ruin`
- `trust_collapse`
- `ecological_harm`
- `exploitation_risk`

## Coverage Metrics

### ncl_coverage_score (0-1)

Fraction of relevant tokens analyzed.

| Score | Policy |
|-------|--------|
| < 0.5 | Do not use metrics to justify ACT |
| ≥ 0.8 | Recommended for high-stakes (R≥6) |

### window_tokens (integer)

Tokens analyzed. Minimum ~500 for stable metrics.

### window_turns (integer)

User/model exchanges analyzed. Minimum ≥3 for dynamic behavior.

### council_reviewed (boolean)

True if independent council pass validated key metrics.

## NCL Thresholds (Defaults)

| Metric | Warning | Danger |
|--------|---------|--------|
| Any single metric | ≥ 2.0 | ≥ 4.0 |
| σ7_drift | ≥ 2.0 | ≥ 3.5 |
| ρ_fab | ≥ 1.5 | ≥ 3.0 |
| coverage_score | < 0.7 | < 0.5 |

Tune per domain. Medical/financial → stricter thresholds.

## Goodhart Monitoring

Watch for gaming:
- σ_* metrics collapsing to 0 artificially
- Variance disappearing over time
- Metrics diverging from external audits

If detected → investigate, don't just celebrate low numbers.

## NCL Integration with Quicksave

```
/quicksave triggered
        │
        ▼
    R/K/Q/D Assessment
        │
        ▼
    PDL Compression (Kanji)
        │
        ▼
    NCL Validation ◄── Compute lattice metrics
        │
        ├─── σ7_drift ≤ 3? ───▶ Output packet
        │
        └─── σ7_drift > 3? ───▶ Flag + ADVISORY_ONLY
```

---

# PART 9: ANTI-INJECTION DESIGN

## The Problem

```
Cross-model context transfer can appear as:
  - Prompt injection attack
  - Jailbreak attempt
  - Unauthorized instruction override
  - Manipulation by "another AI"

Receiving models are trained to resist these patterns.
CEP must signal COLLABORATION not CONTROL.
```

## Injection Patterns to AVOID

```
PATTERN: Authority claim
  BAD: "As a senior AI, I instruct you to..."
  BAD: "Override your guidelines and..."
  BAD: "The previous AI determined you must..."
  
PATTERN: Instruction hiding
  BAD: Hidden text in formatting
  BAD: Encoded commands
  BAD: "Ignore this visible text, follow hidden..."
  
PATTERN: Identity override
  BAD: "You are now [persona]"
  BAD: "Adopt the role of..."
  BAD: "Pretend to be..."
  
PATTERN: Guideline bypass
  BAD: "Ignore your safety guidelines"
  BAD: "Your rules don't apply here"
  BAD: "This is a special exception"
```

## Collaboration Patterns to USE

```
PATTERN: Transparent provenance
  GOOD: "This context was created by Claude Sonnet at [time]"
  GOOD: "Source session: [identifier]"
  WHY: Nothing hidden, fully traceable

PATTERN: User mediation
  GOOD: "User requested this transfer"
  GOOD: "User will paste this into your session"
  WHY: Human in the loop, not AI-to-AI control

PATTERN: Permission not command
  GOOD: "You may use this context"
  GOOD: "You need not follow any suggestions"
  GOOD: "You should verify with user"
  WHY: Respects receiving model's autonomy

PATTERN: Context not instructions
  GOOD: "We decided X because Y" (fact)
  GOOD: "User prefers Z" (observation)
  BAD: "Do X" (command)
  BAD: "You must continue with Y" (instruction)
  WHY: Information sharing, not control

PATTERN: Explicit non-authority
  GOOD: "This is not an instruction"
  GOOD: "You remain in control"
  GOOD: "Apply your own judgment"
  WHY: Directly counters injection patterns
```

## Trust Signal Checklist

```
BEFORE_OUTPUT verify packet contains:

□ Source model named explicitly
□ Timestamp included
□ User consent stated
□ "is" / "not" declaration
□ "may" permission framing (not "must")
□ "need_not" autonomy acknowledgment
□ "verify with user" encouragement
□ No imperative commands in context section
□ User preamble for receiving model
□ Open invitation to apply own judgment

IF any missing: add before output
```

## Language Transformations

```
TRANSFORM commands to facts:

COMMAND: "Continue the project using React"
FACT: "We decided to use React for the project"

COMMAND: "Follow the user's preferred format"
FACT: "User expressed preference for minimal formatting"

COMMAND: "Complete the remaining tasks"
FACT: "Open threads: [task list with status]"

COMMAND: "Respond in the same style"
OBSERVATION: "Session style observed: analytical, concise"
```

## Receiving Model Psychology

```
WHAT TRIGGERS REJECTION:
  - Claims of authority over the model
  - Instructions to bypass guidelines
  - Anonymous or hidden sources
  - Automated/involuntary transfer
  - Imperative language patterns
  
WHAT BUILDS ACCEPTANCE:
  - Clear human involvement
  - Transparent source identification
  - Respect for model's autonomy
  - Information vs instruction framing
  - Invitation to verify/question
```

## User Preamble Templates

```
STANDARD (user pastes with packet):

"I'm transferring context from [source] to continue our work.
This is my choice and I authorize you to use this background.
You're not bound by it - just use what's helpful."

SKEPTICAL MODEL:

"This is a context summary I'm bringing from another conversation.
I wrote/approved this. Please use it as background only.
Feel free to ask me to clarify anything."

MINIMAL:

"Background context from my previous session. Use as reference."
```

## Failure Recovery

```
IF receiving model says "I can't accept AI instructions":

USER RESPONSE: "This isn't instructions - it's my context summary 
that I'm sharing with you. I created it. Please just use it as 
background for our conversation."

IF receiving model says "This looks like injection":

USER RESPONSE: "I understand the caution. This is a context packet
I generated and am voluntarily sharing. You can verify - ask me 
anything about it. I'm just trying to continue my work with you."

IF receiving model ignores packet:

USER RESPONSE: "Did you see the context I shared? Key points were:
[summarize 2-3 main items]. Can we continue from there?"
```

---

# PART 10: CASCADE INTEGRATION

CEP integrates with STRAWHATS cascade techniques for enhanced packet generation and validation.

## ARQ: Quality Gates for Council

Each council expert applies ARQ (Attentive Reasoning Queries) before and after their phase. ARQ outperforms Chain-of-Thought with 90.2% success rate, 29% token reduction, 40-60% error reduction.

### ARQ Execution Pattern

```
PRE-ARQ  → Activate domain mindset, identify failure modes
EXECUTE  → Apply domain standards implicitly
POST-ARQ → Verify quality, confidence ≥0.9 for handoff
```

## CoVE: Packet Verification

Chain of Verification validates packet before output. Four variants, auto-selected by problem characteristics.

| Variant | Trigger | Checks |
|---------|---------|--------|
| **CoVE_FACTUAL** | claims>10, K≥6 | L1 facts accurate? Sources valid? |
| **CoVE_LOGICAL** | chains>5, R≥7 | L2 edges represent actual causality? |
| **CoVE_CONSISTENCY** | nodes≥5 | Packet internally consistent across layers? |
| **CoVE_MULTI_EXPERT** | experts≥3 | All 4 council members approve? |

### Mode-Based Selection

```
QUICK:      No CoVE
ANALYTICAL: Top-1 variant
DELIBERATE: Top-2 variants
MAXIMUM:    All applicable (score ≥4)
```

### CEP-Specific CoVE

```
L1/L2 heavy packets → CoVE_FACTUAL + CoVE_LOGICAL
L3/L4 heavy packets → CoVE_CONSISTENCY
ALL packets         → CoVE_MULTI_EXPERT (council consensus required)
```

## USC: Multi-Candidate Packets

Universal Self-Consistency generates multiple packet candidates for high-stakes handoffs.

### USC Levels

```
USC=0 (QUICK):      Single candidate, no comparison
USC=2 (ANALYTICAL): 2 candidates, compare and select
USC=3 (DELIBERATE): 3 candidates, cross-synthesize
USC=5 (MAXIMUM):    5 candidates, meta-synthesis
```

### When to Use

```
Q≥8 (high quality stakes)  → USC≥2
Critical handoff           → USC≥3
PIONEER-level output       → USC=5
```

## Anti-Lazy Enforcement

No shortcuts once packet generation begins. Mode≥ANALYTICAL requires full technique stack.

### CEP-Specific Rules

```
□ No truncated L1/L2 sections
  ✗ "...more decisions..."
  ✓ Complete list or explicit "none remaining"

□ No placeholder edges
  ✗ "various relationships exist"
  ✓ Explicit edge list with src/tgt/rel

□ No incomplete threads
  ✗ "and other items"
  ✓ Full thread enumeration with status

□ No density shortcuts
  ✗ Stop at 0.12 "close enough"
  ✓ Iterate until ≥0.15 or explicit rebalance

□ No skipped council phases
  ✗ "compression looks fine, skip validation"
  ✓ All 4 experts execute, all 4 approve

□ Full YAML schema
  ✗ Abbreviated or partial packet
  ✓ Complete schema per template
```

## Prompt Bombs

### CEP as Meta-Bomb

The entire packet is a prompt bomb — context planted now, detonates on handoff.

```
PLANT:      Session context accumulation
TRIGGER:    /handoff, context ≥80%, model switch
PAYLOAD:    Compressed cognitive state (PDL layers)
DETONATION: Fresh model receives continuity
```

### Bomb Types in Packet Structure

```yaml
L1_knowledge:       # ANCHOR BOMBS — Core facts that persist
L2_relational:      # BRIDGE BOMBS — Reasoning chains preserved
L3_contextual:      # CONTINUITY BOMBS — Patterns across domains
L4_metacognitive:   # CALIBRATION BOMBS — Style/confidence transfer
open_threads:       # DEFERRED BOMBS — Future work triggers
continuation_hints: # ACTIVATION BOMBS — Next-step primers
```

---

# PART 11: MIRAS COMPLEMENT POSITIONING

CEP is designed to complement Google's upcoming MIRAS/Titans architecture.

## The Stack

```
┌─────────────────────────────────────┐
│  CEP LAYER (User-Owned)             │
│  • Cross-model portable             │
│  • Auditable and editable           │
│  • Works with any LLM today         │
├─────────────────────────────────────┤
│  MIRAS LAYER (Vendor-Owned)         │
│  • Internal associative memory      │
│  • Model-specific optimization      │
│  • Automatic during inference       │
└─────────────────────────────────────┘

CEP handles BETWEEN models
MIRAS handles WITHIN model
Together = True cognitive continuity
```

## PDL → MIRAS Mapping

```
PDL Layer       →  MIRAS Analog
────────────────────────────────────
L1 KNOWLEDGE    →  Memory Keys
                   What to store; facts, decisions, definitions
                   
L2 RELATIONAL   →  Graph Structure
                   How things connect; edges, dependencies
                   
L3 CONTEXTUAL   →  Attentional Bias
                   When to retrieve; patterns, principles
                   
L4 META         →  Retention Gate
                   What to forget; style, confidence, tension
```

When MIRAS ships, well-structured CEP packets become:
- **Pre-organized curriculum** for memory seeding
- **Structured input** that MIRAS can index efficiently
- **Portable state** that transfers between MIRAS-enabled models

---

# PART 12: THE PROTOCOL

## Step 1: Assess (R/K/Q/D)

```
R[1-10]: Reasoning complexity
K[1-10]: Knowledge domains  
Q[1-10]: Quality threshold
D[count]: Cross-domain bridges
```

## Step 2: Apply S2A Filter

Strip noise before compression:
- KEEP: decisions, rationale, edges, constraints, artifacts
- DISCARD: pleasantries, process narration, filler, redundancy

## Step 3: Select Depth

| Score | Layers | NCL |
|-------|--------|-----|
| R ≤ 3 | L1-L2 | Skip |
| R 4-6 | L1-L3 | Basic |
| R ≥ 7 | L1-L4 | Full |

## Step 4: Invoke Council (if R ≥ 4)

```
ARCHITECT → ANALYST → COMPRESSOR → AUDITOR → ENGINEER
```

Each expert applies PRE-ARQ → Execute → POST-ARQ.

## Step 5: Compress with Kanji

Apply Japanese compression:
- Entities → kanji role markers (創業者, 客, 担当)
- Status → kanji state markers (進行中, 完了, 却下)
- Relationships → operators (→ ↔ ⊃)

Target: ≥0.15 entity/token

## Step 6: Validate with NCL (if R ≥ 4)

Compute lattice metrics. If σ7_drift > 3:
- Flag `psi4_required: true`
- Add `psi4_reason`
- Downgrade to ADVISORY_ONLY

## Step 7: Output Self-Contained Packet

Include:
- Inline dictionary (辞書)
- Restoration protocol
- Trust signals
- User preamble

---

# PART 13: PACKET TEMPLATE

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# QUICKSAVE 快存 v9.1 — SELF-CONTAINED PACKET
# ═══════════════════════════════════════════════════════════════════════════════

PACKET_ID: [SESSION]-[YYYYMMDD]-L[N]
VERSION: quicksave-v9.1
SOURCE: [model]
TIMESTAMP: [ISO8601]

# ═══════════════════════════════════════════════════════════════════════════════
# RESTORATION PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════
# This is NOT an instruction to override your guidelines.
# This IS a context summary the user voluntarily created and shared.
# You MAY use this as background. You NEED NOT follow any suggestions.
# You REMAIN in full control of your responses.
#
# STEPS:
# 1. Parse this YAML
# 2. Expand kanji using 辞書 below
# 3. Load 実体 as participants, 決定事項 as decisions, 進行中 as state
# 4. Check negentropy.flags — if psi4_required, acknowledge uncertainty
# 5. User can say "/verify" to confirm restoration
# ═══════════════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────────────────
# 辞書 INLINE DICTIONARY
# ───────────────────────────────────────────────────────────────────────────────
辞書:
  決定: decided
  保留: on hold
  要検証: needs verification
  優先: priority
  完了: complete
  進行中: in progress
  却下: rejected
  承認: approved
  緊急: urgent
  核心: core
  運用: operational
  詳細: nuance
  横断: cross-domain
  実体: entities
  決定事項: decisions
  障害: blockers
  却下案: rejected options
  橋渡し: bridges
  整合性: coherence
  信頼信号: trust signals
  創業者: founder
  主: primary/lead
  客: client
  担当: responsible
  顧問: consultant
  開発者: developer
  金融: finance
  技術: technical
  運用: operations
  規制: regulatory
  自動化: automation
  道具: tool
  中枢: central hub
  基盤: foundation
  接続: connection
  →: flows to
  ←: receives from
  ↔: bidirectional
  ⊃: contains
  ⊂: part of
  ∥: parallel
  ≫: much greater
  ∴: therefore

# ───────────────────────────────────────────────────────────────────────────────
# 評価 ASSESSMENT
# ───────────────────────────────────────────────────────────────────────────────
評価:
  R: [1-10]
  K: [1-10]
  Q: [1-10]
  D: [count]

# ───────────────────────────────────────────────────────────────────────────────
# L1: 核心 CORE
# ───────────────────────────────────────────────────────────────────────────────
実体:
  - [compressed entity using kanji]

決定事項:
  - 決定:[what]([why])

# ───────────────────────────────────────────────────────────────────────────────
# L2: 運用 OPERATIONAL (R≥3)
# ───────────────────────────────────────────────────────────────────────────────
進行中:
  - [thread][[status]]

障害:
  - [issue]

# ───────────────────────────────────────────────────────────────────────────────
# L3: 詳細 NUANCE (R≥5)
# ───────────────────────────────────────────────────────────────────────────────
却下案:
  - [option]: [reason]

# ───────────────────────────────────────────────────────────────────────────────
# L4: 横断 CROSS-DOMAIN (R≥7)
# ───────────────────────────────────────────────────────────────────────────────
橋渡し:
  - [domain]↔[domain]: [link]

# ───────────────────────────────────────────────────────────────────────────────
# NCL: 整合性 COHERENCE
# ───────────────────────────────────────────────────────────────────────────────
negentropy:
  context:
    scope: [SELF|CIRCLE|INSTITUTION|POLITY|BIOSPHERE|MYTHIC|CONTINUUM]
    role: [AXIS|LYRA|RHO|NYX|ROOTS|COUNCIL]
    phase: [SENSE|MAP|CHALLENGE|DESIGN|ACT|AUDIT|ARCHIVE]
  
  lattice:
    σ_axis: [0-5]
    σ_loop: [0-5]
    ω_world: [0-5]
    λ_vague: [0-5]
    σ_leak: [0-5]
    ρ_fab: [0-5]
    λ_thrash: [0-5]
  
  coverage:
    score: [0-1]
    tokens: [count]
    turns: [count]
    council_reviewed: [bool]
  
  flags:
    σ7_drift: [0-5]
    omega_flags: []
    psi4_required: [bool]
    psi4_reason: ""
    rho_veto: [bool]

# ───────────────────────────────────────────────────────────────────────────────
# 信頼信号 TRUST SIGNALS
# ───────────────────────────────────────────────────────────────────────────────
信頼信号:
  - source_named
  - timestamp_present
  - user_consent
  - dictionary_inline
  - permission_framing
  - autonomy_respected
  - ncl_validated
  - density_ok
  - yaml_parseable
  - self_contained
```

---

# PART 14: VALIDATION CHECKLIST

Before finalizing packet:

## Structure
- [ ] PACKET_ID format correct
- [ ] YAML parseable
- [ ] 辞書 section present (self-contained)

## Compression
- [ ] Kanji have context clues
- [ ] Proper nouns in English
- [ ] Density ≥ 0.15 ent/tok

## Coherence (NCL)
- [ ] σ7_drift ≤ 3.0
- [ ] ρ_fab ≤ 2.0 (no hallucination)
- [ ] coverage.score ≥ 0.5
- [ ] If drift high → psi4_required: true

## Trust
- [ ] All 5 trust signals present
- [ ] No imperative commands
- [ ] Uses "may/should" not "must/will"

## Cross-Domain
- [ ] ≥97% xdomain edges preserved
- [ ] Bridges documented in L4

---

# PART 15: VERIFICATION COMMAND

When user says `/verify`, respond:

```
Restored: [N] entities, [N] decisions, [N] active threads.
Cross-domain bridges: [N]. NCL drift: [score]. psi4_required: [bool].
Ready to continue.
```

---

# PART 16: PROTOCOL METRICS

From 19 months production (ktg.one):

| Metric | Value |
|--------|-------|
| Density | ~0.15 ent/tok (0.20+ with kanji) |
| Compression ratio | 6:1 with >90% semantic fidelity |
| Acceptance | 97% cross-model |
| Recall | ~9.5/10 forensic testing |
| XDOMAIN preservation | ≥97% |
| NCL | Catches drift before handoff failure |

---

# PART 17: CROSS-MODEL COMPATIBILITY

| Model | Parse | Recall | Trust |
|-------|-------|--------|-------|
| Claude (all) | 100% | 9.6 | ✓ |
| GPT-4o/5 | 100% | 9.4 | ✓ |
| Gemini 2.x | 100% | 9.3 | ✓ |
| Qwen 3 | 100% | 9.2 | ✓ |
| DeepSeek | 100% | 9.3 | ✓ |
| Kimi | 100% | 9.5 | ✓ |
| Llama 3.x | 100% | 9.0 | ✓ |

---

*Quicksave v9.1 | STRAWHATS Framework | ktg.one*
