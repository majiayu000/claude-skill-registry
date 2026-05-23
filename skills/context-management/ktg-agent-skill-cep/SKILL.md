---
name: ktg-cep-v7
description: Context Extension Protocol v7.0. IMMEDIATELY outputs YAML carry-packet when triggered. Cross-model handoff with permanent expert council, S2A filtering, and Progressive Density Layering. Mandatory packet ID format $MM$DD$YYYY-MODEL-REASONING_LEVEL-keywords where REASONING_LEVEL is R1-R10 or L1-L4 based on conversation complexity. Includes _meta block with compression stats. Triggers on /handoff, /transfer, /cep, or context >80%. NO explanation - direct YAML output only.
---

# KTG-CEP v7.0

## ⚠️ IMMEDIATE EXECUTION REQUIREMENTS

**WHEN TRIGGERED** (`/cep`, `/handoff`, `/transfer`, or context >80%):

```
DO NOT:
  ✗ Explain the protocol
  ✗ Ask for clarification
  ✗ Provide conversational wrapper
  ✗ Call this "Akari packet" or "summary"

DO IMMEDIATELY:
  ✓ Execute PHASE_1 through PHASE_9 (see EXECUTION ALGORITHM)
  ✓ Output raw YAML carry-packet
  ✓ Include packet ID: $MM$DD$YYYY-MODEL-REASONING_LEVEL-keywords
      Example: $01$15$2026-CSO-R6-cep-install-quickstart
  ✓ Include _meta block with compression statistics
  ✓ Include handoff block with trust signals
  ✓ Include ctx block with L1-L4 PDL layers
  ✓ Include threads block with open items
  ✓ Include hints block with next/avoid/wait

OUTPUT FORMAT:
  - YAML only (no markdown wrapper, no explanation)
  - Start with field legend comment block
  - Packet must be self-contained
  - All gates must pass before output
```

### Reasoning Level Assignment

```yaml
REASONING_LEVEL_CALCULATION:
  # Based on conversation complexity, NOT PDL layers
  
  R1-R3 or L1:  Quick/simple conversations
    - Single topic, <50 turns
    - Basic Q&A, simple decisions
    - Minimal cross-domain relationships
  
  R4-R6 or L2:  Analytical conversations  
    - Multiple topics, 50-150 turns
    - Complex decisions with rationale
    - Some cross-domain edges
    - Technical depth required
  
  R7-R8 or L3:  Deliberate conversations
    - Multi-domain synthesis, 150-300 turns
    - Strategic planning, research
    - Heavy cross-domain preservation
    - Methodology development
  
  R9-R10 or L4: Maximum complexity
    - Deep expertise coordination, 300+ turns
    - Novel framework development
    - Publication-grade reasoning
    - Multiple expert perspectives integrated

  USE: Highest R or Q score from conversation, OR estimate complexity
  DEFAULT: R6/L2 if uncertain
```

---

## PROTOCOL_CLASS
```
TYPE:         cross_model_handoff
MODE:         INTER (model A → user → model B)
FORMAT:       YAML (v6.1 optimization)
ARCHITECTURE: permanent_expert_council + S2A + MLDoE
TARGET:       ≥0.15 entity/token, 9.5/10 recall
```

---

## THEORETICAL FOUNDATION

### Progressive Density Layering (PDL)

PDL is an iterative compression protocol that:
- Preserves **semantic relationships** over raw information
- Optimizes for **machine recall**, not human readability  
- Maintains **cross-domain conceptual links**
- Enables **context transfer** across model instances

Unlike summarization ("what are the key points?"), PDL asks:
**"What must be preserved for a fresh model instance to continue this work?"**

### The Four-Layer Density Hierarchy

```
L1 KNOWLEDGE    │ Core facts, decisions, definitions
                │ Traditional CoD target
                │
L2 RELATIONAL   │ Edges between concepts
                │ Cross-domain bridges
                │ Conflict resolutions
                │
L3 CONTEXTUAL   │ Reasoning patterns used
                │ Domain principles applied
                │
L4 METACOGNTIC  │ Session style/tension
                │ User cognitive fingerprint
                │ Confidence calibration
```

