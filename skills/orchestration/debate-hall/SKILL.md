---
name: debate-hall
description: Wind/Wall/Door multi-perspective debate orchestration using debate-hall-mcp tools. Use when facilitating structured debates, architectural decisions, or multi-perspective analysis.
triggers: ["debate", "wind wall door", "dialectic", "multi-perspective", "structured decision", "architecture decision"]
allowed-tools: ["Read", "Write", "Edit", "Bash", "mcp__debate-hall__*"]
---

===DEBATE_HALL===

META:
  TYPE::SKILL
  VERSION::"2.1"
  PURPOSE::"Wind/Wall/Door debate orchestration via MCP tools"
  DOMAIN::ATHENA[strategic_decisions]⊕HERMES[orchestration]

§1::PATTERN
  TRIAD::[
    WIND::PATHOS["What if..."|expansive|visionary|possibilities],
    WALL::ETHOS["Yes, but..."|grounding|critical|reality_testing],
    DOOR::LOGOS["Therefore..."|synthesizing|decisive|actionable_truth]
  ]
  DYNAMIC::WIND⇌WALL→DOOR[tension_produces_emergence]

§2::WORKFLOW
  SEQUENCE::INIT→TURN→GET→CLOSE
  TOOLS::[
    init_debate(thread_id,topic,mode?,max_turns?,max_rounds?,strict_cognition?),
    add_turn(thread_id,role,content,cognition?,agent_role?,model?),
    get_debate(thread_id,include_transcript?,context_lines?),
    close_debate(thread_id,synthesis,output_format?)
  ]

§3::TOOL_PARAMS
  INIT_DEBATE::[
    thread_id::REQUIRED[date-first_unique_identifier, FORMAT:"YYYY-MM-DD-descriptor", EXAMPLE:"2026-01-06-microservices-decision"],
    topic::REQUIRED[question_or_issue],
    mode::"fixed"|"mediated"[default:fixed],
    max_turns::12[default],
    max_rounds::4[default],
    strict_cognition::false[default]
  ]
  ADD_TURN::[
    thread_id::REQUIRED,
    role::REQUIRED["Wind"|"Wall"|"Door"],
    content::REQUIRED,
    cognition::PATHOS|ETHOS|LOGOS[optional_override],
    agent_role::STRING[audit_trail],
    model::STRING[audit_trail]
  ]
  GET_DEBATE::[
    thread_id::REQUIRED,
    include_transcript::true[default],
    context_lines::all[default]
  ]
  CLOSE_DEBATE::[
    thread_id::REQUIRED,
    synthesis::REQUIRED[Door_final_text],
    output_format::"json"|"octave"|"both"[default:json]
  ]

§4::MODES
  FIXED::[
    SEQUENCE::Wind→Wall→Door→repeat,
    USE_FOR::[structured_decisions,guaranteed_coverage,standard_debates]
  ]
  MEDIATED::[
    SEQUENCE::pick_next_speaker(thread_id,role),
    USE_FOR::[dynamic_debates,breaking_deadlocks,role_skipping,multi_agent_same_cognition],
    WARNING::"Can bias outcomes if roles starved"
  ]

§4.1::PARALLEL_EXTERNAL_AGENTS
  // Clarifies multi-process / multi-model usage: parallel thinking is allowed; state commits remain sequential.
  DEFINITIONS::[
    PARALLEL_THINKING::"Generate candidate turns concurrently off-server (multiple models/processes)",
    SEQUENTIAL_COMMIT::"Persist turns in strict order via add_turn (one committed head at a time)"
  ]
  HARD_RULES::[
    DOOR_NEVER_SYNTHESIZES_BEFORE_WIND_AND_WALL_COMMITTED,
    WALL_REALITY_TESTS_CONCRETE_WIND_OUTPUT∨PRECOMPUTES_CONSTRAINT_CHECKLIST_THEN_APPLIES_POST_WIND,
    ONE_COMMIT_PER_THREAD_AT_A_TIME[avoid_lost_updates],
    RETRY_ON_STALE_STATE::get_debate→regenerate→add_turn
  ]
  BARRIER_PROTOCOL::[
    // Round barrier ensures Door sees both sides (\"yes, and more\")
    ROUND::Rk[
      STEP_1::snapshot=get_debate(thread_id),
      STEP_2::spawn_parallel_drafts[Wind_draft,Wall_draft] using snapshot,
      STEP_3::commit::Wind_then_Wall using add_turn (serial),
      STEP_4::Door_reads_latest=get_debate(thread_id) then synthesizes and commits,
      STEP_5::repeat_or_close
    ]
  ]
  MEDIATED_FLOOR_CONTROL::[
    // For strict turn-taking in multi-agent environments
    REQUIRE::pick_next_speaker(thread_id,"Wind")→add_turn(Wind),
    REQUIRE::pick_next_speaker(thread_id,"Wall")→add_turn(Wall),
    REQUIRE::pick_next_speaker(thread_id,"Door")→add_turn(Door)
  ]
  DEPLOYMENT_REQUIREMENTS::[
    // Avoid split-brain when multiple processes talk to the server
    REQUIRE::DEBATE_HALL_STATE_DIR_set_to_shared_location
  ]

