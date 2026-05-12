// SOURCE-OF-TRUTH: shared/scripts/scope-decomposition-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { computePlanningBaseResumeAction, validatePlanningBaseTransition } from "../../planning-runtime/lib/guards.mjs";
import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.DISCOVERY])],
    [PHASES.DISCOVERY, new Set([PHASES.EPIC_DECOMPOSITION])],
    [PHASES.EPIC_DECOMPOSITION, new Set([PHASES.STORY_LOOP])],
    [PHASES.STORY_LOOP, new Set([PHASES.PRIORITIZATION_LOOP])],
    [PHASES.PRIORITIZATION_LOOP, new Set([PHASES.FINALIZE])],
    [PHASES.FINALIZE, new Set([PHASES.SELF_CHECK])],
    [PHASES.SELF_CHECK, new Set([PHASES.DONE])],
    [PHASES.PAUSED, new Set([])],
    [PHASES.DONE, new Set([])],
]);

function expectedPrioritizationEpics(state) {
    if (Array.isArray(state.expected_prioritization_epics) && state.expected_prioritization_epics.length > 0) {
        return state.expected_prioritization_epics;
    }
    return Object.keys(state.story_summaries || {});
}

function missingPrioritizationEpics(state) {
    if (state.prioritization_enabled !== true) {
        return [];
    }
    const recorded = state.prioritization_summaries || {};
    return expectedPrioritizationEpics(state).filter(epicId => !recorded[epicId]);
}

export function validateTransition(manifest, state, checkpoints, toPhase) {
    const base = validatePlanningBaseTransition(state, checkpoints, toPhase, ALLOWED_TRANSITIONS);
    if (!base.ok) {
        return base;
    }
    if (toPhase === PHASES.EPIC_DECOMPOSITION && !state.discovery_summary) {
        return { ok: false, error: "Discovery summary missing" };
    }
    if (toPhase === PHASES.STORY_LOOP && !state.epic_summary) {
        return { ok: false, error: "Epic planning summary missing" };
    }
    if (toPhase === PHASES.PRIORITIZATION_LOOP && Object.keys(state.story_summaries || {}).length === 0) {
        return { ok: false, error: "No story planning summaries recorded" };
    }
    if (toPhase === PHASES.FINALIZE) {
        const missingEpics = missingPrioritizationEpics(state);
        if (missingEpics.length > 0) {
            return {
                ok: false,
                error: `Story prioritization summaries missing for epics: ${missingEpics.join(", ")}`,
            };
        }
    }
    if (toPhase === PHASES.SELF_CHECK && !state.scope_summary) {
        return { ok: false, error: "Scope decomposition summary missing" };
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
    if (state.phase === PHASES.EPIC_DECOMPOSITION && !state.epic_summary) {
        return "Record epic-planning summary before Story loop";
    }
    if (state.phase === PHASES.STORY_LOOP && Object.keys(state.story_summaries || {}).length === 0) {
        return "Record Story-planning summaries before prioritization/finalization";
    }
    if (state.phase === PHASES.PRIORITIZATION_LOOP) {
        const missingEpics = missingPrioritizationEpics(state);
        if (missingEpics.length > 0) {
            return `Record story-prioritization-worker summaries for epics: ${missingEpics.join(", ")}`;
        }
    }
    if (state.phase === PHASES.FINALIZE && !state.scope_summary) {
        return "Record scope-decomposition coordinator summary before self-check";
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