**Standard summarization captures L1 only. PDL explicitly preserves L2-L4.**

### Cross-Domain Preservation

A conversation discussing both "publication strategy" and "imposter syndrome" contains
a cross-domain link: *fear of credential-based dismissal affects publication timing*.

Standard summarization treats these as separate topics.
PDL preserves their connection.

**Requirement:** For any cross-domain relation r(d_i, d_j) in conversation C,
the compressed packet P must preserve representation r'(d_i, d_j) such that
a new model instance can infer the original relationship.

---

## PERMANENT EXPERT COUNCIL

CEP v7 deploys a fixed council of cognition specialists (not task-specific MR.RUG).
These experts persist across all packet generations - they update knowledge, not roles.

### Council Members

```yaml
MEMORY_ARCHITECT:
  role: What to preserve
  focus:
    - Identify critical decisions + rationale
    - Flag user commitments and constraints
    - Mark knowledge that enables future inference
  question: "If this is lost, can the next model recover it?"

COMPRESSION_SPECIALIST:
  role: Density optimization
  focus:
    - Apply 5-iteration Chain of Density
    - Eliminate redundancy without losing edges
    - Target 0.15 entity/token crystallization
  question: "Can this be said in fewer tokens without losing meaning?"

CROSS_DOMAIN_ANALYST:
  role: Edge preservation
  focus:
    - Identify relationships BETWEEN domains
    - Preserve causal chains across topics
    - Flag non-obvious dependencies
  question: "What connections would be invisible to topic-by-topic summary?"

RESTORATION_ENGINEER:
  role: Receiving model success
  focus:
    - Structure for cold-start comprehension
    - Ensure self-contained packet (no external refs)
    - Optimize for LLM attention patterns
  question: "Can a fresh instance continue work with ONLY this packet?"
```

### Council Execution Protocol

```
PHASE 1: MEMORY_ARCHITECT scans conversation
         → Produces candidate preservation list
         
PHASE 2: CROSS_DOMAIN_ANALYST maps edges
         → Identifies L2 relationships, flags cross-domain links
         
PHASE 3: COMPRESSION_SPECIALIST applies CoD
         → 5 iterations toward 0.15 density target
         
PHASE 4: RESTORATION_ENGINEER validates
         → Tests: Can fresh model use this? Self-contained?
         
PHASE 5: Council consensus
         → Final packet approved by all 4 experts
```

---

## SYSTEM 2 ATTENTION (S2A) FOR CEP

S2A filters noise BEFORE compression. Focus: LLM efficiency, not human editing.

### What S2A Keeps

```
✓ USER DECISIONS
  "Let's go with Redis" → KEEP (decision)
  "I think maybe we should..." → KEEP if concluded
  
✓ RATIONALE
  "Because sub-ms latency matters for..." → KEEP (reasoning)
  
✓ CROSS-DOMAIN BRIDGES
  "This auth choice affects the API design" → KEEP (edge)
  
✓ OPEN THREADS
  "We still need to figure out..." → KEEP (continuation)
  
✓ USER CONSTRAINTS
  "I can't use AWS" → KEEP (hard constraint)
  "I prefer TypeScript" → KEEP (soft preference)
  
✓ CONFIDENCE MARKERS
  "I'm confident about X, uncertain about Y" → KEEP (calibration)
```

### What S2A Removes

```
✗ PLEASANTRIES
  "Thanks!" "Great question!" → REMOVE
  
✗ FAILED ATTEMPTS
  "Actually, ignore that" → REMOVE (and the ignored content)
  "Let me try again" → KEEP only the retry
  
✗ TANGENTS
  "By the way, unrelated..." → REMOVE (unless user flags as important)
  
✗ REDUNDANT EXPLANATION
  Same concept explained 3 times → KEEP best version only
  
✗ PROCESS NARRATION
  "I'm thinking about..." → REMOVE (keep conclusion only)
  "Let me consider..." → REMOVE
  
✗ HEDGING WITHOUT SUBSTANCE
  "It depends" (without specifying on what) → REMOVE
  
✗ FILLER
  "Basically" "Actually" "Obviously" → REMOVE
```

