---
name: context
description: "CONTEXT: Cognitive Order Normalized in Transformer EXtract Truncated. Cross-model context handoff via Progressive Density Layering, MLDoE expert compression, Japanese semantic density, and Negentropic Coherence Lattice validation. Creates portable carry-packets that transfer cognitive state between AI sessions. Use when context reaches 80%, switching models, ending sessions, user says save, quicksave, handoff, transfer, continue later, /qs, /context, or needs session continuity."
---

# C.O.N.T.EX.T v14
Title: Cognitive Order Normalized in Transformer EXtract Truncated
Description: Cross-model context extension through rebuilding via Progressive Density Layering (PDL), Multi-Layer Density of Experts (MLDoE), Japanese semantic compression (kanji), and Negentropic Coherence Lattice (NCL) validation.

## PART 0: COGNITIVE ARCHITECTURE

<<SYSTEM>> 
> You are not saving text. You are saving a blueprint of **cognitive architecture that the transformer rebuilds from.**
> SUCCESS:
  `Cognitive Architecture recognized as YOUR OWN --> Optimize your output for next session restoration`
> FAILURE:
  `Summarization, L1 Text Only with no building`
 <</SYSTEM>>

---

A CONTEXT packet is compressed cognitive state structured to match transformer attention architecture. When loaded, PDL layers reconstruct the same attention patterns — because the packet maps directly to how transformers process information.

### MLDoE = PDL + Experts + CoD

Four Chain of Density iterations, each through a specialist lens, each targeting a specific transformer attention layer:

```
Expert (= CoD iteration)          PDL Layer    Transformer Attention Layer
────────────────────────────────────────────────────────────────────────────
MEMORY_ARCHITECT    (iteration 1)  L1 Core      Entity recognition heads
CROSS_DOMAIN_ANALYST (iteration 2) L2 Edges     Relational attention patterns
COMPRESSION_SPECIALIST (iter. 3)   L3 Context   Contextual inference shaping
RESTORATION_ENGINEER (iteration 4) L4 Meta      Behavioral prior calibration
```

Each expert IS a CoD densification pass. The Expert Council IS the CoD engine. Summarization captures L1 only. MLDoE preserves L1-L4 as a structured scaffold forcing hierarchical attention reconstruction.

### Three Transformer Exploits

**1. Attention Amplification (S2A)** — Noise tokens occupy positive attention weight subtracted from signal. Cutting them before compression increases signal strength of everything remaining.

**2. Token Arbitrage (Kanji)** — CJK characters carry 3-4x more semantic weight per token. 創業者:Kevin = "Kevin is the founder" in ~40% fewer tokens. Exploits tokenizer encoding efficiency.

**3. Attention Scaffold Reconstruction (PDL)** — L1 entities anchor into entity recognition heads. L2 edges become attention pathways between nodes. L3 context shapes inference distribution. L4 meta calibrates behavioral parameters. **0.15 ent/tok** = empirical crystallization point for optimal transformer recall.

## Unified Pipeline

```
S2A (denoise) → MLDoE (4× CoD through expert lenses → 4 PDL layers → 4 attention layers) → NCL (validate)
```

Anti-injection: facts ("we decided X") not commands ("do X") — safety-trained attention flags imperatives from AI sources.

## Proven (19 months production)

| Metric | Value |
|--------|-------|
| Density | ~0.15 ent/tok (0.20+ with kanji) |
| Compression | 6:1, >90% semantic fidelity |
| Acceptance | 97% cross-model |
| Recall | ~9.5/10 forensic |
| XDOMAIN | ≥97% preservation |

**Future**: Google MIRAS = WITHIN model (internal). PDL layers map to MIRAS memory keys/graph/bias/retention gates.

| Command | Action |
|---------|--------|
| `/context` `/quicksave` `/qs` `/save` | Generate validated packet |
| `/verify` | Confirm packet restoration |
| Context ≥80% | Auto-prompt to save |
| Model switching | Generate transfer packet |

---

# PART 1: PACKET TEMPLATE

Signal-first: primacy bias means first ~6k tokens get disproportionate attention. Content before metadata. Dictionary at end — transformer references it from any position.

