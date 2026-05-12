// SOURCE-OF-TRUTH: shared/scripts/test-planning-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.DISCOVERY])],
    [PHASES.DISCOVERY, new Set([PHASES.RESEARCH])],
    [PHASES.RESEARCH, new Set([PHASES.MANUAL_TESTING])],
    [PHASES.MANUAL_TESTING, new Set([PHASES.AUTO_TEST_PLANNING])],
    [PHASES.AUTO_TEST_PLANNING, new Set([PHASES.FINALIZE])],
    [PHASES.FINALIZE, new Set([PHASES.SELF_CHECK])],
    [PHASES.SELF_CHECK, new Set([PHASES.DONE])],
    [PHASES.PAUSED, new Set([])],
    [PHASES.DONE, new Set([])],
]);

function hasCheckpoint(checkpoints, phase) {
    return Boolean(checkpoints?.[phase]);
}

function hasWorker(state, worker) {
    return Boolean(state.worker_results?.[worker]);
}

function childRunMessage(state, worker, suffix) {
    const childRun = state.child_runs?.[worker];
    if (!childRun?.run_id) {
        return null;
    }
    return `Check child runtime ${childRun.run_id} for ${worker}${suffix}`;
}

export function validateTransition(manifest, state, checkpoints, toPhase) {
    const allowed = ALLOWED_TRANSITIONS.get(state.phase);
    if (!allowed || !allowed.has(toPhase)) {
        return { ok: false, error: `Invalid transition: ${state.phase} -> ${toPhase}` };
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return { ok: false, error: `Checkpoint missing for ${state.phase}` };
    }
    if (toPhase === PHASES.MANUAL_TESTING && !state.simplified && !hasWorker(state, "ln-521")) {
        return { ok: false, error: "ln-521 summary missing" };
    }
    if (toPhase === PHASES.AUTO_TEST_PLANNING && !state.simplified && !hasWorker(state, "ln-522")) {
        return { ok: false, error: "ln-522 summary missing" };
    }
    if (toPhase === PHASES.FINALIZE && !hasWorker(state, "ln-523")) {
        return { ok: false, error: "ln-523 summary missing" };
    }
    if (toPhase === PHASES.DONE) {
        if (!state.self_check_passed) {
            return { ok: false, error: "Self-check must pass before completion" };
        }
        if (!state.final_result) {
            return { ok: false, error: "Final result not recorded" };
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
    if (state.phase === PHASES.RESEARCH && !state.simplified && !hasWorker(state, "ln-521")) {
        return childRunMessage(state, "ln-521", " or record its worker summary before manual testing")
            || "Record ln-521 worker summary before manual testing";
    }
    if (state.phase === PHASES.MANUAL_TESTING && !state.simplified && !hasWorker(state, "ln-522")) {
        return childRunMessage(state, "ln-522", " or record its worker summary before auto-test planning")
            || "Record ln-522 worker summary before auto-test planning";
    }
    if (state.phase === PHASES.AUTO_TEST_PLANNING && !hasWorker(state, "ln-523")) {
        return childRunMessage(state, "ln-523", " or record its worker summary before finalization")
            || "Record ln-523 worker summary before finalization";
    }
    if (state.phase === PHASES.SELF_CHECK && !state.self_check_passed) {
        return `Fix self-check failures, then checkpoint ${PHASES.SELF_CHECK} with pass=true`;
    }
    const nextPhase = Array.from(ALLOWED_TRANSITIONS.get(state.phase) || [])[0];
    return nextPhase ? `Advance to ${nextPhase}` : "No automatic resume action available";
}