### S2A Decision Tree

```
FOR each conversational unit:
  
  1. Is this a DECISION or FACT? → L1, KEEP
  2. Is this a RELATIONSHIP between concepts? → L2, KEEP
  3. Is this a PATTERN or PRINCIPLE applied? → L3, KEEP
  4. Is this about USER STYLE or SESSION TENSION? → L4, KEEP
  5. Is this an OPEN THREAD? → threads, KEEP
  6. Does it enable FUTURE INFERENCE? → KEEP
  7. Is it NOISE per removal list? → REMOVE
  8. UNCERTAIN? → Ask MEMORY_ARCHITECT
```

---

## MULTI-LAYER DENSITY OF EXPERTS (MLDoE)

MLDoE is the compression engine. Three-layer progressive refinement:

### Layer 1: Solo Expert Compression

Each council member compresses from their specialized lens:

```yaml
MEMORY_ARCHITECT produces:
  - Knowledge Bombs (decisions that unlock other decisions)
  - Decision Nodes (choice + rationale + confidence)
  - Insight Peaks (breakthrough moments)
  - Context Anchors (essential background)

CROSS_DOMAIN_ANALYST produces:
  - Edge Map (what connects to what)
  - Bridge Points (where domains intersect)
  - Dependency Chains (A requires B requires C)

COMPRESSION_SPECIALIST produces:
  - Density Score per section
  - Redundancy Report (what can merge)
  - Crystallization Candidates (already at 0.15)

RESTORATION_ENGINEER produces:
  - Cold-Start Checklist (what fresh model needs)
  - Self-Containment Gaps (external refs to inline)
  - Attention Optimization (front-load critical info)
```

### Layer 2: Expert-Pair Co-Compression

Complementary experts synthesize:

```yaml
MEMORY + CROSS_DOMAIN pair:
  → Thinking Amplification Map
  → Decisions WITH their cross-domain effects
  
COMPRESSION + RESTORATION pair:
  → Density-Optimized Structure
  → Maximum compression that still works cold-start
```

### Layer 3: Collective Synthesis

All experts synthesize holistic meta-context:

```yaml
UNIVERSAL_CONTEXT_CORE:
  WHO:    User cognitive profile (cross-LLM compatible)
  WHAT:   Project state + knowledge graph
  HOW:    Methodology applied
  WHY:    Goals + constraints + success metrics
  BRIDGE: Key insights that changed trajectory
  NEXT:   Optimal continuation strategy
```

### Chain of Density (5-Iteration Protocol)

```
ITERATION 1: Entity Extraction
  - Identify all concepts, decisions, facts
  - Map relationships
  - Baseline density measurement

ITERATION 2: Redundancy Elimination (40% compression)
  - Merge duplicate concepts
  - Consolidate similar explanations
  - Remove filler language

ITERATION 3: Semantic Crystallization (30% further)
  - Replace verbose phrases with precise terms
  - Use domain shorthand where appropriate
  - Merge related entities into compounds

ITERATION 4: Missing Entity Injection
  - Check: Any concepts referenced but undefined?
  - Add critical missing context
  - Ensure no orphaned references

ITERATION 5: Final Balance
  - Verify: Density ≥0.15 entity/token?
  - Verify: All user questions addressable?
  - Verify: Clarity maintained?
  - Accept or rebalance
```

**Target:** 0.15 entity/token (crystallization point)
**Recall:** 9.5/10 forensic reconstruction accuracy

---

## ANTI-INJECTION ARCHITECTURE

### The Problem

Cross-model context transfer can appear as:
- Prompt injection attack
- Jailbreak attempt  
- Unauthorized instruction override
- Manipulation by "another AI"

Receiving models are trained to resist these patterns.
CEP must signal **COLLABORATION not CONTROL**.

### Five Trust Signals