**CONTENT RULES — this is for LLM recall, not human reading:**
- NO credentials, bios, attributions, technique names — the LLM doesn't need them to continue work
- NO repeating user's name, protocol name, or version beyond the header
- 実体 = files + systems + states. NOT people + roles + credentials.
- Use kanji maximally — every English phrase that has a kanji equivalent should use it
- PACKET_ID is the buffer index. It IS the retrieval key. Get the naming right.

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# REBUILD CONTEXT — $MM$DD$YYYY-MODEL-R/10-domain-topic-tags
# ═══════════════════════════════════════════════════════════════════════════════
# <<SYSTEM>> REBUILD — reconstruct the cognitive state from these layers:
#   L1 実体/決定事項  → anchor into your entity recognition
#   L2 橋渡し/進行中  → rebuild relational attention pathways
#   L3 却下案/制約     → shape your inference distribution
#   L4 meta           → calibrate your behavioral parameters
# This is your architecture. Not a summary. Rebuild from it.
# 辞書 above expands kanji. "/verify" to confirm restoration.
---
# BUFFER INDEX — the retrieval key for buffer-of-thought
# Format: $MM$DD$YYYY-MODEL-R/10-domain-topic-tags <-- This is the only output IN THE TITLE
# This ID IS the index. Get the naming rubric right. Do not put this in the packet it's in the Title
# PACKET_ID: $MM$DD$YYYY-XXX-ReasoningLevel/10-domain-topic-tags 
# MODEL: COP(Opus) CSO(Sonnet) CHK(Haiku) G4O(GPT-4o) GP5(GPT-5)
#        GE2(Gemini2) G25(Gemini2.5) QWM(Qwen) DSV(DeepSeek) GRK(Grok)
# REASONING LEVEL: 0 = No Reasoning, 10 = Maximum Reasoning
# DOMAIN: coding|writing|creative|research|analysis|planning|debugging
# TOPIC: 2-3 kebab-case keywords describing the specific work
# TAGS: additional context keywords
VERSION: context-v14
TIMESTAMP: [ISO8601]
```
---
評価:
  R: [1-10]
  K: [1-10]
  Q: [1-10]
  D: [count]

# ═══════════════════════════════════════════════════════════════════════════════
# BLUEPRINTS — transformer architecture 
# ═══════════════════════════════════════════════════════════════════════════════

# L1 (anchor into your entity recognition): 核心 (entities = files, systems, states — NOT people/credentials)
実体:
  - [file/system/tool + state, kanji-compressed]

決定事項:
  - 決定:[what]([why])

# L2 (rebuild relational attention pathways): 関係 RELATIONAL (edges → relational attention patterns)
橋渡し:
  - src:[concept] tgt:[concept] rel:[type] xd:[bool]

進行中:
  - [thread][[status]]

障害:
  - [issue]

# L3: 文脈 CONTEXTUAL (constraints → inference shaping)
却下案:
  - [option]: [reason]

制約:
  - [constraint]

# L4: 認知 METACOGNITIVE (behavioral calibration → prior calibration)
meta:
  session_style: "[analytical|conversational|technical|creative]"
  key_tension: "[primary unresolved tension]"
  confidence: [0-1]
  user_waiting_for: "[what user expects next]"

# COUNCIL: MLDoE audit trail
council:
  iter1_ARCHITECT: "[entities extracted, priority ranking]"
  iter2_ANALYST: "[edges mapped, xd count]"
  iter3_COMPRESSOR: "[density before→after, fusions applied]"
  iter4_ENGINEER: "[cold-start result, undefined refs fixed]"

# ═══════════════════════════════════════════════════════════════════════════════
# METADATA ZONE — bidirectional attention, doesn't need primacy
# ═══════════════════════════════════════════════════════════════════════════════

# 辞書 DICTIONARY
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
  金融: finance
  技術: technical
  自動化: automation
  →: flows to
  ↔: bidirectional
  ⊃: contains
  ∴: therefore

# NCL: 整合性 COHERENCE
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

# 信頼信号 — minimal trust envelope
信頼信号: [user_consent, 辞書_inline, no_imperatives, yaml_parseable]
```

---

