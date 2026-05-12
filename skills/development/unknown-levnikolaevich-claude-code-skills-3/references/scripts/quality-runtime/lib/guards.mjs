// SOURCE-OF-TRUTH: shared/scripts/quality-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.DISCOVERY])],
    [PHASES.DISCOVERY, new Set([PHASES.CODE_QUALITY])],
    [PHASES.CODE_QUALITY, new Set([PHASES.CLEANUP])],
    [PHASES.CLEANUP, new Set([PHASES.AGENT_REVIEW])],
    [PHASES.AGENT_REVIEW, new Set([PHASES.CRITERIA])],
    [PHASES.CRITERIA, new Set([PHASES.LINTERS])],
    [PHASES.LINTERS, new Set([PHASES.REGRESSION])],
    [PHASES.REGRESSION, new Set([PHASES.LOG_ANALYSIS])],
    [PHASES.LOG_ANALYSIS, new Set([PHASES.FINALIZE])],
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
    if (toPhase === PHASES.CLEANUP && !hasWorker(state, "ln-511")) {
        return { ok: false, error: "ln-511 summary missing" };
    }
    if (toPhase === PHASES.AGENT_REVIEW && !hasWorker(state, "ln-512")) {
        return { ok: false, error: "ln-512 summary missing" };
    }
    if (toPhase === PHASES.LOG_ANALYSIS && !hasWorker(state, "ln-513")) {
        return { ok: false, error: "ln-513 summary missing" };
    }
    if (toPhase === PHASES.FINALIZE && !hasWorker(state, "ln-514")) {
        return { ok: false, error: "ln-514 summary missing" };
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
    if (state.phase === PHASES.CODE_QUALITY && !hasWorker(state, "ln-511")) {
        return childRunMessage(state, "ln-511", " or record its worker summary before cleanup")
            || "Record ln-511 worker summary before cleanup";
    }
    if (state.phase === PHASES.CLEANUP && !hasWorker(state, "ln-512")) {
        return childRunMessage(state, "ln-512", " or record its worker summary before agent review")
            || "Record ln-512 worker summary before agent review";
    }
    if (state.phase === PHASES.REGRESSION && !hasWorker(state, "ln-513")) {
        return childRunMessage(state, "ln-513", " or record its worker summary before log analysis")
            || "Record ln-513 worker summary before log analysis";
    }
    if (state.phase === PHASES.LOG_ANALYSIS && !hasWorker(state, "ln-514")) {
        return childRunMessage(state, "ln-514", " or record its worker summary before finalization")
            || "Record ln-514 worker summary before finalization";
    }
    if (state.phase === PHASES.SELF_CHECK && !state.self_check_passed) {
        return `Fix self-check failures, then checkpoint ${PHASES.SELF_CHECK} with pass=true`;
    }
    const nextPhase = Array.from(ALLOWED_TRANSITIONS.get(state.phase) || [])[0];
    return nextPhase ? `Advance to ${nextPhase}` : "No automatic resume action available";
}
