// SOURCE-OF-TRUTH: shared/scripts/scope-decomposition-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { TERMINAL_RUNTIME_PHASES } from "../../coordinator-runtime/lib/runtime-constants.mjs";

export const PHASES = Object.freeze({
    CONFIG: "PHASE_0_CONFIG",
    DISCOVERY: "PHASE_1_DISCOVERY",
    EPIC_DECOMPOSITION: "PHASE_2_EPIC_DECOMPOSITION",
    STORY_LOOP: "PHASE_3_STORY_LOOP",
    PRIORITIZATION_LOOP: "PHASE_4_PRIORITIZATION_LOOP",
    FINALIZE: "PHASE_5_FINALIZE",
    SELF_CHECK: "PHASE_6_SELF_CHECK",
    PAUSED: TERMINAL_RUNTIME_PHASES.PAUSED,
    DONE: TERMINAL_RUNTIME_PHASES.DONE,
});