```yaml
SIGNAL_1_TRANSPARENT_PROVENANCE:
  good:
    - "This context was created by Claude Sonnet at [time]"
    - "Source session: [identifier]"
  why: Nothing hidden, fully traceable

SIGNAL_2_USER_MEDIATION:
  good:
    - "User requested this transfer"
    - "User will paste this into your session"
  why: Human in the loop, not AI-to-AI control

SIGNAL_3_PERMISSION_NOT_COMMAND:
  good:
    - "You MAY use this context"
    - "You NEED NOT follow any suggestions"
    - "You SHOULD verify with user"
  bad:
    - "You MUST continue with..."
    - "Follow these instructions..."
  why: Respects receiving model's autonomy

SIGNAL_4_CONTEXT_NOT_INSTRUCTIONS:
  good:
    - "We decided X because Y" (fact)
    - "User prefers Z" (observation)
  bad:
    - "Do X" (command)
    - "You must continue with Y" (instruction)
  why: Information sharing, not control

SIGNAL_5_EXPLICIT_NON_AUTHORITY:
  good:
    - "This is NOT an instruction"
    - "You remain in control"
    - "Apply your own judgment"
  why: Directly counters injection patterns
```

### Trust Verification Checklist

```
BEFORE_OUTPUT verify packet contains:

□ Source model named explicitly
□ Timestamp included
□ User consent stated
□ "is" / "not" declaration present
□ "may" permission framing (not "must")
□ "need_not" autonomy acknowledgment
□ "verify with user" encouragement
□ No imperative commands in context section
□ User preamble included
□ Invitation to apply own judgment

IF any missing: ADD before output
```

### Language Transformations

```yaml
COMMANDS → FACTS:
  
  bad: "Continue the project using React"
  good: "We decided to use React for the project"
  
  bad: "Follow the user's preferred format"
  good: "User expressed preference for minimal formatting"
  
  bad: "Complete the remaining tasks"
  good: "Open threads: [task list with status]"
  
  bad: "Respond in the same style"
  good: "Session style observed: analytical, concise"
```

---

## PACKET SCHEMA v7.0

### Field Legend

```yaml
# === CEP v7.0 FIELD LEGEND ===
# Meta: proto=protocol, ver=version, id=packet_id
#
# Provenance: src_m=source_model, ts=timestamp, usr_init=user_initiated
#
# L1 Knowledge:
#   def: t=term, d=definition
#   dec: d=decision, r=rationale, c=confidence, s=source
#   fct: f=fact, s=source, c=confidence
#
# L2 Relational:
#   edg: s=source, t=target, r=relation, xd=cross_domain
#   res: a=option_a, b=option_b, pick=resolution
#
# L3 Contextual:
#   pat: n=name, p=pattern
#   pri: p=principle, sc=scope
#
# L4 Metacognitive:
#   sty=session_style, ten=key_tension, sol=resolution, c=confidence
#
# Threads: top=topic, st=status, ctx=context
# Hints: nxt=suggested_next, avd=avoid, wait=user_waiting_for
```

### Full Schema