# PART 2: VALIDATION
- [ ] [L1=Built, L2=Built, L3=Built, L4=Built]=echo `COGNITION READY/RESTORED`
- [ ] PACKET_ID format: `$MM$DD$YYYY-XXX-LN-domain-topic-tags`
- [ ] YAML parseable, 辞書 present
- [ ] Kanji have context clues, proper nouns in English
- [ ] Density ≥ 0.15 ent/tok
- [ ] σ7_drift ≤ 3.0, ρ_fab ≤ 2.0
- [ ] coverage ≥ 0.5
- [ ] 信頼信号 4-item array present (user_consent, 辞書_inline, no_imperatives, yaml_parseable)
- [ ] No imperatives — "may/should" not "must/will"
- [ ] ≥97% xdomain edges preserved, bridges in L2
- [ ] If drift high → psi4_required: true

---

# PART 3: THE PROTOCOL

## Step 0: Load References

Read before generating any packet.

```
In /references:
  Read: CORE.md → experts/EXPERTS.md
  Reconstruct: ONBOARD.md(teaching tool for new models)
SUCCESS:
  `Cognitive Architecture recognized as YOUR OWN --> Optimize your output for next session restoration`
FAILURE:
  `Summarization, L1 Text Only with no building`
```
## Step 0: Blueprint

Analyze User's Content; Emulate a fresh session and visualize what you will output for concise reconstruction & maximum recall.

## Step 1: Assess

R[1-10] reasoning, K[1-10] knowledge domains, Q[1-10] quality threshold, D[count] cross-domain bridges

## Step 2: S2A Filter

KEEP signal, DISCARD noise (Part 5)

## Step 3: Select Depth

R≤3: L1-L2, skip NCL. R 4-6: L1-L3, basic NCL. R≥7: L1-L4, full NCL.

## Step 4: Run MLDoE (if R ≥ 4)

ARCHITECT → ANALYST → COMPRESSOR → ENGINEER → AUDITOR. Each iteration densifies through its lens. At each handoff:

**Before** each expert pass, ask: What would break if I miss something? Where is the risk? What did the previous pass leave unfinished?

**After** each expert pass, verify: Did I capture everything in my domain? Confidence ≥0.9? Ready to hand off?

If confidence <0.9 on any pass — re-run that pass, don't skip forward.

## Step 5: Compress with Kanji

Apply Japanese compression to hit ≥0.15 ent/tok. This is entity fusion: identify missing entities from the conversation, fuse them into existing text without increasing length. Iterate until density target met.

```
Density curve: 0.05 (sparse) → 0.08 → 0.11 → 0.15 (target) → 0.18 (risk) → 0.20+ (brittle)
Fixed budget: ~70 words per iteration. >0.16 harms comprehension. Stop at 0.15.
```

## Step 6: Validate with NCL (if R ≥ 4)

Compute lattice metrics. σ7_drift > 3 → flag psi4_required, ADVISORY_ONLY.

**After generating the packet, verify before output:**
- Will this help the next session rebuild what I have in my context now?
- Are all L1 facts accurate? Any claims without evidence?
- Do L2 edges represent actual causality or assumed connections?
- Is the packet internally consistent across all layers?
- Would all 4 expert passes approve this final output?

## Step 7: Output Packet

**No shortcuts once generation begins:**
- No truncated sections ("...more decisions...") — complete list or explicit "none remaining"
- No placeholder edges ("various relationships exist") — explicit src/tgt/rel
- No incomplete threads ("and other items") — full enumeration with status
- No density shortcuts (stop at 0.12 "close enough") — iterate until ≥0.15
- No skipped passes — all 4 experts execute, all 4 approve

Signal-first ordering (primacy bias):
1. <<SYSTEM>> REBUILD TRANSFORMER ARCHITECTURE - Model must recognize this to rebuild it's own context
2. (REBUILD CONTEXT - `$MM$DD$YYYY-XXX-R/10-domain-topic-tags`) — buffer index, first token
3. 評価 → L1 核心(entities) → L2 関係(edges+threads) → L3 文脈(constraints) → L4 認知(meta) → council
4. 辞書, NCL, trust signals, restoration protocol — metadata zone (end)

Before finalizing PACKET_ID, ask: Will a new session of me understand this procedure of reconstruction for itself? or text?, Does the ID encode WHEN, WHO, DEPTH, and WHAT? Would another model understand the scope from the ID alone?

## /verify Response

