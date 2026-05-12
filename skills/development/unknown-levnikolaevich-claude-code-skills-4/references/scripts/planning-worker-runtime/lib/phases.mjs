// SOURCE-OF-TRUTH: shared/scripts/planning-worker-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

export const WORKER_PHASES = Object.freeze({
    "ln-201": Object.freeze([
        "PHASE_0_CONFIG",
        "PHASE_1_INPUT_PROCESSING",
        "PHASE_2_KILL_FUNNEL",
        "PHASE_3_RANK_SURVIVORS",
        "PHASE_4_WRITE_DISCOVERY_REPORT",
        "PHASE_5_WRITE_SUMMARY",
        "PHASE_6_SELF_CHECK",
    ]),
    "ln-221": Object.freeze([
        "PHASE_0_CONFIG",
        "PHASE_1_RESOLVE_CONTEXT",
        "PHASE_2_LOAD_TEMPLATE",
        "PHASE_3_GENERATE_STORIES",
        "PHASE_4_VALIDATE_STORIES",
        "PHASE_5_CONFIRM_OR_AUTOAPPROVE",
        "PHASE_6_APPLY_CREATE",
        "PHASE_7_UPDATE_KANBAN",
        "PHASE_8_WRITE_SUMMARY",
        "PHASE_9_SELF_CHECK",
    ]),
    "ln-222": Object.freeze([
        "PHASE_0_CONFIG",
        "PHASE_1_RESOLVE_CONTEXT",
        "PHASE_2_LOAD_EXISTING_STORIES",
        "PHASE_3_CLASSIFY_REPLAN",
        "PHASE_4_CONFIRM_OR_AUTOAPPROVE",
        "PHASE_5_APPLY_REPLAN",
        "PHASE_6_UPDATE_KANBAN",
        "PHASE_7_WRITE_SUMMARY",
        "PHASE_8_SELF_CHECK",
    ]),
    "ln-230": Object.freeze([
        "PHASE_0_CONFIG",
        "PHASE_1_DISCOVERY",
        "PHASE_2_LOAD_STORY_METADATA",
        "PHASE_3_ANALYZE_STORIES",
        "PHASE_4_GENERATE_PRIORITIZATION",
        "PHASE_5_WRITE_SUMMARY",
        "PHASE_6_SELF_CHECK",
    ]),
});

export function getWorkerPhases(skill) {
    return WORKER_PHASES[skill] || null;
}