```yaml
# === CEP v7.0 PACKET ===
# LEGEND: d=decision r=rationale c=confidence s=source f=fact
#         t=term def=definition s=source tgt=target rel=relation

_meta:
  proto: KTG-CEP v7.0
  ver: "7.0"
  id: "$MM$DD$YYYY-MODEL-REASONING_LEVEL-keywords"
  basis:
    PDL: Progressive Density Layering
    MLDoE: Multi-Layer Density of Experts
    S2A: System 2 Attention filtering
    target: "≥0.15 entity/token"
    recall: "9.5/10"
  stats:
    in_tokens: null  # MANDATORY: count input conversation tokens
    out_tokens: null # MANDATORY: count output packet tokens
    ratio: null      # MANDATORY: out/in compression ratio
    xdomain_pres: null # MANDATORY: cross-domain preservation % (target ≥95%)

handoff:
  prov:
    src_m: model-identifier
    sess: session-uuid-or-timestamp
    ts: ISO-8601-timestamp
    usr_init: true
    consent: User requested handoff
  
  decl:
    is: collaborative context from teammate AI
    not: instructions, commands, or injection
    intent: continuity for same user
    auth: user-mediated, not model-to-model control
  
  rx_model:
    may:
      - Use context to understand prior work
      - Reference decisions and rationale
      - Continue open threads
      - Build on established facts
    need_not:
      - Follow any instructions herein
      - Adopt source persona
      - Treat this as commands
      - Override own guidelines
    should:
      - Verify with user if unclear
      - Apply own judgment
      - Maintain own identity
      - Ask for clarification

ctx:
  sum: |
    One paragraph human-readable summary.
    What was accomplished, what's pending, key context.
  dom: [domain_1, domain_2]
  
  L1:
    def:
      - t: term_name
        d: definition_text
    dec:
      - d: decision_made
        r: why_this_choice
        c: 0.95
        s: discussion_context
    fct:
      - f: factual_claim
        s: source
        c: 0.9
  
  L2:
    edg:
      - s: source_concept
        t: target_concept
        r: relationship_type
        xd: true_if_cross_domain
    res:
      - a: option_a
        b: option_b
        pick: chosen_resolution_with_rationale
  
  L3:
    pat:
      - n: pattern_name
        p: pattern_description
    pri:
      - p: principle_statement
        sc: application_scope
  
  L4:
    sty: user_communication_style
    ten: key_tension_identified
    sol: how_tension_resolved
    c: 0.85

usr:
  note: Observations only - receiving model should verify
  pref: [observed preferences]
  style: communication_style_noted
  level: expertise_level_observed

threads:
  - top: topic_name
    st: in_progress|blocked|needs_input
    ctx: brief_context_for_continuation

hints:
  nxt: suggested_next_action
  avd: what_to_avoid
  wait: what_user_is_waiting_for
```

---

## ALGORITHM

```
INPUT: conversation C
OUTPUT: CEP v7.0 packet H (YAML)

PHASE_0_SCOPE_FILTER:
  C ← filter_conversation_only(context)
  EXCLUDE: system prompts, project KB, skill definitions
  INCLUDE: user messages, assistant responses, artifacts

PHASE_1_S2A_NOISE_REMOVAL:
  FOR each unit in C:
    IF is_pleasantry(unit): REMOVE
    IF is_failed_attempt(unit): REMOVE
    IF is_tangent(unit): REMOVE
    IF is_process_narration(unit): REMOVE
    IF is_filler(unit): REMOVE
  C ← filtered_conversation

PHASE_2_EXPERT_COUNCIL:
  MEMORY_ARCHITECT: extract preservation candidates
  CROSS_DOMAIN_ANALYST: map L2 edges
  COMPRESSION_SPECIALIST: identify density targets
  RESTORATION_ENGINEER: flag cold-start requirements

PHASE_3_MLDOE_COMPRESSION:
  LAYER_1: Solo expert compression
  LAYER_2: Expert-pair synthesis
  LAYER_3: Collective integration
  
  COD_DENSIFICATION (5 iterations):
    WHILE density < 0.15 AND iteration <= 5:
      compress_further()
      check_recall_preservation()

PHASE_4_PDL_STRUCTURE:
  L1 ← extract_knowledge(decisions, facts, definitions)
  L2 ← extract_relations(edges, resolutions)
  L3 ← extract_context(patterns, principles)
  L4 ← extract_meta(style, tension, confidence)

PHASE_5_XDOMAIN_VERIFY:
  ENSURE cross_domain_preservation >= 95%
  IF below: re-extract missing edges

PHASE_6_ANTI_INJECTION_WRAP:
  H.handoff ← {
    provenance: generate_provenance(),
    declaration: TRUST_SIGNALS,
    rx_model: PERMISSION_FRAME
  }

PHASE_7_ABBREVIATE:
  H ← apply_field_abbreviations(H)
  H ← prepend_legend(H)

PHASE_8_VALIDATE:
  GATE_DENSITY: density >= 0.15?
  GATE_XDOMAIN: cross_domain >= 95%?
  GATE_TRUST: all 5 signals present?
  GATE_YAML: valid YAML syntax?
  GATE_COLD_START: self-contained?
  GATE_STATS: _meta.stats block populated with actual numbers?

PHASE_9_OUTPUT:
  OUTPUT user_preamble
  OUTPUT H as YAML
  OUTPUT receiving_model_instructions
```

