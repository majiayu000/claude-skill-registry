// SOURCE-OF-TRUTH: shared/scripts/story-planning-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import {
    storyPlanCoordinatorSummarySchema,
    storyPlanWorkerSummarySchema,
} from "../../coordinator-runtime/lib/schemas.mjs";
import {
    createPlanningManifestSchema,
    createPlanningRuntimeStore,
    createPlanningState,
} from "../../planning-runtime/lib/store.mjs";
import { PHASES } from "./phases.mjs";

const storyPlanningStore = createPlanningRuntimeStore({
    baseRootParts: [".hex-skills", "story-planning", "runtime"],
    manifestSchema: createPlanningManifestSchema("epic_id"),
    normalizeManifest(manifestInput, projectRoot) {
        const epicId = manifestInput.epic_id || manifestInput.identifier;
        return {
            skill: "ln-220",
            mode: manifestInput.mode || "story_planning",
            identifier: manifestInput.identifier || `epic-${epicId}`,
            epic_id: epicId,
            task_provider: manifestInput.task_provider || "unknown",
            auto_approve: manifestInput.auto_approve === true,
            project_root: resolve(projectRoot || process.cwd()),
            created_at: new Date().toISOString(),
        };
    },
    defaultState(manifest, runId) {
        return createPlanningState(manifest, runId, PHASES.CONFIG, {
            epic_id: manifest.epic_id,
            context_ready: false,
            research_file: null,
            research_status: null,
            ideal_plan_summary: null,
            routing_summary: null,
            epic_group_modes: {},
            epic_results: {},
            story_plan_summary: null,
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
    updateState,
} = storyPlanningStore;

export function recordEpic(projectRoot, runId, summary) {
    return storyPlanningStore.recordSummary(
        projectRoot,
        runId,
        summary,
        storyPlanWorkerSummarySchema,
        "story plan worker summary",
        (state, nextSummary) => ({
            ...state,
            epic_results: {
                ...state.epic_results,
                [nextSummary.payload.epic_id]: nextSummary,
            },
        }),
    );
}

export function recordPlanSummary(projectRoot, runId, summary) {
    return storyPlanningStore.recordCoordinatorSummary(
        projectRoot,
        runId,
        summary,
        storyPlanCoordinatorSummarySchema,
        "story planning coordinator summary",
        "story_plan_summary",
    );
}
