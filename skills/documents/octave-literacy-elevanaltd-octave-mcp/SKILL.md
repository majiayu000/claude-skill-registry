---
name: octave-literacy
description: Fundamental reading and writing capability for the OCTAVE format. Basic structural competence without full architectural specifications
allowed-tools: ["Read", "Write", "Edit"]
triggers: ["octave format", "write octave", "octave syntax", "structured output", "OCTAVE basics", "OCTAVE literacy", "OCTAVE structure", "semantic format", "key::value", "OCTAVE notation"]
version: "1.3.0"
---

===OCTAVE_LITERACY===
META:
  TYPE::SKILL
  VERSION::"1.3.0"
  STATUS::ACTIVE
  PURPOSE::"Essential syntax and operators for basic OCTAVE competence"
  TIER::LOSSLESS
  SPEC_REFERENCE::octave-core-spec.oct.md
  V6_FEATURES::"Adds CONTRACT/GRAMMAR blocks, assembly rules, .oct.md extension"

§1::CORE_SYNTAX
  ASSIGNMENT::KEY::value   // Double colon is MANDATORY for data
  BLOCK::KEY:[indent_2]    // Single colon + newline + 2 spaces starts a block
  LIST::[a,b,c]            // Brackets for collections
  STRING::"value"∨bare_word  // Quotes required if contains spaces or special chars
  NUMBER::42∨3.14∨-1e10    // No quotes for numeric values
  BOOLEAN::true∨false      // Lowercase only
  NULL::null               // Lowercase only
  COMMENT:://              // Standard comment syntax

  §1b::BRACKET_FORMS
    CONTAINER::[a,b,c]              // Bare brackets = list
    CONSTRUCTOR::NAME[args]         // NAME[...] = constructor (REGEX[pattern], ENUM[a,b])
    INLINE_MAP::[key::val,key2::val2]  // Dense key-value pairs (values must be atoms)
    HOLOGRAPHIC::[\"value\"∧CONSTRAINT→§TARGET]  // Schema mode only

§2::OPERATORS
  // EXPRESSION OPERATORS (with precedence - lower number = tighter binding)
  []::Container [a,b,c] (precedence 1)
  ⧺::Concatenation A⧺B (mechanical join) (precedence 2) | ASCII: ~
  ⊕::Synthesis A⊕B (emergent whole) (precedence 3) | ASCII: +
  ⇌::Tension A⇌B (binary opposition) (precedence 4) | ASCII: vs [requires word boundaries]
  ∧::Constraint [A∧B∧C] (precedence 5) | ASCII: &
  ∨::Alternative A∨B (precedence 6) | ASCII: |
  →::Flow A→B→C (precedence 7, right-associative) | ASCII: ->

  // PREFIX/SPECIAL
  §::Target (→§DECISION_LOG)
  //::Comment (line start or after value)

  §2b::ASCII_ALIASES
    ALL_OPERATORS::accept_both_unicode_and_ascii
    CANONICAL_OUTPUT::prefer_unicode_in_emission
    vs_BOUNDARY_RULE::"vs requires word boundaries [whitespace∨bracket∨paren∨start∨end]"
    VALID::"A vs B"∨"[Speed vs Quality]"
    INVALID::"SpeedvsQuality"[no_boundaries]

§3::CRITICAL_RULES
  1::No spaces around assignment :: (KEY::value, not KEY :: value)
  2::Indent exactly 2 spaces per level (NO TABS)
  3::All keys must be [A-Z, a-z, 0-9, _] and start with letter or underscore
  4::Envelopes are ===NAME=== at start and ===END=== at finish (NAME must be [A-Z_][A-Z0-9_]*)
  5::Use lowercase for true, false, null (NOT True, False, NULL)
  6::∧ only appears inside brackets, never bare: [A∧B∧C] is valid, A∧B is not
  7::⇌ is binary only (A⇌B), not chained (A⇌B⇌C is invalid)
  8::File extension .oct.md is canonical (v6), .octave.txt deprecated

  §3b::V6_ENVELOPE_STRUCTURE
    FILE_STRUCTURE::[===NAME===,META_BLOCK,SEPARATOR_OPTIONAL,BODY,===END===]
    META_REQUIRED::[TYPE,VERSION]
    META_V6_OPTIONAL::[CONTRACT,GRAMMAR]  // New in v6 for holographic contracts
    CONTRACT::HOLOGRAPHIC[validation_law_in_document]
    GRAMMAR::GBNF_COMPILER[generate_constrained_output]

  §3c::ASSEMBLY_RULES
    WHEN_CONCATENATING_PROFILES::omit_intermediate_===END===[only_final_===END===_terminates]
    USE_CASES::[agent_context_injection,specification_layering,multi_part_documents]
    EXAMPLE::core_profile⊕schema_profile→single_===END===_at_finish
    V6_PATTERN::multiple_profiles_one_document[no_intermediate_terminators]

§4::EXAMPLE_BLOCK
  ===EXAMPLE===
  STATUS::ACTIVE
  PHASES:
    PLAN::[Research → Design]
    BUILD::[Code ⊕ Test]
  METRICS:
    SPEED::"High"
    QUALITY::"Verified"
  ===END===

===END===