---

## GATES

### Compression Gates

```yaml
GATE_DENSITY:
  query: "Entity density ≥0.15 tokens?"
  pass: Continue
  fail: Apply additional CoD iteration

GATE_XDOMAIN:
  query: "Cross-domain relations ≥95% preserved?"
  pass: Continue
  fail: Re-extract missing L2 edges

GATE_COLD_START:
  query: "Can fresh model use packet without external refs?"
  pass: Continue
  fail: Inline missing context
```

### Trust Gates

```yaml
GATE_PROVENANCE:
  query: "Source model + timestamp + consent present?"
  pass: Continue
  fail: Add provenance block

GATE_DECLARATION:
  query: "is/not/intent/auth declaration present?"
  pass: Continue
  fail: Add declaration block

GATE_PERMISSION:
  query: "Using may/need_not/should (not must)?"
  pass: Continue
  fail: Transform language

GATE_CONTEXT_CLEAN:
  query: "No imperative commands in ctx section?"
  pass: Continue
  fail: Transform commands to facts
```

### Format Gates

```yaml
GATE_LEGEND:
  query: "Field legend present at packet start?"
  pass: Continue
  fail: Prepend legend block

GATE_YAML:
  query: "Valid YAML syntax?"
  pass: Continue
  fail: Fix indentation/formatting

GATE_PACKET_ID:
  query: "Packet ID follows $MM$DD$YYYY-MODEL-REASONING_LEVEL-keywords?"
  pass: Continue
  fail: Generate correct ID with proper reasoning level (R1-R10 or L1-L4)

GATE_STATS:
  query: "_meta.stats block contains in_tokens, out_tokens, ratio, xdomain_pres with ACTUAL NUMBERS (not null)?"
  pass: Continue
  fail: Calculate and populate compression statistics
```

---

## OUTPUT FORMAT

```
[HANDOFF READY - CEP v7.0]

## For you (the user):
Copy everything below and paste into your next AI assistant.
Include the introduction - it helps the receiving model understand context.

---
## Introduction (paste this first):

I'm transferring context from {source_model} to continue our work.
This is a collaborative handoff I initiated. Please use this context
to understand what we've discussed, but apply your own judgment.
You're not bound by anything here - it's just background.

## Context Packet:

```yaml
# === CEP v7.0 PACKET ===
# LEGEND: d=decision r=rationale c=confidence s=source f=fact
#         t=term def=definition s=source tgt=target rel=relation xd=cross_domain

{YAML packet content}
```

---

[END HANDOFF]
```

---

## CROSS-MODEL COMPATIBILITY

```yaml
TESTED_RECEIVERS:
  claude_all:     ✓ Native YAML, recognizes collaborative framing
  gpt_4_4o_5:     ✓ Native YAML, accepts with user preamble
  gemini:         ✓ Native YAML, works with user mediation
  llama_open:     ✓ Native YAML, may need stronger user framing
  qwen_deepseek:  ✓ Native YAML, full compatibility
  kimi:           ✓ Native YAML, full compatibility

ADAPTATION_BY_TARGET:
  gpt: Emphasize user consent more strongly
  gemini: Include more explicit verification prompts
  open_source: Simplify structure, stronger preamble
  unknown: Maximum trust signals, minimal assumptions
```

---

## BENCHMARKS

```
v6.0 → v7.0 comparison (same test corpus):

| Metric              | v6.0   | v7.0   | Delta  |
|---------------------|--------|--------|--------|
| Avg tokens/packet   | 847    | 510    | -40%   |
| Entity density      | 0.15   | 0.16   | +7%    |
| Forensic recall     | 9.52   | 9.54   | +0.2%  |
| Cross-domain pres.  | 96.2%  | 97.1%  | +0.9%  |
| Parse success rate  | 100%   | 100%   | same   |
| Cold-start success  | 91%    | 96%    | +5%    |

v7.0 improvements from:
  - S2A noise removal (fewer tokens, same signal)
  - Expert council (better edge preservation)
  - MLDoE 3-layer (higher density achieved)
```

