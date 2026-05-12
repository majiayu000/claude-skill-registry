// SOURCE-OF-TRUTH: shared/scripts/story-gate-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import {
    STORY_GATE_COMPLETED_TEST_STATUS_LIST,
    STORY_GATE_PRE_VERIFICATION_ALLOWED_TEST_STATUS_LIST,
    STORY_GATE_VERDICT_LIST,
} from "../../coordinator-runtime/lib/runtime-constants.mjs";
import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.DISCOVERY])],
    [PHASES.DISCOVERY, new Set([PHASES.FAST_TRACK])],
    [PHASES.FAST_TRACK, new Set([PHASES.QUALITY_CHECKS])],
    [PHASES.QUALITY_CHECKS, new Set([PHASES.TEST_PLANNING, PHASES.VERDICT])],
    [PHASES.TEST_PLANNING, new Set([PHASES.TEST_VERIFICATION])],
    [PHASES.TEST_VERIFICATION, new Set([PHASES.VERDICT])],
    [PHASES.VERDICT, new Set([PHASES.FINALIZATION])],
    [PHASES.FINALIZATION, new Set([PHASES.SELF_CHECK])],
    [PHASES.SELF_CHECK, new Set([PHASES.DONE])],
    [PHASES.PAUSED, new Set([])],
    [PHASES.DONE, new Set([])],
]);

function hasCheckpoint(checkpoints, phase) {
    return Boolean(checkpoints?.[phase]);
}

function childRunMessage(state, worker, suffix) {
    const childRun = state.child_runs?.[worker];
    if (!childRun?.run_id) {
        return null;
    }
    return `Check child runtime ${childRun.run_id} for ${worker}${suffix}`;
}

function verdictAllowsFinalization(verdict) {
    return STORY_GATE_VERDICT_LIST.includes(verdict);
}

function hasCompletedStage3Summary(state) {
    return state.stage_summary?.summary_kind === "pipeline-stage"
        && state.stage_summary?.payload?.stage === 3
        && state.stage_summary?.payload?.status === "completed";
}

export function validateTransition(manifest, state, checkpoints, toPhase) {
    const allowed = ALLOWED_TRANSITIONS.get(state.phase);
    if (!allowed || !allowed.has(toPhase)) {
        return { ok: false, error: `Invalid transition: ${state.phase} -> ${toPhase}` };
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return { ok: false, error: `Checkpoint missing for ${state.phase}` };
    }

    if (toPhase === PHASES.TEST_PLANNING || toPhase === PHASES.VERDICT) {
        if (!state.quality_summary) {
            return { ok: false, error: "Quality summary missing" };
        }
    }

    if (toPhase === PHASES.TEST_VERIFICATION && !state.test_planner_invoked && !STORY_GATE_PRE_VERIFICATION_ALLOWED_TEST_STATUS_LIST.includes(state.test_task_status || "")) {
        return { ok: false, error: "Test planner not recorded before test verification" };
    }

    if (toPhase === PHASES.VERDICT && state.phase === PHASES.TEST_VERIFICATION && !STORY_GATE_COMPLETED_TEST_STATUS_LIST.includes(state.test_task_status || "")) {
        return { ok: false, error: "Test verification not complete" };
    }

    if (toPhase === PHASES.FINALIZATION && !verdictAllowsFinalization(state.final_result)) {
        return { ok: false, error: "Final verdict not recorded" };
    }

    if (toPhase === PHASES.DONE) {
        if (!state.self_check_passed) {
            return { ok: false, error: "Self-check must pass before completion" };
        }
        if (!state.story_final_status) {
            return { ok: false, error: "Final Story status not recorded" };
        }
        if (!hasCompletedStage3Summary(state)) {
            return { ok: false, error: "Stage 3 coordinator artifact not recorded" };
        }
    }

    return { ok: true };
}

export function computeResumeAction(manifest, state, checkpoints) {
    if (state.complete || state.phase === PHASES.DONE) {
        return "Run complete";
    }
    if (state.phase === PHASES.PAUSED) {
        return `Paused: ${state.paused_reason || "manual intervention required"}`;
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return `Complete ${state.phase} and write its checkpoint`;
    }
    if (state.phase === PHASES.QUALITY_CHECKS && !state.quality_summary) {
        return childRunMessage(state, "ln-510", " or record its coordinator summary before test planning")
            || "Persist ln-510 summary, then checkpoint PHASE_3_QUALITY_CHECKS";
    }
    if (state.phase === PHASES.TEST_PLANNING
        && !state.test_planner_invoked
        && !STORY_GATE_PRE_VERIFICATION_ALLOWED_TEST_STATUS_LIST.includes(state.test_task_status || "")) {
        return childRunMessage(state, "ln-520", " or record its coordinator summary before test verification")
            || "Record ln-520 summary or reused terminal test state before test verification";
    }
    if (state.phase === PHASES.TEST_VERIFICATION && !STORY_GATE_COMPLETED_TEST_STATUS_LIST.includes(state.test_task_status || "")) {
        return "Wait for the test task to finish, then resume PHASE_5_TEST_VERIFICATION";
    }
    if (state.phase === PHASES.VERDICT && !state.final_result) {
        return "Calculate final verdict and checkpoint PHASE_6_VERDICT";
    }
    if (state.phase === PHASES.FINALIZATION && !state.story_final_status) {
        return "Record Story status/finalization result and checkpoint PHASE_7_FINALIZATION";
    }
    if (state.phase === PHASES.SELF_CHECK && !hasCompletedStage3Summary(state)) {
        return "Record the Stage 3 coordinator artifact before completion";
    }
    if (state.phase === PHASES.SELF_CHECK && !state.self_check_passed) {
        return "Fix self-check failures, then checkpoint PHASE_8_SELF_CHECK with pass=true";
    }

    const nextPhase = Array.from(ALLOWED_TRANSITIONS.get(state.phase) || [])[0];
    return nextPhase ? `Advance to ${nextPhase}` : "No automatic resume action available";
}
