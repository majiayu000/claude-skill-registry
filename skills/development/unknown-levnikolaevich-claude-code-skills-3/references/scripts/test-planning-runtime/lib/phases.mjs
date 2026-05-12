// SOURCE-OF-TRUTH: shared/scripts/test-planning-runtime/lib/phases.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { TERMINAL_RUNTIME_PHASES } from "../../coordinator-runtime/lib/runtime-constants.mjs";

export const PHASES = Object.freeze({
    CONFIG: "PHASE_0_CONFIG",
    DISCOVERY: "PHASE_1_DISCOVERY",
    RESEARCH: "PHASE_2_RESEARCH",
    MANUAL_TESTING: "PHASE_3_MANUAL_TESTING",
    AUTO_TEST_PLANNING: "PHASE_4_AUTO_TEST_PLANNING",
    FINALIZE: "PHASE_5_FINALIZE",
    SELF_CHECK: "PHASE_6_SELF_CHECK",
    PAUSED: TERMINAL_RUNTIME_PHASES.PAUSED,
    DONE: TERMINAL_RUNTIME_PHASES.DONE,
});