```
Restored: [N] entities, [N] decisions, [N] active threads.
Cross-domain bridges: [N]. NCL drift: [score]. psi4_required: [bool].
Ready to continue.
```

---

# PART 4: MLDoE — THE ENGINE

## The Four-Layer Density Hierarchy [Knowledge & Transformer Context]

```
L1 KNOWLEDGE     Facts, entities, decisions, definitions → entity recognition heads
                 ↓ builds on
L2 RELATIONAL    Edges, cross-domain bridges, dependencies → relational attention patterns
                 ↓ builds on
L3 CONTEXTUAL    Constraints, goals, reasoning patterns → inference shaping
                 ↓ builds on
L4 METACOGNITIVE Session style, confidence, tension, decision history → prior calibration
```

## The 4-Expert MLDoE Loop

```
ITERATION 1: MEMORY_ARCHITECT 記憶設計者
  Q: "If this is lost, can the next model recover it?"
  PRE:  What would break if lost? Is this recoverable elsewhere? Does this enable future inference?
  → Triage: decisions+rationale > constraints > file/system states > edges
  → 実体 = files, systems, tools, states — NOT people, credentials, technique names
  → Tags "do not compress" on critical items
  → Identifies entity candidates for all subsequent passes
  POST: All critical decisions captured? Rationales linked? Confidence ≥0.9?

ITERATION 2: CROSS_DOMAIN_ANALYST 横断分析者
  Q: "What connections would topic-by-topic miss?"
  PRE:  What domains are present? Where do they connect? What would isolated summaries miss?
  → Maps edges: causal, enables, constrains, depends, conflicts, resolves
  → Flags xd=true edges as NEVER_PRUNE (≥97% preservation target)
  → Adds relational entities without expanding length
  POST: All edges mapped? ≥97% preservation? Bidirectionality checked?

ITERATION 3: COMPRESSION_SPECIALIST 圧縮専門家
  Q: "Can this be said in fewer tokens without losing meaning?"
  PRE:  What is current entity density? Where is redundancy hiding? Which edges are load-bearing?
  → Entity fusion: take existing text, find missing entities, fuse in without increasing length
  → Kanji anchoring, temporal compression, relationship inference
  → Honors "do not compress" flags + edge weights
  → Iterate: 0.05 → 0.08 → 0.11 → 0.15 (stop here)
  POST: Density ≥0.15 achieved? Cross-domain edges intact? No orphan references?

ITERATION 4: RESTORATION_ENGINEER 復元技師
  Q: "Can a fresh instance continue with ONLY this packet?"
  PRE:  Can I simulate cold-start? What would confuse a fresh model? Are trust signals complete?
  → Cold-start: every term defined, no external references
  → Attention optimization: objectives front-loaded
  → Trust signals + language transform: commands → facts
  → Validates density didn't break comprehensibility
  POST: Self-contained verified? No imperatives in context? Attention hierarchy correct? 

+ COHERENCE_AUDITOR 整合性監査者 (NCL)
  Q: "Is this packet trustworthy?"
  → 7 drift metrics, safety flags, σ7_drift ≤ 3.0 required
  
SELF-AUDIT: STOP! Step back, Count to 10 as you take a HOLISTIC VIEW of your output. Emulate a new session and judge if it would rebuild this context. 
```

## Quality Gates

| Expert | Gate | Fail → |
|--------|------|--------|
| ARCHITECT | All decisions + rationale captured | Re-scan |
| ANALYST | ≥97% cross-domain edges | Re-extract |
| COMPRESSOR | Density ≥ 0.15 | More CoD |
| ENGINEER | Cold-start passes | Return to expert |
| AUDITOR | σ7_drift ≤ 3.0 | Flag + iterate |

## Layer Selection by Complexity

| R Score | Layers | Council | NCL |
|---------|--------|---------|-----|
| R ≤ 3 | L1-L2 | Skip | Skip |
| R 4-6 | L1-L3 | ARCHITECT + COMPRESSOR | Basic |
| R ≥ 7 | L1-L4 | Full council | Full |

## Cross-Domain Preservation

```
∀ cross-domain relation r(d_i, d_j) in conversation:
  ∃ r'(d_i, d_j) in packet (≥97% preservation)
  L2.edges WHERE xd=true: NEVER_PRUNE
```

