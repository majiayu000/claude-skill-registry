// SOURCE-OF-TRUTH: shared/scripts/epic-planning-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import {
    computePlanningBaseResumeAction,
    hasChoice,
    validatePlanningBaseTransition,
} from "../../planning-runtime/lib/guards.mjs";
import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.DISCOVERY])],
    [PHASES.DISCOVERY, new Set([PHASES.RESEARCH])],
    [PHASES.RESEARCH, new Set([PHASES.PLAN])],
    [PHASES.PLAN, new Set([PHASES.MODE_DETECTION])],
    [PHASES.MODE_DETECTION, new Set([PHASES.PREVIEW])],
    [PHASES.PREVIEW, new Set([PHASES.DELEGATE])],
    [PHASES.DELEGATE, new Set([PHASES.FINALIZE])],
    [PHASES.FINALIZE, new Set([PHASES.SELF_CHECK])],
    [PHASES.SELF_CHECK, new Set([PHASES.DONE])],
    [PHASES.PAUSED, new Set([])],
    [PHASES.DONE, new Set([])],
]);

export function validateTransition(manifest, state, checkpoints, toPhase) {
    const base = validatePlanningBaseTransition(state, checkpoints, toPhase, ALLOWED_TRANSITIONS);
    if (!base.ok) {
        return base;
    }
    if (toPhase === PHASES.RESEARCH && !state.discovery_summary) {
        return { ok: false, error: "Discovery summary missing" };
    }
    if (toPhase === PHASES.PLAN && !state.research_summary) {
        return { ok: false, error: "Research summary missing" };
    }
    if (toPhase === PHASES.MODE_DETECTION && !state.ideal_plan_summary) {
        return { ok: false, error: "Ideal epic plan missing" };
    }
    if (toPhase === PHASES.DELEGATE && !manifest.auto_approve && !hasChoice(state.decisions, "confirm_epic_preview")) {
        return { ok: false, error: "Preview confirmation decision missing" };
    }
    if (toPhase === PHASES.SELF_CHECK && !state.epic_plan_summary) {
        return { ok: false, error: "Epic plan coordinator summary missing" };
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
    if (state.phase === PHASES.FINALIZE && !state.epic_plan_summary) {
        return "Record epic-plan coordinator summary before self-check";
    }
    if (state.phase === PHASES.SELF_CHECK && !state.self_check_passed) {
        return `Fix self-check failures, then checkpoint ${PHASES.SELF_CHECK} with pass=true`;
    }
    return computePlanningBaseResumeAction(
        state,
        checkpoints,
        ALLOWED_TRANSITIONS,
        PHASES.PAUSED,
        PHASES.DONE,
    );
}
