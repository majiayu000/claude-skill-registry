// SOURCE-OF-TRUTH: shared/scripts/planning-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

export function hasCheckpoint(checkpoints, phase) {
    return Boolean(checkpoints?.[phase]);
}

export function hasChoice(decisions, choice) {
    return (decisions || []).some(entry => entry.selected_choice === choice);
}

export function validatePlanningBaseTransition(state, checkpoints, toPhase, allowedTransitions) {
    const allowed = allowedTransitions.get(state.phase);
    if (!allowed || !allowed.has(toPhase)) {
        return { ok: false, error: `Invalid transition: ${state.phase} -> ${toPhase}` };
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return { ok: false, error: `Checkpoint missing for ${state.phase}` };
    }
    if (state.pending_decision) {
        return { ok: false, error: "Pending decision must be resolved before advancing" };
    }
    return { ok: true };
}

export function computePlanningBaseResumeAction(state, checkpoints, allowedTransitions, pausedPhase, donePhase) {
    if (state.complete || state.phase === donePhase) {
        return "Run complete";
    }
    if (state.phase === pausedPhase) {
        if (state.pending_decision) {
            return `Resolve pending decision: ${state.pending_decision.kind}`;
        }
        return `Paused: ${state.paused_reason || "manual intervention required"}`;
    }
    if (!hasCheckpoint(checkpoints, state.phase)) {
        return `Complete ${state.phase} and write its checkpoint`;
    }
    const nextPhase = Array.from(ALLOWED_OR_EMPTY(allowedTransitions, state.phase))[0];
    return nextPhase ? `Advance to ${nextPhase}` : "No automatic resume action available";
}

function ALLOWED_OR_EMPTY(allowedTransitions, phase) {
    return allowedTransitions.get(phase) || [];
}
