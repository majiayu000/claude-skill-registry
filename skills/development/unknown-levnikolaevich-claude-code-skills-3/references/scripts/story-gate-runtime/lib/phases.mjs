// SOURCE-OF-TRUTH: shared/scripts/story-gate-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { TERMINAL_RUNTIME_PHASES } from "../../coordinator-runtime/lib/runtime-constants.mjs";

export const PHASES = Object.freeze({
    CONFIG: "PHASE_0_CONFIG",
    DISCOVERY: "PHASE_1_DISCOVERY",
    FAST_TRACK: "PHASE_2_FAST_TRACK",
    QUALITY_CHECKS: "PHASE_3_QUALITY_CHECKS",
    TEST_PLANNING: "PHASE_4_TEST_PLANNING",
    TEST_VERIFICATION: "PHASE_5_TEST_VERIFICATION",
    VERDICT: "PHASE_6_VERDICT",
    FINALIZATION: "PHASE_7_FINALIZATION",
    SELF_CHECK: "PHASE_8_SELF_CHECK",
    PAUSED: TERMINAL_RUNTIME_PHASES.PAUSED,
    DONE: TERMINAL_RUNTIME_PHASES.DONE,
});
