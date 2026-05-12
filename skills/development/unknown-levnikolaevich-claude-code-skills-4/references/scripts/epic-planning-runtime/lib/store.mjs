// SOURCE-OF-TRUTH: shared/scripts/epic-planning-runtime/lib/store.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { resolve } from "node:path";
import { epicPlanCoordinatorSummarySchema } from "../../coordinator-runtime/lib/schemas.mjs";
import {
    createPlanningManifestSchema,
    createPlanningRuntimeStore,
    createPlanningState,
} from "../../planning-runtime/lib/store.mjs";
import { PHASES } from "./phases.mjs";

const epicStore = createPlanningRuntimeStore({
    baseRootParts: [".hex-skills", "epic-planning", "runtime"],
    manifestSchema: createPlanningManifestSchema("scope_identifier"),
    normalizeManifest(manifestInput, projectRoot) {
        const scopeIdentifier = manifestInput.scope_identifier || manifestInput.identifier || "scope";
        return {
            skill: "ln-210",
            mode: manifestInput.mode || "epic_planning",
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
            research_summary: null,
            ideal_plan_summary: null,
            mode_detection: null,
            epic_plan_summary: null,
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
} = epicStore;

export function recordPlanSummary(projectRoot, runId, summary) {
    return epicStore.recordCoordinatorSummary(
        projectRoot,
        runId,
        summary,
        epicPlanCoordinatorSummarySchema,
        "epic planning coordinator summary",
        "epic_plan_summary",
    );
}
