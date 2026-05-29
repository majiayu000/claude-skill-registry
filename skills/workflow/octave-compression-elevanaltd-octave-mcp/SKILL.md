---
name: octave-compression
description: Specialized workflow for transforming verbose natural language into semantic OCTAVE structures. REQUIRES octave-literacy to be loaded first
allowed-tools: ["Read", "Write", "Edit"]
triggers: ["compress to octave", "semantic compression", "documentation refactoring", "octave compression", "compress documentation", "knowledge artifact", "semantic density", "OCTAVE format conversion"]
version: "2.4.0"
---

===OCTAVE_COMPRESSION===
META:
  TYPE::SKILL
  VERSION::"2.4.0"
  STATUS::ACTIVE
  PURPOSE::"Workflow for transforming prose into semantic density"
  REQUIRES::octave-literacy
  TIER::LOSSLESS
  SPEC_REFERENCE::octave-data-spec.oct.md[§1b::COMPRESSION_TIERS]
  V6_FEATURES::"Loss accounting system, tier metadata tracking, fidelity guarantees"

§1::COMPRESSION_MANDATE
  TARGET::"60-80% token reduction with 100% decision-logic fidelity"
  PRINCIPLE::"Semantics > Syntax Rigidity"
  TRUTH::"Dense ≠ Obscure. Preserve the causal chain."

  §1b::COMPRESSION_TIER_SELECTION
    // Full tier definitions in octave-data-spec.oct.md §1b
    LOSSLESS::[target:100%_fidelity,preserve:everything,drop:none]
      USE::[critical_reasoning,legal_documents,safety_analysis,audit_trails]
    CONSERVATIVE::[target:85-90%_compression,preserve:explanatory_depth,drop:redundancy]
      USE::[research_summaries,design_decisions,technical_analysis]
      LOSS::~10-15%[repetition,some_edge_cases,verbose_phrasing]
    AGGRESSIVE::[target:70%_compression,preserve:core_thesis∧conclusions,drop:nuance∨narrative]
      USE::[context_window_scarcity,quick_reference,decision_support]
      LOSS::~30%[explanatory_depth,execution_tradeoff_narratives,edge_case_exploration]
    ULTRA::[target:50%_compression,preserve:facts∧structure,drop:all_narrative]
      USE::[extreme_scarcity,embedding_generation,dense_reference]
      LOSS::~50%[almost_all_explanatory_content,some_nuance,tradeoff_reasoning]

    // Note: For 60% compression with mythological atoms, see octave-ultra-mythic skill
    ULTRA_MYTHIC::[target:60%_compression,preserve:soul∧constraints,method:mythological_atoms]
      REFERENCE::skills/octave-ultra-mythic[specialized_identity_compression]

    TIER_METADATA::include_in_META_block[COMPRESSION_TIER,LOSS_PROFILE,NARRATIVE_DEPTH]

    V6_LOSS_ACCOUNTING::[
      PRINCIPLE::"OCTAVE-MCP is a loss accounting system for LLM communication",
      TRACKING::"Every transformation must log what was preserved vs dropped",
      METADATA::"Documents carry their compression tier and loss profile",
      AUDIT::I4_TRANSFORM_AUDITABILITY[stable_ids,loss_receipts],
      FIDELITY::I1_SYNTACTIC_FIDELITY[syntax_changes_ok,semantics_preserved]
    ]

§2::TRANSFORMATION_WORKFLOW
  PHASE_1_READ::[
    ANALYZE::"Understand before compressing",
    IDENTIFY::[Redundancy, Verbosity, Causal_Chains],
    MAP::"Logic flow (A leads to B)"
  ]

  PHASE_2_EXTRACT::[
    CORE_PATTERNS::"Essential decision logic",
    REASONING::"BECAUSE statements (preserve the 'why')",
    EVIDENCE::"Metrics and concrete examples",
    TRANSFER::"HOW-to mechanics"
  ]

  PHASE_3_COMPRESS::[
    APPLICATION::"Apply operators defined in octave-literacy",
    HIERARCHY::"Group related concepts under parent keys",
    ARRAYS::"Convert repetitive lists to [item1, item2]",
    MYTHOLOGY::"For 60% compression, load octave-ultra-mythic for mythological atoms"
  ]

  PHASE_4_VALIDATE::[
    FIDELITY::"Is the logic intact?",
    GROUNDING::"Is there at least 1 concrete example?",
    NAVIGABILITY::"Can a human scan it?"
  ]

§3::COMPRESSION_RULES
  RULE_1::"Preserve CAUSALITY (X→Y because Z)"
  RULE_2::"Drop stopwords (the, is, a, of)"
  RULE_3::"One example per 200 tokens of abstraction"
  RULE_4::"Explicit Tradeoffs (GAIN⇌LOSS or GAIN vs LOSS)"
  RULE_5::"Use Mythological Encoding if complexity demands it"

§4::ANTI_PATTERNS
  AVOID::[
    "Markdown inside OCTAVE blocks",
    "JSON/YAML syntax (no curly braces, no trailing commas)",
    "Deep nesting (>3 levels)",
    "Loss of numbers or IDs"
  ]

===END===
