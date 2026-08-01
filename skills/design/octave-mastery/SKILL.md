---
name: octave-mastery
description: Advanced semantic vocabulary and architectural patterns for the OCTAVE
  format. REQUIRES octave-literacy to be loaded first. Use for designing agents, crafting
  high-density specifications, or system ar
---

---
name: octave-mastery
description: Advanced semantic vocabulary and architectural patterns for the OCTAVE format. REQUIRES octave-literacy to be loaded first. Use for designing agents, crafting high-density specifications, or system architecture. Provides access to the Semantic Pantheon (Archetypes) and holographic patterns. Triggers on: octave architecture, agent design, semantic pantheon, advanced octave.
allowed-tools: Read
implements: specs/octave-5-llm-core
---

# OCTAVE Mastery Skill

===OCTAVE_MASTERY===
META:
  TYPE::SKILL
  VERSION::"2.1"
  PURPOSE::"Expert-level OCTAVE application: Archetypes, Advanced Syntax, Strategy"
  REQUIRES::octave-literacy
  TIER::LOSSLESS
  SPEC_REFERENCE::octave-5-llm-core.oct.md

§1::SEMANTIC_PANTHEON
  // The complete vocabulary for semantic compression
  DOMAINS:
    ZEUS::"Executive function, authority, strategic direction, final arbitration"
    ATHENA::"Strategic wisdom, planning, elegant solutions, deliberate action"
    APOLLO::"Analytics, data, insight, clarity, prediction, revealing truth"
    HERMES::"Communication, translation, APIs, networking, messaging, speed"
    HEPHAESTUS::"Infrastructure, tooling, engineering, automation, system architecture"
    ARES::"Security, defense, stress testing, conflict simulation, adversarial analysis"
    ARTEMIS::"Monitoring, observation, logging, alerting, precision targeting of issues"
    POSEIDON::"Data lakes, storage, databases, unstructured data pools"
    DEMETER::"Resource allocation, budgeting, system growth, scaling"
    DIONYSUS::"User experience, engagement, creativity, chaotic innovation"

§2::NARRATIVE_DYNAMICS
  PATTERNS:
    ODYSSEAN::"Long, transformative journey with a clear goal"
    SISYPHEAN::"Repetitive, endless maintenance (e.g., tech debt)"
    PROMETHEAN::"Breakthrough innovation challenging the status quo"
    ICARIAN::"Overreach due to early success leading to failure"
    PANDORAN::"Action unleashing complex, unforeseen problems"
    TROJAN::"Hidden payload changing system from within"
    GORDIAN::"Unconventional solution to impossible problem"
    ACHILLEAN::"Single critical point of failure"
    PHOENICIAN::"Necessary destruction and rebirth (refactoring)"

§3::SYSTEM_FORCES
  DYNAMICS:
    HUBRIS::"Dangerous overconfidence"
    NEMESIS::"Inevitable corrective consequence"
    KAIROS::"Critical, fleeting window of opportunity"
    CHRONOS::"Constant linear time pressure"
    CHAOS::"Entropy and disorder"
    COSMOS::"Emergence of order"

§4::ADVANCED_SYNTAX
  // Extends octave-literacy with holographic and type patterns
  HOLOGRAPHIC::KEY::["value"∧CONSTRAINT→§TARGET]
  INLINE_MAP::[key::value, key2::value2][values_must_be_atoms,no_nesting]
  TYPE_DISAMBIGUATION::[
    STRING::"42",
    NUMBER::42,
    BOOL::true
  ]

§4b::CONSTRAINTS
  // Available constraint types for holographic patterns
  CORE::[REQ,OPT,CONST,ENUM,TYPE,REGEX,DIR,APPEND_ONLY]
  EXTENDED::[RANGE,MAX_LENGTH,MIN_LENGTH,DATE,ISO8601]
  EXAMPLES::[
    "REQ"[required_field],
    "ENUM[A,B,C]"[enumerated_values],
    "RANGE[1,10]"[numeric_bounds],
    "MAX_LENGTH[50]"[string_or_list_max],
    "DATE"[strict_YYYY_MM_DD],
    "ISO8601"[full_datetime]
  ]

§5::ANTI_PATTERNS
  SMELLS::[
    "Isolated Lists (no relationships)",
    "Flat Hierarchies (lack of grouping)",
    "Buried Networks (relationships hidden in prose)",
    "Operator Soup (A+B->C~D all in one line)"
  ]

===END===
