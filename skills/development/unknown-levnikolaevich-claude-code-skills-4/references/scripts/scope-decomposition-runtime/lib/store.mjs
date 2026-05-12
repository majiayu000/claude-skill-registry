// SOURCE-OF-TRUTH: shared/scripts/scope-decomposition-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import {
    epicPlanCoordinatorSummarySchema,
    scopeDecompositionSummarySchema,
    storyPlanCoordinatorSummarySchema,
    storyPrioritizationWorkerSummarySchema,
} from "../../coordinator-runtime/lib/schemas.mjs";
import {
    createPlanningManifestSchema,
    createPlanningRuntimeStore,
    createPlanningState,
} from "../../planning-runtime/lib/store.mjs";
import { PHASES } from "./phases.mjs";

const scopeStore = createPlanningRuntimeStore({
    baseRootParts: [".hex-skills", "scope-decomposition", "runtime"],
    manifestSchema: createPlanningManifestSchema("scope_identifier"),
    normalizeManifest(manifestInput, projectRoot) {
        const scopeIdentifier = manifestInput.scope_identifier || manifestInput.identifier || "scope";
        return {
            skill: "ln-200",
            mode: manifestInput.mode || "scope_decomposition",
            identifier: manifestInput.identifier || scopeIdentifier,
            scope_identifier: scopeIdentifier,
            task_provider: manifestInput.task_provider || "unknown",
            auto_approve: manifestInput.auto_approve === true,
            project_root: resolve(projectRoot || process.cwd()),
            created_at: new Date().toISOString(),
        };
    },
    defaultState(manifest, runId) {
        return createPlanningState(manifest, runId, PHASES.CONFIG, {
            scope_identifier: manifest.scope_identifier,
            discovery_summary: null,
            epic_summary: null,
            story_summaries: {},
            prioritization_enabled: false,
            expected_prioritization_epics: [],
            prioritization_summaries: {},
            scope_summary: null,
        });
    },
    pausedPhase: PHASES.PAUSED,
    resumablePhases: new Set(Object.values(PHASES).filter(p => p !== PHASES.PAUSED && p !== PHASES.DONE)),
});

export const {
    checkpointPhase,
    completeRun,
    loadActiveRun,
    listActiveRuns,
    loadRun,
    pauseRun,
    readJsonFile,
    recordDecision,
    resolveRunId,
    runtimePaths,
    saveState,
    setPendingDecision,
    startRun,
} = scopeStore;

export function recordEpicSummary(projectRoot, runId, summary) {
    return scopeStore.recordSummary(
        projectRoot,
        runId,
        summary,
        epicPlanCoordinatorSummarySchema,
        "epic planning summary",
        (state, nextSummary) => ({
            ...state,
            epic_summary: nextSummary,
        }),
    );
}

export function recordStorySummary(projectRoot, runId, summary) {
    return scopeStore.recordSummary(
        projectRoot,
        runId,
        summary,
        storyPlanCoordinatorSummarySchema,
        "story planning summary",
        (state, nextSummary) => ({
            ...state,
            story_summaries: {
                ...state.story_summaries,
                [nextSummary.payload.epic_id]: nextSummary,
            },
        }),
    );
}

export function recordPrioritizationSummary(projectRoot, runId, summary) {
    return scopeStore.recordSummary(
        projectRoot,
        runId,
        summary,
        storyPrioritizationWorkerSummarySchema,
        "story prioritization summary",
        (state, nextSummary) => ({
            ...state,
            prioritization_summaries: {
                ...(state.prioritization_summaries || {}),
                [nextSummary.payload.epic_id]: nextSummary,
            },
        }),
    );
}

export function recordScopeSummary(projectRoot, runId, summary) {
    return scopeStore.recordCoordinatorSummary(
        projectRoot,
        runId,
        summary,
        scopeDecompositionSummarySchema,
        "scope decomposition summary",
        "scope_summary",
    );
}