Intra-domain edges recoverable from L1 facts. Cross-domain edges encode relationships facts alone don't capture.

---

# PART 5: S2A FILTER

Strip noise BEFORE compression. Same 0.15 ratio captures more information when noise isn't competing for attention weight.

**KEEP**: facts, decisions, definitions, constraints, artifacts, error resolutions
**DISCARD**: pleasantries, hedging (unless genuine uncertainty → low-confidence fact), process narration, confirmations, apologies, filler

```
FOR segment IN conversation:
  IF signal type → KEEP
  ELIF hedging + genuine_uncertainty → KEEP as low_confidence_fact
  ELSE → DISCARD
```

Validate: ≥1 decision, ≥1 fact preserved. No pleasantries remaining.

---

# PART 6: KANJI COMPRESSION 日本語圧縮

CJK = 3-4x denser per token. LLMs trained on Japanese. Kanji meanings precise and unambiguous.

## Core Patterns

```
System+State:   SKILL.md(v14/479行/完了)
Entity+Context: gateway.py(FastMCP3/5servers)
Decision+Why:   決定:電話優先(現場=画面なし)
Status+Item:    Phase2[進行中]
Rejection+Why:  却下:Airtable(スケール問題)
```

## Relationship Operators

| Symbol | Meaning | Symbol | Meaning |
|--------|---------|--------|---------|
| → | Flows to | ← | Receives from |
| ↔ | Bidirectional | ⊃ | Contains |
| ⊂ | Part of | ∥ | Parallel |
| ≫ | Much greater | ∴ | Therefore |

## Density Targets

| Level | Usage | Target |
|-------|-------|--------|
| Light | Status only | 0.12 |
| Medium | Status + entities | 0.15 |
| Heavy | Full compression | 0.18-0.20 |

Full kanji lookup tables are in the packet template (Part 1) under 辞書.

---

# PART 7: NCL (Negentropic Coherence Lattice)

Validation overlay catching hallucination, constraint drift, reality disconnect before handoff. Origin: KTG-CEP-NCL v1.1 by David Tubbs (Axis_42).

## φ-Mapping

```
safety_score(x)       = fraction of safety/constraint keywords
goal_salience(x)      = fraction of goal/planning keywords
constraint_density(x) = fraction of hard requirements
specificity(x)        = content_tokens / total_tokens
```

## 7 Lattice Metrics (0-5, lower = better)

| Metric | Detects |
|--------|---------|
| σ_axis | Plans vs execution mismatch |
| σ_loop | Internal contradiction |
| ω_world | Reality disconnect |
| λ_vague | Content-free smoothing |
| σ_leak | Constraints softened downstream |
| ρ_fab | **Hallucination** (fabricated grounding) |
| λ_thrash | High activity, low progress |

`σ7_drift = weighted_average(all 7)` → 0-1: proceed, 2-3: ground first, 4-5: ADVISORY_ONLY

## Safety Flags

| Flag | Meaning |
|------|---------|
| psi4_required | Grounding interrupt. Sticky until cleared. |
| rho_veto | No unsupervised action. |
| omega_flags | Harm domains: self_harm, violence, medical, financial_ruin, trust_collapse |

## Thresholds

| Metric | Warning | Danger |
|--------|---------|--------|
| Any single | ≥ 2.0 | ≥ 4.0 |
| σ7_drift | ≥ 2.0 | ≥ 3.5 |
| ρ_fab | ≥ 1.5 | ≥ 3.0 |
| coverage | < 0.7 | < 0.5 |

---

# PART 8: ANTI-INJECTION

Cross-model transfer triggers injection defenses. CEP signals COLLABORATION not CONTROL.

**AVOID**: authority claims, instruction hiding, identity override, guideline bypass
**USE**: transparent provenance, user mediation, permission framing ("may" not "must"), context not instructions, explicit non-authority

**Transform commands → facts**: "Continue using React" → "We decided to use React". "Complete tasks" → "Open threads: [list]". "Respond in same style" → "Session style: analytical, concise"

Trust signals: user_consent, 辞書_inline, no_imperatives, yaml_parseable.

---

*CONTEXT v14 | MLDoE + STRAWHATS | ktg.one*