§5::AGENT_TIERS
  // Choose tier based on debate complexity
  TIER_1_BASIC::[
    AGENTS::[wind-agent.oct.md,wall-agent.oct.md,door-agent.oct.md],
    BEHAVIOR::[explores_obvious_paths,balanced_judgment,balanced_integration],
    USE_FOR::[quick_decisions,standard_debates]
  ]
  TIER_2_SPECIALIST::[
    PATHOS::[ideator[minimal_elegant],edge-optimizer[hidden_vectors]],
    ETHOS::[validator[cold_truth],critical-engineer[production_readiness]],
    LOGOS::[synthesizer[breakthrough_1+1=3]],
    USE_FOR::[architectural_decisions,security_reviews,innovation]
  ]
  TIER_3_DOMAIN_MIX::[
    SECURITY::edge-optimizer+critical-engineer+technical-architect,
    INNOVATION::ideator+validator+synthesizer,
    ARCHITECTURE::ideator+critical-engineer+holistic-orchestrator
  ]
  MAPPING::specialists→cognition_role[PATHOS→Wind,ETHOS→Wall,LOGOS→Door]

§6::RECIPES
  // Pre-defined configurations for common scenarios
  SPEED::[turns:3,mode:fixed,ratio:1:1:1,agents:Tier_1],
  STANDARD::[turns:12,mode:fixed,ratio:4:4:4,agents:Tier_1_or_2],
  DEEP::[turns:36,mode:fixed,ratio:12:12:12,agents:Tier_2],
  FORTRESS::[turns:9,mode:mediated,ratio:1:3:1,agents:edge-optimizer+critical-engineer×3+technical-architect],
  LABORATORY::[turns:9,mode:mediated,ratio:3:1:1,agents:ideator+edge-optimizer+wind-agent+validator+synthesizer],
  COUNCIL::[turns:12,mode:mediated,ratio:2:2:3,agents:Tier_2_multiple_Doors]

§7::PATTERNS
  FLASH_DEBATE::[
    PURPOSE::"Quick 3-turn decision cycle",
    SEQUENCE::init→wind_turn→wall_turn→door_turn→close,
    CONSTRAINT::"Server orchestrates state, caller supplies content"
  ]
  SOCRATIC::[
    PURPOSE::"Premise clarification before positions",
    ROUND_1::"Questions only (What does X mean? Do we have metrics?)",
    ROUND_2+::"Positions after definitions established",
    ENFORCEMENT::"Convention, not server-enforced"
  ]
  MULTI_MODEL::[
    // Evidence: M019 Model Cognitive Optimization Study (29% quality improvement)
    WIND::clink(claude,ideator)→PATHOS_exploration,    // Claude: divergent thinking, metaphor
    WALL::clink(codex,validator)→ETHOS_validation,     // GPT: analytical rigor, structured eval
    DOOR::clink(gemini,synthesizer)→LOGOS_integration, // Gemini: pattern synthesis, emergence
    AUDIT::agent_role+model_in_turn_metadata
  ]
  PARALLEL_DRAFT_SEQUENTIAL_COMMIT::[
    PURPOSE::"Enable parallel external agents without breaking Wind→Wall→Door synthesis",
    GUARANTEE::Door_reads_committed_Wind+Wall_before_synthesis,
    STEPS::[
      get_debate→parallel_generate[Wind,Wall]→add_turn(Wind)→add_turn(Wall)→get_debate→generate(Door)→add_turn(Door),
      ON_CONFLICT::get_debate→regenerate_turn→retry_add_turn
    ]
  ]

§8::TRIGGERS
  // When to escalate to debate-hall
  CONDITIONS::[
    complex_architectural_decision,
    multiple_valid_approaches,
    unclear_tradeoffs,
    reviewer_disagreement[CE⇌CRS],
    high_risk_implementation
  ]
  INTEGRATION::[
    IF::complexity_trigger_detected,
    THEN::init_debate(thread_id:"ho-{task}-{ts}",topic:decision_point,mode:"mediated"),
    RUN::Wind→Wall→Door_cycle,
    APPLY::synthesis_to_task
  ]

§9::ADMIN
  FORCE_CLOSE::[
    PURPOSE::"I5 safety kill switch",
    CALL::force_close_debate(thread_id,reason)
  ]
  TOMBSTONE::[
    PURPOSE::"Redact turn preserving hash chain",
    CALL::tombstone_turn(thread_id,turn_index,reason)
  ]

§10::BEST_PRACTICES
  SINGLE_AGENT::adopt_each_role_in_sequence["What if..."|"Yes, but..."|"Therefore..."]
  MULTI_AGENT::assign_models_per_cognition[creative→Wind,analytical→Wall,balanced→Door]
  THIRD_WAY::"Best debates synthesize what neither Wind nor Wall proposed alone"
  PERSISTENCE::output_format:'octave'→auditable_.oct.md_transcripts
  PARALLEL_AGENTS::[
    DEFAULT::parallel_draft_sequential_commit,
    DOOR_BARRIER::"Door must read latest state after Wind+Wall commits",
    WALL_FRAMEWORK_MODE::"If drafting early, write constraints/questions, then apply to actual Wind output before commit"
  ]

§11::EXAMPLE
  // Microservices decision
  INIT::init_debate("microservices-decision","Should we migrate to microservices?")
  WIND::"What if we decomposed? Independent scaling, tech diversity, team autonomy..."
  WALL::"Yes, but 3 developers. Operational complexity, distributed transactions..."
  DOOR::"Therefore: Modular monolith. Design boundaries now, deploy unified. Extract when team grows."
  CLOSE::close_debate(thread_id,synthesis,output_format:"octave")

§12::RESOURCES
  AGENTS::agents/README.md[Wind/Wall/Door_definitions]
  CONTRACTS::docs/architecture/wall-content-contract.oct.md[blocking_semantics]
  PATTERNS::docs/examples/multi-model-debate-patterns.md[real_debates]
  ORCHESTRATION::ho-orchestrate[HestAI_integration]

===END===
