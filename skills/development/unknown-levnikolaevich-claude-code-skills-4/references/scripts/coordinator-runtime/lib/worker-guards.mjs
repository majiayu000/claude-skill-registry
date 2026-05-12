// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/worker-guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

export function createLinearPhaseMap(phases) {
    const phaseList = Array.isArray(phases) ? [...phases] : [];
    const transitions = new Map();
    for (let index = 0; index < phaseList.length - 1; index += 1) {
        transitions.set(phaseList[index], new Set([phaseList[index + 1]]));
    }
    if (phaseList.length > 0) {
        transitions.set(phaseList[phaseList.length - 1], new Set(["DONE"]));
    }
    transitions.set("PAUSED", new Set([]));
    transitions.set("DONE", new Set([]));
    return transitions;
}

function hasCheckpoint(checkpoints, phase) {
    return Boolean(checkpoints?.[phase]);
}

export function validateLinearWorkerTransition(state, checkpoints, toPhase, phases, extraValidation = null) {
    const allowedTransitions = createLinearPhaseMap(phases);
    const allowed = allowedTransitions.get(state.phase);
    if (!allowed || !allowed.has(toPhase)) {
        return { ok: false, error: `Invalid transition: ${state.phase} -> ${toPhase}` };
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return { ok: false, error: `Checkpoint missing for ${state.phase}` };
    }
    if (toPhase === "DONE") {
        if (!state.summary_recorded) {
            return { ok: false, error: "Worker summary must be recorded before completion" };
        }
        if (!state.self_check_passed) {
            return { ok: false, error: "Self-check must pass before completion" };
        }
        if (!state.final_result) {
            return { ok: false, error: "Final result not recorded" };
        }
    }
    if (typeof extraValidation === "function") {
        return extraValidation(state, checkpoints, toPhase) || { ok: true };
    }
    return { ok: true };
}

export function computeLinearWorkerResumeAction(state, checkpoints, phases, extraResumeAction = null) {
    if (state.complete || state.phase === "DONE") {
        return "Run complete";
    }
    if (state.phase === "PAUSED") {
        return `Paused: ${state.paused_reason || "manual intervention required"}`;
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return `Complete ${state.phase} and write its checkpoint`;
    }
    if (typeof extraResumeAction === "function") {
        const nextAction = extraResumeAction(state, checkpoints);
        if (typeof nextAction === "string" && nextAction.length > 0) {
            return nextAction;
        }
    }
    if (state.phase === phases.at(-1)) {
        if (!state.summary_recorded) {
            return "Record worker summary before completion";
        }
        if (!state.self_check_passed) {
            return `Fix self-check failures, then checkpoint ${state.phase} with pass=true`;
        }
    }
    const nextPhaseIndex = phases.indexOf(state.phase);
    if (nextPhaseIndex >= 0 && phases[nextPhaseIndex + 1]) {
        return `Advance to ${phases[nextPhaseIndex + 1]}`;
    }
    if (phases.includes(state.phase)) {
        return "Advance to DONE";
    }
    return "No automatic resume action available";
}
