// SOURCE-OF-TRUTH: shared/scripts/story-planning-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { TERMINAL_RUNTIME_PHASES } from "../../coordinator-runtime/lib/runtime-constants.mjs";

export const PHASES = Object.freeze({
    CONFIG: "PHASE_0_CONFIG",
    CONTEXT_ASSEMBLY: "PHASE_1_CONTEXT_ASSEMBLY",
    RESEARCH: "PHASE_2_RESEARCH",
    PLAN: "PHASE_3_PLAN",
    ROUTING: "PHASE_4_ROUTING",
    MODE_DETECTION: "PHASE_5_MODE_DETECTION",
    DELEGATE: "PHASE_6_DELEGATE",
    FINALIZE: "PHASE_7_FINALIZE",
    SELF_CHECK: "PHASE_8_SELF_CHECK",
    PAUSED: TERMINAL_RUNTIME_PHASES.PAUSED,
    DONE: TERMINAL_RUNTIME_PHASES.DONE,
});