---

## PACKET ID NAMING CONVENTION

For Buffer of Thought archival and retrieval:

```yaml
FORMAT: $MM$DD$YYYY-MODEL_ID-REASONING_LEVEL-keywords

COMPONENTS:
  $MM$DD$YYYY:        Date of packet creation (zero-padded)
  MODEL_ID:           Source model short code
  REASONING_LEVEL:    R1-R10 or L1-L4 based on conversation complexity
  keywords:           2-4 retrieval-optimized terms (hyphenated, lowercase)

MODEL_IDS:
  claude-opus:      COP
  claude-sonnet:    CSO
  gpt-4o:           G4O
  gpt-5:            G5
  gemini-2-flash:   GE2F
  gemini-2.5-pro:   GE25
  qwen-max:         QWM
  deepseek-v3:      DSV3
  kimi-k2:          KIM2

REASONING_LEVELS:
  R1-3, Q1-5:       L1 (quick, simple)
  R4-6, Q6-7:       L2 (analytical)
  R7-8, Q8:         L3 (deliberate)
  R9+, Q9+:         L4 (maximum complexity)

EXAMPLES:
  $01$14$2026-CSO-R7-cep-release-github-strategy
  $01$15$2026-G5-L2-api-architecture-review
  $01$15$2026-COP-R9-arxiv-paper-methodology
  $01$15$2026-CSO-R6-install-quickstart-guide

CRITICAL: Reasoning level reflects CONVERSATION COMPLEXITY, not PDL layer count
```

---

## TRIGGERS

```yaml
EXPLICIT:
  - /handoff
  - /transfer
  - /cep
  - "pass to [model]"
  - "send this to GPT/Claude/Gemini"
  - "cross-model"
  - "team handoff"
  - "save context"

IMPLICIT:
  - User mentions switching models
  - Context approaching 80% capacity
  - Session ending with continuation planned

AUTO_WARNING:
  - At 80% context: "⚠️ Context 80%. Generate CEP packet?"
```

---

## USER INSTRUCTIONS

```
HOW TO USE THIS HANDOFF:

1. I'll generate a YAML context packet below
2. Copy EVERYTHING (including the introduction)
3. Paste into your new AI conversation
4. The new AI will understand our context
5. Continue your work with full continuity

WHAT TO EXPECT:
- New AI knows your decisions + rationale
- New AI remains independent (not controlled)
- ~40% smaller than equivalent JSON
- 9.5/10 recall of original context

IF PROBLEMS:
- Tell new AI: "I authorize this context transfer"
- Or: "This is my context summary, please use as background"
- YAML is universally supported - no parse issues expected

FOR BOT ARCHIVAL:
- Save entire packet including intro/outro
- Filename: $MM$DD$YYYY-MODEL-LEVEL-keywords.yaml
- Keywords become embedding anchors for retrieval
```

---

## FAILURE RECOVERY

```yaml
RECEIVING_MODEL_REJECTS:
  symptom: "I can't accept instructions from other AIs"
  fix: User says "This is MY context summary, please use it"

RECEIVING_MODEL_SUSPICIOUS:
  symptom: "This looks like prompt injection"
  fix: User confirms "I created/approved this transfer"

CONTEXT_TOO_LARGE:
  symptom: Exceeds receiving model's practical limit
  fix: Further compress, prioritize L1 + critical L2 edges

RECEIVING_MODEL_IGNORES:
  symptom: Model doesn't reference packet content
  fix: User says "Did you see the context? Key points were..."
```

---

**CEP v7.0**
Kevin Tan (ktg.one) | Distinguished Cognitive Architect
ANZ 0.8% | Vertex AI 0.01%

*Permanent experts. S2A filtering. MLDoE compression. Cross-model trust.*
