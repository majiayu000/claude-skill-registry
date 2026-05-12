// SOURCE-OF-TRUTH: shared/scripts/story-planning-runtime/lib/guards.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import {
    computePlanningBaseResumeAction,
    hasChoice,
    validatePlanningBaseTransition,
} from "../../planning-runtime/lib/guards.mjs";
import { PHASES } from "./phases.mjs";

const ALLOWED_TRANSITIONS = new Map([
    [PHASES.CONFIG, new Set([PHASES.CONTEXT_ASSEMBLY])],
    [PHASES.CONTEXT_ASSEMBLY, new Set([PHASES.RESEARCH])],
    [PHASES.RESEARCH, new Set([PHASES.PLAN])],
    [PHASES.PLAN, new Set([PHASES.ROUTING])],
    [PHASES.ROUTING, new Set([PHASES.MODE_DETECTION])],
    [PHASES.MODE_DETECTION, new Set([PHASES.DELEGATE])],
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
    if (toPhase === PHASES.RESEARCH && !state.context_ready) {
        return { ok: false, error: "Context assembly not recorded" };
    }
    if (toPhase === PHASES.PLAN && !state.research_status) {
        return { ok: false, error: "Research result not recorded" };
    }
    if (toPhase === PHASES.ROUTING && !state.ideal_plan_summary) {
        return { ok: false, error: "Ideal plan summary missing" };
    }
    if (toPhase === PHASES.MODE_DETECTION && !state.routing_summary) {
        return { ok: false, error: "Routing summary missing" };
    }
    if (toPhase === PHASES.DELEGATE) {
        if (Object.keys(state.epic_group_modes || {}).length === 0) {
            return { ok: false, error: "Epic group modes missing" };
        }
        if (!manifest.auto_approve && !hasChoice(state.decisions, "confirm_preview")) {
            return { ok: false, error: "Preview confirmation decision missing" };
        }
    }
    if (toPhase === PHASES.FINALIZE) {
        const expectedGroups = Object.keys(state.epic_group_modes || {}).length;
        const actualGroups = Object.keys(state.epic_results || {}).length;
        if (expectedGroups > 0 && actualGroups < expectedGroups) {
            return { ok: false, error: "Not all epic groups produced worker summaries" };
        }
    }
    if (toPhase === PHASES.SELF_CHECK && !state.story_plan_summary) {
        return { ok: false, error: "Story plan coordinator summary missing" };
    }
    if (toPhase === PHASES.SELF_CHECK && !state.template_compliance_passed) {
        return { ok: false, error: "Template compliance not verified. Fetch each created story via get_issue, run validateTemplateCompliance(description, 'story'), record template_compliance_passed in state." };
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
    const baseAction = computePlanningBaseResumeAction(
        state,
        checkpoints,
        ALLOWED_TRANSITIONS,
        PHASES.PAUSED,
        PHASES.DONE,
    );
    if (state.phase === PHASES.DELEGATE) {
        const expected = Object.keys(state.epic_group_modes || {}).length;
        const actual = Object.keys(state.epic_results || {}).length;
        if (expected > actual) {
            return "Record remaining epic worker summaries before finalization";
        }
    }
    if (state.phase === PHASES.FINALIZE && !state.story_plan_summary) {
        return "Record story-plan coordinator summary before self-check";
    }
    if (state.phase === PHASES.SELF_CHECK && !state.self_check_passed) {
        return `Fix self-check failures, then checkpoint ${PHASES.SELF_CHECK} with pass=true`;
    }
    return baseAction;
}
