// SOURCE-OF-TRUTH: shared/scripts/quality-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { TERMINAL_RUNTIME_PHASES } from "../../coordinator-runtime/lib/runtime-constants.mjs";

export const PHASES = Object.freeze({
    CONFIG: "PHASE_0_CONFIG",
    DISCOVERY: "PHASE_1_DISCOVERY",
    CODE_QUALITY: "PHASE_2_CODE_QUALITY",
    CLEANUP: "PHASE_3_CLEANUP",
    AGENT_REVIEW: "PHASE_4_AGENT_REVIEW",
    CRITERIA: "PHASE_5_CRITERIA",
    LINTERS: "PHASE_6_LINTERS",
    REGRESSION: "PHASE_7_REGRESSION",
    LOG_ANALYSIS: "PHASE_8_LOG_ANALYSIS",
    FINALIZE: "PHASE_9_FINALIZE",
    SELF_CHECK: "PHASE_10_SELF_CHECK",
    PAUSED: TERMINAL_RUNTIME_PHASES.PAUSED,
    DONE: TERMINAL_RUNTIME_PHASES.DONE,
});
